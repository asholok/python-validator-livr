import copy
DEFAULT_RULES = {};
IS_DEFAULT_AUTO_TRIM = False;

class Validator(object):
    def __init__(self, livr_rules, is_auto_trim = None):
        self.__is_prepare = False
        self.__livr_rules = livr_rules
        self.__validators = {}
        self.__validator_bilders = {}
        self.__errors = None

        if is_auto_trim == None:
            self.__is_auto_trim = IS_DEFAULT_AUTO_TRIM
        else:
            self.__is_auto_trim = is_auto_trim
        self.register_rules(DEFAULT_RULES)
    
    @staticmethod
    def register_defaulr_rules(rules):
        DEFAULT_RULES = copy.deepcopy(rules)

    @staticmethod
    def set_default_auto_trim(is_auto_trim):
        IS_DEFAULT_AUTO_TRIM = bool(is_auto_trim)

    def prepare(self):
        if self.__is_prepare:
            return

        for name, rules in self.__livr_rules.iteritems():
            self.__validators[name] = [self.__build_validator(*(self.__parse_rule(rule))) for rule in rules]
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

        for field_name, validators in self.__validators:
            if not len(validators):
                continue

            mid_result = []
            value = data[field_name]

            for func in validators:
                arg = result[field_name] if field_name in result else value
                error_code = func(arg, data, mid_result)

                if error_code:
                    errors[field_name] = error_code
                    break
                else:
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
        return self.__validator_bilders

    def register_rules(self, rules):
        for rule_name, rule_value in rules.iteritems():
            self.__validator_bilders[rule_name] = rule_value

    def __parse_rule(self,  livr_rule):
        if isinstance(livr_rule, dict):
            name = livr_rule.keys()[0]
            content = livr_rule[name]

            if not isinstance(content, list):
                content = list(content)
        else:
            name = livr_rule
            content = []

        return {"name": name, "args": content}

    def __build_validator(self, name, args):
        if not name in self.__validator_bilders:
            raise Exception("Rule [{}] not registered".format(name))
        all_args = []

        all_args.extend(args)
        all_args.append(self.__validator_bilders)

        return self.__validator_bilders[name](*all_args)

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

