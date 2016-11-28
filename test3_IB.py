from sysIB.wrapper_v3 import IBWrapper, IBclient
from swigibpy import Contract as IBcontract
import time

if __name__ == "__main__":

    """
    This simple example returns streaming price data
    """

    callback = IBWrapper()
    client = IBclient(callback)

    ibcontract = IBcontract()
    ibcontract.secType = "FUT"
    ibcontract.expiry = "201712"
    ibcontract.symbol = "GE"
    ibcontract.exchange = "GLOBEX"

    ans = client.get_IB_market_data(ibcontract)

    WAIT_TIME = 5
    try:
        client.cb.got_sample.wait(timeout=WAIT_TIME)
    except KeyboardInterrupt:
        pass
    finally:
        if not callback.got_sample.is_set():
            print('Failed to get contract within %d seconds' % WAIT_TIME)

        print("\nDisconnecting...")
        client.cancelMktData()
    print("Bid size, Ask size; Bid price; Ask price")
    print(ans)
