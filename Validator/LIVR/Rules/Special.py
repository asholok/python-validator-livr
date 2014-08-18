import re

class Email(object):
    _reg_exp_mail = '^(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])+$'
    def __init__(self, *args):
        pass
    
    def __call__(self, email, unuse, unuse_):
        if not email or email == 0:
            return
        if not re.match(_reg_exp_mail, email):
            return 'WRONG_EMAIL'

class EqualToField(object):
    def __init__(self, *args):
        self._field = args[1]

    def __call__(self, value, params, unuse):
        if not value or value == 0:
            return
        if value != params[self._field]:
            return 'FIELDS_NOT_EQUAL'
