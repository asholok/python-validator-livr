#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import datetime

try:
    import constants
except ImportError:
    from . import constants

def basic_check(func):
    def dec(obj, value, unuse, output):
        if constants.EMPTY_PRIMITIVE(value):
            return
        if not isinstance(value, constants.PRIMITIVE_LIST):
            return 'FORMAT_ERROR'
        return func(obj, value, unuse, output)
    return dec


class Email(object):
    _reg_exp_mail = r'^(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])+\Z'
    def __init__(self, *args):
        pass
    
    @basic_check
    def __call__(self, email=None, unuse=None, unuse_=None):
        if not re.match(self._reg_exp_mail, constants.TO_STRING(email), re.IGNORECASE):
            return 'WRONG_EMAIL'
        if re.match(r'\@.*\@', constants.TO_STRING(email)):
            return 'WRONG_EMAIL'
        if re.match(r'\@.*_', constants.TO_STRING(email)):
            return 'WRONG_EMAIL'


class EqualToField(object):
    def __init__(self, *args):
        self._field = args[1]

    @basic_check
    def __call__(self, value, params, unuse):
        other = params.get(self._field)
        # Values are compared as strings, a missing field is not equal to any value
        if not isinstance(other, constants.PRIMITIVE_LIST):
            return 'FIELDS_NOT_EQUAL'
        if constants.TO_STRING(value) != constants.TO_STRING(other):
            return 'FIELDS_NOT_EQUAL'


class Url(object):
    _url_re = re.compile(
        r'^(?:http|https)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)\Z', re.I)
    
    def __init__(self, *args):
        pass

    @basic_check
    def __call__(self, value, params, unuse):
        value = constants.TO_STRING(value)
        if len(value) < 2083 and self._url_re.match(value):
            return

        return 'WRONG_URL'


class IsoDate(object):
    def __init__(self, *args):
        pass

    @basic_check
    def __call__(self, value, params, unuse):
        value = constants.TO_STRING(value)
        # strptime() also accepts one-digit months and days ("2024-1-1")
        if not re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}\Z', value):
            return 'WRONG_DATE'
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return 'WRONG_DATE'
