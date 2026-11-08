import sys
import os
ROOT_PATH = '/'.join(str(os.path.abspath(__file__)).split('/')[:-2])
sys.path.insert(0,ROOT_PATH)
try:
    import constants
    import internal_reactor
    import Helper
except ImportError:
    from . import constants
    from . import internal_reactor
    from . import Helper

def get_selected_validator(validators, obj, selector_field):
    # The selector value must be a primitive value listed in livrs
    if not isinstance(obj, dict):
        return
    selector = obj.get(selector_field)
    if constants.EMPTY_PRIMITIVE(selector) or not isinstance(selector, constants.PRIMITIVE_LIST):
        return
    for form in constants.COMPARISON_FORMS(selector):
        if form in validators:
            return validators[form]

def build_field_validator(rule_builders, rules, rule_name=None):
    # A validator of one field, "field", with rules in any form that a field accepts. The new
    # rules that take rules reject an empty rule list, also inside a rule list: use "any" for no rules
    if rule_name and isinstance(rules, list):
        if not rules:
            Helper.schema_error(rule_name, 'an empty rule list, use "any" for no rules')
        for rule in rules:
            if isinstance(rule, list):
                Helper.schema_error(rule_name, 'a rule list inside a rule list')
    validator = internal_reactor.InternalValidator({'field': rules})

    validator.register_rules(rule_builders)
    validator.prepare()
    return validator

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
            # Items have no containing object: a reference in their rules is a missing value
            result = []
            error_code = self._validator.validate_field('field', val, {}, result)

            if error_code:
                error_flag = True
                errors.append(error_code)
            else:
                results.append(result[0] if result else val)
                errors.append(None)

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

    def __call__(self, value, all_values, output):
        last_error = None

        # The rule sets are transparent: their rules see the siblings of the field
        for validator in self._validators:
            error_code = validator.validate_field('field', value, all_values, output)

            if not error_code:
                return
            last_error = error_code

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


class When(object):
    # {"when": [REFERENCE, CONDITION, RULES_IF_TRUE, RULES_IF_FALSE]} or {"when": [REFERENCE, CASES]}
    def __init__(self, *args):
        rule_builders = args[0]
        args = args[1:5]
        if len(args) < 2:
            Helper.schema_error('when', 'a reference and rules are required')
        self._reference = Helper.parse_reference('when', args[0])

        if len(args) == 2:
            cases = args[1]
            if not isinstance(cases, dict) or not cases:
                Helper.schema_error('when', 'cases must be an object with at least one key')
            self._cases = {}
            for key, rules in cases.items():
                self._cases[key] = build_field_validator(rule_builders, rules, 'when')
            return

        self._cases = None
        self._condition, self._if_true = [build_field_validator(rule_builders, rules, 'when') for rules in args[1:3]]
        self._if_false = build_field_validator(rule_builders, args[3], 'when') if len(args) > 3 else None

    def __call__(self, value, all_values, output):
        other = Helper.get_reference(all_values, self._reference)

        if self._cases is not None:
            validator = None
            if not Helper.is_empty(other) and Helper.is_primitive(other):
                validator = self._cases.get(Helper.string_form(other))
            if validator is None:
                return None if Helper.is_empty(value) else 'NOT_ALLOWED_VALUE'
        else:
            # The condition is true for a filled referenced value that passes its rules
            is_true = not Helper.is_empty(other) and not self._condition.validate_field('field', other, all_values, [])
            validator = self._if_true if is_true else self._if_false
            if validator is None:
                return

        return validator.validate_field('field', value, all_values, output)


class Values(object):
    def __init__(self, *args):
        self._validator = build_field_validator(args[0], Helper.rules_argument('values', args), 'values')

    def __call__(self, obj, unuse, output):
        if constants.EMPTY_PRIMITIVE(obj):
            return
        if not isinstance(obj, dict):
            return 'FORMAT_ERROR'

        results = {}
        errors = {}
        for key, value in obj.items():
            # Values have no containing object: a reference in their rules is a missing value
            result = []
            error_code = self._validator.validate_field('field', value, {}, result)
            if error_code:
                errors[key] = error_code
            else:
                results[key] = result[0] if result else value

        if errors:
            return errors
        output.append(results)


class Keys(object):
    def __init__(self, *args):
        self._validator = build_field_validator(args[0], Helper.rules_argument('keys', args), 'keys')

    def __call__(self, obj, unuse, output):
        if constants.EMPTY_PRIMITIVE(obj):
            return
        if not isinstance(obj, dict):
            return 'FORMAT_ERROR'

        # The rules only check the keys, their output is ignored
        errors = {}
        for key in obj:
            if self._validator.validate_field('field', key, {}, []):
                errors[key] = 'WRONG_KEY'

        if errors:
            return errors
