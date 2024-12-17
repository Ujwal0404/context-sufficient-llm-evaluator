from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from datetime import datetime
import uuid

from app.core.evaluator import ContextEvaluator
from app.models.request_models import EvaluationRequest
from app.models.response_models import EvaluationResponse, DataQuality, HealthCheck
from app.config import get_settings

router = APIRouter(tags=["Evaluation"])

def create_error_response(error_message: str, request_id: str) -> Dict[str, Any]:
    """Helper function to create error response"""
    return {
        "confidence_score": None,
        "explanation": "Error in evaluation process",
        "relevancy_analysis": "Error occurred",
        "accuracy_analysis": "Error occurred",
        "missing_information": [str(error_message)],
        "data_quality": {
            "format": "Error in detection",
            "structure_quality": "Error in assessment",
            "completeness": "Error in assessment"
        },
        "timestamp": datetime.now(),
        "request_id": request_id,
        "error": str(error_message)
    }

@router.post(
    "/evaluate",
    response_model=EvaluationResponse,
    summary="Evaluate Context",
    description="Evaluate if the given context is sufficient to answer the question"
)
async def evaluate_context(
    request: EvaluationRequest,
    settings = Depends(get_settings)
) -> Dict[str, Any]:
    """
    Evaluate if the given context is sufficient to answer the question.
    """
    try:
        evaluator = ContextEvaluator(settings)
        result = await evaluator.evaluate_context(
            context=request.context,
            question=request.question,
            context_type=request.context_type
        )
        return result
    except Exception as e:
        return create_error_response(str(e), str(uuid.uuid4()))

@router.get(
    "/health",
    response_model=HealthCheck,  # Updated to use the new model name
    summary="Health Check",
    description="Check if the API is running"
)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now()
    }