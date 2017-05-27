class SingleTestHandler(object):
    def __init__(self, host, port, ticker):
        self.ticker = ticker
        self.base_url = str.format('http://{0}:{1}/list={2}', host, port, ticker)
    