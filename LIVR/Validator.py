try:
    import BuildAliasedRule
    import DEFAULT_RULES
    import internal_reactor
except ImportError:
    from . import internal_reactor
    from . import BuildAliasedRule
    from . import DEFAULT_RULES

class Validator(internal_reactor.InternalValidator):
    def __init__(self, livr_rules, is_auto_trim = False):
        self.__is_prepare = False
        self.__livr_rules = livr_rules
        self.__validators = {}
        self.__validator_builders = {}
        self.__errors = None
        self.__is_auto_trim = is_auto_trim
        
        self.register_rules(DEFAULT_RULES.DEFAULT_RULES)
    
    @staticmethod
    def register_default_rules(rules):
        for name, rule in rules.items():
            DEFAULT_RULES.DEFAULT_RULES[name] = rule

    @staticmethod
    def register_aliased_default_rule(alias):
        BuildAliasedRule.BuildAliasedRule(DEFAULT_RULES.DEFAULT_RULES, alias)

    @staticmethod
    def set_default_auto_trim(is_auto_trim):
        IS_DEFAULT_AUTO_TRIM = bool(is_auto_trim)

    
