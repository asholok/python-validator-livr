
class InternalValidator(object):
    def __init__(self, livr_rules, is_auto_trim = False):
        self.__is_prepare = False
        self.__livr_rules = livr_rules
        self.__validators = {}
        self.__validator_builders = {}
        self.__errors = None
        self.__is_auto_trim = is_auto_trim

    def __make_validators(self, rules):
        if isinstance(rules, dict):
            return [self.__build_validator(**self.__parse_rule({name:rule})) for name, rule in rules.items()]
        if isinstance(rules, list):
            return [self.__build_validator(**self.__parse_rule(rule)) for rule in rules]
        
        return [self.__build_validator(**self.__parse_rule(rules))]

    def prepare(self):
        if self.__is_prepare:
            return

        for name, rules in self.__livr_rules.items():
            self.__validators[name] = self.__make_validators(rules)
        
        self.__is_prepare = True
    
    def validate(self, data):
        if not self.__is_prepare:
            self.prepare()
        if self.__is_auto_trim:
            self.__auto_trim(data)
        if not isinstance(data, dict):
            self.__error = "FORMAT_ERROR"
            return
        
        errors  = {}
        result = {}

        for field_name, validators in self.__validators.items():
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
            self.__errors = None
            return result
        else:
            self.__errors = errors
            return False

    def get_errors(self):
        return self.__errors

    def get_rules(self):
        return self.__validator_builders

    def register_rules(self, rules):
        for rule_name, rule_value in rules.items():
            self.__validator_builders[rule_name] = rule_value

    def __parse_rule(self,  livr_rule):
        if isinstance(livr_rule, dict):
            name = list(livr_rule.keys())[0]
            content = livr_rule[name]

            if not isinstance(content, list):
                content = [content]
        else:
            name = livr_rule
            content = []
        return {"name": name, "args": content}

    def __build_validator(self, name, args):
        if not name in self.__validator_builders:
            raise Exception("Rule [{}] not registered".format(name))
        return self.__validator_builders[name](self.__validator_builders, *args)

    def __auto_trim(self, data):
        if type(data) is str:
            return data.strip()
        
        elif type(data) is list:
            trimmed_list = []
            
            for val in data:
                trimmed_list.append(self.__auto_trim(val))

            return trimmed_list
       
        elif type(data) is dict:
            trimmed_dict = {}

            for key in data:
                trimmed_dict[key] = self.__auto_trim(data[key])

            return trimmed_dict

        return data


