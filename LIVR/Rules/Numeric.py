#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import math
try:
    import constants
    import Helper
except ImportError:
    from . import constants
    from . import Helper

def basic_integer_check(func):
    def dec(obj, value, unuse, output):
        if constants.EMPTY_PRIMITIVE(value):
            return
        if not isinstance(value, constants.PRIMITIVE_LIST):
            return 'FORMAT_ERROR'
        return func(obj, value, unuse, output)
    return dec

def formatize_numeric_value(value):
    if isinstance(value, constants.STRING_TYPES):
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
    return value


class Integer(object):
    def __init__(self, *args):
        pass

    @basic_integer_check
    def __call__(self, value, unuse, output):
        if not re.match(r"^-?[0-9]+\Z", constants.TO_STRING(value)):
            return 'NOT_INTEGER'
        output.append(int(value))

class PositiveInteger(object):
    def __init__(self, *args):
        pass

    @basic_integer_check
    def __call__(self, value, unuse, output):
        if not re.match(r"^[1-9][0-9]*\Z", constants.TO_STRING(value)):
            return 'NOT_POSITIVE_INTEGER'
        output.append(int(value))

class Decimal(object):
    def __init__(self, *args):
        pass

    @basic_integer_check
    def __call__(self, value, unuse, output):
        if not re.match(r"^-?(?:[0-9]+\.[0-9]+|[0-9]+)\Z", constants.TO_STRING(value)):
            return 'NOT_DECIMAL'
        output.append(formatize_numeric_value(value))

class PositiveDecimal(object):
    def __init__(self, *args):
        pass

    @basic_integer_check
    def __call__(self, value, unuse, output):
        if not re.match(r"^(?:(?:[0-9]*\.[0-9]+)|(?:[1-9][0-9]*))\Z", constants.TO_STRING(value)):
            return 'NOT_POSITIVE_DECIMAL'
        if float(value) <= 0:
            return 'NOT_POSITIVE_DECIMAL'
        output.append(formatize_numeric_value(value))

class MaxNumber(object):
    def __init__(self, *args):
        self._max_number = float(args[1])

    @basic_integer_check
    def __call__(self, number, unuse, output):
        try:
            if float(number) > self._max_number:
                return 'TOO_HIGH'
        except:
            return "NOT_NUMBER"
        output.append(formatize_numeric_value(number))

class MinNumber(object):
    def __init__(self, *args):
        self._min_number = float(args[1])

    @basic_integer_check
    def __call__(self, number, unuse, output):
        try:
            if float(number) < self._min_number:
                return 'TOO_LOW'
        except:
            return "NOT_NUMBER"
        output.append(formatize_numeric_value(number))

class BetweenNumbers(object):
    def __init__(self, *args):
        self._min_number = float(args[1])
        self._max_number = float(args[2])

    @basic_integer_check
    def __call__(self, number, unuse, output):
        try:
            if float(number) > self._max_number:
                return 'TOO_HIGH'
            if float(number) < self._min_number:
                return 'TOO_LOW'
        except:
            return "NOT_NUMBER"
        output.append(formatize_numeric_value(number))

class MaxDecimals(object):
    def __init__(self, *args):
        if len(args) < 2:
            Helper.schema_error('max_decimals', 'a non-negative integer is required')
        self._max_decimals = Helper.non_negative_integer_argument('max_decimals', args[1])

    def __call__(self, value, unuse, output):
        if Helper.is_empty(value):
            return
        if not Helper.is_primitive(value):
            return 'FORMAT_ERROR'
        if isinstance(value, bool):
            return 'NOT_NUMBER'
        if isinstance(value, constants.STRING_TYPES):
            if not re.match(r'-?[0-9]+(?:\.[0-9]+)?\Z', value):
                return 'NOT_NUMBER'
            text = value
        else:
            text = Helper.string_form(value)
        # The output is a number, so it must be a finite double
        try:
            if math.isinf(float(value)):
                return 'NOT_NUMBER'
        except OverflowError:
            return 'NOT_NUMBER'

        # Trailing zeros after the decimal point do not count
        fraction = text.partition('.')[2].rstrip('0')
        if len(fraction) > self._max_decimals:
            return 'TOO_MANY_DECIMALS'
        output.append(formatize_numeric_value(value))
