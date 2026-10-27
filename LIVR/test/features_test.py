#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import unittest
PATH_TO_VALIDATOR = '/'.join(str(os.path.abspath(__file__)).split('/')[:-2])
sys.path.insert(0,PATH_TO_VALIDATOR)
import Validator


class TestAutoTrim(unittest.TestCase):
    def setUp(self):
        self.validator = Validator.Validator({
            'code': 'required',
            'password': ['required', {'min_length': 3}],
            'list': {'list_of': ['string']},
            'address': {'nested_object': {
                'street': {'min_length': 5}
            }}
        }, True)

    def test_negative(self):
        output = self.validator.validate({
            'code': '  ',
            'password': ' 12  ',
            'address': {'street': '  hell '}
        })

        self.assertFalse(output)
        self.assertEqual(self.validator.get_errors(), {
            'code': 'REQUIRED',
            'password': 'TOO_SHORT',
            'address': {'street': 'TOO_SHORT'}
        })

    def test_positive(self):
        output = self.validator.validate({
            'code': ' A ',
            'password': ' 123  ',
            'list': [' aaa ', ' bbb '],
            'address': {'street': '  hello '}
        })

        self.assertEqual(output, {
            'code': 'A',
            'password': '123',
            'list': ['aaa', 'bbb'],
            'address': {'street': 'hello'}
        })

    def test_default_auto_trim(self):
        Validator.Validator.set_default_auto_trim(True)
        try:
            output = Validator.Validator({'code': 'required'}).validate({'code': ' A '})
        finally:
            Validator.Validator.set_default_auto_trim(False)

        self.assertEqual(output, {'code': 'A'})
        self.assertEqual(Validator.Validator({'code': 'required'}).validate({'code': ' A '}), {'code': ' A '})


class PatchedRule(object):
    def __init__(self, rule_name, rule_builder):
        self._rule_name = rule_name
        self._rule_builder = rule_builder

    def __call__(self, *args):
        rule_validator = self._rule_builder(*args)
        rule = {self._rule_name: list(args[1:])}

        def validate(*params):
            error_code = rule_validator(*params)
            if error_code:
                return {'code': error_code, 'rule': rule}
        return validate


class TestRulesReplacement(unittest.TestCase):
    def test_replace_default_rules(self):
        original_rules = dict(Validator.Validator.get_default_rules())
        new_rules = {}

        for name, rule_builder in original_rules.items():
            new_rules[name] = PatchedRule(name, rule_builder)

        Validator.Validator.register_default_rules(new_rules)
        try:
            validator = Validator.Validator({
                'name': ['required'],
                'phone': {'max_length': 10}
            })
            output = validator.validate({'phone': '123456789123456'})
        finally:
            Validator.Validator.register_default_rules(original_rules)

        self.assertFalse(output)
        self.assertEqual(validator.get_errors(), {
            'name': {'code': 'REQUIRED', 'rule': {'required': []}},
            'phone': {'code': 'TOO_LONG', 'rule': {'max_length': [10]}}
        })


class TestNotObjectInput(unittest.TestCase):
    def test_not_object(self):
        validator = Validator.Validator({'code': 'required'})

        for data in ['code', ['code'], None]:
            self.assertEqual(validator.validate(data), False)
            self.assertEqual(validator.get_errors(), 'FORMAT_ERROR')


class TestLike(unittest.TestCase):
    def test_not_anchored(self):
        validator = Validator.Validator({'code': {'like': '[0-9]+'}})

        self.assertEqual(validator.validate({'code': 'abc123'}), {'code': 'abc123'})

    def test_end_of_value(self):
        validator = Validator.Validator({
            'zip1': {'like': '^[0-9]{5}$'},
            'zip2': {'like': ['^[0-9]{5}$', 'i']},
            'zip3': {'like': '^[0-9]{5}$'}
        })
        output = validator.validate({'zip1': '12345\n', 'zip2': '12345\n', 'zip3': '12345'})

        self.assertFalse(output)
        self.assertEqual(validator.get_errors(), {'zip1': 'WRONG_FORMAT', 'zip2': 'WRONG_FORMAT'})

    def test_literal_dollar(self):
        validator = Validator.Validator({
            'price': {'like': '^\\$[0-9]+$'},
            'chars': {'like': '^[$^]+$'},
            'bracket': {'like': '^[]$]+$'}
        })
        output = validator.validate({'price': '$10', 'chars': '$^$', 'bracket': ']$'})

        self.assertEqual(output, {'price': '$10', 'chars': '$^$', 'bracket': ']$'})


# Python 2 has unicode strings, long integers and shorter str() of floats
class TestPython2(unittest.TestCase):
    def test_unicode_characters(self):
        validator = Validator.Validator({
            'removed': {'remove': u'ä-'},
            'left': {'leave_only': u'äb'},
            'word': {'like': [u'^\\w+$', 'i']}
        })
        output = validator.validate({'removed': u'bä-c', 'left': u'bä-c', 'word': u'Привет'})

        self.assertEqual(output, {'removed': u'bc', 'left': u'bä', 'word': u'Привет'})

    def test_long_integer(self):
        validator = Validator.Validator({'number': 'integer', 'text': 'string'})
        output = validator.validate({'number': 12345678901234567890, 'text': 12345678901234567890})

        self.assertEqual(output, {'number': 12345678901234567890, 'text': '12345678901234567890'})

    def test_float(self):
        validator = Validator.Validator({'text': 'string', 'value': {'eq': '0.3'}})
        output = validator.validate({'text': 0.1 + 0.2, 'value': 0.1 + 0.2})

        self.assertFalse(output)
        self.assertEqual(validator.get_errors(), {'value': 'NOT_ALLOWED_VALUE'})
        self.assertEqual(validator.validate({'text': 0.1 + 0.2}), {'text': '0.30000000000000004'})


if __name__ == '__main__':
    unittest.main()
