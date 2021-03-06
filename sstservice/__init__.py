import pandas as pd
import os
from sststrategy import SignalFinder as F
from enum import Enum

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
LOOK_BACK_PERIOD = 10


class Status(Enum):
    INIT = 'Initial State'
    AMBIGUOUS_DOWN = 'Ambiguous Downward'
    AMBIGUOUS_UP = 'Ambiguous Up'
    OWL_LONG = 'Owl Long'
    OWL_SHORT = 'Owl Short'


class TradeDirection(Enum):
    LONG = 'Long'
    SHORT = 'Short'


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
        self._state = Status.INIT
        self.map = {
            Status.INIT: self.initial_status,
            Status.AMBIGUOUS_UP: self.ambiguous_up,
            Status.AMBIGUOUS_DOWN: self.ambiguous_down,
            # Status.OWL_LONG: self.initial_status,
            # Status.OWL_SHORT: self.initial_status,
        }

        self._last_move_index = 0

    def run_test(self):
        for curr_i in range(1, len(self._date) - 1):
            # if self._date[curr_i].strftime(DATETIME_FORMAT) == '2017-05-15 12:01:00':
            #     print(self._date[curr_i].strftime(DATETIME_FORMAT))
            self.map.get(self._state)(curr_i + 1)

    def initial_status(self, i):
        if F.is_ambiguous_downwards_move(rl10=self.rl10[:i], bb1_lower=self.bb1_lower[:i], ambiguous_move_percent=0.85,
                                         look_back_period=LOOK_BACK_PERIOD):
            self._state = Status.AMBIGUOUS_DOWN
        if F.is_ambiguous_upwards_move(rl10=self.rl10[:i], bb1_upper=self.bb1_upper[:i], ambiguous_move_percent=0.85,
                                       look_back_period=LOOK_BACK_PERIOD):
            self._state = Status.AMBIGUOUS_UP

    def ambiguous_up(self, i):
        if F.is_owl_short_after_ambiguous_up(self.rl10[:i], self.rl30[:i], self.dragon_mean[:i], self.dragon_lower[:i],
                                             LOOK_BACK_PERIOD):
            # if F.is_slope_negative(self.rl10[:i]) and \
            #         F.is_slope_negative(self.rl30[:i]) and \
            #         F.is_slope_negative(self.dragon_mean[:i]) and \
            #         F.is_cross_below(self.rl10[:i], self.rl30[:i], look_back_period=LOOK_BACK_PERIOD) and \
            #         F.is_cross_below(self.rl10[:i], self.dragon_lower[:i], look_back_period=LOOK_BACK_PERIOD):
            print(self._date[:i][-1].strftime(DATETIME_FORMAT) + ' ' + 'SHORT OWL')
            # TODO: should here enter the trade and figure out the exit strategy
            self._state = Status.INIT
        if not F.is_ambiguous_upwards_move(self.rl10[:i], self.bb1_upper[:i], LOOK_BACK_PERIOD, 0.85) and \
                        (i - self._last_move_index) > LOOK_BACK_PERIOD:
            # we here check if the price has moved a lot but took too long to reverse.
            self._state = Status.INIT
        self._last_move_index = i

    def ambiguous_down(self, i):
        if F.is_owl_long_after_ambiguous_down(self.rl10[:i], self.rl30[:i], self.dragon_mean[:i], self.dragon_upper[:i],
                                              LOOK_BACK_PERIOD):
            # if F.is_slope_positive(self.rl10[:i]) and \
            #         F.is_slope_positive(self.rl30[:i]) and \
            #         F.is_slope_positive(self.dragon_mean[:i]) and \
            #         F.is_cross_above(self.rl10[:i], self.rl30[:i], look_back_period=LOOK_BACK_PERIOD) and \
            #         F.is_cross_above(self.rl10[:i], self.dragon_upper[:i], look_back_period=LOOK_BACK_PERIOD):
            print(self._date[:i][-1].strftime(DATETIME_FORMAT) + ' ' + 'LONG OWL')
            # TODO: should here enter the trade and figure out the exit strategy
            self._state = Status.INIT

        if not F.is_ambiguous_downwards_move(self.rl10[:i], self.bb1_lower[:i], LOOK_BACK_PERIOD, 0.85) and \
                        (i - self._last_move_index) > LOOK_BACK_PERIOD:
            # we here check if the price has moved a lot but took too long to reverse.
            self._state = Status.INIT
        self._last_move_index = i

    def owl_long(self, i):
        pass

    def owl_short(self, i):
        pass

    def pocket_long(self, i):
        pass

    def pocket_short(self, i):
        pass


class Trade(object):
    def __init__(self, enter_price, trade_direction, enter_time, stop_price):
        self.enter_price = enter_price
        self.direction = trade_direction
        self.enter_time = enter_time
        self.exit_price = None
        self.exit_time = None
        self.initial_stop = stop_price
        self.stop_price = stop_price

    def is_stop_hit(self, high, low, curr_time):
        if (self.direction == TradeDirection.LONG and self.stop_price >= low) or (
                self.direction == TradeDirection.SHORT and self.stop_price <= high):
            self.exit_price = self.stop_price
            self.exit_time = curr_time
            return True
        return False

    def is_open_trade(self):
        return self.exit_price is None

    @staticmethod
    def output_header():
        return 'Instrument,Action,Type,Quantity,Limit,Stop,State,Filled,Avg. price,Remaining,Name,Strategy,OCO,TIF,Account display name,ID,Time,Cancel,' + os.linesep


# For an initial exit strategy:
# in the money => 1) really go my way 2) just in the money, it is separated if I have already made the R
# if I am really deep in the money, then, price jump out of dragon. RL10 X RL30, RL30 turned, hit Z3. trailing stop with maximum bar.
# if not working, really stop out.