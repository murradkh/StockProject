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
    def __init__(self, message="the amount of bought stocks is less than requested stocks to sell!"):
        self.message = message
        super(InvalidSellQuantityValue, self).__init__(message)


class InAdequateBudgetLeft(Exception):
    def __init__(self, message="no enough budget left to user to perform buy transaction!"):
        self.message = message
        super(InAdequateBudgetLeft, self).__init__(message)


class InvalidQuantityValue(Exception):
    def __init__(self, message="Invalid quantity value, less than 1"):
        self.message = message
        super(InvalidQuantityValue, self).__init__(message)
