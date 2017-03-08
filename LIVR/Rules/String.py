#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

try:
    import constants
except ImportError:
    from . import constants

def base_string_check(func):
    def dec(obj, value, unuse, output):
        if isinstance(value, (int, float)):
            value = str(value)
        if constants.EMPTY_PRIMITIVE(value):
            return
        if not isinstance(value, constants.PRIMITIVE_LIST):
            return 'FORMAT_ERROR'
        return func(obj, value, unuse, output)
    return dec


class OneOf(object):
    def __init__(self, *args):
        self._allowed_list = args[1]
        
        if not isinstance(self._allowed_list, list):
            self._allowed_list = args[1:]
    
    @base_string_check
    def __call__(self, value, unuse, output):
        for val in self._allowed_list:
            if str(value) == str(val):
                output.append(val)
                return
        return 'NOT_ALLOWED_VALUE'

class MaxLength(object):
    def __init__(self, *args):
        self._max_length = int(args[1])
        # if self._max_length < 1:
        #     raise Exception('Wrong standard value! Only positive value')

    @base_string_check
    def __call__(self, value, unuse, output):
        if len(value) > self._max_length:
            return 'TOO_LONG'
        output.append(value)

class MinLength(object):
    def __init__(self, *args):
        self._min_length = args[1]

    @base_string_check
    def __call__(self, value, unuse, output):        
        if len(value) < self._min_length:
            return 'TOO_SHORT'
        output.append(value)

class EqualLength(object):
    def __init__(self, *args):
        self._length = args[1]

    @base_string_check
    def __call__(self, value, unuse, output):
        if len(value) > self._length:
            return 'TOO_LONG'
        if len(value) < self._length:
            return 'TOO_SHORT'
        output.append(value)

class BetweenLength(object):
    def __init__(self, *args):
        self._min_length = args[1]
        self._max_length = args[2]
        # if self._max_length < 1:
        #     raise Exception('Wrong standard value! Only positive value')

    @base_string_check
    def __call__(self, value, unuse, output):
        if len(value) > self._max_length:
            return 'TOO_LONG'
        if len(value) < self._min_length:
            return 'TOO_SHORT'
        output.append(value)

class Like(object):
    def __init__(self, *args):
        self._sample = args[1]
        try:
            self._flag = str(args[2]).lower()
        except:
            self._flag = ''

    @base_string_check
    def __call__(self, value, unuse, output):
        if not re.match(self._sample, str(value), re.I if self._flag == 'i' else re.U):
            return 'WRONG_FORMAT'
        output.append(value)

class Eq(object):
    def __init__(self, *args):
        self._allowed_value = args[1]

    @base_string_check
    def __call__(self, value, unuse, output):
        if str(self._allowed_value) == str(value):
            output.append(self._allowed_value)
            return
        return 'NOT_ALLOWED_VALUE'

class String(object):
    def __init__(self, *args):
        pass
        
    @base_string_check
    def __call__(self, value, unuse, output):
        output.append(value)

