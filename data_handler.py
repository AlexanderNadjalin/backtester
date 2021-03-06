import refinitiv.dataplatform as rdp
import configparser as cp
import pandas as pd
import datetime as dt
from loguru import logger
from pathlib import Path


@logger.catch
def config() -> cp.ConfigParser:
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
def read_csv(input_file_name: str) -> pd.DataFrame:
    """

    Read config.ini file. Read specified input .csv file.
    :param input_file_name: Filename including suffix.
    :return: pandas dataframe.
    """
    conf = config()

    input_file_directory = Path(conf['input_files']['input_file_directory'])
    input_file_path = Path.joinpath(input_file_directory, input_file_name)

    raw_data = pd.DataFrame()

    if file_valid(input_file_path):
        try:
            raw_data = pd.read_csv(input_file_path, sep=',', index_col='DATE', parse_dates=True)
        except ValueError as e:
            logger.error('File read failed with the following exception:')
            logger.error('   ' + str(e))
            logger.info('Aborted.')
            quit()
        else:
            logger.success('Data file "' + input_file_name + '" read.')

    return raw_data


@logger.catch
def file_valid(file_path: Path):
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


def get_eod_data(start_date: str, end_date: str, rics: list, fields: list, count: int) -> pd.DataFrame:
    """

    Get end-of-day data for RICs as a Pandas dataframe.

    :param start_date: Earliest date in format YYYY-MM-DD.
    :param end_date: Latest date in format YYYY-MM-DD.
    :param rics: RIC(s).
    :param fields: Field name(s).
    :param count: Latest n data entries.
    :return: Pandas dataframe.
    """
    # API credentials and session start.
    conf = config()
    app_key = conf['ws_login']['app_key']
    user = conf['ws_login']['user']
    password = conf['ws_login']['password']
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

    df.dropna(how='all',
              inplace=True)
    return df
