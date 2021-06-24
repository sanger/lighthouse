from lighthouse.messages.message import Message


class SequencescapeMessage(Message):
    def __init__(self):
        self._barcode = None
        self._contents = {}

    def set_barcode(self, barcode):
        self._barcode = barcode

    def set_well_sample(self, location, sample_info):
        self._contents[location] = sample_info
