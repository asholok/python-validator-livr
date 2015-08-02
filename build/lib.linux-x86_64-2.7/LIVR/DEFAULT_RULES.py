import os
import sys
PATH_TO_RULES = '/'.join(str(os.path.abspath(__file__)).split('/')[:-1])+'/Rules'
sys.path.insert(0,PATH_TO_RULES)

import Common
import Filters
import Special
import String
import Numeric
import Helper


DEFAULT_RULES = {
    'required':         Common.Required,
    'not_empty':        Common.NotEmpty,
    'not_empty_list':   Common.NotEmptyList,

    'one_of':           String.OneOf,
    'max_length':       String.MaxLength,
    'min_length':       String.MinLength,
    'length_equal':     String.EqualLength,
    'length_between':   String.BetweenLength,
    'like':             String.Like,

    'integer':          Numeric.Integer,
    'positive_integer': Numeric.PositiveInteger,
    'decimal':          Numeric.Decimal,
    'positive_decimal': Numeric.PositiveDecimal,
    'max_number':       Numeric.MaxNumber,
    'min_number':       Numeric.MinNumber,
    'number_between':   Numeric.BetweenNumbers,

    'email':            Special.Email,
    'equal_to_field':   Special.EqualToField,
    'url':              Special.Url,
    'iso_date':         Special.IsoDate,

    'nested_object':    Helper.NestedObject,
    'list_of':          Helper.ListOf,
    'list_of_objects':  Helper.ListOfObjects,
    'list_of_different_objects': Helper.ListOfDiferentObjects,

    'trim':             Filters.Trim,
    'to_lc':            Filters.ToLc,
    'to_uc':            Filters.ToUc,
    'remove':           Filters.Remove,
    'leave_only':       Filters.LeaveOnly,

}

