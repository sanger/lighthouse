import logging
from typing import Iterable, Optional, Tuple, cast

from flask.wrappers import Request

logger = logging.getLogger(__name__)


def get_required_params(request: Request, required_params: Tuple[str, ...]) -> Tuple[str, ...]:
    """Get the required parameters parsed from the URL of the request; in the order they were provided.

    Args:
        request (Request): the request which contains the parameters to be extracted from.
        required_params (Tuple[str, ...]): the parameters to extract and test.

    Raises:
        Exception: if any of the required parameters are missing or empty.

    Returns:
        Tuple[str, ...]: the parameters extracted from the request, in the order provided.
    """
    logger.info(f"Extracting the following parameters from the request: {required_params}")

    def extract_and_test(param: str) -> Optional[str]:
        # extract the parameter from the request
        param_from_req = request.args.get(param, type=str)

        # check that the value is not None or an empty string
        if param_from_req is not None and param_from_req:
            return param_from_req

        return None

    required_params_dict = {param: extract_and_test(param) for param in required_params}

    #  get a list of all those which have not been set, i.e. empty strings
    missing_params = list(filter(lambda param: required_params_dict.get(param) is None, required_params_dict))

    if missing_params:
        formatted_missing_params = "'{0}'".format("', '".join(missing_params))

        raise Exception(f"GET request needs {formatted_missing_params} in URL")

    return tuple(cast(Iterable[str], required_params_dict.values()))
