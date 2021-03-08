import refinitiv.dataplatform as rdp
import configparser as cp
import pandas as pd
import datetime as dt
from loguru import logger
from pathlib import Path


class Data_handler:
    def __init__(self):
        self.config = self.config()
        self.data = pd.DataFrame()

    def __getitem__(self, data):
        return self.data

    @logger.catch
    def config(self) -> cp.ConfigParser:
        """

        Read config file and return a config object. Used to designate target directories for data and models.
        Config.ini file is located in project base directory.

        :return: A ConfigParser object.
        """
        conf = cp.ConfigParser()
        conf.read('config.ini')
        logger.success('I/O info read from config.ini file.')

        return conf

    @logger.catch
    def read_csv(self, input_file_name: str) -> None:
        """

        Read config.ini file. Read specified input .csv file.
        :param input_file_name: Filename including suffix.
        :return: pandas dataframe.
        """

        input_file_directory = Path(self.config['input_files']['input_file_directory'])
        input_file_path = Path.joinpath(input_file_directory, input_file_name)

        raw_data = pd.DataFrame()

        if self.file_valid(input_file_path):
            # date_parser = lambda x: dt.datetime.strptime(x, '%Y-%d-%m')
            try:
                raw_data = pd.read_csv(input_file_path, sep=',', parse_dates=['DATE'])
            except ValueError as e:
                logger.error('File read failed with the following exception:')
                logger.error('   ' + str(e))
                logger.info('Aborted.')
                quit()
            else:
                logger.success('Data file "' + input_file_name + '" read.')

        raw_data = raw_data.set_index(['DATE'])
        # raw_data['DATE'] = raw_data['DATE'].dt.date

        self.data = raw_data

    @logger.catch
    def file_valid(self, file_path: Path):
        """

        Check if file path is valid. Otherwise Abort.
        :param file_path: File Path object (directory + file name).
        :return: Boolean.
        """
        if file_path.exists():
            return True
        else:
            logger.critical('File directory or file name is incorrect. Aborted')
            quit()
