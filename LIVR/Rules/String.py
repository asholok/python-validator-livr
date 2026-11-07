#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

try:
    import constants
    import Helper
except ImportError:
    from . import constants
    from . import Helper

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


def comparison_check(func):
    # Like base_string_check, but the value keeps its type: a boolean has two comparison forms
    def dec(obj, value, unuse, output):
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

        # Built on the first validation, so building a validator stays cheap
        self._allowed = None

    def _build_allowed(self):
        # The allowed value of each comparison form, the first one wins
        allowed = {}
        for val in reversed(self._allowed_list):
            allowed[constants.TO_STRING(val)] = val
            if isinstance(val, bool):
                allowed[constants.TO_STRING_2_0(val)] = val
        return allowed
    
    @comparison_check
    def __call__(self, value, unuse, output):
        allowed = self._allowed
        if allowed is None:
            allowed = self._allowed = self._build_allowed()
        for form in constants.COMPARISON_FORMS(value):
            if form in allowed:
                output.append(allowed[form])
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
        self._allowed_forms = constants.COMPARISON_FORMS(self._allowed_value)

    @comparison_check
    def __call__(self, value, unuse, output):
        for form in constants.COMPARISON_FORMS(value):
            if form in self._allowed_forms:
                output.append(self._allowed_value)
                return
        return 'NOT_ALLOWED_VALUE'

class String(object):
    def __init__(self, *args):
        pass
        
    @base_string_check
    def __call__(self, value, unuse, output):
        output.append(value)


def string_rule(func):
    # LIVR 2.5 string rules: empty values pass, the check gets the string form
    def dec(obj, value, unuse, output):
        if Helper.is_empty(value):
            return
        if not Helper.is_primitive(value):
            return 'FORMAT_ERROR'
        return func(obj, Helper.string_form(value), output)
    return dec

class NotOneOf(object):
    def __init__(self, *args):
        if len(args) < 2:
            Helper.schema_error('not_one_of', 'one or more values are required')
        for val in args[1:]:
            if not Helper.is_primitive(val):
                Helper.schema_error('not_one_of', 'values must be primitive values')
        self._forbidden = set(Helper.string_form(val) for val in args[1:])

    def __call__(self, value, unuse, output):
        if Helper.is_empty(value):
            return
        if not Helper.is_primitive(value):
            return 'FORMAT_ERROR'
        if Helper.string_form(value) in self._forbidden:
            return 'NOT_ALLOWED_VALUE'

class Digits(object):
    def __init__(self, *args):
        Helper.no_arguments('digits', args)

    @string_rule
    def __call__(self, value, output):
        if not re.match(r'[0-9]+\Z', value):
            return 'NOT_DIGITS'
        output.append(value)

class Affix(object):
    # starts_with, ends_with and contains: one or more non-empty strings
    _rule_name = None

    def __init__(self, *args):
        if len(args) < 2:
            Helper.schema_error(self._rule_name, 'one or more strings are required')
        self._affixes = [Helper.string_argument(self._rule_name, arg) for arg in args[1:]]
        if '' in self._affixes:
            Helper.schema_error(self._rule_name, 'strings must not be empty')

    @string_rule
    def __call__(self, value, output):
        for affix in self._affixes:
            if self._matches(value, affix):
                output.append(value)
                return
        return 'WRONG_FORMAT'

class StartsWith(Affix):
    _rule_name = 'starts_with'

    def _matches(self, value, affix):
        return value.startswith(affix)

class EndsWith(Affix):
    _rule_name = 'ends_with'

    def _matches(self, value, affix):
        return value.endswith(affix)

class Contains(Affix):
    _rule_name = 'contains'

    def _matches(self, value, affix):
        return affix in value
