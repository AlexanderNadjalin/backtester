import refinitiv.dataplatform as rdp
import configparser as cp
import pandas as pd
import datetime as dt


def config() -> cp.ConfigParser:
    """

    Read config file and return a config object. Used to designate target directories for data and models.
    Config.ini file is located in project base directory.

    :return: A ConfigParser object.
    """
    conf = cp.ConfigParser()
    conf.read('config.ini')
    return conf


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
