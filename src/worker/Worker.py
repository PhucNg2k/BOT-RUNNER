from bots.SimpleBot import SimpleBot
from client_platform.BinancePlatform import BinancePlatform

class Worker:
    def __init__(self, bot_class, platform_class):
        self.bot = bot_class()
        self.platform = platform_class()

    def execute(self):
        data = self.platform.fetch_data()
        signal = self.bot.generate_action()
        #result = self.platform.send_signal(signal)
        
        result = self.platform.get_account_info()
        return result
    
    def test_integration(self):
        print("\nCHECKING CREDENTIALS")
        platform_check = BinancePlatform.validate_binance_credentials()[0]
        #payload = self.bot.generate_signal({})
        #bot_check = self.platform._make_request("GET", "/api/v3/ticker/price", payload)
        return platform_check

    def give_status():
        pass
    
    
if __name__ == "__main__":
    
    worker = Worker(SimpleBot, BinancePlatform)
    res = worker.test_integration()
    print(res)
    
    
    