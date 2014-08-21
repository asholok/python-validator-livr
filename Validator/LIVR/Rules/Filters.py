
class Trim(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, output):
        if value == None or value == '':
            return

        if isinstance(value, dict):
            output.append({key: val.strip() for key, val in value.items()})
        elif isinstance(value, list):
            output.append([val.strip() for val in value])
        elif isinstance(value, str):
            output.append(value.strip())

class ToLc(object):
    def __init__(self, *args):
        pass

    def __call__(self, value, unuse, output):
        if value == None or value == '':
            return

        if isinstance(value, dict):
            output.append({key: val.lower() for key, val in value.items()})
        elif isinstance(value, list):
            output.append([val.lower() for val in value])
        elif isinstance(value, str):
            output.append(value.lower())

class ToUc(object):
    def __init__(self, *args):
        pass
    
    def __call__(self, value, unuse, output):
        if value == None or value == '':
            return

        if isinstance(value, dict):
            output.append({key: val.upper() for key, val in value.items()})
        elif isinstance(value, list):
            output.append([val.upper() for val in value])
        if isinstance(value, str):
            output.append(value.upper())
