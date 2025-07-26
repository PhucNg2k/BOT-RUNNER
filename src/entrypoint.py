import os
import sys
from runner.SimpleRunner import SimpleRunner  # Your concrete Runner subclass

def main():
    bot_path = os.environ.get("BOT_PATH")
    platform_name = os.environ.get("PLATFORM_NAME")
    print(f"[DEBUG] BOT_PATH: {bot_path}")
    print(f"[DEBUG] PLATFORM_NAME: {platform_name}")
    if not bot_path or not os.path.isfile(bot_path):
        print(f"[ERROR] Bot file not found: {bot_path}")
        sys.exit(1)
    if not platform_name:
        print(f"[ERROR] PLATFORM_NAME not set.")
        sys.exit(1)
    runner = SimpleRunner(bot_path=bot_path, target_platform=platform_name)
    try:
        runner.prepare_worker()
        connection_status = runner.test_worker_integration()
        if connection_status:
            print("\nBOT IS WORKING!\n", flush=True)
            runner.run_bot_loop(interval=15)
        else:
            raise Exception("BOT IS NOT WORKING!")
    except Exception as e:
        print(f"❌ Failed to run bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
