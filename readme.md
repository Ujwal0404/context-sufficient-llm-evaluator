# Context Sufficiency Evaluator API

## Problem Statement
In Large Language Model (LLM) applications, determining whether a given context contains sufficient information to answer a question is crucial for ensuring accurate and reliable responses. This project addresses this challenge by providing an API that:

1. **Evaluates Context Completeness**: Analyzes whether the provided context contains all necessary information to answer a specific question.
2. **Measures Information Relevancy**: Determines how well the context aligns with the question being asked.
3. **Identifies Information Gaps**: Highlights any missing crucial information needed for a complete answer.
4. **Provides Confidence Scoring**: Quantifies the likelihood of getting an accurate answer based on the available context.

This is particularly useful in scenarios where:
- You want to validate if your data retrieval system is fetching relevant context
- You need to ensure the quality of context before generating responses
- You want to identify information gaps in your knowledge base
- You need to assess the reliability of potential responses

## Features

- Multiple context input formats support (Text, CSV, List, DataFrame)
- Comprehensive context evaluation using Groq's LLM
- Detailed analysis of context sufficiency
- Confidence scoring system
- Data quality assessment
- Async API endpoints
- Structured JSON responses
- Health check endpoint

## Use Cases

### 1. Question-Answering Systems
```json
{
    "context": "The Python programming language was created by Guido van Rossum and was first released in 1991.",
    "question": "Who created Python?",
    "context_type": "text"
}
```
Response indicates high confidence (95%) as the context directly contains the answer.

### 2. Knowledge Base Validation
```json
{
    "context": [
        "Customer Support Hours: 9 AM - 5 PM",
        "Phone: 1-800-123-4567",
        "Email: support@example.com"
    ],
    "question": "How can I contact customer support on weekends?",
    "context_type": "list"
}
```
Response identifies missing weekend-specific information.

### 3. Data Retrieval Quality Assessment
```json
{
    "context": {
        "product": ["iPhone 14 Pro", "iPhone 14", "iPhone 13"],
        "release_date": ["September 2022", "September 2022", "September 2021"],
        "base_price": [999, 799, 699]
    },
    "question": "What are the camera specifications of iPhone 14 Pro?",
    "context_type": "dataframe"
}
```
Response indicates insufficient information and missing camera specifications.

## Prerequisites

- Python 3.8+
- Groq API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ujwal0404/context-sufficient-llm-evaluator.git
cd context-sufficient-llm-evaluator
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama2-70b-4096
```

## Usage

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

#### POST /api/evaluate
Evaluates if the given context is sufficient to answer a question.

Example request:
```json
{
    "context": "The iPhone 14 Pro features the A16 Bionic chip and was released in September 2022.",
    "question": "When was the iPhone 14 Pro released?",
    "context_type": "text"
}
```

Example response:
```json
{
    "confidence_score": 95,
    "explanation": "The context directly provides the release date information.",
    "relevancy_analysis": "The context is highly relevant as it explicitly states the release date.",
    "accuracy_analysis": "The information is precise and accurate.",
    "missing_information": [],
    "data_quality": {
        "format": "Clear and concise text",
        "structure_quality": "Well-structured",
        "completeness": "Complete for the specific question"
    },
    "timestamp": "2024-12-17T22:30:00.000Z",
    "request_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### GET /api/health
Health check endpoint to verify if the service is running.

### Supported Context Types

1. Text Format:
```json
{
    "context": "Plain text description or information",
    "context_type": "text"
}
```

2. CSV Format:
```json
{
    "context": "header1,header2\nvalue1,value2\nvalue3,value4",
    "context_type": "csv"
}
```

3. List Format:
```json
{
    "context": ["item1", "item2", "item3"],
    "context_type": "list"
}
```

4. DataFrame Format:
```json
{
    "context": {
        "column1": ["value1", "value2"],
        "column2": ["value3", "value4"]
    },
    "context_type": "dataframe"
}
```

## Response Interpretation

```json
{
    "confidence_score": 75,
    "explanation": "The context provides basic information about the topic but lacks some specific details.",
    "relevancy_analysis": "Content is directly related to the question but missing some key aspects.",
    "accuracy_analysis": "Available information is accurate but incomplete.",
    "missing_information": [
        "Specific technical details",
        "Numerical data",
        "Time-related information"
    ],
    "data_quality": {
        "format": "Well-structured but missing sections",
        "structure_quality": "Good organization of available information",
        "completeness": "Partially complete, key sections missing"
    }
}
```

This response helps in:
- Deciding whether to proceed with generating an answer
- Identifying what additional information needs to be retrieved
- Assessing the quality of your information retrieval system
- Improving your knowledge base or documentation

## Project Structure

```
context-sufficient-llm-evaluator/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── evaluator.py
│   │   └── llm_provider.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request_models.py
│   │   └── response_models.py
│   └── utils/
│       ├── __init__.py
│       └── preprocessing.py
├── requirements.txt
└── .env
```

## Configuration

The application can be configured using environment variables:
- `GROQ_API_KEY`: Your Groq API key
- `MODEL_NAME`: LLM model to use (default: "llama2-70b-4096")

## Error Handling

The API provides detailed error messages and maintains a consistent response structure even in error cases. Error responses include:
- Error description
- Null confidence score
- Error status in analysis fields
- Request ID for tracking
- Timestamp of the error

Example error response:
```json
{
    "confidence_score": null,
    "explanation": "Error in evaluation process",
    "relevancy_analysis": "Error occurred",
    "accuracy_analysis": "Error occurred",
    "missing_information": [
        "Error processing request: Invalid input format"
    ],
    "data_quality": {
        "format": "Error in detection",
        "structure_quality": "Error in assessment",
        "completeness": "Error in assessment"
    },
    "timestamp": "2024-12-17T22:30:00.000Z",
    "request_id": "123e4567-e89b-12d3-a456-426614174001",
    "error": "Invalid input format detected"
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Groq for providing the LLM API
- FastAPI for the web framework
- The open-source community for various tools and libraries used in this project