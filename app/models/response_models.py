from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class DataQuality(BaseModel):
    format: str
    structure_quality: str
    completeness: str

class EvaluationResponse(BaseModel):
    confidence_score: Optional[int] = Field(
        None,  # Making it optional for error cases
        description="Confidence score between 1 and 100",
        ge=1,
        le=100
    )
    explanation: str
    relevancy_analysis: str
    accuracy_analysis: str
    missing_information: List[str]
    data_quality: DataQuality
    timestamp: datetime
    request_id: str
    error: Optional[str] = None

class HealthCheck(BaseModel):  # Changed name to avoid confusion
    status: str
    timestamp: datetime