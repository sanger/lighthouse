import logging
import logging.config
from http import HTTPStatus

from eve import Eve  # type: ignore
from flask_apscheduler import APScheduler  # type: ignore
from lighthouse.authorization import APIKeyAuth
from lighthouse.constants import DUPLICATE_SAMPLES, NON_EXISTING_SAMPLE

scheduler = APScheduler()

from flask import current_app as app

def get_root_sample_id(obj):
    return obj['root_sample_id']

def get_samples(request):
    json = request.get_json()

    if isinstance(json, list):
        return list(map(get_root_sample_id, json))
    else:
        return [get_root_sample_id(json)]

def find_duplicates(sample_ids):
    duplicate_sample_ids = []  
    index = 0

    while (index < len(sample_ids)):
        sample_id = sample_ids[index]

        if (sample_ids.count(sample_id) > 1) and not (sample_id in duplicate_sample_ids):
            duplicate_sample_ids.append(sample_id)
        index = index + 1

    return duplicate_sample_ids


def find_non_exist_samples(sample_ids):
    cursor = app.data.driver.db.samples.find({"Root Sample ID": { "$in": sample_ids } }, {"Root Sample ID": 1})
    
    existing_sample_ids = [val["Root Sample ID"] for val in cursor]
    not_exist_sample_ids = [val for val in sample_ids if not (val in existing_sample_ids)]
    
    return not_exist_sample_ids

def add_flags(request_element, sample_id, sample_ids, flag):
    if sample_id in sample_ids:
        if "validation_flags" in request_element:
            request_element["validation_flags"].append(flag)
        else:
            request_element["validation_flags"]=[flag]
    
def pre_samples_declarations_post_callback(request):
    sample_ids = get_samples(request)

    duplicate_sample_ids = find_duplicates(sample_ids)
    non_exist_samples = find_non_exist_samples(sample_ids)
    
    index = 0
    while (index < len(request.json)):
        sample = request.json[index]
    
        add_flags(request.json[index], sample["root_sample_id"], duplicate_sample_ids, DUPLICATE_SAMPLES)
        add_flags(request.json[index], sample["root_sample_id"], non_exist_samples, NON_EXISTING_SAMPLE)
        index = index + 1 
            
    return request

from eve.io.mongo import Validator
    # fail in validator -> returns correct response
class MyValidator(Validator):
    def _validate_validation_errors(self, validation_errors, field, value):
        if validation_errors and ('validation_flags' in self.document):
            for flag in self.document['validation_flags']:
                if flag == DUPLICATE_SAMPLES:
                    self._error(field, "Sample is a duplicate")
                if flag == NON_EXISTING_SAMPLE:
                    self._error(field, "Sample does not exist in database")

def create_app() -> Eve:
    app = Eve(__name__, validator=MyValidator, auth=APIKeyAuth)
    app.on_pre_POST_samples_declarations += pre_samples_declarations_post_callback

    # setup logging
    logging.config.dictConfig(app.config["LOGGING"])

    from lighthouse.blueprints import plates
    from lighthouse.blueprints import reports

    app.register_blueprint(plates.bp)
    app.register_blueprint(reports.bp)

    if app.config.get("SCHEDULER_RUN", False):
        scheduler.init_app(app)
        scheduler.start()

    @app.route("/health")
    def health_check():
        return "Factory working", HTTPStatus.OK

    return app
