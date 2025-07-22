import docker
import uuid
import os

class RunnerManager:
    docker_client = docker.from_env()
    container_prefix = "bot_runner_"
    active_containers = {}  # Optional mapping: runner_id -> container_name

    @staticmethod
    def create_runner(bot_path: str, platform_name: str, image_name: str = "bot-runner:latest") -> str:
        runner_id = str(uuid.uuid4())
        container_name = f"{RunnerManager.container_prefix}{runner_id}"

        abs_bot_path = os.path.abspath(bot_path)
        #bot_dir = os.path.dirname(abs_bot_path) # host-side
        bot_dir = os.path.abspath("../../user-bots")
        bot_file = os.path.basename(abs_bot_path)

        try:
            RunnerManager.docker_client.containers.run(
                image=image_name,
                name=container_name,
                detach=True,
                environment={
                    "BOT_PATH": f"/app/bots/{bot_file}",
                    "PLATFORM_NAME": platform_name
                },
                volumes={ # bind-mount local bot folder into container for runtime access
                    bot_dir: {  # -> server local folder
                        "bind": "/app/bots", # this is the path *inside* the container
                        "mode": "ro" # read-only to protect host files
                    }
                },
                restart_policy={"Name": "on-failure"}  # Optional: add resilience
            )
            
            # Just store container name, not the container object
            RunnerManager.active_containers[runner_id] = container_name
            return runner_id
        
        except Exception as e:
            raise RuntimeError(f"Failed to run bot container: {e}")

    @staticmethod
    def delete_runner(runner_id: str) -> bool:
        container_name = RunnerManager.active_containers.get(runner_id) or f"{RunnerManager.container_prefix}{runner_id}"
        try:
            container = RunnerManager.docker_client.containers.get(container_name)
            container.stop()
            container.remove()
            RunnerManager.active_containers.pop(runner_id, None)
            return True
        except docker.errors.NotFound:
            return False
        except Exception as e:
            raise RuntimeError(f"Failed to delete container {container_name}: {e}")

    @staticmethod
    def get_runner_state(runner_id: str) -> str:
        container_name = RunnerManager.active_containers.get(runner_id) or f"{RunnerManager.container_prefix}{runner_id}"
        try:
            container = RunnerManager.docker_client.containers.get(container_name)
            container.reload()
            return container.status  # e.g., 'running', 'exited'
        except docker.errors.NotFound:
            return "not_found"
        except Exception as e:
            return f"error: {e}"
