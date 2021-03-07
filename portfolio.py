from loguru import logger


class Portfolio:
    """


    """
    def __init__(self,
                 name: str,
                 init_cash: float,
                 broker=None):
        self.name = name

        # Dollar value
        self.init_cash = init_cash
        self.current_cash = init_cash

        # Accumulated transaction costs
        self.acc_tc = 0
        self.broker = broker

        self.positions = {}

        self.transactions = []

    def transact_position(self,
                          buy_sell: str,
                          ric: str,
                          number_shares: int,
                          price: float,
                          verbose=False) -> None:
        """

        Transact portfolio position
        Handles broker fees if portfolio.broker is added.
        Accumulates transaction costs.
        Adds all transactions to portfolio.transactions in a list.
        :param buy_sell: 'B' for buy, 'S' for sell.
        :param ric: Identifier.
        :param number_shares: Number of shares to transact.
        :param price: Price of transaction.
        :param verbose: If True, prints transaction details.
        :return: None.
        """
        cost = number_shares * price
        transaction_cost = self.broker_fee_plan(cost)
        self.acc_tc += transaction_cost
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
                           '. Tc: ' + str(transaction_cost) + '.' + ' Total cost: ' + str(total_cost) + '.'
            self.transactions.append(trans_string)

            if verbose:
                logger.info(trans_string)

        else:
            # Short position
            if ric not in self.positions.keys():
                self.positions.update({ric: -no_shares})
            # Sell from existing position
            else:
                no_shares = self.positions[ric] - number_shares
                self.positions.update({ric: no_shares})
            self.current_cash += total_cost

            trans_string = 'Sold ' + str(number_shares) + ' ' + ric + ' ' + '@ ' + str(price) + \
                           '. Tc: ' + str(transaction_cost) + '.' + ' Total cost: ' + str(total_cost) + '.'
            self.transactions.append(trans_string)

            if verbose:
                logger.info(trans_string)

    def broker_fee_plan(self, cost) -> float:
        """

        Adds logic for broker fees.
        :param cost: Transaction size (number of shares * price)
        :return: Transaction cost.
        """
        if self.broker == 'Avanza':
            # Courtageklass Small
            if cost < 26000.0:
                return 36.0
            else:
                return round(cost * 0.0015, 2)
        else:
            return 0.0
