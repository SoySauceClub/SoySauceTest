import pandas as pd

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class SingleTestHandler(object):
    def __init__(self, host, port, ticker):
        self.ticker = ticker
        self.base_url = str.format('http://{0}:{1}/list?instrument={2}', host, port, ticker)
        self.treade_list = []

    def run_test(self, start_date, end_date):
        pass

    def run_date(self, run_date):
        url = str.format('{0}&start={1}&end={1}', self.base_url, run_date)
        df = pd.read_json(url).set_index('date')
        sdt = SingleDayTest(self.ticker, df)
        sdt.run_test()


class SingleDayTest(object):
    def __init__(self, ticker, df):
        self.bb1_lower = df['BB1Lower'].tolist()
        self.bb1_upper = df['BB1Upper'].tolist()
        self.bb2_upper = df['BB2Upper'].tolist()
        self.bb2_lower = df['BB2Lower'].tolist()
        self.bb3_upper = df['BB3Upper'].tolist()
        self.bb3_lower = df['BB3Lower'].tolist()
        self.dragon_upper = df['DragonUpper'].tolist()
        self.dragon_lower = df['DragonLower'].tolist()
        self.bb_mean = df['BBMean'].tolist()
        self.dragon_mean = df['DragonMean'].tolist()
        self.rl10 = df['RegLine10'].tolist()
        self.rl30 = df['RegLine30'].tolist()
        self.rl90 = df['RegLine90'].tolist()
        self.rl270 = df['RegLine270'].tolist()
        self._close = df['close'].tolist()
        self._open = df['open'].tolist()
        self._high = df['high'].tolist()
        self._low = df['low'].tolist()
        self._date = df.index.tolist()
        self.ticker = ticker

    def run_test(self):
        for curr_i in range(1, len(self._date) -1):
            print(self._date[curr_i].strftime(DATETIME_FORMAT))
