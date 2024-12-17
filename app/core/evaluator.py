from typing import Dict, Any, Union, List
import pandas as pd
from datetime import datetime
import uuid
from app.utils.preprocessing import preprocess_context
from app.models.request_models import ContextType
from app.core.llm_provider import GroqProvider

class ContextEvaluator:
    def __init__(self, settings):
        self.settings = settings
        try:
            self.llm = GroqProvider(
                api_key=self.settings.GROQ_API_KEY,
                model_name=self.settings.MODEL_NAME
            )
        except Exception as e:
            raise Exception(f"Failed to initialize GroqProvider: {str(e)}")
        
    def _construct_prompt(self, context: str, question: str) -> str:
        return f"""Please evaluate if the following context is sufficient to accurately answer the given question.
        Consider both relevancy and accuracy.

        Context:
        {context}

        Question:
        {question}

        Evaluate and provide your response in the following JSON format:
        {{
            "confidence_score": <integer between 1 and 100>,
            "explanation": <detailed explanation of the score>,
            "relevancy_analysis": <analysis of how relevant the context is>,
            "accuracy_analysis": <analysis of the information accuracy>,
            "missing_information": [<list of any missing critical information>],
            "data_quality": {{
                "format": <assessment of data format>,
                "structure_quality": <assessment of data structure>,
                "completeness": <assessment of data completeness>
            }}
        }}

        Ensure all fields are present and properly formatted.
        """

    async def evaluate_context(
        self, 
        context: Union[str, List[str], pd.DataFrame],
        question: str,
        context_type: ContextType
    ) -> Dict[str, Any]:
        try:
            # Process the context
            processed_context = preprocess_context(context, context_type)
            
            # Construct the evaluation prompt
            prompt = self._construct_prompt(processed_context, question)
            
            # Get evaluation from LLM
            result = await self.llm.generate_evaluation(prompt)
            
            # Add request ID
            result["request_id"] = str(uuid.uuid4())
            
            return result
            
        except Exception as e:
            return {
                "confidence_score": None,
                "explanation": "Error in evaluation process",
                "relevancy_analysis": "Error occurred",
                "accuracy_analysis": "Error occurred",
                "missing_information": [str(e)],
                "data_quality": {
                    "format": "Error in detection",
                    "structure_quality": "Error in assessment",
                    "completeness": "Error in assessment"
                },
                "timestamp": datetime.now(),
                "request_id": str(uuid.uuid4()),
                "error": str(e)
            }