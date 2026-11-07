try:
    import constants
    import Helper
except ImportError:
    from . import constants
    from . import Helper


class Required(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, unuse_):
        if value == None or value == '':
            return 'REQUIRED'


class NotEmpty(object):
    def __init__(self, *args):
        pass
        
    def __call__(self, value, unuse, unuse_):
        if value == '':
            return 'CANNOT_BE_EMPTY'


class NotEmptyList(object):
    def __init__(self, *args):
        pass
        
    def __call__(self, lst, unuse, unuse_):
        if lst == None or lst == '':
            return 'CANNOT_BE_EMPTY'
        if not isinstance(lst, list):
            return 'FORMAT_ERROR'
        if not lst:
            return 'CANNOT_BE_EMPTY'


class AnyObject(object):
    def __init__(self, *args):
        pass
        
    def __call__(self, lst, unuse, unuse_):
        if constants.EMPTY_PRIMITIVE(lst):
            return
        if not isinstance(lst, dict):
            return 'FORMAT_ERROR'


class Boolean(object):
    _values = {'1': True, '0': False, 'true': True, 'false': False}

    def __init__(self, *args):
        Helper.no_arguments('boolean', args)

    def __call__(self, value, unuse, output):
        if Helper.is_empty(value):
            return
        if not Helper.is_primitive(value):
            return 'FORMAT_ERROR'
        if isinstance(value, bool):
            output.append(value)
        elif isinstance(value, constants.NUMBER_LIST):
            # 1.0 is 1
            if value != 1 and value != 0:
                return 'NOT_BOOLEAN'
            output.append(value == 1)
        elif value in self._values:
            output.append(self._values[value])
        else:
            return 'NOT_BOOLEAN'


class Any(object):
    def __init__(self, *args):
        Helper.no_arguments('any', args)

    def __call__(self, value, unuse, unuse_):
        pass


class RequiredIf(object):
    def __init__(self, *args):
        conditions = args[1] if len(args) > 1 else None
        if not isinstance(conditions, dict) or not conditions:
            Helper.schema_error('required_if', 'an object with at least one entry is required')

        self._conditions = []
        for reference, allowed in conditions.items():
            allowed = allowed if isinstance(allowed, list) else [allowed]
            if not allowed:
                Helper.schema_error('required_if', 'an empty list of values never matches')
            for item in allowed:
                if not Helper.is_primitive(item) or item == '':
                    Helper.schema_error('required_if', 'values must be primitive values other than null and ""')
            self._conditions.append((
                Helper.parse_reference('required_if', reference),
                set(Helper.string_form(item) for item in allowed)
            ))

    def __call__(self, value, all_values, unuse):
        if not Helper.is_empty(value):
            return
        for reference, allowed in self._conditions:
            other = Helper.get_reference(all_values, reference)
            if Helper.is_empty(other) or not Helper.is_primitive(other):
                return
            if Helper.string_form(other) not in allowed:
                return
        return 'REQUIRED'
