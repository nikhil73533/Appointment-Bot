from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 
from api.v1.app import tools
import uvicorn

# Create FastAPI app instance
app = FastAPI()

# Enable CORS (allow all origins for now; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tools)

if __name__=="__main__":
    uvicorn.run("setup:app", host="127.0.0.1", port=8000, reload=True)
