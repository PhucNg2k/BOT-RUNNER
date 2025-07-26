import docker
import uuid
import os
from dotenv import dotenv_values
import subprocess

class RunnerManager:
    docker_client = docker.from_env()
    container_prefix = "bot_runner_"
    
    @staticmethod
    def create_runner(user_id: str, bot_filename: str, platform_name: str, image_name: str = "bot-runner:latest") -> str:

        # Always resolve from project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        user_dir_host = os.path.join(project_root, "user-bots", user_id)
        runner_id = f"{uuid.uuid4().hex[:8]}"
        container_name = f"{RunnerManager.container_prefix}{runner_id}"
        
        user_dir_container = "/app/user_bots"
        env_file_path = os.path.join(user_dir_host, ".env")
        
        print('USER HOST: ', user_dir_host)
        
        # Load .env file and merge with required environment variables
        user_env = dotenv_values(env_file_path)
        user_env.update({
            "BOT_PATH": f"{user_dir_container}/{bot_filename}",
            "PLATFORM_NAME": platform_name
        })
        try:
            container = RunnerManager.docker_client.containers.run(
                image=image_name,
                name=container_name,
                detach=True,
                volumes={
                    user_dir_host: {
                        "bind": user_dir_container,
                        "mode": "ro"
                    }
                },
                environment=user_env,
                #restart_policy={"Name": "on-failure"}  # Optional: add resilience
            )
            
            # Just store container name, not the container object
            return runner_id
        
        except Exception as e:
            raise RuntimeError(f"Failed to run bot container: {e}")

    @staticmethod
    def delete_runner(runner_id: str) -> bool:
        container_name = f"{RunnerManager.container_prefix}{runner_id}"
        try:
            container = RunnerManager.docker_client.containers.get(container_name)
            container.stop()
            container.remove()
            return True
        except docker.errors.NotFound:
            return False
        except Exception as e:
            raise RuntimeError(f"Failed to delete container {container_name}: {e}")

    @staticmethod
    def get_runner_state(runner_id: str) -> str:
        container_name = f"{RunnerManager.container_prefix}{runner_id}"
        try:
            container = RunnerManager.docker_client.containers.get(container_name)
            container.reload()
            return container.status  # e.g., 'running', 'exited'
        except docker.errors.NotFound:
            return "not_found"
        except Exception as e:
            return f"error: {e}"

    @staticmethod
    def list_runners():
        # Returns a dict of runner_id -> container_name
        return {}


if __name__ == "__main__":
    bot_filename = 'SimpleBot.py'
    platform_name = 'Binance'

    user_id = 'user_1'
    container_id = RunnerManager.create_runner(user_id, bot_filename, platform_name)
    print(f"Runner container created: {container_id}")
        
    user_id = 'user_2'
    container_id = RunnerManager.create_runner(user_id, bot_filename, platform_name)
    print(f"Runner container created: {container_id}")
