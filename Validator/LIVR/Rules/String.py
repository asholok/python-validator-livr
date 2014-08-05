
class OneOf(object):
	def __init__(self, allowed_list):
		if not isinstance(allowed_list, list):
			raise Exception('Wrong standart value! List Required')
		self._allowed_list = allowed_list
	
	def __call__(self, value, unuse, unuse_):
		if not value and value != 0:
			return
		if not value in self._allowed_list:
			return 'NOT_ALLOWED_VALUE'

class MaxLength(object):
	def __init__(self, max_length):
		if max_length < 1:
			raise Exception('Wrong standart value! Onley positive value')
		self._max_length = max_length

	def __call__(self, value, unuse, unuse_):
		if not value:
			return
		if len(str(value)) > self._max_length:
			return 'TOO_LONG'

class MinLength(object):
	def __init__(self, min_length):
		self._min_length = min_length

	def __call__(self, value, unuse, unuse_):
		if not value:
			return
		if len(str(value)) < self._min_length:
			return 'TOO_SHORT'

class EqualLength(object):
	def __init__(self, length):
		self._length = length

	def __call__(self, value, unuse, unuse_):
		if not value:
			return
		if len(str(value)) > self._length:
			return 'TOO_LONG'
		if len(str(value)) < self._length:
			return 'TOO_SHORT'

class BetweenLength(object):
	def __init__(self, min_length, max_length):
		if max_length < 1:
			raise Exception('Wrong standart value! Onley positive value')
		self._max_length = max_length
		self._min_length = min_length

	def __call__(self, value, unuse, unuse_):
		if not value:
			return
		if len(str(value)) > self._max_length:
			return 'TOO_LONG'
		if len(str(value)) < self._min_length:
			return 'TOO_SHORT'

class Like(object):
	def __init__(self, sample):
		self._sample = sample

	def __call__(self, value, unuse, unuse_):
		if not value and value != 0:
			return
		if not self._sample in value:
			return 'WRONG_FORMAT'
