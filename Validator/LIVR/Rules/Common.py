
class Common(object):
	
	@staticmethod
	def required():
		return lambda value: 'REQUIRED' if not value else 0

	@staticmethod
	def not_empty():
		return lambda value: 'CANNOT_BE_EMPTY' if not value else 0

	@staticmethod
	def not_empty_list():
		return (lambda lst: 'CANNOT_BE_EMPTY' if not lst 
			else 'WRONG_TYPE' if not isinstance(list, lst) or not isinstance(dict, lst)
			else 'CANNOT_BE_EMPTY' if not lst else 0)

