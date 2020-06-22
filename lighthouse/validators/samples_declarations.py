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


def get_samples(request):
    json = request.get_json()

    if isinstance(json, list):
        return list(map(get_root_sample_id, json))
    else:
        return [get_root_sample_id(json)]


def find_duplicates(sample_ids):
    duplicate_sample_ids = []
    index = 0

    while index < len(sample_ids):
        sample_id = sample_ids[index]

        if (sample_ids.count(sample_id) > 1) and not (sample_id in duplicate_sample_ids):
            duplicate_sample_ids.append(sample_id)
        index = index + 1

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


def pre_samples_declarations_post_callback(request):
    sample_ids = get_samples(request)

    duplicate_sample_ids = find_duplicates(sample_ids)
    non_exist_samples = find_non_exist_samples(sample_ids)

    if (len(duplicate_sample_ids) == 0) and (len(non_exist_samples) == 0):
        return request

    index = 0
    while index < len(request.json):
        sample = request.json[index]

        add_flags(
            request.json[index],
            get_root_sample_id(sample),
            duplicate_sample_ids,
            DUPLICATE_SAMPLES,
        )
        add_flags(
            request.json[index], get_root_sample_id(sample), non_exist_samples, NON_EXISTING_SAMPLE,
        )
        index = index + 1

    return request


def build_clean_elems_object(items, request):
    i = 0
    clean_elems = {}
    while i < len(items):
        if items[i]["_status"] == "OK":
            clean_elems[i] = request.json[i]
        i = i + 1
    return clean_elems


def merge_response_into_payload(payload, response, clean_elems):
    pos = 0
    keys = list(clean_elems.keys())

    if len(keys) == 1:
        payload.json["_items"][keys[0]] = response
    else:
        while pos < len(keys):
            key = keys[pos]
            payload.json["_items"][key] = response["_items"][pos]
            pos = pos + 1

    return payload


def post_samples_declarations_post_callback(request, payload):
    if payload.json["_status"] == "OK":
        return payload

    items = payload.json["_items"]

    clean_elems = build_clean_elems_object(items, request)
    if clean_elems:
        clean_payload = clean_elems.values()

        new_response = post_internal(
            "samples_declarations", payl=clean_payload, skip_validation=True
        )

        merged_payload = merge_response_into_payload(payload, new_response[0], clean_elems)

        return merged_payload
    return None

