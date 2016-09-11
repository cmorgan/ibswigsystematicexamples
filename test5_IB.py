from sysIB.wrapper_v5 import IBWrapper, IBclient
from swigibpy import Contract as IBcontract

import time
from pprint import pprint

if __name__ == "__main__":

    """
    Example of getting contract and account details
    """

    callback = IBWrapper()
    client = IBclient(callback)

    ibcontract = IBcontract()
    ibcontract.secType = "FUT"
    ibcontract.symbol = "GBL"
    ibcontract.exchange = "DTB"

    # Get contract details
    cdetails = client.get_contract_details(ibcontract)

    # In particular we want the expiry. You cannot just use
    # cdetails['expiry'][:6] to map back to the yyyymm expiry since certain
    # contracts expire the month before they should!
    pprint(cdetails)

    # will look something like:
    [{'contractMonth': '201612',
      'currency': 'EUR',
      'evMultiplier': 0.0,
      'evRule': '',
      'exchange': 'DTB',
      'expiry': '20161208',
      'liquidHours': '20160925:CLOSED;20160926:0800-2205',
      'longName': 'Euro Bund (10 Year Bond)',
      'minTick': 0.01,
      'secType': 'FUT',
      'symbol': 'GBL',
      'timeZoneId': 'MET',
      'tradingHours': '20160925:CLOSED;20160926:0800-2205',
      'underConId': 11284196},
     {'contractMonth': '201703',
      'currency': 'EUR',
      'evMultiplier': 0.0,
      'evRule': '',
      'exchange': 'DTB',
      'expiry': '20170308',
      'liquidHours': '20160925:CLOSED;20160926:0800-2205',
      'longName': 'Euro Bund (10 Year Bond)',
      'minTick': 0.01,
      'secType': 'FUT',
      'symbol': 'GBL',
      'timeZoneId': 'MET',
      'tradingHours': '20160925:CLOSED;20160926:0800-2205',
      'underConId': 11284196},
     {'contractMonth': '201706',
      'currency': 'EUR',
      'evMultiplier': 0.0,
      'evRule': '',
      'exchange': 'DTB',
      'expiry': '20170608',
      'liquidHours': '20160925:CLOSED;20160926:0800-2205',
      'longName': 'Euro Bund (10 Year Bond)',
      'minTick': 0.01,
      'secType': 'FUT',
      'symbol': 'GBL',
      'timeZoneId': 'MET',
      'tradingHours': '20160925:CLOSED;20160926:0800-2205',
      'underConId': 11284196}]
