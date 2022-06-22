class DataError(Exception):
    """Raised when the input value is not well structured"""

    def __init__(self, line, message="Check your input data file near the line: '{}'"):
        self.message = message.format(line)
        super().__init__(self.message)


class DayOutboundError(Exception):
    """Raised when the schedule go across two or more days"""

    def __init__(self, line,
                 message="No single lapse in schedule can go across two days. you should separate them. line: {}"):
        self.message = message.format(line)
        super().__init__(self.message)
