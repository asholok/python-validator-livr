
try:
    STRING_TYPES = (str, unicode)
except NameError:
    STRING_TYPES = (str,)


def apply_rules(validators, value, all_values, output):
    # The output of a rule is the input of the next one
    mid_result = []

    for func in validators:
        error_code = func(mid_result[-1] if mid_result else value, all_values, mid_result)
        if error_code:
            return error_code

    if mid_result:
        output.append(mid_result[-1])


class InternalValidator(object):
    def __init__(self, livr_rules, is_auto_trim = False):
        self._is_prepare = False
        self._livr_rules = livr_rules
        self._validators = {}
        self._validator_builders = {}
        self._errors = None
        self._is_auto_trim = is_auto_trim

    def _make_validators(self, rules):
        if isinstance(rules, dict):
            return [self._build_validator(**self._parse_rule({name:rule})) for name, rule in rules.items()]
        if isinstance(rules, list):
            return [self._build_validator(**self._parse_rule(rule)) for rule in rules]
        return [self._build_validator(**self._parse_rule(rules))]

    def prepare(self):
        if self._is_prepare:
            return
        for name, rules in self._livr_rules.items():
            self._validators[name] = self._make_validators(rules)
        self._is_prepare = True
    
    def validate(self, data):
        errors = {}
        result = {}

        if not self._is_prepare:
            self.prepare()
        if self._is_auto_trim:
            data = self._auto_trim(data)
        if not isinstance(data, dict):
            self._errors = "FORMAT_ERROR"
            return False

        for field_name, validators in self._validators.items():
            if not validators:
                continue
            output = []
            error_code = apply_rules(validators, data.get(field_name), data, output)

            if error_code:
                errors[field_name] = error_code
            elif output:
                result[field_name] = output[0]
            elif field_name in data:
                result[field_name] = data[field_name]

        if not errors:
            self._errors = None
            return result
        else:
            self._errors = errors
            return False

    def validate_field(self, field_name, value, all_values, output):
        """Validates value with the rules of field_name. The rules see the fields of all_values,
        the containing object (LIVR 2.5, 2.5). Returns the error; the output goes to output,
        nothing when the value stays as it is"""
        if not self._is_prepare:
            self.prepare()
        return apply_rules(self._validators[field_name], value, all_values, output)

    def get_errors(self):
        return self._errors

    def get_rules(self):
        return self._validator_builders

    def register_rules(self, rules):
        self._validator_builders.update(rules)

    def _parse_rule(self,  livr_rule):
        if isinstance(livr_rule, dict):
            name = list(livr_rule.keys())[0]
            content = livr_rule[name]

            if not isinstance(content, list):
                content = [content]
        else:
            name = livr_rule
            content = []
        return {"name": name, "args": content}

    def _build_validator(self, name, args):
        if not name in self._validator_builders:
            raise Exception("Rule [{}] not registered".format(name))
        return self._validator_builders[name](self._validator_builders, *args)

    def _auto_trim(self, data):
        if isinstance(data, STRING_TYPES):
            return data.strip()
        
        elif type(data) is list:
            trimmed_list = []
            
            for val in data:
                trimmed_list.append(self._auto_trim(val))
            return trimmed_list
       
        elif type(data) is dict:
            trimmed_dict = {}

            for key in data:
                trimmed_dict[key] = self._auto_trim(data[key])
            return trimmed_dict
        return data
