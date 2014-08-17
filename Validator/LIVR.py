import os
import sys
PATH_TO_RULES = '/'.join(str(os.path.abspath(__file__)).split('/')[:-1])+'/LIVR/Rules'
sys.path.insert(0,PATH_TO_RULES)

from Common import *
from Filters import *
from Helper import *
from Special import *
from String import *
from Numeric import *


DEFAULT_RULES = {
    'required':         Required,
    'not_empty':        NotEmpty,
    'not_empty_list':   NotEmptyList,

    'one_of':           OneOf,
    'max_length':       MaxLength,
    'min_length':       MinLength,
    'length_equal':     EqualLength,
    'length_between':   BetweenLength,
    'like':             Like,

    'integer':          Integer,
    'positive_integer': PositiveInteger,
    'decimal':          Decimal,
    'positive_decimal': PositiveDecimal,
    'max_number':       MaxNumber,
    'min_number':       MinNumber,
    'number_between':   BetweenNumbers,

    'email':            Email,
    'equal_to_field':   EqualToField,

    'nested_object':    NestedObject,
    'list_of':          ListOf,
    'list_of_objects':  ListOfObjects,
    'list_of_different_objects': ListOfDiferentObjects,

    'trim':             Trim,
    'to_lc':            ToLc,
    'to_uc':            ToUc
}
print PATH_TO_RULES