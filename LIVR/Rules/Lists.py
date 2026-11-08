try:
    import constants
    import Helper
except ImportError:
    from . import constants
    from . import Helper


class ListLength(object):
    # {"list_length": 2}, {"list_length": [1, 10]} or {"list_length": {"min": 1, "max": 10}}
    def __init__(self, *args):
        if len(args) < 2:
            Helper.schema_error('list_length', 'a length is required')

        if isinstance(args[1], dict):
            options = Helper.options_argument('list_length', args, ('min', 'max'))
            if not options:
                Helper.schema_error('list_length', 'min or max is required')
            self._min = self._length(options['min']) if 'min' in options else None
            self._max = self._length(options['max']) if 'max' in options else None
        elif len(args) > 2:
            self._min, self._max = self._length(args[1]), self._length(args[2])
        else:
            self._min = self._max = self._length(args[1])

        if self._min is not None and self._max is not None and self._min > self._max:
            Helper.schema_error('list_length', 'min is greater than max')

    def _length(self, value):
        return Helper.non_negative_integer_argument('list_length', value)

    def __call__(self, value, unuse, unuse_):
        if constants.EMPTY_PRIMITIVE(value):
            return
        if not isinstance(value, list):
            return 'FORMAT_ERROR'
        if self._min is not None and len(value) < self._min:
            return 'TOO_FEW_ITEMS'
        if self._max is not None and len(value) > self._max:
            return 'TOO_MANY_ITEMS'


class Unique(object):
    # "unique" for primitive items, {"unique": ["country", "zip"]} for objects
    def __init__(self, *args):
        self._keys = [Helper.string_argument('unique', key) for key in Helper.arguments(args)]

    def __call__(self, items, unuse, unuse_):
        if constants.EMPTY_PRIMITIVE(items):
            return
        if not isinstance(items, list):
            return 'FORMAT_ERROR'

        seen = set()
        has_duplicates = False
        # A wrong-type item gives FORMAT_ERROR even after duplicates, so all items are checked
        for item in items:
            if Helper.is_empty(item):
                continue
            if self._keys:
                if not isinstance(item, dict):
                    return 'FORMAT_ERROR'
                values = [item.get(key) for key in self._keys]
            else:
                values = [item]

            if [value for value in values if not Helper.is_empty(value) and not Helper.is_primitive(value)]:
                return 'FORMAT_ERROR'
            if [value for value in values if Helper.is_empty(value)]:
                continue

            item_key = tuple(Helper.string_form(value) for value in values)
            if item_key in seen:
                has_duplicates = True
            seen.add(item_key)

        if has_duplicates:
            return 'NOT_UNIQUE_ITEMS'
