#!/usr/bin/python
# -*- coding: utf-8 -*-
# Checksum rules of LIVR 2.5. The string form is checked as it is: use modifiers before
import re

try:
    import Helper
except ImportError:
    from . import Helper


def is_luhn_valid(digits):
    total = 0
    for index, digit in enumerate(reversed(digits)):
        digit = int(digit)
        if index % 2:
            digit = digit * 2 - 9 if digit > 4 else digit * 2
        total += digit
    return total % 10 == 0


class Luhn(object):
    def __init__(self, *args):
        Helper.no_arguments('luhn', args)

    @Helper.format_rule('WRONG_CHECKSUM')
    def __call__(self, value):
        return bool(re.match(r'[0-9]{2,}\Z', value)) and is_luhn_valid(value)


class CreditCard(object):
    def __init__(self, *args):
        Helper.no_arguments('credit_card', args)

    @Helper.format_rule('WRONG_CREDIT_CARD_NUMBER')
    def __call__(self, value):
        return bool(re.match(r'[0-9]{12,19}\Z', value)) and is_luhn_valid(value)


class Iban(object):
    def __init__(self, *args):
        Helper.no_arguments('iban', args)

    @Helper.format_rule('WRONG_IBAN')
    def __call__(self, value):
        if not re.match(r'[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}\Z', value):
            return False
        # Letters are two digits: A = 10 ... Z = 35
        number = ''.join(str(int(char, 36)) for char in value[4:] + value[:4])
        return int(number) % 97 == 1
