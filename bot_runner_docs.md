# 🧠 Bot Runner System – Overview & Class Relationships

This system is designed to run **custom trading bots** in isolated Docker containers, using a plugin-style architecture. Each container runs a "runner" that loads bot logic dynamically and connects it to a trading platform (like Binance).

---

## 🏗️ Class Responsibilities & Relationships

### 1. **BaseBot**
- Located in: `src/bots/BaseBot.py`
- An abstract base class for all user-defined bots.
- Defines the required interface (e.g., `generate_signal(data)`).
- User bots must inherit from `BaseBot` and implement the interface.

### 2. **BasePlatform**
- Located in: `src/platform/BasePlatform.py`
- Abstract class defining how to interact with a trading platform.
- Methods like `fetch_data()` and `send_signal(signal)` must be implemented by concrete platforms (e.g., `BinancePlatform`).

### 3. **Loader**
- Loads a user-defined bot class from a file path.
- Dynamically locates the class that inherits from `BaseBot`.
- Used by the Runner to plug in any custom bot at runtime.

### 4. **Worker**
- Combines a bot class and platform class to run the trading loop.
- Calls:
  - `platform.fetch_data()`
  - `bot.generate_signal(data)`
  - `platform.send_signal(signal)`

### 5. **Runner**
- Abstract class that defines:
  - `prepare_config()`: loads bot and platform classes.
  - `prepare_worker()`: initializes the `Worker`.
  - `run_bot_cycle()`: runs the bot periodically.

### 6. **SimpleRunner (inherits from Runner)**
- Implements concrete logic for platform selection.
- Uses a platform map (`"Binance"` → `BinancePlatform`) and the `Loader` to prepare the worker.

---

## 🐳 RunnerManager – Docker Container Manager

### Purpose:
Runs each bot in a **separate Docker container** with runtime-loaded bot code, while using a pre-built image for consistency and speed,

### Key Method: `create_runner(bot_path, platform_name, image_name)`
- Creates a unique container for each bot instance.
- Mounts the local bot directory (e.g., `user-bots/`) into `/app/bots` inside the container using Docker bind volumes.
- Passes bot filename and platform name as ENV variables:
  - `BOT_PATH=/app/bots/custom_bot.py`
  - `PLATFORM_NAME=Binance`
- Each bot runs in a separate container managed by the Docker engine.

### Flow:
1. **User uploads bot** → saved in server `user-bots/`
2. **RunnerManager** spins up container, mounts bot folder
3. **Entrypoint script** in Docker reads env vars
4. **SimpleRunner** loads the custom bot via `Loader`
5. **Worker** runs the bot on the selected platform

---

## 🧠 Summary

- The system uses **dependency injection**: runner injects a dynamically loaded bot and selected platform into the worker.
- **Custom bots are isolated per container**, ensuring safety and separation.
- **Bot code is not baked into the image**—it’s mounted at runtime, making the system extensible without rebuilding images.

---

Let me know if you want a visual diagram or a more detailed deployment guide!

