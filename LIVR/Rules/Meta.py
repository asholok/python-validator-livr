import sys
import os
ROOT_PATH = '/'.join(str(os.path.abspath(__file__)).split('/')[:-2])
sys.path.insert(0,ROOT_PATH)
try:
    import constants
    import internal_reactor
except ImportError:
    from . import constants
    from . import internal_reactor

def get_selected_validator(validators, obj, selector_field):
    # The selector value must be a primitive value listed in livrs
    if not isinstance(obj, dict):
        return
    selector = obj.get(selector_field)
    if constants.EMPTY_PRIMITIVE(selector) or not isinstance(selector, constants.PRIMITIVE_LIST):
        return
    return validators.get(constants.TO_STRING(selector))

class NestedObject(object):
    def __init__(self, *args):
        _livr = args[1]
        _rule_builders = args[0]
        self._validator = internal_reactor.InternalValidator(_livr)

        self._validator.register_rules(_rule_builders)
        self._validator.prepare()

    def __call__(self, nested_obj, unuse, output):
        if constants.EMPTY_PRIMITIVE(nested_obj):
            return
        if not isinstance(nested_obj, dict):
            return 'FORMAT_ERROR'

        result = self._validator.validate(nested_obj)

        if result is False:
            return self._validator.get_errors()

        output.append(result) 

class ListOf(object):
    def __init__(self, *args):
        # {"list_of": [["required", "integer"]]} or {"list_of": ["required", "integer"]}
        _livr = args[1] if isinstance(args[1], list) else list(args[1:])
        _rule_builders = args[0]
        self._validator = internal_reactor.InternalValidator({'field':_livr})

        self._validator.register_rules(_rule_builders)
        self._validator.prepare()

    def __call__(self, values, unuse, output):   
        if constants.EMPTY_PRIMITIVE(values):
            return
        if not isinstance(values, list):
            return 'FORMAT_ERROR'
        return self._check_validation(values, output)

    def _check_validation(self, values, output):
        results = []
        errors = []
        error_flag = False

        for val in values:
            result = self._validator.validate({'field': val})
            
            if result:
                results.append(result['field'])
                errors.append(None)
            else:
                error_flag = True
                errors.append(self._validator.get_errors()['field'])

        if error_flag:
            return errors

        output.append(results)

class ListOfObjects(object):
    def __init__(self, *args):
        _livr = args[1]
        _rule_builders = args[0]
        self._validator = internal_reactor.InternalValidator(_livr)

        self._validator.register_rules(_rule_builders)
        self._validator.prepare()

    def __call__(self, objects, unuse, output):
        if objects == None or objects == '':
            return
        if not isinstance(objects, list):
            return 'FORMAT_ERROR'   

        return self._check_validation(objects, output)

    def _check_validation(self, objects, output):
        results = []
        errors = []
        error_flag = False

        for obj in objects:
            if not isinstance(obj, dict):
                error_flag = True
                errors.append('FORMAT_ERROR')
                continue

            result = self._validator.validate(obj)
            
            if result is not False:
                results.append(result)
                errors.append(None)
            else:
                error_flag = True
                errors.append(self._validator.get_errors())

        if error_flag:
            return errors

        output.append(results)

class ListOfDiferentObjects(object):
    def __init__(self, *args):
        _rule_builders = args[0]
        _livrs = args[2]
        self._selector_fields = args[1]
        self._validators = {}

        for selector, livr in _livrs.items():
            validator = internal_reactor.InternalValidator(livr)
            
            validator.register_rules(_rule_builders)
            validator.prepare()
            self._validators[selector] = validator

    def __call__(self, objects, unuse, output):
        results = []
        errors = []
        error_flag = False

        if constants.EMPTY_PRIMITIVE(objects):
            return
        if not isinstance(objects, list):
            return 'FORMAT_ERROR'

        for obj in objects:
            validator = get_selected_validator(self._validators, obj, self._selector_fields)
            if validator is None:
                error_flag = True
                errors.append("FORMAT_ERROR")
                continue

            result = validator.validate(obj)

            if result is not False:
                results.append(result)
                errors.append(None)
            else:
                error_flag = True
                errors.append(validator.get_errors())
        
        if error_flag:
            return errors

        output.append(results)


class Or(object):
    def __init__(self, *args):
        rule_builders = args[0]
        self._validators =  [] 
        self.rules = args[1:]
        for rule in args[1:]:
            validator = internal_reactor.InternalValidator({'field': rule})
            
            validator.register_rules(rule_builders)
            validator.prepare()
            self._validators.append(validator)

    def __call__(self, value, unuse, output):
        last_error = None

        # A missing value stays missing: the rules get no field
        data = {} if value is None else {'field': value}

        for validator in self._validators:
            result = validator.validate(data)

            if result is not False:
                if 'field' in result:
                    output.append(result['field'])
                return
            else:
                last_error = validator.get_errors()['field']

        if last_error:
            return last_error


class VariableObject(object):
    def __init__(self, *args):
        _rule_builders = args[0]
        _livrs = args[2]
        self._selector_fields = args[1]
        self._validators = {}

        for selector, livr in _livrs.items():
            validator = internal_reactor.InternalValidator(livr)
            
            validator.register_rules(_rule_builders)
            validator.prepare()
            self._validators[selector] = validator

    def __call__(self, obj, unuse, output):
        if constants.EMPTY_PRIMITIVE(obj):
            return
        validator = get_selected_validator(self._validators, obj, self._selector_fields)
        if validator is None:
            return "FORMAT_ERROR"

        result = validator.validate(obj)
        if result is not False:
            output.append(result)
            return
        return validator.get_errors()

