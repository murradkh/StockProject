import os
import configparser

DEFAULT_MACHINE_TYPE = 'test'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQLITE_DB_PATH = os.path.abspath(os.path.join(BASE_DIR, 'db.sqlite3'))


class Configurator:
    def __init__(self):
        self.machine_type = os.getenv('STOCK_PROJECT_MACHINE_TYPE', DEFAULT_MACHINE_TYPE)
        print("Type: " + self.machine_type)
        self.machine_config_path = os.path.abspath(
            os.path.join(BASE_DIR, 'myrails/configuration/' + self.machine_type + '.cfg'))
        self.test_config_path = os.path.abspath(os.path.join(BASE_DIR, 'myrails/configuration/test.cfg'))

    def parse_machine_config(self):
        if self.machine_type == 'test':
            self.debug_val = True
            self.db_params = {'ENGINE': 'django.db.backends.sqlite3',
                              'NAME': SQLITE_DB_PATH}
            self.db_options = {'timeout': 20}

        else:
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
                if os.getenv("DOCKER_ENV"):
                    self.db_params['HOST'] = self.db_params['HOSTNAME_ON_DOCKER']
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
