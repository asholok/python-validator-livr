try:
    import internal_reactor
except ImportError:
    from . import internal_reactor

class BuildAliasedRule(object):
    def __init__(self, source, alias):
        if not isinstance(alias, dict):
            raise Exception('Wrong alias format. Dict required')
        if not 'name' in alias:
            raise Exception('Alias name required')
        if not 'rules' in alias:
            raise Exception('Alias rules required')
        if 'error' in alias:
            self._error = alias['error']
        else:
            self._error = None

        self._livr = {'value': alias['rules']}
        source[alias['name']] = self

    def __call__(self, *args):
        self.__rule_builders = args[0]
        self.__validator = internal_reactor.InternalValidator(self._livr)

        self.__validator.register_rules(self.__rule_builders)
        self.__validator.prepare()

        return self._validate

    def _validate(self, value, unuse, output):    
        # A missing value stays missing: the rules get no field
        result = self.__validator.validate({} if value is None else {'value': value})

        if result is False:
            return self._error or self.__validator.get_errors()['value']
        
        if 'value' in result:
            output.append(result['value'])

