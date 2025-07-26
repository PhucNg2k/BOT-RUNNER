from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from pydantic import BaseModel

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from src.manager.RunnerManager import RunnerManager

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()

# Legacy request models for backward compatibility
class SubscriptionRequest(BaseModel):
    user_id: str
    bot_filename: str
    platform_name: str

class SubscriptionResponse(BaseModel):
    runner_id: str
    message: str

@router.post("/", response_model=SubscriptionResponse)
def create_subscription(
    request: SubscriptionRequest
):
    try:
        # Call RunnerManager to create a runner
        runner_id = RunnerManager.create_runner(
            user_id=request.user_id,
            bot_filename=request.bot_filename,
            platform_name=request.platform_name
        )
        return SubscriptionResponse(runner_id=runner_id, message="Subscription created successfully.")
    except Exception as e:
        logger.error(f"Error creating subscription: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create subscription."
        )

