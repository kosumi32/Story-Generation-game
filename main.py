# FastAPI definition

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

# Defining App
app = FastAPI(
    title="Choose Your Own Adventure API",
    description="An API for managing and playing through choose-your-own-adventure stories.",
    version="0.1.0",

    # FASTAPI auto comes with doc (view in web browser)
    docs_url="/docs",
    redoc_url="/redoc",
)

# API to use in different origins
app.add_middleware(
    CORSMiddleware,     # cross-origin resource sharing (allowing certain origin/url to interact with the API)
    allow_origins=settings.ALLOW_ORIGINS,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, PUT
    allow_headers=["*"],    # Additional info to be send with a request
)

# Only execute the code below if this file is run directly
if __name__ == "__main__":
    import uvicorn

    # Run the app with uvicorn (web server- serve fastAPI app)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

