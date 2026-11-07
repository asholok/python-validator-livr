import re
try:
    import constants
    import Helper
except ImportError:
    from . import constants
    from . import Helper

ESCAPE_RE = lambda string: re.escape(string)

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

        output.append(constants.TO_STRING(value).strip())


class ToLc(object):
    def __init__(self, *args):
        pass
        
    def __call__(self, value, unuse, output):
        if value == None or value == '' or isinstance(value, constants.OBJECTS_LIST):
            return
        output.append(constants.TO_STRING(value).lower())


class ToUc(object):
    def __init__(self, *args):
        pass
        
    def __call__(self, value, unuse, output):
        if value == None or value == '' or isinstance(value, constants.OBJECTS_LIST):
            return

        output.append(constants.TO_STRING(value).upper())


class Remove(object):
    def __init__(self, *args):
        self._chars = ESCAPE_RE(args[1])

    def __call__(self, value, unuse, output):
        if value == None or value == '' or not isinstance(value, constants.STRING_TYPES):
            return

        output.append(re.sub('[' + self._chars + ']', '', value))


class LeaveOnly(object):
    def __init__(self, *args):
        self._chars = ESCAPE_RE(args[1])

    def __call__(self, value, unuse, output):
        if value == None or value == '' or not isinstance(value, constants.STRING_TYPES):
            return

        output.append(re.sub('[^' + self._chars + ']', '', value))


class Split(object):
    def __init__(self, *args):
        if len(args) < 2:
            Helper.schema_error('split', 'a separator is required')
        self._separator = Helper.string_argument('split', args[1])
        if self._separator == '':
            Helper.schema_error('split', 'the separator must not be empty')

    def __call__(self, value, unuse, output):
        # Lists, objects and empty values stay as they are
        if Helper.is_empty(value) or not Helper.is_primitive(value):
            return
        output.append(Helper.string_form(value).split(self._separator))
