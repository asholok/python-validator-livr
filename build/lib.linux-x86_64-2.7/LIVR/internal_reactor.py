
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
        if not self._is_prepare:
            self.prepare()
        if self._is_auto_trim:
            self._auto_trim(data)
        if not isinstance(data, dict):
            self._error = "FORMAT_ERROR"
            return
        
        errors  = {}
        result = {}

        for field_name, validators in self._validators.items():
            if not validators:
                continue

            mid_result = []
            value = data[field_name] if field_name in data else None
            
            for func in validators:
                arg = result[field_name] if field_name in result else value
                error_code = func(arg, data, mid_result)

                if error_code:
                    errors[field_name] = error_code
                    break
                elif value != None:
                    result[field_name] = mid_result[0] if len(mid_result) else value

        if not errors:
            self._errors = None
            return result
        else:
            self._errors = errors
            return False

    def get_errors(self):
        return self._errors

    def get_rules(self):
        return self._validator_builders

    def register_rules(self, rules):
        for rule_name, rule_value in rules.items():
            self._validator_builders[rule_name] = rule_value

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
        if type(data) is str:
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


