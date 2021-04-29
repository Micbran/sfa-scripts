import random
# I love ABC to death but python2 makes ABC a lot more of a pain
# So, even though ValueRange isn't marked as abstract, it absolutely is


class ValueRange(object):
    def __init__(self, first_value, second_value):
        self.first_value = first_value
        self.second_value = second_value

    def __getitem__(self, item):
        if item == 0:
            return self.first_value
        elif item == 1:
            return self.second_value
        else:
            raise TypeError

    def as_tuple(self):
        return self.first_value, self.second_value

    def as_range(self):
        return range(self.first_value, self.second_value)


class MinMaxRange(ValueRange):
    def __init__(self, first_value, second_value):
        super(MinMaxRange, self).__init__(first_value, second_value)
        self._min = min(first_value, second_value)
        self._max = max(first_value, second_value)

    def __getitem__(self, item):
        if item == 0:
            return self._min
        elif item == 1:
            return self._max
        raise TypeError

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    def as_tuple(self):
        return self._min, self._max

    def as_range(self):
        return range(self._min, self._max)

    def random_value_within(self):
        return random.uniform(self._min, self._max)


class XYZMinMaxRange(object):
    def __init__(self, x_min_max_range, y_min_max_range, z_min_max_range):
        if type(x_min_max_range) is MinMaxRange:
            self._x_min_max_range = x_min_max_range
        elif type(x_min_max_range) is tuple:
            self._x_min_max_range = MinMaxRange(x_min_max_range[0], x_min_max_range[1])
        else:
            raise TypeError

        if type(y_min_max_range) is MinMaxRange:
            self._y_min_max_range = y_min_max_range
        elif type(y_min_max_range) is tuple:
            self._y_min_max_range = MinMaxRange(y_min_max_range[0], y_min_max_range[1])
        else:
            raise TypeError

        if type(z_min_max_range) is MinMaxRange:
            self._z_min_max_range = z_min_max_range
        elif type(z_min_max_range) is tuple:
            self._z_min_max_range = MinMaxRange(z_min_max_range[0], z_min_max_range[1])
        else:
            raise TypeError

    def __getitem__(self, item):
        if item == 'x':
            return self._x_min_max_range
        elif item == 'y':
            return self._y_min_max_range
        elif item == 'z':
            return self._z_min_max_range
        raise TypeError

    def random_values_within(self):
        x_rand = self._x_min_max_range.random_value_within()
        y_rand = self._y_min_max_range.random_value_within()
        z_rand = self._z_min_max_range.random_value_within()
        return x_rand, y_rand, z_rand
