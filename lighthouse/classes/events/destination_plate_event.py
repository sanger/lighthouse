from lighthouse.classes.plate_event import PlateEvent


class DestinationPlateEvent(PlateEvent):
    def __init__(self, name: str) -> None:
        super().__init__(name=name, plate_type=PlateEvent.PlateTypeEnum.DESTINATION)
