from loguru import logger


class Portfolio:
    """


    """
    def __init__(self,
                 name: str,
                 init_cash: float):
        self.name = name

        # Dollar value
        self.init_cash = init_cash
        self.current_cash = init_cash

        # Accumulated transaction costs
        self.acc_tc = 0

        self.positions = {}

        self.transactions = []

    def transact_position(self,
                          buy_sell: str,
                          ric: str,
                          number_shares: int,
                          price: float,
                          verbose=False):
        cost = number_shares * price
        transaction_cost = 0
        total_cost = cost + transaction_cost
        no_shares = number_shares

        if buy_sell == 'B':
            # Buy new position
            if ric not in self.positions.keys():
                self.positions.update({ric: no_shares})
            else:
                no_shares = self.positions[ric] + number_shares
                self.positions.update({ric: no_shares})
            self.current_cash -= total_cost

            trans_string = 'Bought ' + str(number_shares) + ' ' + ric + ' ' + '@ ' + str(price) + \
                           '. Transaction cost ' + str(transaction_cost)
            self.transactions.append(trans_string)

            if verbose:
                logger.info(trans_string)

        else:
            # Short position
            if ric not in self.positions.keys():
                self.positions.update({ric: -no_shares})
            else:
                no_shares = self.positions[ric] - number_shares
                self.positions.update({ric: no_shares})
            self.current_cash += total_cost

            trans_string = 'Sold ' + str(number_shares) + ' ' + ric + ' ' + '@ ' + str(price) + \
                           '. Transaction cost ' + str(transaction_cost)
            self.transactions.append(trans_string)

            if verbose:
                logger.info(trans_string)