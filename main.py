import data_handler as dh

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
    print(df)
