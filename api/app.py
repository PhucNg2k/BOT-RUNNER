from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from manager import RunnerManager

app = FastAPI()

class RunnerRequest(BaseModel):
    bot_path: str
    platform_name: str

@app.post("/api/runner")
def create_runner(req: RunnerRequest):
    try:
        runner_id = RunnerManager.create_runner(req.bot_path, req.platform_name)
        return {"runner_id": runner_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/runner/{runner_id}")
def get_runner_status(runner_id: str):
    state = RunnerManager.get_runner_state(runner_id)
    if state == "not_found":
        raise HTTPException(status_code=404, detail="Runner not found")
    return {"runner_id": runner_id, "state": state}

@app.delete("/api/runner/{runner_id}")
def delete_runner(runner_id: str):
    success = RunnerManager.delete_runner(runner_id)
    if not success:
        raise HTTPException(status_code=404, detail="Runner not found or already stopped")
    return {"runner_id": runner_id, "status": "stopped"}
