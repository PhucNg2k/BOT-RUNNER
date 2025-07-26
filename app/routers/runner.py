import logging
from fastapi import APIRouter, HTTPException
from src.manager.RunnerManager import RunnerManager

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def list_runners():
    """List all running bot containers with their details"""
    runners = RunnerManager.list_runners()
    return {"runners": runners}

@router.get("/{runner_id}")
def get_runner_status(runner_id: str):
    """Get runner status"""
    state = RunnerManager.get_runner_state(runner_id)
    if state == "not_found":
        raise HTTPException(status_code=404, detail="Runner not found")
    return {"runner_id": runner_id, "state": state}

@router.delete("/{runner_id}")
def delete_runner(runner_id: str):
    """Delete a runner"""
    success = RunnerManager.delete_runner(runner_id)
    if not success:
        raise HTTPException(status_code=404, detail="Runner not found or already stopped")
    return {"runner_id": runner_id, "status": "stopped"}

@router.post("/{runner_id}/start")
def start_runner(runner_id: str):
    """Start a stopped runner"""
    success = RunnerManager.start_runner(runner_id)
    if not success:
        raise HTTPException(status_code=404, detail="Runner not found or already running")
    return {"runner_id": runner_id, "status": "started"}

@router.post("/{runner_id}/stop")
def stop_runner(runner_id: str):
    """Stop a running runner"""
    success = RunnerManager.stop_runner(runner_id)
    if not success:
        raise HTTPException(status_code=404, detail="Runner not found or already stopped")
    return {"runner_id": runner_id, "status": "stopped"}

@router.get("/{runner_id}/inspect")
def inspect_runner(runner_id: str):
    """Inspect a runner to get detailed information"""
    try:
        details = RunnerManager.inspect_runner(runner_id)
        return {"runner_id": runner_id, "details": details}
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=str(e))


