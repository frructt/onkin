from optparse import OptionParser

import prepare_environment
from dto.config_ini import ParseConfigINI

config_file_path = prepare_environment.get_config_file_path(__file__)
config = ParseConfigINI(config_file_path)
db_section = config.get_section_obj("DBSection")
server_section = config.get_section_obj("ServerSection")

api_url_base = server_section.api_url_base


def get_argv(param_name):
    parser = OptionParser()
    parser.add_option("--serverName", action="store")
    parser.add_option("--junitxml", action="store")
    parser.add_option("-m", action="store")
    parser.add_option("-s", action="store")
    parser.add_option("-v", action="store")
    parser.add_option("-l", action="store")
    options, remainder = parser.parse_args()
    options_dict = vars(options)
    for k, v in options_dict.items():
        if k == param_name:
            return v
    return None


server = get_argv("serverName")
if not server:
    server = db_section.server
database = db_section.dbname
uid = db_section.uid
pwd = db_section.password
