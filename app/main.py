from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routers.subscription import router as subscription_router
from app.routers.runner import router as runner_router



app = FastAPI(
    title="Trading Bot API",
    description="A comprehensive API for managing trading bot subscriptions and runners",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscription_router, prefix="/api/subscription", tags=["subscriptions"])
app.include_router(runner_router, prefix="/api/runner", tags=["runners"])

@app.get("/")
def read_root():
    return {
        "message": "Trading Bot API v2.0", 
        "features": [
            "User authentication",
            "Bot marketplace",
            "Subscription management",
            "Docker runner integration",
            "Trade tracking",
            "Performance analytics"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
