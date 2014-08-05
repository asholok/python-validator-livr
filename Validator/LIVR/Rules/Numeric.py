import re

class Numeric(object):
	def __call__(self, value, unuse, unuse_):
		if not value and value != 0:
			return
		if not isinstance(value, int) or not re.match("^-?[0-9]+$", str(value)):
			return 'NOT_INTEGER'

class PositiveIneger(object):
	def __call__(self, value, unuse, unuse_):
		if not value and value != 0:
			return
		if not isinstance(value, int) or not re.match("^[1-9]+$", str(value)):
			return 'NOT_INTEGER'

class Decimal(object):
	def __call__(self, value, unuse, unuse_):
		if not value and value != 0:
			return
		if not isinstance(value, float) or not re.match("^(?:-?([0-9]+\.[0-9]+)|(?:[0-9]+))+$", str(value)):
			return 'NOT_DECIMAL'

class PositiveDecimal(object):
	def __call__(self, value, unuse, unuse_):
		if not value and value != 0:
			return
		if not isinstance(value, int) or not re.match("^(?:([0-9]+\.[0-9]+)|(?:[0-9]+))+$", str(value)):
			return 'NOT_POSITIVE_DECIMAL'

class MaxNumber(object):
	def __init__(self, max_number):
		self._max_number = max_number

	def __call__(self, number, unuse, unuse_):
		if not number and number != 0:
			return

		if number > self._max_number:
			return 'TOO_HIGH'

class MinNumber(object):
	def __init__(self, min_number):
		self._min_number = min_number

	def __call__(self, number, unuse, unuse_):
		if not number and number != 0:
			return

		if number < self._min_number:
			return 'TOO_LOW'

class BetweenNumber(object):
	def __init__(self, max_number, min_number):
		self._max_number = max_number
		self._min_number = min_number

	def __call__(self, number, unuse, unuse_):
		if not number and number != 0:
			return

		if number > self._max_number:
			return 'TOO_HIGH'
		if number < self._min_number:
			return 'TOO_LOW'
