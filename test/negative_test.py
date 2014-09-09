import os
import sys
import yaml
import unittest
PATH_TO_NEGATIVE_TESTS = '/'.join(str(os.path.abspath(__file__)).split('/')[:-1])+'/test_suite/negative'
PATH_TO_VALIDATOR = '/'.join(str(os.path.abspath(__file__)).split('/')[:-2])+'/Validator'
sys.path.insert(0,PATH_TO_VALIDATOR)
import Validator

class NegativeTests(unittest.TestCase):
	def runTest(self):
		for root, dirs, files in os.walk(PATH_TO_NEGATIVE_TESTS):
			self._curent_test = ''.join(root.split('/')[-1])
			files_path = ['/'.join([root,file_name]) for file_name in files]

			self._check(self._prepare(files_path))

	def _prepare(self, files_path):
		data = {}

		for path in files_path:
			name_in_dict = ''.join(path.split('/')[-1]).replace('.json', '')
			with open(path) as f:
				data[name_in_dict] = yaml.load(f)
		
		return data

	def _check(self, data): 
		if not 'rules' in data or not 'input' in data or not 'errors' in data:
			return
		standard_errors = data['errors']
		validator = Validator.Validator(data['rules'])
		validator.validate(data['input'])
		current_errors = validator.get_errors()
		
		""" If need to debug uncoment next code"""
		# if standard_errors == current_errors:
		# 	print 'Test \'{}\' is Passed!!'.format(self._curent_test)
		# else:
		# 	print 'Test \'{}\' is NOT passed \n Gives:\n\n{}\n\n Must give:\n\n{}\n\n'.format(self._curent_test,
		# 																						current_errors,
		# 																						standard_errors)
		self.assertEqual(standard_errors, current_errors)


c = NegativeTests()

c.runTest()


