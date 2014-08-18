
class Required(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, unuse_):
        if not value or value == 0:
            return 'REQUIRED'

class NotEmpty(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, unuse_):
        if not value or value == 0:
            return 'CANNOT_BE_EMPTY'

class NotEmptyList(object):
    def __init__(self, *args):
        pass
        
    def __call__(self, lst, unuse, unuse_):
        if not lst or lst == 0:
            return 'CANNOT_BE_EMPTY'
        if not isinstance(list, lst) or not isinstance(dict, lst):
            return 'WRONG_TYPE'

