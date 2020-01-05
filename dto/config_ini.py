from configparser import ConfigParser


class DBSection:
    def __init__(self, _list):
        self.server = _list[0][1]
        self.dbname = _list[1][1]
        self.uid = _list[2][1]
        self.password = _list[3][1]


class ServerSection:
    def __init__(self, _list):
        self.api_url_base = _list[0][1]


class DataGeneration:
    def __init__(self, _list):
        self.data_gen = _list[0][1]


class ParseConfigINI:
    def __init__(self, f):
        self.f = f
        self.__read()

    def __read(self):
        self.cfg = ConfigParser()
        self.cfg.read(self.f)

    def items(self, section):
        try:
            return self.cfg.items(section)
        except KeyError:
            return []

    def get_section_obj(self, section):
        _list = self.items(section)
        if section == "DBSection":
            return DBSection(_list)
        elif section == "ServerSection":
            return ServerSection(_list)
        else:
            return None  # just return None if not found
