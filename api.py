from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
from prometheus_fastapi_instrumentator import Instrumentator

import os

app = FastAPI()

# Global variable to store the current scale
current_scale = 3

# Instrument the app
Instrumentator().instrument(app).expose(app)
class ScaleResponse(BaseModel):
    desiredReplicas: int

class ScaleRequest(BaseModel):
    desiredReplicas: conint(ge=0, le=9)  # Constrained int between 0 and 9

@app.get("/health")
async def health_check():
    # Simple health check endpoint
    return {"status": "OK"}

@app.get("/scale", response_model=ScaleResponse)
def get_scale():
    return ScaleResponse(desiredReplicas=current_scale)

@app.post("/scale", response_model=ScaleResponse)
def set_scale(scale_request: ScaleRequest):
    global current_scale
    current_scale = scale_request.desiredReplicas
    return ScaleResponse(desiredReplicas=current_scale)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
