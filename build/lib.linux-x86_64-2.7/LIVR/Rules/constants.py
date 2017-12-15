import sys

OBJECTS_LIST = (list, dict)
NUMBER_LIST = (int, float)
PRIMITIVE_LIST = NUMBER_LIST + (str, bool)
EMPTY_PRIMITIVE = lambda x: x == None or x == '' 

if sys.version_info[0] < 3:
	PRIMITIVE_LIST += (unicode,) 
