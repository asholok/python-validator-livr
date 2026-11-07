#!/usr/bin/python
# -*- coding: utf-8 -*-
# Helpers of the LIVR 2.5 rules: the string form of values, arguments and references
import re
import decimal

try:
    import constants
except ImportError:
    from . import constants


def schema_error(rule_name, message):
    # A wrong argument of a rule: building the validator fails
    raise Exception('Rule [{}]: {}'.format(rule_name, message))


def is_empty(value):
    return value is None or (isinstance(value, constants.STRING_TYPES) and value == '')


def is_primitive(value):
    return isinstance(value, constants.PRIMITIVE_LIST)


def string_form(value):
    # LIVR 2.5, 2.2: true -> "true", 1.0 -> "1", 0.1 -> "0.1", 1e-05 -> "0.00001"
    if isinstance(value, constants.STRING_TYPES):
        return value
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        # repr() is the shortest decimal that reads back as the same double
        text = repr(value)
        if 'e' in text:
            text = format(decimal.Decimal(text), 'f')
        return text
    return str(value)


def format_rule_error(value, error_code):
    # The error of a format or checksum rule for a value without a string form: a boolean is not
    # a hostname or Base64 ("true" is), an object or a list is a wrong structure
    if isinstance(value, bool):
        return error_code
    return 'FORMAT_ERROR'


def format_rule(error_code):
    # Format and checksum rules: empty values pass, the check gets the string form and returns
    # whether it is right, the output is the string form
    def decorator(func):
        def dec(obj, value, unuse, output):
            if is_empty(value):
                return
            if isinstance(value, bool) or not is_primitive(value):
                return format_rule_error(value, error_code)
            value = string_form(value)
            if not func(obj, value):
                return error_code
            output.append(value)
        return dec
    return decorator


def arguments(args):
    # args are the arguments of a rule builder, the first one is the rule builders.
    # {"rule": null} is one null argument
    return args[1:]


def no_arguments(rule_name, args):
    if arguments(args):
        schema_error(rule_name, 'takes no arguments')


def string_argument(rule_name, value):
    # A number is its string form; booleans, null, objects and lists are not strings
    if isinstance(value, bool) or not is_primitive(value):
        schema_error(rule_name, 'a string is required')
    return string_form(value)


def non_negative_integer_argument(rule_name, value):
    # A string with a number is the same number
    if isinstance(value, constants.STRING_TYPES) and re.match(r'-?[0-9]+(?:\.[0-9]+)?\Z', value):
        value = float(value)
    if isinstance(value, bool) or not isinstance(value, constants.NUMBER_LIST):
        schema_error(rule_name, 'a non-negative integer is required')
    if value < 0 or value != int(value):
        schema_error(rule_name, 'a non-negative integer is required')
    return int(value)


def options_argument(rule_name, args, names):
    # The first argument is an options object, the arguments after it are ignored
    args = arguments(args)
    if not args:
        return {}
    options = args[0]
    if not isinstance(options, dict):
        schema_error(rule_name, 'the argument must be an options object')
    for name in options:
        if name not in names:
            schema_error(rule_name, 'unknown option "{}"'.format(name))
    return options


def rules_argument(rule_name, args):
    # Rules taken like list_of: {"values": ["required", "string"]} or {"values": [["required", "string"]]}
    rules = args[1] if len(args) > 1 and isinstance(args[1], list) else list(args[1:])
    if rules == []:
        schema_error(rule_name, 'rules are required')
    return rules


def parse_reference(rule_name, reference):
    # "a/b/c" with JSON Pointer escapes: "~1" is "/" and "~0" is "~"
    if not isinstance(reference, constants.STRING_TYPES) or reference == '':
        schema_error(rule_name, 'a reference must be a non-empty string')

    segments = reference.split('/')
    for segment in segments:
        if segment == '' or re.search(r'~(?![01])', segment):
            schema_error(rule_name, 'wrong reference "{}"'.format(reference))
    return [segment.replace('~1', '/').replace('~0', '~') for segment in segments]


def get_reference(all_values, segments):
    # The referenced value, None when it is missing
    value = all_values
    for segment in segments:
        if isinstance(value, dict):
            if segment not in value:
                return None
            value = value[segment]
        elif isinstance(value, list) and re.match(r'(?:0|[1-9][0-9]*)\Z', segment):
            index = int(segment)
            if index >= len(value):
                return None
            value = value[index]
        else:
            return None
    return value
