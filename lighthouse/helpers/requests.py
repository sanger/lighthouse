import logging
from typing import Any, Iterable, Optional, Tuple, Type, cast

from flask.wrappers import Request

from lighthouse.types import EndpointParamsException

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


def get_required_params_from_json_body(
    request: Request, required_params: Tuple[str, ...], expected_types: Tuple[Type, ...]
) -> Tuple[Any, ...]:
    """Get the required parameters parsed from the JSON body of the request; in the order they were provided.

    Arguments:
        request (Request): the request which contains the parameters to be extracted from.
        required_params (Tuple[str, ...]): the parameters to extract and test.
        expected_types (Tuple[Type, ...]): the expected types of the parameters.

    Raises:
        EndpointParamsException: if any of the required parameters are missing, empty or of the wrong type.

    Returns:
        Tuple[str, ...]: the parameters extracted from the request, in the order provided.
    """
    logger.info(f"Extracting the following parameters from the request body's JSON: {required_params}")

    if (request_json := request.get_json()) is None or not isinstance(request_json, dict):
        raise EndpointParamsException("The request body must contain a JSON dictionary.")

    def extract_and_test(param: str) -> Any:
        # check that the value exists in the dictionary, is not None and is not an empty string
        if (
            request_json is None
            or (param_value := request_json.get(param)) is None
            or (type(param_value) is str and not param_value)
        ):
            return None

        return param_value

    required_params_dict = {param: extract_and_test(param) for param in required_params}

    #  get a list of all those which have not been set
    missing_params = [param for (param, value) in required_params_dict.items() if value is None]

    if missing_params:
        formatted_missing_params = "'{0}'".format("', '".join(missing_params))
        raise EndpointParamsException(f"POST request body JSON needs {formatted_missing_params} parameter(s).")

    # check the type of all the values
    wrong_types = [
        param
        for ((param, value), exp_type) in zip(required_params_dict.items(), expected_types)
        if type(value) != exp_type
    ]

    if wrong_types:
        formatted_type_params = "'{0}'".format("', '".join(wrong_types))
        raise EndpointParamsException(
            f"POST request body JSON contains parameter(s) {formatted_type_params} of the wrong type."
        )

    # we can rely on the order of values in the dictionary since Python 3.7
    return tuple(required_params_dict.values())
