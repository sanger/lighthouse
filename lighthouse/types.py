from typing import Any, Dict, List, Optional, Protocol, Tuple, Union

SampleDoc = Dict[str, Any]
SampleDocs = List[SampleDoc]
SourcePlateDoc = Dict[str, Any]
FlaskResponse = Tuple[Dict[str, Any], int]

EventDoc = Dict[str, Any]

Subject = Dict[str, str]
Event = Dict[str, Union[str, List[Subject], Dict]]
EventMessage = Dict[str, Union[str, Event]]


class EventPropertyProtocol(Protocol):
    def get_param_value(self, param_name: str) -> Optional[Any]:
        ...

    def process_validation(self, condition: bool, message: str) -> None:
        ...

    def validation_scope(self):
        ...


class PlateEvent(Protocol):
    """This class is used to assist the mixin while type checking."""

    @property
    def properties(self) -> Dict[str, Any]:
        ...

    @property
    def plate_barcode(self) -> str:
        ...

    @property
    def robot_serial_number(self) -> str:
        ...
