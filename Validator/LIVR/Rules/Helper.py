import sys
sys.path.insert(0,'/home/asholok/St/Projects/Python-validator-livr/Validator')
from Validator import Validator

class NestedObject(object):
	def __init__(self, livr, rule_bilders):
			self._validator = Validator(livr)

			self._validator.register_rules(rule_bilders)
			self._validator.prepare()

	def __call__(self, nested_obj, params, output):
		if not nested_obj:
			return
		if not isinstance(nested_obj, dict):
			return 'FORMAT_ERROR'

		result = self._validator.validate(nested_obj)

		if not result:	
			return self._validator.get_errors()

		output = result 

class ListOf(object):
	def __init__(self, livr, rule_bilders):
		self._validator = Validator({'field':livr})

		self._validator.register_rules(rule_bilders)
		self._validator.prepare()

	def __call__(self, values, params, output):
		if not values:
			return
		if not isinstance(values, dict) or not isinstance(values, list):
			return 'FORMAT_ERROR'

		return self._check_validation(values, output)

	def _check_validation(self, values, output):
		results = errors = []

		for val in values:
			result = self._validator.validate({'field': val})

			if result:
				results.append(result['field'])
			else:
				errors = self._validator.get_errors()['field']

		if errors:
			return errors

		output = results

class ListOfObjects(object):
	def __init__(self, livr, rule_bilders):
		self._validator = Validator({'field':livr})

		self._validator.register_rules(rule_bilders)
		self._validator.prepare()

	def __call__(self, objects, params, output):
		if not objects:
			return
		if not isinstance(objects, dict) or not isinstance(objects, list):
			return 'FORMAT_ERROR'

		return self._check_validation(objects, output)

	def _check_validation(self, objects, output):
		results = errors = []

		for obj in objects:
			result = self._validator.validate(obj)
			
			if result:
				results.append(result['field'])
			else:
				errors = self._validator.get_errors()['field']

		if errors:
			return errors

		output = results

class ListOfDiferentObjects(object):
	def __init__(self, selector_fields, livrs, rule_bilders):
		self._validators = {}
		self._selector_fields = selector_fields

		for selector, livr in livrs:
			validator = Validator(livr)
			
			validator.register_rules(rule_bilders)
			validator.prepare()
			self._validators[selector] = validator

	def __call__(self, objects, params, output):
		results = errors = []

		for obj in objects:
			if not isinstance(objects, list) or not self._validators[obj] or not self._validators[obj[self._selector_fields]]:
				errors.append("FORMAT_ERROR")
				continue

			validator = self._validators[obj[self._selector_fields]]
			result = validator.validate(obj)

			if result:
				results.append(result['field'])
			else:
				errors = self._validator.get_errors()['field']

		if errors:
			return errors

		output = results
