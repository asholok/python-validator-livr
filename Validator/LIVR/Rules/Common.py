
class Required(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, unuse_):
        if value == None or value == '':
            return 'REQUIRED'

class NotEmpty(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, unuse_):
        if value == '':
            return 'CANNOT_BE_EMPTY'

class NotEmptyList(object):
    def __init__(self, *args):
        pass
        
    def __call__(self, lst, unuse, unuse_):
        if lst == None or lst == '':
            return 'CANNOT_BE_EMPTY'
        if not isinstance(lst, list):
            return 'WRONG_FORMAT'
        if not lst:
            return 'CANNOT_BE_EMPTY'
