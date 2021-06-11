class ServiceCherryTrackerMixin(object):
    def get_run_info(self, run_id):
        return None

    def get_samples_from_source_plates(self, source_plates):
        return None

    def get_samples_from_mongo(self, samples):
        return []
