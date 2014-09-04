import re
import datetime

class Email(object):
    _reg_exp_mail = r'^(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])+$'
    def __init__(self, *args):
        pass
    
    def __call__(self, email, unuse, unuse_):
        if not email or email == 0:
            return
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
    _url_re_str = r'^(?:(?:http|https)://)(?:\\S+(?::\\S*)?@)?(?:(?:(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}(?:\\.(?:[0-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))|(?:(?:[a-z\\u00a1-\\uffff0-9]+-?)*[a-z\\u00a1-\\uffff0-9]+)(?:\\.(?:[a-z\\u00a1-\\uffff0-9]+-?)*[a-z\\u00a1-\\uffff0-9]+)*(?:\\.(?:[a-z\\u00a1-\\uffff]{2,})))|localhost)(?::\\d{2,5})?(?:(/|\\?|#)[^\\s]*)?$'
    def __init__(self, *args):
        pass

    def __call__(self, value, params, unuse):
        if not value or value == 0:
            return

        if len(value) > 2082 and not re.match(self._url_re_str, value):
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
            print 'Wrong date'
