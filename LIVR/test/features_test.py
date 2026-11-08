#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import unittest
PATH_TO_VALIDATOR = '/'.join(str(os.path.abspath(__file__)).split('/')[:-2])
sys.path.insert(0,PATH_TO_VALIDATOR)
import Validator
import Dates
import Helper


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


class TestDecimal(unittest.TestCase):
    def test_negative_integer(self):
        validator = Validator.Validator({'string': 'decimal', 'number': 'decimal'})

        self.assertEqual(validator.validate({'string': '-200', 'number': -200}), {'string': -200, 'number': -200})


class Upper(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, output):
        if value != value.upper():
            return 'NOT_UPPER'


class TestExtraArguments(unittest.TestCase):
    def test_meta_rules_keep_custom_rules(self):
        # Extra arguments are ignored, the rules of the validator stay with the meta rules
        validator = Validator.Validator({
            'object': {'nested_object': [{'code': 'upper'}, 'extra']},
            'list': {'list_of': [['upper'], 'extra']},
            'objects': {'list_of_objects': [{'code': 'upper'}, 'extra']},
            'variable': {'variable_object': ['type', {'a': {'code': 'upper'}}, 'extra']},
            'different': {'list_of_different_objects': ['type', {'a': {'code': 'upper'}}, 'extra']}
        })
        validator.register_rules({'upper': Upper})
        output = validator.validate({
            'object': {'code': 'x'},
            'list': ['x'],
            'objects': [{'code': 'x'}],
            'variable': {'type': 'a', 'code': 'x'},
            'different': [{'type': 'a', 'code': 'x'}]
        })

        self.assertFalse(output)
        self.assertEqual(validator.get_errors(), {
            'object': {'code': 'NOT_UPPER'},
            'list': ['NOT_UPPER'],
            'objects': [{'code': 'NOT_UPPER'}],
            'variable': {'code': 'NOT_UPPER'},
            'different': [{'code': 'NOT_UPPER'}]
        })

    def test_like_keeps_flag(self):
        validator = Validator.Validator({'code': {'like': ['^[a-z]+$', 'i', 'extra']}})

        self.assertEqual(validator.validate({'code': 'ABC'}), {'code': 'ABC'})


# LIVR 2.5
class TestArguments(unittest.TestCase):
    def assertSchemaError(self, rules):
        self.assertRaises(Exception, Validator.Validator(rules).prepare)

    def test_rule_list_inside_rule_list(self):
        self.assertSchemaError({'field': {'when': ['x', 'any', ['required', []]]}})
        self.assertSchemaError({'field': {'when': ['x', {'a': ['required', []]}]}})
        self.assertSchemaError({'field': {'values': ['required', []]}})
        self.assertSchemaError({'field': {'keys': [['string', []]]}})

    def test_number_strings(self):
        # A string in the grammar of "decimal" is the same number
        validator = Validator.Validator({'mac': {'mac': '64.0'}, 'amount': {'max_decimals': '02'}})

        self.assertEqual(validator.validate({'mac': '70-B3-D5-7E-D0-00-12-34', 'amount': '1.25'}),
                         {'mac': '70-B3-D5-7E-D0-00-12-34', 'amount': 1.25})
        self.assertSchemaError({'mac': {'mac': '0x40'}})
        self.assertSchemaError({'amount': {'max_decimals': ' 2'}})
        self.assertSchemaError({'amount': {'max_decimals': '1e1'}})


class TestStringForm(unittest.TestCase):
    def test_numbers(self):
        for number, string in [(1.0, '1'), (-0.0, '0'), (100, '100'), (1e3, '1000'), (0.1, '0.1'),
                               (-12.25, '-12.25'), (123456789012345, '123456789012345'), (1e-05, '0.00001')]:
            self.assertEqual(Helper.string_form(number), string)

    def test_booleans(self):
        validator = Validator.Validator({'a': {'eq': True}, 'b': {'one_of': [True, False]}, 'c': 'string'})

        self.assertEqual(validator.validate({'a': 'true', 'b': 'false', 'c': True}), {'a': True, 'b': False, 'c': 'true'})


