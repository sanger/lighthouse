import logging
from typing import cast, Optional, List, Dict, Any

from eve import Eve
from flask import current_app as app

logger = logging.getLogger(__name__)

class BaracodaServiceMixin:

    def get_barcodes_for_samples(self, num_samples, centre_prefix):
        logger.info(f"Getting COG-UK barcodes for {num_samples} samples")
        baracoda_url = f"http://{app.config['BARACODA_URL']}/barcodes_group/{centre_prefix}/new?count={num_samples}"
        
        return self._post_request_to_baracoda(baracoda_url)

    def _post_request_to_baracoda(self, baracoda_url):

        retries = app.config["BARACODA_RETRY_ATTEMPTS"]
        success_operation = False
        except_obj = None
        barcodes = []

        while retries > 0:
            try:
                logger.debug(f"Attempting POST to {baracoda_url}")
                response = requests.post(baracoda_url)
                if response.status_code == HTTPStatus.CREATED:
                    success_operation = True
                    retries = 0
                    barcodes = response.json()["barcodes_group"]["barcodes"]
                else:
                    retries = retries - 1
                    logger.error("Unable to create COG barcodes")
                    logger.error(response.json())
                    except_obj = Exception("Unable to create COG barcodes")
            except requests.ConnectionError:
                retries = retries - 1
                logger.error("Unable to access baracoda")
                except_obj = requests.ConnectionError("Unable to access baracoda")

        if not success_operation and except_obj is not None:
            raise except_obj

        return barcodes