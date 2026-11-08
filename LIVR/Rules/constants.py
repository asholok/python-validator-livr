import sys

OBJECTS_LIST = (list, dict)
NUMBER_LIST = (int, float)
PRIMITIVE_LIST = NUMBER_LIST + (str, bool)
EMPTY_PRIMITIVE = lambda x: x == None or x == '' 
STRING_TYPES = (str,)

if sys.version_info[0] < 3:
	NUMBER_LIST += (long,)
	PRIMITIVE_LIST += (unicode, long)
	STRING_TYPES += (unicode,)

# repr() of a float is str() of Python 3, str() on Python 2 rounds to 12 digits.
# Booleans are "true" and "false", as in JSON, so {"eq": true} accepts true and "true"
TO_STRING = lambda x: x if isinstance(x, STRING_TYPES) else repr(x) if isinstance(x, float) \
    else ('true' if x else 'false') if isinstance(x, bool) else str(x)

# LIVR 2.0 wrote booleans as "True" and "False". eq, one_of, equal_to_field and the selectors of
# variable_object keep matching that form too, so data that matched before still matches.
# COMPARISON_FORMS has the 2.0 form first
TO_STRING_2_0 = lambda x: str(x) if isinstance(x, bool) else TO_STRING(x)
COMPARISON_FORMS = lambda x: (str(x), TO_STRING(x)) if isinstance(x, bool) else (TO_STRING(x),)
