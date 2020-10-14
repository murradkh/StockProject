class StockServerUnReachable(Exception):
    def __init__(self, message):
        self.message = message
        super(StockServerUnReachable, self).__init__(message)


class StockSymbolNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super(StockSymbolNotFound, self).__init__(message)
