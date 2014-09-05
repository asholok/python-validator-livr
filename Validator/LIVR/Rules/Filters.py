import re
ESCAPE_RE = lambda string: string.replace('[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]', "\\$&")

class Trim(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, output):
        if value == None or value == '' or not isinstance(value, str):
            return

        output.append(value.strip())

class ToLc(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, output):
        if value == None or value == '' or not isinstance(value, str):
            return

        output.append(value.lower())

class ToUc(object):
    def __init__(self, *args):
        pass
    
    def __call__(self, value, unuse, output):
        if value == None or value == '' or not isinstance(value, str):
            return

        output.append(value.upper())

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
