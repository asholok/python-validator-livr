import os
import sys
import yaml
PATH_TO_NEGATIVE_TESTS = '/'.join(str(os.path.abspath(__file__)).split('/')[:-1])+'/test_suite/positive'
PATH_TO_VALIDATOR = '/'.join(str(os.path.abspath(__file__)).split('/')[:-2])+'/Validator'
sys.path.insert(0,PATH_TO_VALIDATOR)
from Validator import Validator

class PositiveTests(object):
    def run(self):
        for root, dirs, files in os.walk(PATH_TO_NEGATIVE_TESTS):
            self._current_test = ''.join(root.split('/')[-1])
            files_path = ['/'.join([root,file_name]) for file_name in files]
            print self._current_test
            self._check(self._prepare(files_path))

    def _prepare(self, files_path):
        data = {}

        for path in files_path:
            name_in_dict = ''.join(path.split('/')[-1]).replace('.json', '')
            with open(path) as f:
                data[name_in_dict] = yaml.load(f)
        
        return data

    def _check(self, data): 
        if not 'rules' in data or not 'input' in data or not 'output' in data:
            return
        standart_output = data['output']
        validator = Validator(data['rules'])
        result = validator.validate(data['input'])
        current_errors = validator.get_errors()
        
        if result:
            if standart_output == result:
                print 'Test \'{}\' is Passed!!'.format(self._current_test)
            else:
                print 'Test \'{}\' is NOT passed\nGives result:\n\n{}\n\nMust give:\n\n{}\n\n'.format(self._current_test,
                                                                                                result,
                                                                                                standart_output)
        else:
            print 'Test \'{}\' is NOT passed\nGives errors:\n\n{}\n\n Must give:\n\n{}\n\n'.format(self._current_test,
                                                                                                current_errors,
                                                                                                standart_output)

c = PositiveTests()

c.run()


