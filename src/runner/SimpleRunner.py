import time
from runner.Loader import Loader
from runner.Runner import Runner
from worker.Worker import Worker
from client_platform.BinancePlatform import BinancePlatform

class SimpleRunner(Runner):
    platform_map = {
        "BINANCE": BinancePlatform,
    }
    
    def __init__(self, bot_path, target_platform):
        self.platform_class = SimpleRunner.platform_map[target_platform.upper()]   
        self.bot_class = Loader.load_bot(bot_path)
        
        
    def prepare_worker(self):
        if (self.bot_class and self.platform_class):
            self.worker = Worker(self.bot_class, self.platform_class)

    def test_worker_integration(self):
        return self.worker.test_integration()
        
    def run_bot_loop(self, interval=60):
        print("Starting bot loop. Press Ctrl+C to stop.")
        self.running = True
        while self.running:
            try:
                result = self.worker.execute()
                print('\n' +'#'*10)
                print(f"[Runner] Execution result:\n{result}")
            except Exception as e:
                print(f"[Runner] Error during execution: {e}")
            time.sleep(interval)
        

if __name__ == '__main__':
    runner = SimpleRunner(bot_path="bots/SimpleBot.py", target_platform="Binance")
    runner.prepare_worker()
    connection_status = runner.test_worker_integration()
    if connection_status:
        print("BOT IS WORKING!\n")
        runner.run_bot_loop(interval=15)