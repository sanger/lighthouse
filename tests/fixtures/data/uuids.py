from uuid import uuid4
from uuid import UUID

TESTING_UUIDS = {}


def testing_uuid(num: int) -> UUID:
    if not (num in TESTING_UUIDS):
        TESTING_UUIDS[num] = uuid4()
    return TESTING_UUIDS[num]


def testing_uuid_utf8(num: int) -> bytes:
    return str(testing_uuid(num)).encode("utf-8")


def testing_uuid_binary(num: int) -> bytes:
    return testing_uuid(num).bytes