class TestContainingObject(unittest.TestCase):
    def test_alias_and_or_see_siblings(self):
        validator = Validator.Validator({
            'password': 'required',
            'password2': 'same_password',
            'password3': {'or': [{'equal_to_field': 'password'}, 'integer']}
        })
        validator.register_aliased_rule({'name': 'same_password', 'rules': {'equal_to_field': 'password'}})

        self.assertEqual(validator.validate({'password': 'secret', 'password2': 'secret', 'password3': 'secret'}),
                         {'password': 'secret', 'password2': 'secret', 'password3': 'secret'})

    def test_list_items_see_no_fields(self):
        validator = Validator.Validator({'codes': {'list_of': {'equal_to_field': 'codes'}}})

        self.assertFalse(validator.validate({'codes': ['a']}))
        self.assertEqual(validator.get_errors(), {'codes': ['FIELDS_NOT_EQUAL']})

    def test_auto_trim(self):
        # References see trimmed values, keys are not trimmed
        validator = Validator.Validator({
            'type': 'string',
            'vat': {'required_if': {'type': 'company'}},
            'names': {'keys': {'one_of': ['en', 'uk']}}
        }, True)

        self.assertFalse(validator.validate({'type': ' company ', 'names': {' en': 'x'}}))
        self.assertEqual(validator.get_errors(), {'vat': 'REQUIRED', 'names': {' en': 'WRONG_KEY'}})


class TestClock(unittest.TestCase):
    def test_utc_date(self):
        validator = Validator.Validator({
            'date': {'iso_date': {'max': 'today'}},
            'datetime': {'iso_datetime': {'min': 'tomorrow'}}
        })
        utc_now = Dates.utc_now
        # 2026-10-18T23:30:00Z, the next day in UTC+1 already
        Dates.utc_now = lambda: 1792366200
        try:
            output = validator.validate({'date': '2026-10-19', 'datetime': '2026-10-19T00:00+00:00'})
            errors = validator.get_errors()
        finally:
            Dates.utc_now = utc_now

        self.assertFalse(output)
        self.assertEqual(errors, {'date': 'DATE_TOO_LATE'})


class TestBooleanCompatibility(unittest.TestCase):
    # LIVR 2.0 compared booleans in the form "True" and "False": that form keeps matching
    def assertValid(self, rules, data, output):
        validator = Validator.Validator(rules)
        self.assertEqual(validator.validate(data), output, validator.get_errors())

    def assertErrors(self, rules, data, errors):
        validator = Validator.Validator(rules)
        self.assertFalse(validator.validate(data))
        self.assertEqual(validator.get_errors(), errors)

    def test_eq(self):
        for value in [True, 'true', 'True']:
            self.assertValid({'a': {'eq': True}}, {'a': value}, {'a': True})
        for value in [False, 'false', 'False']:
            self.assertValid({'a': {'eq': False}}, {'a': value}, {'a': False})
        # A boolean value and a string rule
        self.assertValid({'a': {'eq': 'True'}, 'b': {'eq': 'false'}}, {'a': True, 'b': False}, {'a': 'True', 'b': 'false'})

        self.assertErrors({'a': {'eq': True}, 'b': {'eq': True}, 'c': {'eq': True}, 'd': {'eq': 'True'}},
                          {'a': 'TRUE', 'b': 1, 'c': False, 'd': 'true'},
                          {'a': 'NOT_ALLOWED_VALUE', 'b': 'NOT_ALLOWED_VALUE', 'c': 'NOT_ALLOWED_VALUE', 'd': 'NOT_ALLOWED_VALUE'})

    def test_one_of(self):
        for value in [True, 'true', 'True']:
            self.assertValid({'a': {'one_of': [True, False]}}, {'a': value}, {'a': True})
        for value in [False, 'false', 'False']:
            self.assertValid({'a': {'one_of': [[True, False]]}}, {'a': value}, {'a': False})
        self.assertValid({'a': {'one_of': ['x', 'True']}, 'b': {'one_of': ['false', 'y']}}, {'a': True, 'b': False}, {'a': 'True', 'b': 'false'})
        # The first allowed value that matches, as in 2.0
        self.assertValid({'a': {'one_of': ['True', True]}}, {'a': True}, {'a': 'True'})

        self.assertErrors({'a': {'one_of': [True]}, 'b': {'one_of': ['True']}, 'c': {'one_of': [1, 0]}},
                          {'a': 'FALSE', 'b': 'true', 'c': True},
                          {'a': 'NOT_ALLOWED_VALUE', 'b': 'NOT_ALLOWED_VALUE', 'c': 'NOT_ALLOWED_VALUE'})

    def test_equal_to_field(self):
        rules = {'a': 'any', 'b': {'equal_to_field': 'a'}}
        for a, b in [(True, 'True'), ('True', True), (True, 'true'), ('false', False), (True, True)]:
            self.assertValid(rules, {'a': a, 'b': b}, {'a': a, 'b': b})
        self.assertErrors(rules, {'a': True, 'b': 'TRUE'}, {'b': 'FIELDS_NOT_EQUAL'})

    def test_selector(self):
        for key in ['True', 'true']:
            rules = {'data': {'variable_object': ['flag', {key: {'flag': 'required', 'x': 'integer'}}]}}
            self.assertValid(rules, {'data': {'flag': True, 'x': '1'}}, {'data': {'flag': True, 'x': 1}})


