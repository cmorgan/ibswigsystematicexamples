from swigibpy import EWrapper
from swigibpy import EPosixClientSocket
from threading import Event

MEANINGLESS_ID = 999
CLIENT_ID = 9999

tick_type_map = {
    0: 'bid_size',
    1: 'bid_price',
    2: 'ask_price',
    3: 'ask_size',
    4: 'last_price',
    5: 'last_size',
    6: 'high',
    7: 'low',
    8: 'volume',
    9: 'close_price',
    14: 'open_tick',
    21: 'avg_volume',
    22: 'open_interest',
    27: 'option_call_open_interest',
    45: 'last_timestamp',
}


def return_IB_connection_info():
    """
    Returns the tuple host, port, clientID required by eConnect
    """

    host = ""

    port = 4001
    clientid = CLIENT_ID

    return (host, port, clientid)


class IBWrapper(EWrapper):
    """

    Callback object passed to TWS, these functions will be called directly by
    the TWS or Gateway.

    """
    def __init__(self):
        super(IBWrapper, self).__init__()
        self.got_sample = Event()

    # We need these but don't use them
    def nextValidId(self, orderId):
        pass

    def managedAccounts(self, openOrderEnd):
        pass

    # error handling

    def init_error(self):
        setattr(self, "flag_iserror", False)
        setattr(self, "error_msg", "")

    def error(self, id, errorCode, errorString):
        """
        error handling, simple for now

        Here are some typical IB errors
        INFO: 2107, 2106
        WARNING 326 - can't connect as already connected
        CRITICAL: 502, 504 can't connect to TWS.
            200 no security definition found
            162 no trades

        """
        # Any errors not on this list we just treat as information
        ERRORS_TO_TRIGGER = [201, 103, 502, 504, 509,
                             200, 162, 420, 2105, 1100, 478, 201, 399]

        if errorCode in ERRORS_TO_TRIGGER:
            errormsg = "IB error id %d errorcode %d string %s" % (
                id, errorCode, errorString)
            print(errormsg)
            setattr(self, "flag_iserror", True)
            setattr(self, "error_msg", True)

        # Wrapper functions don't have to return anything

    def init_tickdata(self, tickerid):
        '''
        tickdata is a dict of {tickerid: [, , , ,]}
        '''
        self.fullsample = False
        print('init')
        if "data_tickdata" not in self.__dict__:
            tickdict = dict()
        else:
            tickdict = self.data_tickdata

        tickdict[tickerid] = [False] * 4
        setattr(self, "data_tickdata", tickdict)

    def check_full(self, tickerid):
        data = self.data_tickdata[tickerid]
        if all(data):
            self.got_sample.set()

    def tickString(self, tickerid, field, value):
        unmapped_field = int(field)
        print('tickString: {}: {}'.format(tick_type_map[unmapped_field],
                                          value))
        marketdata = self.data_tickdata[tickerid]

        # update string ticks
        tick_type = field
        # 45 is last timestamp
        if int(tick_type) == 0:
            # bid size
            marketdata[0] = int(value)
        elif int(tick_type) == 3:
            # ask size
            marketdata[1] = int(value)

        elif int(tick_type) == 1:
            # bid
            marketdata[0][2] = float(value)
        elif int(tick_type) == 2:
            # ask
            marketdata[0][3] = float(value)

        self.check_full(tickerid)

    def tickGeneric(self, tickerid, tick_type, value):
        print('tickGeneric')
        marketdata = self.data_tickdata[tickerid]

        # update generic ticks
        if int(tick_type) == 0:
            # bid size
            marketdata[0] = int(value)
        elif int(tick_type) == 3:
            # ask size
            marketdata[1] = int(value)

        elif int(tick_type) == 1:
            # bid
            marketdata[2] = float(value)
        elif int(tick_type) == 2:
            # ask
            marketdata[3] = float(value)

        self.check_full(tickerid)

    def tickSize(self, tickerid, tick_type, size):
        print('tickSize: tick_type: {}, size: {}'.
              format(tick_type_map[tick_type], size))

        # update ticks of the form new size
        marketdata = self.data_tickdata[tickerid]

        if int(tick_type) == 0:
            # bid
            marketdata[0] = int(size)
        elif int(tick_type) == 3:
            # ask
            marketdata[1] = int(size)
        self.check_full(tickerid)

    def tickPrice(self, tickerid, tick_type, price, canautoexecute):
        # update ticks of the form new price
        print('tickPrice: tick_type: {}, price: {}'.
              format(tick_type_map[tick_type], price))
        marketdata = self.data_tickdata[tickerid]

        if int(tick_type) == 1:
            # bid
            marketdata[2] = float(price)
        elif int(tick_type) == 2:
            # ask
            marketdata[3] = float(price)
        self.check_full(tickerid)

    def updateMktDepth(self, id, position, operation, side, price, size):
        """
        Only here for completeness - not required. Market depth is only
        available if you subscribe to L2 data.

        Since I don't I haven't managed to test this.

        Here is the client side call for interest

        tws.reqMktDepth(999, ibcontract, 9)

        """
        pass

    def tickSnapshotEnd(self, tickerId):

        print("No longer want to get %d" % tickerId)


class IBclient(object):
    """
    Client object

    Used to interface with TWS for outside world, does all handling of
    streaming waiting etc

    Create like this
    callback = IBWrapper()
    client=IBclient(callback)

    We then use various methods to get prices etc
    """

    def __init__(self, callback):
        """
        Create like this
        callback = IBWrapper()
        client=IBclient(callback)
        """

        tws = EPosixClientSocket(callback)
        (host, port, clientid) = return_IB_connection_info()
        tws.eConnect(host, port, clientid)

        self.tws = tws
        self.cb = callback

    def get_IB_market_data(self, ibcontract, tickerid=MEANINGLESS_ID):
        """
        Returns granular market data

        Returns a tuple (bid price, bid size, ask price, ask size)
        """

        # initialise the tuple
        self.cb.init_tickdata(tickerid)
        self.cb.init_error()

        # Request a market data stream
        self.tws.reqMktData(
            tickerid,
            ibcontract,
            "",
            False,
            None)

        marketdata = self.cb.data_tickdata[tickerid]
        return marketdata

    def cancelMktData(self, tickerid=MEANINGLESS_ID):
        self.tws.cancelMktData(tickerid)
