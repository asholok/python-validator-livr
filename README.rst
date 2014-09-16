NAME
----
LIVR.Validator - Lightweight validator supporting Language Independent Validation Rules Specification (LIVR)

SYNOPSIS
--------
Common usage::

    from LIVR import Validator
    Validator.set_default_auto_trim(True)

    validator = Validator({
        'name':      'required',
        'email':     [ 'required', 'email' ],
        'gender':    { 'one_of' : [['male', 'female']] },
        'phone':     { 'max_length' : 10 },
        'password':  [ 'required', {'min_length' : 10} ],
        'password2': { 'equal_to_field' : 'password' }
    });
    
    valid_data = validator.validate(user_data)
    
    if valid_data:
        save_user_data(valid_data);
    else:
        some_error_hendler(validator.get_errors())
    


You can use filters separately or can combine them with validation::

    validator = Validator({
        'email': [ 'required', 'trim', 'email', 'to_lc' ]
    })
    


Feel free to register your own rules::

    validator = Validator({
        'password': ['required', 'strong_password']
    })
    
    class StrongPassword(object):
        def __init__(self, *args):
            pass

        def __call__(self, value, unuse, unuse):
            value == None or value == '':
                return

            if len(value) < 6:
                return 'WEAK_PASSWORD'

    validator.registerRules({ 'strong_password': StrongPassword})


DESCRIPTION
-----------

See http://livr-spec.org for detailed documentation and list of supported rules.

Features:

 * Rules are declarative and language independent
 * Any number of rules for each field
 * Return together errors for all fields
 * Excludes all fields that do not have validation rules described
 * Has possibility to validatate complex hierarchical structures
 * Easy to describe and undersand rules
 * Returns understandable error codes(not error messages)
 * Easy to add own rules
 * Rules are be able to change results output ("trim", "nested_object", for example)
 * Multipurpose (user input validation, configs validation, contracts programming etc)

INSTALL
-------
Install LIVR from PyPI using PIP::
    sudo pip install LIVR

CLASS METHODS
-------------

Validator(livr, is_auto_trim)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contructor creates validator objects.
livr - validations rules. Rules description is available here - https://github.com/koorchik/LIVR

is_auto_trim - asks validator to trim all values before validation. Output will be also trimmed.
    if is_auto_trim is undefined(or None) than default_auto_trim value will be used.


LIVR.Validator.registerDefaultRules({"rule_name": rule_builder })
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
rule_builder - is a function reference which will be called for building single rule validator.
::
    
    class MyRule(object):
        def __init__(self, *args):
            rule_builders = args[0]
            # rule_builders - are rules from original validator
            # to allow you create new validator with all supported rules
            # validator = Validator(livr)
            # validator.register_rules(rule_builders)
            # validator.prepare()

        def __call__(self, value, all_values, output_array):
            if not_valid:
                return "SOME_ERROR_CODE"
            else:
                # some usefull code

    Validator.register_default_rules( {"my_rule": MyRule} )

Then you can use "my_rule" for validation::
    
    {
        'name1': 'my_rule' # Call without parameters
        'name2': { 'my_rule': arg1 } # Call with one parameter.
        'name3': { 'my_rule': [arg1] } # Call with one parameter.
        'name4': { 'my_rule': [ arg1, arg2, arg3 ] } # Call with many parameters.
    }

Here is "max_number" implemenation::
    
    class MaxNumber(object):
    def __init__(self, *args):
        self._max_number = float(args[1])

    def __call__(self, number, unuse, unuse_):
        # We do not validate empty fields. We have "required" rule for this purpose
        if number == None or number == '':
            return

        #return error message
        if float(number) > self._max_number:
            return 'TOO_HIGH'

    Validator.register_default_rules({ "max_number": MaxNumber });

All rules for the validator are equal. It does not distinguish "required", "list_of_different_objects" and "trim" rules. So, you can extend validator with any rules you like.

Validator.get_default_rules()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
returns object containing all default rule_builders for the validator. You can register new rule or update existing one with "register_rules" method.

Validator.set_default_auto_trim(is_auto_trim)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Enables or disables automatic trim for input data. If is on then every new validator instance will have auto trim option enabled


OBJECT METHODS
--------------

validator.validate(input)
~~~~~~~~~~~~~~~~~~~~~~~~~
Validates user input. On success returns validData (contains only data that has described validation rules). On error return false.
::

    valida_data = validator.validate(input)

    if valida_data: 
        #use valida_data
    else:
        errors = validator.get_errors()

validator.get\_errors()
~~~~~~~~~~~~~~~~~~~~~~~
Returns errors object.
::
   {
        "field1": "ERROR_CODE",
        "field2": "ERROR_CODE",
        ...
    }

For example:
::
    {
        "country":  "NOT_ALLOWED_VALUE",
        "zip":      "NOT_POSITIVE_INTEGER",
        "street":   "REQUIRED",
        "building": "NOT_POSITIVE_INTEGER"
    }

validator.register_rules({"rule_name": rule_builder})
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

rule_builder - is a function reference which will be called for building single rule validator.

See "Validator.register_default_rules" for rules examples.

validator.get_rules()
~~~~~~~~~~~~~~~~~~~~~
returns object containing all ruleBuilders for the validator. You can register new rule or update existing one with "register_rules" method.

AUTHOR
------
koorchik (Viktor Turskyi), asholok (Ihor Kolosha)

BUGS
----
Please report any bugs or feature requests to Github https://github.com/asholok/python-validator-livr