from typing import Dict, Any
from groq import AsyncGroq  # Using the async client
import json
from datetime import datetime

class GroqProvider:
    def __init__(self, api_key: str, model_name: str = "mixtral-8x7b-32768"):
        if not api_key:
            raise ValueError("Groq API key is required")
        
        # Initialize Groq client
        self.client = AsyncGroq(api_key=api_key)  # Using async client
        self.model_name = model_name

    def validate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and ensure the response has all required fields"""
        required_fields = {
            "confidence_score": lambda x: isinstance(x, int) and 1 <= x <= 100,
            "explanation": lambda x: isinstance(x, str) and len(x) > 0,
            "relevancy_analysis": lambda x: isinstance(x, str) and len(x) > 0,
            "accuracy_analysis": lambda x: isinstance(x, str) and len(x) > 0,
            "missing_information": lambda x: isinstance(x, list),
            "data_quality": lambda x: isinstance(x, dict) and all(
                k in x for k in ["format", "structure_quality", "completeness"]
            )
        }

        for field, validator in required_fields.items():
            if field not in response or not validator(response[field]):
                raise ValueError(f"Invalid or missing field: {field}")
        
        return response

    async def generate_evaluation(self, prompt: str) -> Dict[str, Any]:
        """Generate evaluation using Groq API with validation"""
        try:
            completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert at evaluating context completeness and relevance. Always provide responses in the exact JSON format requested."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            if not completion.choices or not completion.choices[0].message.content:
                raise ValueError("Empty response from Groq API")

            try:
                result = json.loads(completion.choices[0].message.content)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON response from Groq API")

            # Validate response structure
            validated_result = self.validate_response(result)
            
            # Add metadata
            validated_result["timestamp"] = datetime.now()

            return validated_result

        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")