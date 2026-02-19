"""
FastAPI Main Entry Point
This will be implemented in Phase 2
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Placeholder for future implementation
app = FastAPI(
    title="NyaaSahayak API",
    description="Multilingual Legal Document Assistant API",
    version="0.1.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "NyaaSahayak API",
        "status": "operational",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
