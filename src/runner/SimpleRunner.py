import time
from .Loader import Loader
from .Runner import Runner
from ..worker.Worker import Worker
from ..client_platform.BinancePlatform import BinancePlatform

class SimpleRunner(Runner):
    platform_map = {
        "Binance": BinancePlatform,
    }
    
    def __init__(self, bot_path, target_platform):
        self.platform_class = SimpleRunner.platform_map[target_platform]   
        self.bot_class = Loader.load_bot(bot_path)
        
        
    def prepare_worker(self):
        if (self.bot_class and self.platform_class):
            self.worker = Worker(self.bot_class, self.platform_class)

    def test_worker_integration(self):
        res = self.worker.test_integration()
        if res:
            return "good"
        return "bad"
        
    def run_bot_loop(self, interval=60):
        print("Starting bot loop. Press Ctrl+C to stop.")
        self.running = True
        while self.running:
            try:
                result = self.worker.execute()
                print(f"[Runner] Execution result: {result}")
            except Exception as e:
                print(f"[Runner] Error during execution: {e}")
            time.sleep(interval)

if __name__ == '__main__':
    runner = SimpleRunner(bot_path="src.bots.SimpleBot", target_platform="Binance")
    runner.prepare_worker()
    print(runner.test_worker_integration())
    runner.run_bot_loop(interval=15)