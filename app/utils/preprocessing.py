from typing import Union, List
import pandas as pd
import io
import re
from app.models.request_models import ContextType

def preprocess_context(
    context: Union[str, List[str], dict],
    context_type: ContextType
) -> str:
    """
    Preprocess the context into a unified format regardless of input type.
    """
    try:
        if context_type == ContextType.TEXT:
            return clean_text(context if isinstance(context, str) else str(context))
            
        elif context_type == ContextType.CSV:
            if isinstance(context, str):
                df = pd.read_csv(io.StringIO(context))
                return format_dataframe(df)
            raise ValueError("CSV context type expects a string input")
            
        elif context_type == ContextType.LIST:
            if isinstance(context, list):
                return "\n".join(str(item) for item in context)
            raise ValueError("LIST context type expects a list input")
            
        elif context_type == ContextType.DATAFRAME:
            if isinstance(context, dict):
                df = pd.DataFrame.from_dict(context)
                return format_dataframe(df)
            raise ValueError("DATAFRAME context type expects a dictionary input")
            
        else:
            raise ValueError(f"Unsupported context type: {context_type}")
                
    except Exception as e:
        raise ValueError(f"Error preprocessing context: {str(e)}")

def format_dataframe(df: pd.DataFrame) -> str:
    """Format a DataFrame into a readable string representation."""
    formatted_text = []
    
    # Add column names as header
    formatted_text.append("This data contains the following information:")
    formatted_text.append(", ".join(df.columns))
    
    # Add row information
    formatted_text.append("\nHere are the details:")
    
    # Convert each row to a natural language sentence
    for idx, row in df.iterrows():
        row_text = []
        for col in df.columns:
            row_text.append(f"{col}: {row[col]}")
        formatted_text.append(" | ".join(row_text))
        
    return "\n".join(formatted_text)

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()