import logging
import logging.config
from http import HTTPStatus

from eve import Eve  # type: ignore
from flask_apscheduler import APScheduler  # type: ignore

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


# [
# {"root_sample_id": "0012", "declared_at": "2013-04-04T10:29:13"}, 
# {"root_sample_id": "0012", "declared_at": "2013-04-04T10:29:13"}, 
# {"root_sample_id": "0010", "declared_at": "2013-04-04T10:29:13"}, 
# {"root_sample_id": "0011", "declared_at": "2013-04-04T10:29:13"}
# ]
def check_samples_are_unique(request):
    sample_ids = get_samples(request)

    dups = []  
    index = 0

    while (index < len(sample_ids)):
        sample = sample_ids[index]
        # print('sample', sample)
        print('index', index)

        if sample_ids.count(sample) > 1:
            print('dup sample', sample)
            dups.append(index)
        index = index + 1

    # duplicates = set([index for index in len(sample_ids) if sample_ids.count(sample_ids[index]) > 1])
    # duplicates = set([x for x, index in sample_ids if sample_ids.count(x) > 1])
    print('duplicates', dups)


    # if unique:
    #     return True
    # else:
    #     data = request.get_data().decode()
    #     print('data', data)
        
    #   add flag to say is a duplicate
    

def check_samples_exist(request):
    sample_ids = get_samples(request)
    cursor = app.data.driver.db.samples.find({"Root Sample ID": { "$exists": "true", "$in": sample_ids } })
    exist = cursor.count()==len(sample_ids)

    if exist: 
        return True
    else:
        data = request.get_data().decode()
        # [{"root_sample_id": "0012", "declared_at": "2013-04-04T10:29:13", "": }]

        # results = cursor.toArray()
        print('cursor', cursor.count())
        
        existing = []

        for record in cursor:
            existing.append(record['Root Sample ID'])
        
        print('existing', existing)
        print('sample_ids', sample_ids)

        print('not exist', exist)
    #   add new field/flag to sample item, says doesnt exist in database

    
# get/ check/ change/ return request
def pre_samples_declarations_post_callback(request):
    check_samples_are_unique(request)
    # check_samples_exist(request)

    return request

    # valid = unique and exist 
    # if valid:
    #     print('valid', valid)
    #     return request
    # else:
    #     print('not valid', valid)
    #     print('request', request)
    #     if not unique:
    #     elif not exist:
    #         
        



    # class validate
    # checks one by one
    # check flag for unique/ exist

    # fail in validator -> returns correct response
    

def create_app() -> Eve:
    app = Eve(__name__)
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
