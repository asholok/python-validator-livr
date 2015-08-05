#!/usr/bin/env python
import os
import sys
PATH_TO_TESTS_INV = '/'.join(str(os.path.abspath(__file__)).split('/')[:-1])
PATH_TO_VALIDATOR = '/'.join(str(os.path.abspath(__file__)).split('/')[:-2])
sys.path.insert(0,PATH_TO_VALIDATOR)
import Validator
from livr_test import TestSuite

def negative_test(data, current_test):
    if not 'rules' in data or not 'input' in data or not 'errors' in data:
        return
    validator = Validator.Validator(data['rules'])
    validator.validate(data['input'])

    """ If need to debug uncoment next code"""
    standard_errors = data['errors']
    current_errors = validator.get_errors()
    if standard_errors == current_errors:
      print('Test \'{0}\' is Passed!!'.format(current_test))
    else:
      print('Test \'{0}\' is NOT passed \n Gives:\n\n{}\n\n Must give:\n\n{}\n\n'.format(current_test,
                                                                                        current_errors,
                                                                                        standard_errors))

    return [data['errors'], validator.get_errors()]

def positive_test(data, current_test):
    if not 'rules' in data or not 'input' in data or not 'output' in data:
            return
    validator = Validator.Validator(data['rules'])
    result = validator.validate(data['input'])

    """ If need to debug uncoment next code"""
    standart_output = data['output']
    if result:
        if standart_output == result:
            print('Test \'{0}\' is Passed!!'.format(current_test))
        else:
            print('Test \'{0}\' is NOT passed\nGives result:\n\n{1}\n\nMust give:\n\n{2}\n\n'.format(current_test,
                                                                                                        result,
                                                                                                        standart_output))
    else:
        print('Test \'{0}\' is NOT passed\nGives errors:\n\n{1}\n\n Must give:\n\n{2}\n\n'.format(current_test,
                                                                                                validator.get_errors(),
                                                                                                standart_output))
    return [data['output'], result]

def aliase_negative_test(data, current_test):

    if not 'rules' in data or not 'input' in data or not 'errors' in data or not 'aliases' in data:
        return
    validator = Validator.Validator(data['rules'])
    
    for alias in data['aliases']:
        validator.register_aliased_rule(alias) 
    validator.validate(data['input'])

    """ If need to debug uncoment next code"""
    standard_errors = data['errors']
    current_errors = validator.get_errors()
    if standard_errors == current_errors:
      print('Test \'{0}\' is Passed!!'.format(current_test))
    else:
      print('Test \'{0}\' is NOT passed \n Gives:\n\n{1}\n\n Must give:\n\n{2}\n\n'.format(current_test,
                                                                                            current_errors,
                                                                                            standard_errors))

    return [data['errors'], validator.get_errors()]

def aliase_positive_test(data, current_test): 
    if not 'rules' in data or not 'input' in data or not 'output' in data or not 'aliases' in data:
        return
    validator = Validator.Validator(data['rules'])
    
    for alias in data['aliases']:
        validator.register_aliased_rule(alias) 
    result = validator.validate(data['input'])

    """ If need to debug uncoment next code"""
    standart_output = data['output']
    if result:
        if standart_output == result:
            print('Test \'{0}\' is Passed!!'.format(current_test))
        else:
            print('Test \'{0}\' is NOT passed\nGives result:\n\n{1}\n\nMust give:\n\n{2}\n\n'.format(current_test,
                                                                                                result,
                                                                                                standart_output))
    else:
        print('Test \'{0}\' is NOT passed\nGives errors:\n\n{1}\n\n Must give:\n\n{2}\n\n'.format(current_test,
                                                                                            validator.get_errors(),
                                                                                            standart_output))

    return [data['output'], result]

if __name__ == "__main__":
    test_engine = TestSuite()

    test_engine.runTest(PATH_TO_TESTS_INV+'/test_suite/positive', positive_test)
    test_engine.runTest(PATH_TO_TESTS_INV+'/test_suite/negative', negative_test)
    test_engine.runTest(PATH_TO_TESTS_INV+'/test_suite/aliases_negative', aliase_negative_test)
    test_engine.runTest(PATH_TO_TESTS_INV+'/test_suite/aliases_positive', aliase_positive_test)
    