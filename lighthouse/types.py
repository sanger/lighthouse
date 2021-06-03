from typing import Any, Dict, List, Protocol, Tuple, Union

SampleDoc = Dict[str, Any]
SampleDocs = List[SampleDoc]
SourcePlateDoc = Dict[str, Any]
FlaskResponse = Tuple[Dict[str, Any], int]

Subject = Dict[str, str]
Event = Dict[str, Union[str, List[Subject], Dict]]
EventMessage = Dict[str, Union[str, Event]]


class PlateEvent(Protocol):
    """This class is used to assist the mixin while type checking."""

    @property
    def plate_barcode(self) -> str:
        ...

    @property
    def robot_serial_number(self) -> str:
        ...
