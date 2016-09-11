from sysIB.wrapper_v2 import IBWrapper, IBclient
from swigibpy import Contract as IBcontract
import datetime


def main():
    """
    This simple example returns historical data
    """

    callback = IBWrapper()
    client = IBclient(callback)

    ibcontract = IBcontract()
    ibcontract.secType = "FUT"
    ibcontract.expiry = "202009"
    ibcontract.symbol = "GE"
    ibcontract.exchange = "GLOBEX"

    # ibcontract.secType = "STK"
    # ibcontract.exchange = "SMART"
    # ibcontract.symbol = "MMM"
    # ibcontract.currency = "USD"

    end_dt = datetime.datetime(2016, 8, 3)
    ans = client.get_IB_historical_data(ibcontract,
                                        durationStr='5 d',
                                        barSizeSetting='5 mins',
                                        end_dt=end_dt)
    return ans


if __name__ == "__main__":
    data = main()
    print(data)
