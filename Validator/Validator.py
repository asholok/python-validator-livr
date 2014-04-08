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
        all_rules = copy.deepcopy(self.__livr_rules)

        for field in livr_rule:
            validators = []
            rules_quantity = len(all_rules[field])
            
            for x in range(rules_quantity):
                parsed = self._parse_rule(rules_quantity[x])
                validators.addend(self._build_validator(parsed["name"], parsed["args"]))

            self.__validators[field] = validators

        self.__is_prepare = True 
        #return self ???
    
    def valdate(self, data):
        if not self.__is_prepare:
            self.prepare()
        if self.__is_auto_trim:
            self.__auto_trim(data)
        if not isinstance(data, dict):
            self.__error = "FORMAT_ERROR"
            return
        errors  = {}
        result = {}

        for field_name in self.__validators:
            #isOk --- wtf?
            validators = self.__validators[field_name]
            rules_quantity = len(validators)

            if rules_quantity == 0:
                continue
            
            value = data[field_name] # if data HASE NO such field_name

            for x in range(rules_quantity):
                field_result_arr = []

                errorCode = validators[x](
                    result[field_name] if field_name in result else value,
                    data,
                    field_result_arr
                    )

                if errorCode:
                    errors[field_name] = errorCode
                    break
                if field_name in data:
                    if len(field_result_arr):
                        result[field_name] = field_result_arr[0]
                    else:
                        result[field_name] = value
        if not len(errors):
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
        #return self Why?

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
            raise AttributeError("Rule [{}] not registered".format(name))
        all_args = []

        all_args.extend(args)
        all_args.append(self.__validator_bilders)

        return getattr(self.__validator_bilders, name)(*all_args)

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

