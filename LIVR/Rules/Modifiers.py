import re
try:
    import constants
except ImportError:
    from . import constants

ESCAPE_RE = lambda string: string.replace('[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]', "\\$&")

class Default(object):
    def __init__(self, *args):
        self._default = args[1]

    def __call__(self, value, unuse, output):
        if constants.EMPTY_PRIMITIVE(value):
            output.append(self._default)


class Trim(object):
    def __init__(self, *args):
        pass
        
    def __call__(self, value, unuse, output):
        if value == None or value == '' or isinstance(value, constants.OBJECTS_LIST):
            return

        output.append(str(value).strip())


class ToLc(object):
    def __init__(self, *args):
        pass
        
    def __call__(self, value, unuse, output):
        if value == None or value == '' or isinstance(value, constants.OBJECTS_LIST):
            return
        output.append(str(value).lower())


class ToUc(object):
    def __init__(self, *args):
        pass
        
    def __call__(self, value, unuse, output):
        if value == None or value == '' or isinstance(value, constants.OBJECTS_LIST):
            return

        output.append(str(value).upper())


class Remove(object):
    def __init__(self, *args):
        self._chars = ESCAPE_RE(args[1])

    def __call__(self, value, unuse, output):
        if value == None or value == '' or not isinstance(value, str):
            return

        output.append(re.sub('[{}]'.format(self._chars), '', value))


class LeaveOnly(object):
    def __init__(self, *args):
        self._chars = ESCAPE_RE(args[1])

    def __call__(self, value, unuse, output):
        if value == None or value == '' or not isinstance(value, str):
            return

        output.append(re.sub('[^{}]'.format(self._chars), '', value))
