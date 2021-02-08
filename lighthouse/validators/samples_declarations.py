from flask import current_app as app
from eve.io.mongo import Validator  # type: ignore
from eve.methods.post import post_internal  # type: ignore
from lighthouse.constants import DUPLICATE_SAMPLES, NON_EXISTING_SAMPLE, FIELD_ROOT_SAMPLE_ID
from collections import Counter


# fail in validator -> returns correct response


class SamplesDeclarationsValidator(Validator):
    def _validate_validation_errors(self, validation_errors, field, value):
        if validation_errors and ("validation_flags" in self.document):
            for flag in self.document["validation_flags"]:
                if flag == DUPLICATE_SAMPLES:
                    self._error(field, f"Sample is a duplicate: {value}")
                if flag == NON_EXISTING_SAMPLE:
                    self._error(field, f"Sample does not exist in database: {value}")


def get_root_sample_id(obj):
    return obj["root_sample_id"]


def root_sample_id_present(obj):
    return "root_sample_id" in obj


def get_samples(request):

    json = request.get_json()

    if isinstance(json, list):
        valid_samples = list(filter(root_sample_id_present, json))
        return list(map(get_root_sample_id, valid_samples))
    else:
        if root_sample_id_present(json):
            return [get_root_sample_id(json)]
        else:
            return []


# https://stackoverflow.com/questions/46554866/efficiently-finding-duplicates-in-a-list
def find_duplicates(sample_ids):
    c = Counter(sample_ids)
    return [k for k in c if c[k] > 1]


# https://stackoverflow.com/questions/3462143/get-difference-between-two-lists
def find_non_exist_samples(sample_ids):
    cursor = app.data.driver.db.samples.find({FIELD_ROOT_SAMPLE_ID: {"$in": sample_ids}}, {FIELD_ROOT_SAMPLE_ID: 1})

    existing_sample_ids = [val[FIELD_ROOT_SAMPLE_ID] for val in cursor]
    return list(set(sample_ids) - set(existing_sample_ids))


def add_flags(sample, sample_ids, flag):
    sample_id = get_root_sample_id(sample)

    if sample_id in sample_ids:
        if "validation_flags" in sample:
            sample["validation_flags"].append(flag)
        else:
            sample["validation_flags"] = [flag]


def add_validation_flags(sample, duplicate_sample_ids, non_exist_samples):
    if len(duplicate_sample_ids) > 0:
        add_flags(sample, duplicate_sample_ids, DUPLICATE_SAMPLES)

    if len(non_exist_samples) > 0:
        add_flags(sample, non_exist_samples, NON_EXISTING_SAMPLE)


def pre_samples_declarations_post_callback(request):
    sample_ids = get_samples(request)

    if len(sample_ids) == 0:
        return request

    duplicate_sample_ids = find_duplicates(sample_ids)
    non_exist_samples = find_non_exist_samples(sample_ids)

    if (len(duplicate_sample_ids) == 0) and (len(non_exist_samples) == 0):
        return request

    add_errors(request, duplicate_sample_ids, non_exist_samples)
    return request


def add_errors(request, duplicate_sample_ids, non_exist_samples):
    if isinstance(request.json, list):
        for index in range(len(request.json)):
            if root_sample_id_present(request.json[index]):
                add_validation_flags(request.json[index], duplicate_sample_ids, non_exist_samples)
    else:
        add_validation_flags(request.json, duplicate_sample_ids, non_exist_samples)


# Filters a selection of items that have been validated successfully (OK status)
# although rejected because of the presence of wrong items in the payload. This
# selection will allow us to generate the new clean payload and also to be able
# to map the answer back into the position of items in the original
# response
def build_clean_elems_object(items, request):
    clean_elems = {}
    for i in range(len(items)):
        if items[i]["_status"] == "OK":
            clean_elems[i] = request.json[i]
    return clean_elems


# From the new response, we merge the answer from the elements into the original
# response
def merge_response_into_payload(payload, response, clean_elems):
    keys = list(clean_elems.keys())

    if len(keys) == 1:
        # When the new clean payload request thaw we have just performed earlier
        # in post_samples_declarations_pos_callback) only modifies one element,
        # the response will not have an items attribute, but it will contain the
        # attributes of the element in root.
        payload.json["_items"][keys[0]] = response
    else:
        for pos in range(len(keys)):
            key = keys[pos]
            payload.json["_items"][key] = response["_items"][pos]

    return payload


# Performs a partial update of OK items when they are in a payload when there are
# some ERR items so the OK items won't be rejected
def post_samples_declarations_post_callback(request, payload):
    if payload.json["_status"] == "OK":
        return payload

    if "_items" in payload.json:
        items = payload.json["_items"]

        # Extract only the OK items that have been rejected just because the group
        # contained ERR items too
        clean_elems = build_clean_elems_object(items, request)
        if clean_elems:
            clean_payload = clean_elems.values()

            # We re-perform the request again with the OK items without performing
            # the validation again, so they will go to the database
            new_response = post_internal("samples_declarations", payl=clean_payload, skip_validation=True)

            # We re-generate the response by merging new response with the original response
            merged_payload = merge_response_into_payload(payload, new_response[0], clean_elems)

            return merged_payload
    return None
