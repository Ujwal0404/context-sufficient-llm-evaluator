from pydantic import BaseModel, Field
from typing import Union, List
from enum import Enum

class ContextType(str, Enum):
    TEXT = "text"
    CSV = "csv"
    LIST = "list"
    DATAFRAME = "dataframe"

class EvaluationRequest(BaseModel):
    context: Union[str, List[str], dict] = Field(
        ..., 
        description="The context to evaluate based on context_type"
    )
    question: str = Field(
        ..., 
        description="The question to be answered",
        min_length=3
    )
    context_type: ContextType = Field(
        ..., 
        description="Type of the context provided"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "context": "product,release_date,price,features\niPhone 14 Pro,September 2022,999,A16 Bionic\niPhone 14,September 2022,799,A15 Bionic",
                    "question": "When was the iPhone 14 Pro released and how much does it cost?",
                    "context_type": "csv"
                }
            ]
        }