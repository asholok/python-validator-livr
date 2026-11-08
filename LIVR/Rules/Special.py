#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

try:
    import constants
    import Dates
except ImportError:
    from . import constants
    from . import Dates

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
        if constants.TO_STRING(value) != constants.TO_STRING(other) \
                and constants.TO_STRING_2_0(value) != constants.TO_STRING_2_0(other):
            return 'FIELDS_NOT_EQUAL'


class Url(object):
    # LIVR 2.5: no dot after the host, labels of 1-63 characters (the top-level domain too),
    # ports of 1-5 ASCII digits up to 65535. Labels cannot contain ".", so they do not overlap
    _url_re = re.compile(
        r'^(?:http|https)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,63})|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::(?:[0-9]{1,4}|[0-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?'
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
        # LIVR 2.5: an options object with the bounds "min" and "max". LIVR 2.0 ignored the
        # arguments, so {"iso_date": null} stays the plain iso_date
        if len(args) == 2 and args[1] is None:
            args = args[:1]
        self._min, self._max = Dates.date_bounds('iso_date', args)

    @basic_check
    def __call__(self, value, params, unuse):
        if not isinstance(value, constants.STRING_TYPES) or Dates.parse_date(value) is None:
            return 'WRONG_DATE'
        return Dates.check_date_bounds(value, self._min, self._max)
