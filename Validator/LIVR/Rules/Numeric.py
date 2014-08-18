import re

class Integer(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, unuse_):
        if not value:
            return
        if not re.match("^-?[0-9]+$", str(value)):
            return 'NOT_INTEGER'

class PositiveInteger(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, unuse_):
        if not value:
            return
        if not re.match("^[1-9][0-9]*$", str(value)):
            return 'NOT_POSITIVE_INTEGER'

class Decimal(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, unuse_):
        if not value:
            return
        if not re.match("^(?:-?([0-9]+\.[0-9]+)|(?:[0-9]+))+$", str(value)):
            return 'NOT_DECIMAL'

class PositiveDecimal(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, unuse_):
        if not value:
            return
        if not re.match("^(?:([0-9]+\.[0-9]+)|(?:[0-9]+))+$", str(value)):
            return 'NOT_POSITIVE_DECIMAL'

class MaxNumber(object):
    def __init__(self, *args):
        self._max_number = args[1]

    def __call__(self, number, unuse, unuse_):
        if not number:
            return

        if number > self._max_number:
            return 'TOO_HIGH'

class MinNumber(object):
    def __init__(self, *args):
        self._min_number = args[1]

    def __call__(self, number, unuse, unuse_):
        if not number:
            return

        if number < self._min_number:
            return 'TOO_LOW'

class BetweenNumbers(object):
    def __init__(self, *args):
        self._min_number = args[1]
        self._max_number = args[2]

    def __call__(self, number, unuse, unuse_):
        if not number:
            return

        if number > self._max_number:
            return 'TOO_HIGH'
        if number < self._min_number:
            return 'TOO_LOW'
