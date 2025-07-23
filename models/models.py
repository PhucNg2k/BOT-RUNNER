from enum import Enum
class FileType(str, Enum):
    CODE = "CODE"
    MODEL = "MODEL"
    WEIGHTS = "WEIGHTS"
    CONFIG = "CONFIG"
    DATA = "DATA"

class ExchangeType(str, Enum):
    BINANCE = "BINANCE"
    COINBASE = "COINBASE"
    KRAKEN = "KRAKEN"
    BYBIT = "BYBIT"
    HUOBI = "HUOBI"
    
    
    
exchange: ExchangeType = ExchangeType.BINANCE

def connect(exchange: ExchangeType):
    print(exchange)
    
connect("binace")