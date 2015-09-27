import re
import datetime

class Email(object):
    _reg_exp_mail = '^(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])+$'
    def __init__(self, *args):
        pass
    
    def __call__(self, email=None, unuse=None, unuse_=None):
        if email == '' or email == None:
            return
        if not isinstance(email, str):
            return 'FORMAT_ERROR'            
        if not re.match(self._reg_exp_mail, email):
            return 'WRONG_EMAIL'

class EqualToField(object):
    def __init__(self, *args):
        self._field = args[1]

    def __call__(self, value, params, unuse):
        if not value or value == 0:
            return
        if value != params[self._field]:
            return 'FIELDS_NOT_EQUAL'

class Url(object):
    _url_re = re.compile(
        r'^(?:http|https)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.I)
    
    def __init__(self, *args):
        pass

    def __call__(self, value, params, unuse):
        if not value or value == 0:
            return
        if len(value) < 2083 and self._url_re.match(value):
            return

        return 'WRONG_URL'

class IsoDate(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, params, unuse):
        if not value or value == 0:
            return

        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return 'WRONG_DATE'
