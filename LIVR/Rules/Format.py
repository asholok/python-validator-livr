#!/usr/bin/python
# -*- coding: utf-8 -*-
# Format rules of LIVR 2.5. Every grammar matches the whole string with ASCII classes
import re

try:
    import Helper
except ImportError:
    from . import Helper

HEX = '[0-9a-fA-F]'
IPV4_RE = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\Z')
IPV6_GROUP_RE = re.compile(HEX + r'{1,4}\Z')
UUID_RE = re.compile(r'{0}{{8}}-{0}{{4}}-({0}){0}{{3}}-({0}){0}{{3}}-{0}{{12}}\Z'.format(HEX))
NIL_UUID = '00000000-0000-0000-0000-000000000000'
MAX_UUID = 'ffffffff-ffff-ffff-ffff-ffffffffffff'
LABEL_RE = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\Z')
BASE64_RE = re.compile(r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?\Z')
BASE64_URL_RE = re.compile(r'(?:[A-Za-z0-9_-]{4})*(?:[A-Za-z0-9_-]{2}==|[A-Za-z0-9_-]{3}=)?\Z')
BASE64_URL_UNPADDED_RE = re.compile(r'[A-Za-z0-9_-]*\Z')
HEX_RE = re.compile(HEX + r'+\Z')
MONGO_ID_RE = re.compile(HEX + r'{24}\Z')
HEX_COLOR_RE = re.compile(r'#(?:{0}{{3,4}}|{0}{{6}}|{0}{{8}})\Z'.format(HEX))
MAC_RE = {
    48: re.compile(r'{0}{{2}}([:-]){0}{{2}}(?:\1{0}{{2}}){{4}}\Z'.format(HEX)),
    64: re.compile(r'{0}{{2}}([:-]){0}{{2}}(?:\1{0}{{2}}){{6}}\Z'.format(HEX)),
}
E164_RE = re.compile(r'\+[1-9][0-9]{6,14}\Z')
SEMVER_NUMBER = r'(?:0|[1-9][0-9]*)'
SEMVER_PRE_ID = r'(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)'
SEMVER_RE = re.compile(
    r'{0}\.{0}\.{0}(?:-{1}(?:\.{1})*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?\Z'.format(SEMVER_NUMBER, SEMVER_PRE_ID)
)
JWT_RE = re.compile(r'([A-Za-z0-9_-]+)\.([A-Za-z0-9_-]+)\.([A-Za-z0-9_-]*)\Z')
DIGEST_LENGTHS = {'md5': 32, 'sha1': 40, 'sha256': 64, 'sha384': 96, 'sha512': 128}


def one_of_arguments(rule_name, args, allowed):
    # Each argument must be one of the allowed values
    values = [Helper.string_argument(rule_name, arg) for arg in args]
    for value in values:
        if value not in allowed:
            Helper.schema_error(rule_name, 'unknown argument "{}"'.format(value))
    return values


def version_argument(rule_name, args):
    # None, "v4" or "v6"; the arguments after the first one are ignored
    args = Helper.arguments(args)
    return one_of_arguments(rule_name, args[:1], ('v4', 'v6'))[0] if args else None


def is_ipv4(value):
    return bool(IPV4_RE.match(value))


def is_ipv6(value):
    # The last two groups may be an IPv4 address
    if '.' in value:
        ipv4 = value.rsplit(':', 1)[-1]
        if not is_ipv4(ipv4):
            return False
        value = value[:-len(ipv4)] + '0:0'

    if '::' in value:
        parts = value.split('::')
        if len(parts) > 2:
            return False
        groups = [group for part in parts if part for group in part.split(':')]
        if len(groups) > 7:
            return False
    else:
        groups = value.split(':')
        if len(groups) != 8:
            return False

    for group in groups:
        if not IPV6_GROUP_RE.match(group):
            return False
    return True


def is_ip(value, version):
    if version == 'v4':
        return is_ipv4(value)
    if version == 'v6':
        return is_ipv6(value)
    return is_ipv4(value) or is_ipv6(value)


class Uuid(object):
    def __init__(self, *args):
        self._versions = one_of_arguments('uuid', Helper.arguments(args), ['v' + str(n) for n in range(1, 9)])

    @Helper.format_rule('WRONG_UUID')
    def __call__(self, value):
        match = UUID_RE.match(value)
        if not match:
            return False
        version, variant = match.groups()
        if not self._versions and value.lower() in (NIL_UUID, MAX_UUID):
            return True
        if variant not in '89abAB':
            return False
        if self._versions:
            return 'v' + version in self._versions
        return version in '12345678'


class Ip(object):
    def __init__(self, *args):
        self._version = version_argument('ip', args)

    @Helper.format_rule('WRONG_IP')
    def __call__(self, value):
        return is_ip(value, self._version)


class Cidr(object):
    def __init__(self, *args):
        self._version = version_argument('cidr', args)

    @Helper.format_rule('WRONG_CIDR')
    def __call__(self, value):
        address, _, prefix = value.partition('/')
        if not re.match(r'(?:0|[1-9][0-9]{0,2})\Z', prefix):
            return False
        if is_ip(address, 'v4') and self._version != 'v6':
            return int(prefix) <= 32
        if is_ip(address, 'v6') and self._version != 'v4':
            return int(prefix) <= 128
        return False


class Hostname(object):
    def __init__(self, *args):
        Helper.no_arguments('hostname', args)

    @Helper.format_rule('WRONG_HOSTNAME')
    def __call__(self, value):
        if len(value) > 253:
            return False
        labels = value.split('.')
        # The last label is not all digits, so a hostname is never an IPv4 address
        if re.match(r'[0-9]+\Z', labels[-1]):
            return False
        for label in labels:
            if not LABEL_RE.match(label):
                return False
        return True


class Base64(object):
    def __init__(self, *args):
        self._is_url = bool(one_of_arguments('base64', Helper.arguments(args)[:1], ('url',)))

    @Helper.format_rule('WRONG_BASE64')
    def __call__(self, value):
        if not self._is_url:
            return len(value) % 4 == 0 and bool(BASE64_RE.match(value))
        # The padding is optional, but complete when it is there
        if '=' in value:
            return len(value) % 4 == 0 and bool(BASE64_URL_RE.match(value))
        return len(value) % 4 != 1 and bool(BASE64_URL_UNPADDED_RE.match(value))


class Hex(object):
    def __init__(self, *args):
        Helper.no_arguments('hex', args)

    @Helper.format_rule('WRONG_HEX')
    def __call__(self, value):
        return bool(HEX_RE.match(value))


class Digest(object):
    def __init__(self, *args):
        if len(args) < 2:
            Helper.schema_error('digest', 'one or more algorithms are required')
        algorithms = one_of_arguments('digest', args[1:], DIGEST_LENGTHS)
        self._lengths = set(DIGEST_LENGTHS[algorithm] for algorithm in algorithms)

    @Helper.format_rule('WRONG_DIGEST')
    def __call__(self, value):
        return len(value) in self._lengths and bool(HEX_RE.match(value))


class MongoId(object):
    def __init__(self, *args):
        Helper.no_arguments('mongo_id', args)

    @Helper.format_rule('WRONG_MONGO_ID')
    def __call__(self, value):
        return bool(MONGO_ID_RE.match(value))


class HexColor(object):
    def __init__(self, *args):
        Helper.no_arguments('hex_color', args)

    @Helper.format_rule('WRONG_HEX_COLOR')
    def __call__(self, value):
        return bool(HEX_COLOR_RE.match(value))


class Mac(object):
    def __init__(self, *args):
        # 48 (MAC-48 / EUI-48, the default) or 64 (EUI-64) bits, also as a string ("64")
        args = Helper.arguments(args)
        bits = Helper.non_negative_integer_argument('mac', args[0]) if args else 48
        if bits not in MAC_RE:
            Helper.schema_error('mac', 'takes no arguments, 48 or 64')
        self._re = MAC_RE[bits]

    @Helper.format_rule('WRONG_MAC')
    def __call__(self, value):
        return bool(self._re.match(value))


class E164(object):
    def __init__(self, *args):
        Helper.no_arguments('e164', args)

    @Helper.format_rule('WRONG_E164')
    def __call__(self, value):
        return bool(E164_RE.match(value))


class Semver(object):
    def __init__(self, *args):
        Helper.no_arguments('semver', args)

    @Helper.format_rule('WRONG_SEMVER')
    def __call__(self, value):
        return bool(SEMVER_RE.match(value))


class Jwt(object):
    def __init__(self, *args):
        Helper.no_arguments('jwt', args)

    @Helper.format_rule('WRONG_JWT')
    def __call__(self, value):
        # The JWS compact serialization; no base64url text has a length of 1 modulo 4
        match = JWT_RE.match(value)
        if not match:
            return False
        for segment in match.groups():
            if len(segment) % 4 == 1:
                return False
        return True
