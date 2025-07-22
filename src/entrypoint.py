import os
import sys
from simple_runner import SimpleRunner  # Your concrete Runner subclass

def main():
    bot_path = os.environ.get("BOT_PATH")
    platform_name = os.environ.get("PLATFORM_NAME")

    if not bot_path:
        print("❌ BOT_PATH environment variable not set.")
        sys.exit(1)

    print(f"🚀 Starting Runner with bot: {bot_path} on platform: {platform_name}")

    runner = SimpleRunner()
    try:
        runner.prepare_config(bot_path=bot_path, target_platform=platform_name)
        runner.prepare_worker()  # ← You missed this call in your version
        runner.test_worker_integration()
        runner.run_bot_cycle()  # This blocks and runs the main bot loop
    except Exception as e:
        print(f"❌ Failed to run bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
