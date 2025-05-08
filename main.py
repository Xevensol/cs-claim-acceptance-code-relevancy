from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.router import api_router

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for better security
    allow_credentials=True,
    allow_methods=["*"],  # Specify allowed methods like ["GET", "POST"] for more control
    allow_headers=["*"],  # Specify allowed headers for more control
)


@app.get("/")
def root():
    """
    Root endpoint to test API availability.
    """
    return JSONResponse("WELCOME TO CLOUD SOLUTIONS AI")


# Include API router
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3636)
