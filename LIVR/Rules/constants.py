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

# repr() of a float is str() of Python 3, str() on Python 2 rounds to 12 digits
TO_STRING = lambda x: x if isinstance(x, STRING_TYPES) else repr(x) if isinstance(x, float) else str(x)
