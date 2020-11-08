import os
import configparser


DEFAULT_MACHINE_TYPE = 'test'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQLITE_DB_PATH = os.path.abspath(os.path.join(BASE_DIR, 'db.sqlite3'))


class Configurator:
    def __init__(self):
        machine_type = os.getenv('STOCK_PROJECT_MACHINE_TYPE', DEFAULT_MACHINE_TYPE)
        print ("Type: " + machine_type)
        self.machine_config_path = os.path.abspath(os.path.join(BASE_DIR, 'myrails/configuration/' + machine_type + '.cfg'))
        self.test_config_path = os.path.abspath(os.path.join(BASE_DIR, 'myrails/configuration/test.cfg'))


    def set_test_config(self):
        config = configparser.RawConfigParser()
        config.optionxform = str

        config.add_section('debug')
        config.set('debug', 'value', 'True')

        config.add_section('db-params')
        config.set('db-params', 'ENGINE', 'django.db.backends.sqlite3')
        config.set('db-params', 'NAME', SQLITE_DB_PATH)

        config.add_section('db-options')
        config.set('db-options', 'timeout', '20')

        with open(self.test_config_path, 'w+') as config_file:
            config.write(config_file)
    
    def parse_machine_config(self):
        try:
            assert os.path.exists(self.machine_config_path)
        except AssertionError:
            raise AssertionError('Configuration file not found')
        
        config = configparser.RawConfigParser()
        config.optionxform = str
        config.read(self.machine_config_path)

        try:
            self.debug_val = config.getboolean('debug', 'value')
            self.db_params = config._sections.get('db-params')
            self.db_options = config._sections.get('db-options')
        except ValueError:
            raise
        except configparser.NoSectionError:
            raise
    
    def get_debug_val(self):
        return self.debug_val

    def get_db_params(self):
        return self.db_params
    
    def get_db_options(self):
        return self.db_options
