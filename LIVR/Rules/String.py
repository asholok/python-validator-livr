#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

try:
    import constants
except ImportError:
    from . import constants

def base_string_check(func):
    def dec(obj, value, unuse, output):
        if isinstance(value, constants.NUMBER_LIST):
            value = constants.TO_STRING(value)
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
            if constants.TO_STRING(value) == constants.TO_STRING(val):
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

def whole_value_end(pattern):
    # LIVR patterns follow JavaScript, where $ matches only at the end of the value.
    # In Python it also matches before a trailing newline, so "12345\n" would match
    # "^[0-9]{5}$". Replaces $ outside character classes with \Z.
    result = []
    in_class = False
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == '\\':
            result.append(pattern[i:i + 2])
            i += 2
            continue
        if in_class:
            if char == ']':
                in_class = False
        elif char == '[':
            in_class = True
            # "]" right after "[" or "[^" is a literal, not the end of the class
            if pattern[i + 1:i + 2] == '^':
                result.append(char)
                i += 1
                char = '^'
            if pattern[i + 1:i + 2] == ']':
                result.append(char)
                i += 1
                char = ']'
        elif char == '$':
            char = '\\Z'
        result.append(char)
        i += 1
    return ''.join(result)

class Like(object):
    def __init__(self, *args):
        self._sample = whole_value_end(args[1])
        try:
            self._flag = str(args[2]).lower()
        except:
            self._flag = ''

    @base_string_check
    def __call__(self, value, unuse, output):
        if not re.search(self._sample, constants.TO_STRING(value), re.U | (re.I if self._flag == 'i' else 0)):
            return 'WRONG_FORMAT'
        output.append(value)

class Eq(object):
    def __init__(self, *args):
        self._allowed_value = args[1]

    @base_string_check
    def __call__(self, value, unuse, output):
        if constants.TO_STRING(self._allowed_value) == constants.TO_STRING(value):
            output.append(self._allowed_value)
            return
        return 'NOT_ALLOWED_VALUE'

class String(object):
    def __init__(self, *args):
        pass
        
    @base_string_check
    def __call__(self, value, unuse, output):
        output.append(value)

