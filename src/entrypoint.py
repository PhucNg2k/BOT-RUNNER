import os
import sys
from runner.SimpleRunner import SimpleRunner  # Your concrete Runner subclass

def main():
    bot_path = os.environ.get("BOT_PATH")
    platform_name = os.environ.get("PLATFORM_NAME")
    
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
