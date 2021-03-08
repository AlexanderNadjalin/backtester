from data_handler import Data_handler
from portfolio import Portfolio
from backtester import Backtester

if __name__ == '__main__':
    """
    rics = ['ERICb.ST']
    start_date = '2021-01-04'
    end_date = '2021-02-26'
    fields = ['TRDPRC_1']
    df = dh.get_eod_data(
        start_date,
        end_date,
        rics, fields,
        count=0)
    """
    start_date = '2021-01-04'
    end_date = '2021-02-26'

    dh = Data_handler()
    dh.read_csv('RDP_hist_close.csv')

    pf = Portfolio('A1', 10000, broker='Avanza')

    bt = Backtester(market=dh, pf=pf, start_date=start_date, end_date=end_date)

    pf.transact_position('B', 'EA.O', 10, 139, verbose=True)
    pf.transact_position('B', 'EA.O', 1, 139.5, verbose=True)
    pf.transact_position('B', 'AMZN.O', 1, 3186, verbose=True)
    # pf.transact_position('S', '.SPX', 11, 44, verbose=True)
    # pf.transact_position('S', '.SPX', 1, 45, verbose=True)

    print(pf.positions)
    print(pf.current_cash)
    print(pf.transactions)
    print(pf.acc_tc)

    print(bt.pf_value(start_date))
