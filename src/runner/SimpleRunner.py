from runner import Runner
from loader import Loader
from worker import Worker

from platforms.binance import BinancePlatform

class SimpleRunner(Runner):
    platform_map = {
        "Binance": BinancePlatform,
        "Bybit": BybitPlatform
    }
    
    def prepare_config(self, bot_path, target_platform):
        self.platform_class = SimpleRunner.platform_map[target_platform]   
        self.bot_class = Loader.load_bot(bot_path)
        
    def prepare_worker(self):
        if (self.bot_class and self.platform_class):
            self.worker = Worker(self.bot_class, self.platform_class)


if __name__ == '__main__':
    runner = SimpleRunner()
    runner.prepare_config(bot_path="./bots/SimpleBot.py", target_platform="Binance")
    runner.prepare_worker()
    runner.test_worker_integration()
    runner.run_bot_cycle()