from abc import ABC, abstractmethod
from ..worker.Worker import Worker

class Runner(ABC):
    def __init__(self):
        self.worker = None
        self.running = False


    @abstractmethod
    def prepare_worker(self):
        pass 

    def test_worker_integration(self):
        try:
            self.worker.execute()
        except Exception as e:
            print(f"[Runner] Worker test failed: {e}")

    def get_worker_state(self):
        return "ready" if self.worker else "uninitialized"

    def run_bot_cycle(self):
        self.running = True
        while self.running:
            self.worker.execute()


    