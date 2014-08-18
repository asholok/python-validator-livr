
class Trim(object):
    def __init__(self, *args):
        pass

    def __call__(self, val, unuse, output):
        if not val or val == 0:
            return

        if isinstance(value, dict):
            output = {key: val.upper() for key, val in value.items()}
        elif isinstance(val, list):
            output = [val.upper() for val in value]
        elif isinstance(val, str):
            output = val.upper()

class ToLc(object):
    def __init__(self, *args):
        pass

    def __call__(self, val, unuse, output):
        if not val or val == 0:
            return

        if isinstance(value, dict):
            output = {key: val.lower() for key, val in value.items()}
        elif isinstance(val, list):
            output = [val.lower() for val in value]
        elif isinstance(val, str):
            output = val.lower()

class ToUc(object):
    def __init__(self, *args):
        pass
    
    def __call__(self, val, unuse, output):
        if not val or val == 0:
            return

        if isinstance(value, dict):
            output = {key: val.upper() for key, val in value.items()}
        elif isinstance(val, list):
            output = [val.upper() for val in value]
        elif isinstance(val, str):
            output = val.upper()
