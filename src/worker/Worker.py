
class Worker:
    def __init__(self, bot_class, platform_clas):
        self.bot = bot_class()
        self.platform = platform_clas()

    def execute(self):
        data = self.platform.fetch_data()
        signal = self.bot.generate_signal(data)
        self.platform.send_signal(signal)

    