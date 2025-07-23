from ..bots.SimpleBot import SimpleBot
from ..client_platform.BinancePlatform import BinancePlatform

class Worker:
    def __init__(self, bot_class, platform_class):
        self.bot = bot_class()
        self.platform = platform_class()

    def execute(self):
        data = self.platform.fetch_data()
        signal = self.bot.generate_action()
        result = self.platform.send_signal(signal)
        return result
    
    def test_integration(self):
        payload = self.bot.generate_signal({})
        result = self.platform._make_request("GET", "/api/v3/ticker/price", payload)
        return result

    def give_status():
        pass
    
    
if __name__ == "__main__":
    
    worker = Worker(SimpleBot, BinancePlatform)
    res = worker.test_integration()
    
    print(res)
    
    
    