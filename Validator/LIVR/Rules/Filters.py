
class Filters(object):

	def trim_value(value, output):
		if isinstance(value, dict):
			output = {key: val.strip() for key, val in value.items()}
		elif isinstance(val, list):
			output = [val.strip() for val in value]
		elif isinstance(val, str):
			output = val.strip()

	def make_lc(value, output):
		if isinstance(value, dict):
			output = {key: val.lower() for key, val in value.items()}
		elif isinstance(val, list):
			output = [val.lower() for val in value]
		elif isinstance(val, str):
			output = val.lower()

	def make_uc(value, output):
		if isinstance(value, dict):
			output = {key: val.upper() for key, val in value.items()}
		elif isinstance(val, list):
			output = [val.upper() for val in value]
		elif isinstance(val, str):
			output = val.upper()

	@staticmethod
	def trim():
		return lambda val, unuse, output: 0 if val == None or val == '' else Filters.trim_value(val, output)
		
	@staticmethod
	def to_lc():
		return lambda val, unuse, output: 0 if val == None or val == '' else Filters.make_lc(val, output)

	@staticmethod
	def to_uc():
		return lambda val, unuse, output: 0 if val == None or val == '' else Filters.make_uc(val, output)
	