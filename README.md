# NAME
LIVR.Validator - Lightweight validator supporting Language Independent Validation Rules Specification (LIVR)

# SYNOPSIS
Common usage:

    from Validator import Validator
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
    


You can use filters separately or can combine them with validation:

    validator = Validator({
        'email': [ 'required', 'trim', 'email', 'to_lc' ]
    })
    


Feel free to register your own rules:

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


# DESCRIPTION
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
 * Rules are be able to change results output ("trim", "nested\_object", for example)
 * Multipurpose (user input validation, configs validation, contracts programming etc)

# INSTALL

Use npm for nodejs. For browser you can find browserified versions in "dist" folder (livr-debug.js - not minified development version with source maps, livr-min.js - minified production version)

# CLASS METHODS

## new LIVR.Validator(livr, isAutoTrim);
Contructor creates validator objects.
livr - validations rules. Rules description is available here - https://github.com/koorchik/LIVR

isAutoTrim - asks validator to trim all values before validation. Output will be also trimmed.
if isAutoTrim is undefined(or null) than defaultAutoTrim value will be used.

## LIVR.Validator.registerDefaultRules({"rule\_name": ruleBuilder })
ruleBuilder - is a function reference which will be called for building single rule validator.

    LIVR.Validator.registerDefaultRules( "my_rule": function(arg1, arg2, arg3, ruleBuilders) {
        // ruleBuilders - are rules from original validator 
        // to allow you create new validator with all supported rules
        // var validator = new LIVR.Validator(livr).registerRules(ruleBuilders).prepare();
    
        return function(value, allValues, outputArr) {            
            if (notValid) {
                return "SOME_ERROR_CODE";
            }
            else {
                
            }
        }
    });

Then you can use "my\_rule" for validation:
    
    {
        name1: 'my_rule' // Call without parameters
        name2: { 'my_rule': arg1 } // Call with one parameter.
        name3: { 'my_rule': [arg1] } // Call with one parameter.
        name4: { 'my_rule': [ arg1, arg2, arg3 ] } // Call with many parameters.
    }

Here is "max\_number" implemenation:

    function maxNumber(maxNumber) {
        return function(value) {
            // We do not validate empty fields. We have "required" rule for this purpose
            if (value === undefined || value === null || value === '' ) return;
    
            // return error message
            if ( value > maxNumber ) return 'TOO_HIGH';
        };
    };
    LIVR.Validator.registerDefaultRules({ "max_number": maxNumber });

All rules for the validator are equal. It does not distinguish "required", "list\_of\_different\_objects" and "trim" rules. So, you can extend validator with any rules you like.

## LIVR.Validator.getDefaultRules();
returns object containing all default ruleBuilders for the validator. You can register new rule or update existing one with "registerRules" method.

## LIVR.Validator.defaultAutoTrim(isAutoTrim)
Enables or disables automatic trim for input data. If is on then every new validator instance will have auto trim option enabled


# OBJECT METHODS

## validator.validate(input)
Validates user input. On success returns validData (contains only data that has described validation rules). On error return false.

    my validaData = validator.validate(input)

    if (validData) {
        // use validData
    } else {
        var errors = validator.getErrors();
    }

## validator.getErrors()
Returns errors object.

   {
        "field1": "ERROR_CODE",
        "field2": "ERROR_CODE",
        ...
    }

For example:

    {
        "country":  "NOT_ALLOWED_VALUE",
        "zip":      "NOT_POSITIVE_INTEGER",
        "street":   "REQUIRED",
        "building": "NOT_POSITIVE_INTEGER"
    }

## validator.registerRules({"rule_name": ruleBuilder})

ruleBuilder - is a function reference which will be called for building single rule validator.

See "LIVR.Validator.registerDefaultRules" for rules examples.

## validator.getRules()
returns object containing all ruleBuilders for the validator. You can register new rule or update existing one with "registerRules" method.

# AUTHOR
koorchik (Viktor Turskyi)

# BUGS
Please report any bugs or feature requests to Github https://github.com/koorchik/js-validator-livr