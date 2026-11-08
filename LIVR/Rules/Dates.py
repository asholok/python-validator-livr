#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dates and times of LIVR 2.5. The datetime module has no year 0000, so dates are
# counted here, in the proleptic Gregorian calendar
import re
import time

try:
    import constants
    import Helper
except ImportError:
    from . import constants
    from . import Helper

DAY_MS = 86400000
RELATIVE_DAYS = {'yesterday': -1, 'today': 0, 'tomorrow': 1}

DATE_RE = re.compile(r'([0-9]{4})-([0-9]{2})-([0-9]{2})\Z')
DATETIME_RE = re.compile(
    r'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2})(?::([0-9]{2})(?:\.([0-9]{1,9}))?)?'
    r'(?:Z|([+-])([0-9]{2}):([0-9]{2}))\Z'
)
TIME_RE = re.compile(r'([0-9]{2}):([0-9]{2})(?::([0-9]{2})(?:\.([0-9]{1,9}))?)?\Z')


def utc_now():
    # The current time, Unix time in seconds. Tests replace it, or the system clock (freezegun)
    return time.time()


def today():
    # The current date in UTC, days since 1970-01-01
    return int(utc_now() // 86400)


def is_valid_date(year, month, day):
    if month < 1 or month > 12 or day < 1:
        return False
    if month == 2:
        is_leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        return day <= (29 if is_leap else 28)
    return day <= (30 if month in (4, 6, 9, 11) else 31)


def days_from_civil(year, month, day):
    # Days since 1970-01-01 (H. Hinnant's algorithm)
    year -= month <= 2
    era = year // 400
    year_of_era = year - era * 400
    day_of_year = (153 * (month + (-3 if month > 2 else 9)) + 2) // 5 + day - 1
    day_of_era = year_of_era * 365 + year_of_era // 4 - year_of_era // 100 + day_of_year
    return era * 146097 + day_of_era - 719468


def civil_from_days(days):
    days += 719468
    era = days // 146097
    day_of_era = days - era * 146097
    year_of_era = (day_of_era - day_of_era // 1460 + day_of_era // 36524 - day_of_era // 146096) // 365
    day_of_year = day_of_era - (365 * year_of_era + year_of_era // 4 - year_of_era // 100)
    mp = (5 * day_of_year + 2) // 153
    day = day_of_year - (153 * mp + 2) // 5 + 1
    month = mp + (3 if mp < 10 else -9)
    return year_of_era + era * 400 + (month <= 2), month, day


def parse_date(value):
    # Days since 1970-01-01 of a YYYY-MM-DD string, None when it is not a valid date
    match = DATE_RE.match(value)
    if not match:
        return None
    year, month, day = [int(part) for part in match.groups()]
    if not is_valid_date(year, month, day):
        return None
    return days_from_civil(year, month, day)


def parse_datetime(value):
    # Milliseconds since 1970-01-01T00:00:00Z, further fraction digits are cut off
    match = DATETIME_RE.match(value)
    if not match:
        return None
    year, month, day, hour, minute = [int(part) for part in match.groups()[:5]]
    second = int(match.group(6) or 0)
    millisecond = int((match.group(7) or '').ljust(3, '0')[:3])
    sign, offset_hour, offset_minute = match.group(8), int(match.group(9) or 0), int(match.group(10) or 0)

    if not is_valid_date(year, month, day) or hour > 23 or minute > 59 or second > 59:
        return None
    if offset_hour > 23 or offset_minute > 59:
        return None

    offset = (offset_hour * 60 + offset_minute) * 60000 * (-1 if sign == '-' else 1)
    return days_from_civil(year, month, day) * DAY_MS \
        + ((hour * 60 + minute) * 60 + second) * 1000 + millisecond - offset


def format_datetime(ms):
    days, ms = divmod(ms, DAY_MS)
    year, month, day = civil_from_days(days)
    seconds, ms = divmod(ms, 1000)
    return '%04d-%02d-%02dT%02d:%02d:%02d.%03dZ' % (
        year, month, day, seconds // 3600, seconds // 60 % 60, seconds % 60, ms)


def parse_time(value):
    # Nanoseconds since midnight
    match = TIME_RE.match(value)
    if not match:
        return None
    hour, minute = int(match.group(1)), int(match.group(2))
    second = int(match.group(3) or 0)
    nanosecond = int((match.group(4) or '').ljust(9, '0'))
    if hour > 23 or minute > 59 or second > 59:
        return None
    return ((hour * 60 + minute) * 60 + second) * 1000000000 + nanosecond


def date_bound(rule_name, bound):
    # A date bound: ('date', days) or ('relative', days from today)
    if isinstance(bound, constants.STRING_TYPES):
        if bound in RELATIVE_DAYS:
            return ('relative', RELATIVE_DAYS[bound])
        days = parse_date(bound)
        if days is not None:
            return ('date', days)
    Helper.schema_error(rule_name, 'wrong bound {!r}'.format(bound))


def check_bounds_order(rule_name, min_bound, max_bound, value_of):
    # min later than max is checked when both bounds are fixed or both are relative
    if min_bound and max_bound and (min_bound[0] == 'relative') == (max_bound[0] == 'relative'):
        if value_of(min_bound, 'min') > value_of(max_bound, 'max'):
            Helper.schema_error(rule_name, 'min is later than max')


def date_bounds(rule_name, args):
    options = Helper.options_argument(rule_name, args, ('min', 'max'))
    min_bound = date_bound(rule_name, options['min']) if 'min' in options else None
    max_bound = date_bound(rule_name, options['max']) if 'max' in options else None
    check_bounds_order(rule_name, min_bound, max_bound, lambda bound, name: bound[1])
    return min_bound, max_bound


def bound_days(bound):
    return today() + bound[1] if bound[0] == 'relative' else bound[1]


def check_date_bounds(value, min_bound, max_bound):
    # value is a valid YYYY-MM-DD string
    if min_bound is None and max_bound is None:
        return
    days = parse_date(value)
    if min_bound and days < bound_days(min_bound):
        return 'DATE_TOO_EARLY'
    if max_bound and days > bound_days(max_bound):
        return 'DATE_TOO_LATE'


def datetime_bound(bound, name):
    # ('instant', ms) or ('relative', days from today); a date is the start or the end of the day
    if isinstance(bound, constants.STRING_TYPES):
        ms = parse_datetime(bound)
        if ms is not None:
            return ('instant', ms)
        bound = date_bound('iso_datetime', bound)
        if bound[0] == 'date':
            return ('instant', bound[1] * DAY_MS + (DAY_MS - 1 if name == 'max' else 0))
        return bound
    Helper.schema_error('iso_datetime', 'wrong bound {!r}'.format(bound))


def bound_ms(bound, name, today_days=None):
    if bound[0] == 'instant':
        return bound[1]
    days = (today() if today_days is None else today_days) + bound[1]
    return days * DAY_MS + (DAY_MS - 1 if name == 'max' else 0)


class IsoDatetime(object):
    def __init__(self, *args):
        options = Helper.options_argument('iso_datetime', args, ('min', 'max'))
        self._min = datetime_bound(options['min'], 'min') if 'min' in options else None
        self._max = datetime_bound(options['max'], 'max') if 'max' in options else None
        check_bounds_order('iso_datetime', self._min, self._max,
                           lambda bound, name: bound_ms(bound, name, 0))

    def __call__(self, value, unuse, output):
        if Helper.is_empty(value):
            return
        if not Helper.is_primitive(value):
            return 'FORMAT_ERROR'
        if not isinstance(value, constants.STRING_TYPES):
            return 'WRONG_DATETIME'

        ms = parse_datetime(value)
        # The output can be written only for the years 0000-9999
        if ms is None or ms < days_from_civil(0, 1, 1) * DAY_MS or ms >= days_from_civil(10000, 1, 1) * DAY_MS:
            return 'WRONG_DATETIME'
        if self._min and ms < bound_ms(self._min, 'min'):
            return 'DATETIME_TOO_EARLY'
        if self._max and ms > bound_ms(self._max, 'max'):
            return 'DATETIME_TOO_LATE'
        output.append(format_datetime(ms))


class IsoTime(object):
    def __init__(self, *args):
        options = Helper.options_argument('iso_time', args, ('min', 'max'))
        self._min = self._bound(options, 'min')
        self._max = self._bound(options, 'max')

    def _bound(self, options, name):
        if name not in options:
            return None
        bound = options[name]
        nanoseconds = parse_time(bound) if isinstance(bound, constants.STRING_TYPES) else None
        if nanoseconds is None:
            Helper.schema_error('iso_time', 'wrong bound {!r}'.format(bound))
        return nanoseconds

    def __call__(self, value, unuse, output):
        if Helper.is_empty(value):
            return
        if not Helper.is_primitive(value):
            return 'FORMAT_ERROR'
        if not isinstance(value, constants.STRING_TYPES):
            return 'WRONG_TIME'

        time_of_day = parse_time(value)
        if time_of_day is None:
            return 'WRONG_TIME'

        error_code = self._check_bounds(time_of_day)
        if error_code:
            return error_code
        output.append(value)

    def _check_bounds(self, t):
        low, high = self._min, self._max
        if low is not None and high is not None and low > high:
            # A range over midnight: a time in the gap gets the error of the nearer bound
            if t >= low or t <= high:
                return
            return 'TIME_TOO_LATE' if t - high < low - t else 'TIME_TOO_EARLY'
        if low is not None and t < low:
            return 'TIME_TOO_EARLY'
        if high is not None and t > high:
            return 'TIME_TOO_LATE'
