from os import path


def get_log_file_path(file):
    file_dir = path.dirname(path.abspath(file))
    parent_dir = path.dirname(file_dir)
    file_path = path.join(str(parent_dir), 'resources/file.conf')
    while path.basename(parent_dir) not in ['FilmAggregator', 's']:
        parent_dir = path.dirname(parent_dir)
        file_path = path.join(str(parent_dir), 'resources/file.conf')
    return file_path


def get_config_file_path(file):
    file_dir = path.dirname(path.abspath(file))
    print(file_dir)
    if path.basename(file_dir) in ['onkin', 's']:
        file_path = path.join(str(file_dir), 'resources/config.ini')
        print(file_path)
        return file_path
    else:
        parent_dir = path.dirname(file_dir)
        print(parent_dir)
        file_path = path.join(str(parent_dir), 'resources/config.ini')
        print(file_path)
        while path.basename(parent_dir) not in ['onkin', 's']:
            parent_dir = path.dirname(parent_dir)
            file_path = path.join(str(parent_dir), 'resources/config.ini')
        return file_path


def float_or_zero(value):
    try:
        return float(value)
    except:
        return 0.0


class ToBool:
    @staticmethod
    def to_bool(bool_str):
        """Parse the string and return the boolean value encoded or raise an exception"""
        if isinstance(bool_str, str) and bool_str:
            if bool_str.lower() in ['true', "True", "TRUE", 't', '1']:
                return True
            elif bool_str.lower() in ['false', "False", "FALSE", 'f', '0']:
                return False

        # if here we couldn't parse it
        raise ValueError("%s is no recognized as a boolean value" % bool_str)
