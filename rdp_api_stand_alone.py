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
            date_parser = lambda x: dt.datetime.strptime(x, '%Y-%d-%m')
            try:
                raw_data = pd.read_csv(input_file_path, sep=',', index_col='DATE', parse_dates=['DATE'])
            except ValueError as e:
                logger.error('File read failed with the following exception:')
                logger.error('   ' + str(e))
                logger.info('Aborted.')
                quit()
            else:
                logger.success('Data file "' + input_file_name + '" read.')

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

    def rdp_eod_data(self,
                     start_date: str,
                     end_date: str,
                     rics: list,
                     fields: list,
                     count: int,
                     to_csv=False,
                     file_name=False) -> None:
        """

        Get end-of-day data for RICs as a Pandas dataframe.
        """
        # API credentials and session start.
        app_key = self.config['ws_login']['app_key']
        user = self.config['ws_login']['user']
        password = self.config['ws_login']['password']
        rdp.open_platform_session(
            app_key,
            rdp.GrantPassword(
                user,
                password
            )
        )

        # If count has a value, get the last count number of data points. Else use dates.
        if count:
            start_date = dt.timedelta(days=-count)
            end_date = dt.timedelta(days=0)
        else:
            try:
                start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError('"start_date" has incorrect format.')
            try:
                end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError('"end_date" has incorrect format.')

        df = pd.DataFrame()

        # Looped API-call to stay within data threshold.
        for ric in rics:
            try:
                ts = rdp.get_historical_price_summaries(
                    universe=ric,
                    start=start_date,
                    end=end_date,
                    interval=rdp.Intervals.DAILY,
                    fields=fields,
                    adjustments=[
                        rdp.Adjustments.EXCHANGE_CORRECTION,
                        rdp.Adjustments.MANUAL_CORRECTION]
                )
            except rdp.errors.RDPError as err:
                raise err
            if ts is None:  # Check if there is any error.
                print("Error for RIC " + ric + ":" + str(rdp.get_last_status()['error']))
                quit()

            ts.rename(columns={'CLOSE': ric}, inplace=True)
            if len(ts):
                df = pd.concat([df, ts], axis=1)
            else:
                df = ts

        df.dropna(how='all', inplace=True)
        self.data = df

        if to_csv and file_name:
            if len(self.data) > 0:
                self.data.to_csv(self.config['output_files'][file_name], sep=',', header=True)
            else:
                logger.critical('File name not specified. Aborted.')
                quit()
