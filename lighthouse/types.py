from typing import Any, Dict, List, Protocol, Tuple, Union, Optional

SampleDoc = Dict[str, Any]
SampleDocs = List[SampleDoc]
SourcePlateDoc = Dict[str, Any]
FlaskResponse = Tuple[Dict[str, Any], int]

EventDoc = Dict[str, Any]

Subject = Dict[str, str]
Event = Dict[str, Union[str, List[Subject], Dict]]
EventMessage = Dict[str, Union[str, Event]]


class EventPropertyProtocol(Protocol):
    @property
    def _params(self) -> Dict[str, str]:
        ...

    def process_validation(self, condition: bool, message: str) -> None:
        ...

    def validation_scope(self):
        ...

    def is_integer(self, n: Optional[str]) -> bool:
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


class SourceNoPickableSamples(PlateEvent):
    ...


class SourceCompleted(PlateEvent):
    ...
