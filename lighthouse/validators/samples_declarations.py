from flask import current_app as app

from eve.io.mongo import Validator  # type: ignore
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

    # TODO: check
    # if len(duplicate_sample_ids) == 0 and len(non_exist_samples):
    #     return request

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