class Arguments(object):
    def __init__(self, *args):
        self.args = args[1:]
        Arguments.last = self

    def __call__(self, value, unuse, unuse_):
        pass


class TestNullArguments(unittest.TestCase):
    def test_null_is_one_argument(self):
        # The new rules take no null argument
        for rules in [{'boolean': None}, {'uuid': None}, {'ip': None}, {'mac': None}, {'hostname': None},
                      {'unique': None}, {'iso_datetime': None}, {'list_length': None}, {'split': None},
                      {'base64': None}, {'digest': None}, {'max_decimals': None}]:
            self.assertRaises(Exception, Validator.Validator({'field': rules}).prepare)

    def test_iso_date_ignores_null(self):
        # LIVR 2.0 ignored the arguments of iso_date
        validator = Validator.Validator({'date': {'iso_date': None}})

        self.assertEqual(validator.validate({'date': '2026-11-07'}), {'date': '2026-11-07'})
        self.assertFalse(validator.validate({'date': '2026-02-30'}))
        self.assertEqual(validator.get_errors(), {'date': 'WRONG_DATE'})

    def test_null_inside_arguments(self):
        for rules in [{'not_one_of': [None]}, {'required_if': {'type': None}}, {'list_length': {'min': None}},
                      {'list_length': {'max': None}}]:
            self.assertRaises(Exception, Validator.Validator({'field': rules}).prepare)

    def test_default_null(self):
        # The rules of LIVR 2.0 get null as an argument, as before
        validator = Validator.Validator({'a': {'default': None}, 'b': {'default': None}})

        self.assertEqual(validator.validate({'b': ''}), {'a': None, 'b': None})

    def test_custom_rules_get_null(self):
        validator = Validator.Validator({'field': {'custom': None}})
        validator.register_rules({'custom': Arguments})
        validator.prepare()
        self.assertEqual(Arguments.last.args, (None,))


class TestUnique(unittest.TestCase):
    def test_key_value_is_object_next_to_empty_key(self):
        validator = Validator.Validator({'a': {'unique': ['x', 'y']}, 'b': {'unique': ['x', 'y']}})

        self.assertFalse(validator.validate({'a': [{'x': '', 'y': {'z': 1}}], 'b': [{'y': ['z']}]}))
        self.assertEqual(validator.get_errors(), {'a': 'FORMAT_ERROR', 'b': 'FORMAT_ERROR'})


if __name__ == '__main__':
    unittest.main()
