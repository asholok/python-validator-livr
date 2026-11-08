import os
import sys
PATH_TO_RULES = '/'.join(str(os.path.abspath(__file__)).split('/')[:-1])+'/Rules'
sys.path.insert(0,PATH_TO_RULES)

import Common
import Modifiers
import Special
import String
import Numeric
import Meta
import Dates
import Lists
import Format
import Checksum


DEFAULT_RULES = {
    'required':         Common.Required,
    'not_empty':        Common.NotEmpty,
    'not_empty_list':   Common.NotEmptyList,
    'any_object':       Common.AnyObject,

    'one_of':           String.OneOf,
    'max_length':       String.MaxLength,
    'min_length':       String.MinLength,
    'length_equal':     String.EqualLength,
    'length_between':   String.BetweenLength,
    'length_between':   String.BetweenLength,
    'like':             String.Like,
    'eq':               String.Eq,
    'string':           String.String,

    'integer':          Numeric.Integer,
    'positive_integer': Numeric.PositiveInteger,
    'decimal':          Numeric.Decimal,
    'positive_decimal': Numeric.PositiveDecimal,
    'max_number':       Numeric.MaxNumber,
    'min_number':       Numeric.MinNumber,
    'number_between':   Numeric.BetweenNumbers,

    'email':            Special.Email,
    'equal_to_field':   Special.EqualToField,
    'url':              Special.Url,
    'iso_date':         Special.IsoDate,

    'nested_object':    Meta.NestedObject,
    'list_of':          Meta.ListOf,
    'list_of_objects':  Meta.ListOfObjects,
    'or':               Meta.Or,
    'variable_object':  Meta.VariableObject,
    'list_of_different_objects': Meta.ListOfDiferentObjects,

    'default':          Modifiers.Default,
    'trim':             Modifiers.Trim,
    'to_lc':            Modifiers.ToLc,
    'to_uc':            Modifiers.ToUc,
    'remove':           Modifiers.Remove,
    'leave_only':       Modifiers.LeaveOnly,

    # LIVR 2.5
    'boolean':          Common.Boolean,
    'any':              Common.Any,
    'required_if':      Common.RequiredIf,

    'not_one_of':       String.NotOneOf,
    'digits':           String.Digits,
    'starts_with':      String.StartsWith,
    'ends_with':        String.EndsWith,
    'contains':         String.Contains,

    'max_decimals':     Numeric.MaxDecimals,

    'iso_datetime':     Dates.IsoDatetime,
    'iso_time':         Dates.IsoTime,

    'when':             Meta.When,
    'values':           Meta.Values,
    'keys':             Meta.Keys,

    'list_length':      Lists.ListLength,
    'unique':           Lists.Unique,

    'split':            Modifiers.Split,

    'uuid':             Format.Uuid,
    'ip':               Format.Ip,
    'cidr':             Format.Cidr,
    'hostname':         Format.Hostname,
    'base64':           Format.Base64,
    'hex':              Format.Hex,
    'digest':           Format.Digest,
    'mongo_id':         Format.MongoId,
    'hex_color':        Format.HexColor,
    'mac':              Format.Mac,
    'e164':             Format.E164,
    'semver':           Format.Semver,
    'jwt':              Format.Jwt,

    'luhn':             Checksum.Luhn,
    'credit_card':      Checksum.CreditCard,
    'iban':             Checksum.Iban,
}

