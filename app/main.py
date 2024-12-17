from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.config import get_settings
from app.utils.error_handler import error_handler, APIError

app = FastAPI(
    title="Context Evaluator API",
    description="API for evaluating if a given context is sufficient to answer a question",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")

# Add error handlers
app.add_exception_handler(APIError, error_handler)
app.add_exception_handler(Exception, error_handler)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    
@app.on_event("shutdown")
async def shutdown_event():
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)