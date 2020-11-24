class StockServerUnReachable(Exception):
    def __init__(self, message):
        self.message = message
        super(StockServerUnReachable, self).__init__(message)


class StockSymbolNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super(StockSymbolNotFound, self).__init__(message)


class InvalidTimeRange(Exception):
    def __init__(self, message):
        self.message = message
        super(InvalidTimeRange, self).__init__(message)


class InvalidSellQuantityValue(Exception):
    def __init__(self, message):
        self.message = message
        super(InvalidSellQuantityValue, self).__init__(message)
