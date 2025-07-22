from BaseBot import BaseBot

class SimpleBot(BaseBot):
    def __init__(self):
        pass
    
    def generate_signal(self, df):
        # Ignore df, return dummy signal for testing
        return {
            "action": "buy",
            "symbol": "BTCUSDT",
            "confidence": 0.85
        }
