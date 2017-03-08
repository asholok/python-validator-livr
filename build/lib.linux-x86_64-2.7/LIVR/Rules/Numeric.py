#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
try:
    import constants
except ImportError:
    from . import constants

def basic_integer_check(func):
    def dec(obj, value, unuse, output):
        if constants.EMPTY_PRIMITIVE(value):
            return
        if not isinstance(value, constants.PRIMITIVE_LIST):
            return 'FORMAT_ERROR'
        return func(obj, value, unuse, output)
    return dec

def formatize_numeric_value(value):
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError, e:
            pass
        try:
            return float(value)
        except ValueError, e:
            pass
    return value


class Integer(object):
    def __init__(self, *args):
        pass

    @basic_integer_check
    def __call__(self, value, unuse, output):
        if not re.match("^-?[0-9]+$", str(value)):
            return 'NOT_INTEGER'
        output.append(int(value))

class PositiveInteger(object):
    def __init__(self, *args):
        pass

    @basic_integer_check
    def __call__(self, value, unuse, output):
        if not re.match("^[1-9][0-9]*$", str(value)):
            return 'NOT_POSITIVE_INTEGER'
        output.append(int(value))

class Decimal(object):
    def __init__(self, *args):
        pass

    @basic_integer_check
    def __call__(self, value, unuse, output):
        if not re.match("^(?:\-?(?:[0-9]+\.[0-9]+)|(?:[0-9]+))$", str(value)):
            return 'NOT_DECIMAL'
        output.append(formatize_numeric_value(value))

class PositiveDecimal(object):
    def __init__(self, *args):
        pass

    @basic_integer_check
    def __call__(self, value, unuse, output):
        if not re.match("^(?:(?:[0-9]*\.[0-9]+)|(?:[1-9][0-9]*))$", str(value)):
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
