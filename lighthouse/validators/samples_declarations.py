from flask import current_app as app
from eve.io.mongo import Validator  # type: ignore
from eve.methods.post import post_internal  # type: ignore
from lighthouse.constants import DUPLICATE_SAMPLES, NON_EXISTING_SAMPLE


# fail in validator -> returns correct response


class SamplesDeclarationsValidator(Validator):
    def _validate_validation_errors(self, validation_errors, field, value):
        if validation_errors and ("validation_flags" in self.document):
            for flag in self.document["validation_flags"]:
                if flag == DUPLICATE_SAMPLES:
                    self._error(field, "Sample is a duplicate")
                if flag == NON_EXISTING_SAMPLE:
                    self._error(field, "Sample does not exist in database")


def get_root_sample_id(obj):
    return obj["root_sample_id"]

def root_sample_id_present(obj):
    if 'root_sample_id' in obj:
        return True
    else:
        return False

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


def find_duplicates(sample_ids):
    duplicate_sample_ids = []

    for index in range(len(sample_ids)):
        sample_id = sample_ids[index]

        if (sample_ids.count(sample_id) > 1) and not (sample_id in duplicate_sample_ids):
            duplicate_sample_ids.append(sample_id)

    return duplicate_sample_ids


def find_non_exist_samples(sample_ids):
    cursor = app.data.driver.db.samples.find(
        {"Root Sample ID": {"$in": sample_ids}}, {"Root Sample ID": 1}
    )

    existing_sample_ids = [val["Root Sample ID"] for val in cursor]
    not_exist_sample_ids = [val for val in sample_ids if not (val in existing_sample_ids)]

    return not_exist_sample_ids


def add_flags(request_element, sample_id, sample_ids, flag):
    if sample_id in sample_ids:
        if "validation_flags" in request_element:
            request_element["validation_flags"].append(flag)
        else:
            request_element["validation_flags"] = [flag]


def add_validation_flags(sample, duplicate_sample_ids, non_exist_samples):
    add_flags(
        sample,
        get_root_sample_id(sample),
        duplicate_sample_ids,
        DUPLICATE_SAMPLES,
    )
    add_flags(
        sample, get_root_sample_id(sample), non_exist_samples, NON_EXISTING_SAMPLE,
    )

def pre_samples_declarations_post_callback(request):
    sample_ids = get_samples(request)

    if len(sample_ids) == 0:
        return request

    duplicate_sample_ids = find_duplicates(sample_ids)
    non_exist_samples = find_non_exist_samples(sample_ids)

    if (len(duplicate_sample_ids) == 0) and (len(non_exist_samples) == 0):
        return request

    if isinstance(request.json, list):
        for index in range(len(request.json)):
            add_validation_flags(request.json[index], duplicate_sample_ids, non_exist_samples)
    else:
        add_validation_flags(request.json, duplicate_sample_ids, non_exist_samples)

    return request


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
            new_response = post_internal(
                "samples_declarations", payl=clean_payload, skip_validation=True
            )

            # We re-generate the response by merging new response with the original response
            merged_payload = merge_response_into_payload(payload, new_response[0], clean_elems)

            return merged_payload
    return None

