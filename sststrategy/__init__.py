class SignalFinder(object):
    @staticmethod
    def is_ambiguous_downwards_move(rl10, bb1_lower, look_back_period, ambiguous_move_percent):
        if len(rl10) < look_back_period:
            return False
        down_count = 0
        for i in range(0, look_back_period):
            reverse_index = i - look_back_period
            if rl10[reverse_index] <= bb1_lower[reverse_index]:
                down_count += 1
        return float(down_count / look_back_period) >= ambiguous_move_percent

    @staticmethod
    def is_ambiguous_upwards_move(rl10, bb1_upper, look_back_period, ambiguous_move_percent):
        if len(rl10) < look_back_period:
            return False
        up_count = 0
        for i in range(0, look_back_period):
            reverse_index = i - look_back_period
            if rl10[reverse_index] >= bb1_upper[reverse_index]:
                up_count += 1
        return float(up_count / look_back_period) >= ambiguous_move_percent

    @staticmethod
    def is_slope_positive(data_series):
        if len(data_series) < 2:
            return False
        return data_series[-1] / data_series[-2] >= 1

    @staticmethod
    def is_slope_negative(data_series):
        if len(data_series) < 2:
            return False
        return data_series[-1] / data_series[-2] <= 1

    @staticmethod
    def is_cross_above(series_1, series_2, look_back_period):
        if len(series_1) < look_back_period or len(series_2) < look_back_period:
            return False

        if series_1[-1] >= series_2[-1]:
            for i in range(0, look_back_period):
                reverse_index = i - look_back_period
                if series_1[reverse_index] < series_2[reverse_index]:
                    return True
        return False

    @staticmethod
    def is_cross_below(series_1, series_2, look_back_period):
        if len(series_1) < look_back_period or len(series_2) < look_back_period:
            return False

        if series_1[-1] <= series_2[-1]:
            for i in range(0, look_back_period):
                reverse_index = i - look_back_period
                if series_1[reverse_index] > series_2[reverse_index]:
                    return True
        return False
