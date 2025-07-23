from bots.BaseBot import BaseBot

class SimpleBot(BaseBot):
    def __init__(self):
        pass
    
    def generate_action(self):
        # Ignore df, return dummy signal for testing
        return {
            "action": "buy",
            "symbol": "BTCUSDT",
            "confidence": 0.85
        }

    def generate_signal(self, data):
        return {
            "symbol": "BTCUSDT",
        }