from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Union
import traceback
from datetime import datetime

class APIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Union[str, dict] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

async def error_handler(request: Request, exc: Exception):
    """Global error handler for the API"""
    
    if isinstance(exc, APIError):
        content = {
            "error": exc.message,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path,
            "details": exc.details
        }
        return JSONResponse(
            status_code=exc.status_code,
            content=content
        )
    
    # Handle unexpected errors
    content = {
        "error": "Internal server error",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "timestamp": datetime.now().isoformat(),
        "path": request.url.path,
        "details": str(exc),
        "traceback": traceback.format_exc()
    }
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content
    )