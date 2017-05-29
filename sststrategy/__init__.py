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

    @staticmethod
    def get_min_value(series, look_back_period):
        if len(series) <= look_back_period:
            return min(series)
        min_value = min(series[-look_back_period:])
        if min_value == series[-look_back_period]:
            additional_look_back = min(2 * look_back_period, len(series))
            min_value = min(series[-additional_look_back:])
        return min_value

    @staticmethod
    def get_max_value(series, look_back_period):
        if len(series) <= look_back_period:
            return max(series)
        max_value = max(series[-look_back_period:])
        if max_value == series[-look_back_period]:
            additional_look_back = max(2 * look_back_period, len(series))
            max_value = max(series[-additional_look_back:])
        return max_value

    @staticmethod
    def is_owl_short_after_ambiguous_up(rl10, rl30, dragon_mean, dragon_lower, look_back_period):
        return SignalFinder.is_slope_negative(rl10) and \
               SignalFinder.is_slope_negative(rl30) and \
               SignalFinder.is_slope_negative(dragon_mean) and \
               SignalFinder.is_cross_below(rl10, rl30, look_back_period) and \
               SignalFinder.is_cross_below(rl10, dragon_lower, look_back_period)

    @staticmethod
    def is_owl_long_after_ambiguous_down(rl10, rl30, dragon_mean, dragon_upper, look_back_period):
        return SignalFinder.is_slope_positive(rl10) and \
               SignalFinder.is_slope_positive(rl30) and \
               SignalFinder.is_slope_positive(dragon_mean) and \
               SignalFinder.is_cross_above(rl10, rl30, look_back_period) and \
               SignalFinder.is_cross_above(rl10, dragon_upper, look_back_period)
