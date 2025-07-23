import os
import sys
from runner.SimpleRunner import SimpleRunner  # Your concrete Runner subclass

def main():
    bot_path = os.environ.get("BOT_PATH")
    platform_name = os.environ.get("PLATFORM_NAME")
    
    # if not bot_path:
    #     print("❌ BOT_PATH environment variable not set.")
    #     sys.exit(1)

    # print(f"🚀 Starting Runner with bot: {bot_path} on platform: {platform_name}")

    runner = SimpleRunner(bot_path=bot_path, target_platform=platform_name)
    try:
        runner.prepare_worker()
        print(runner.test_worker_integration())
        runner.run_bot_loop(interval=15)
    except Exception as e:
        print(f"❌ Failed to run bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
