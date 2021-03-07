import data_handler as dh
from portfolio import Portfolio as port

if __name__ == '__main__':
    """
    rics = ['ERICb.ST']
    start_date = '2021-01-01'
    end_date = '2021-02-26'
    fields = ['TRDPRC_1']
    df = dh.get_eod_data(
        start_date,
        end_date,
        rics, fields,
        count=0)
    """

    df = dh.read_csv('RDP_hist_close.csv')
    pf = port('A1', 10000)
    pf.transact_position('B', 'EA.O', 100, 20, verbose=True)
    pf.transact_position('B', 'EA.O', 100, 20, verbose=True)
    pf.transact_position('B', 'PLTR.K', 10, 40,verbose=True)

    pf.transact_position('S', '.SPX', 11, 44, verbose=True)
    pf.transact_position('S', '.SPX', 1, 45, verbose=True)

    print(pf.positions)
    print(pf.current_cash)
    print(pf.transactions)
