from data_handler import Data_handler
from portfolio import Portfolio
from loguru import logger
import pandas as pd


class Backtester:
    """

    Eventdriven backtester.
    """
    def __init__(self,
                 market: Data_handler,
                 pf: Portfolio,
                 start_date: str,
                 end_date: str):
        self.market = market
        self.pf = pf
        self.start_date = start_date
        self.end_date = end_date

    def pf_value(self, date: str):
        """

        Calculate total market value of alla positions for given date, including current cash.
        :param date: Date for market value.
        :return:
        """
        pos_value = 0
        bar = pd.DataFrame()
        try:
            bar = self.market.data.loc[date]
        except:
            logger.critical('Date ' + date + ' does not exist in Datahandler.data. Aborted.')
            quit()
        for ric, pos in self.pf.positions.items():
            pos_value += bar[ric] * pos
        pos_value += self.pf.current_cash

        return pos_value
