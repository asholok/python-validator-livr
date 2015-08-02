import re

class OneOf(object):
    def __init__(self, *args):
        self._allowed_list = args[1]
        
        if not isinstance(self._allowed_list, list):
            self._allowed_list = args[1:]
    
    def __call__(self, value, unuse, unuse_):
        if not value:
            return
        if not value in self._allowed_list:
            return 'NOT_ALLOWED_VALUE'

class MaxLength(object):
    def __init__(self, *args):
        self._max_length = int(args[1])
        # if self._max_length < 1:
        #     raise Exception('Wrong standard value! Only positive value')

    def __call__(self, value, unuse, unuse_):
        if not value:
            return
        if len(value) > self._max_length:
            return 'TOO_LONG'

class MinLength(object):
    def __init__(self, *args):
        self._min_length = args[1]

    def __call__(self, value, unuse, unuse_):
        if not value:
            return
        if len(value) < self._min_length:
            return 'TOO_SHORT'

class EqualLength(object):
    def __init__(self, *args):
        self._length = args[1]

    def __call__(self, value, unuse, unuse_):
        if not value:
            return
        if len(value) > self._length:
            return 'TOO_LONG'
        if len(value) < self._length:
            return 'TOO_SHORT'

class BetweenLength(object):
    def __init__(self, *args):
        self._min_length = args[1]
        self._max_length = args[2]
        # if self._max_length < 1:
        #     raise Exception('Wrong standard value! Only positive value')

    def __call__(self, value, unuse, unuse_):
        if not value:
            return
        if len(value) > self._max_length:
            return 'TOO_LONG'
        if len(value) < self._min_length:
            return 'TOO_SHORT'

class Like(object):
    def __init__(self, *args):
        self._sample = args[1]

    def __call__(self, value, unuse, unuse_):
        if not value:
            return
        if not re.match(self._sample, str(value)):
            return 'WRONG_FORMAT'

