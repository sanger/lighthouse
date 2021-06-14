class ServiceMongoMixin(object):
    def __init__(self):
        ...

    def get_samples_from_mongo(self, samples):
        return []

    def get_source_plate_uuid(self, barcode):
        return "1234"
