
A Streamlit application that analyzes and validates the relevance between ICD-10 and SBS codes for medical claim processing.

## Overview

This application helps healthcare providers and insurance companies validate the relationship between diagnosis codes (ICD-10) and procedure codes (SBS) to ensure proper claim processing and reduce claim rejections.

## Features

- ICD-10 and SBS code validation
- AI-powered code relevance analysis
- Real-time code description lookup
- User-friendly Streamlit interface
- Secure API endpoints for integration

## Prerequisites

- Python 3.8+
- SQL Server database
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-org/cs-claim-acceptance-code-relevancy.git
cd cs-claim-acceptance-code-relevancy
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
MSSQL_SERVER=your_server
MSSQL_DATABASE=your_database
MSSQL_USER=your_username
MSSQL_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Running the Streamlit App

```bash
streamlit run main_streamlit_02.py
```

### Running the API Server

```bash
python main.py
```

The API will be available at `http://localhost:3636`

## API Endpoints

- `GET /`: Health check endpoint
- `POST /api/evaluate_codes`: Evaluate code relevance
  - Request body:
    ```json
    {
        "icd_codes": ["code1", "code2"],
        "sbs_codes": ["code1", "code2"]
    }
    ```

## Project Structure

```
cs-claim-acceptance-code-relevancy/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core functionality
│   ├── schemas/        # Data models
│   ├── services/       # Business logic
│   └── utils/          # Utility functions
├── logs/               # Application logs
├── main.py            # FastAPI application
├── main_streamlit_02.py # Streamlit application
└── requirements.txt    # Project dependencies
```

## Development

### Code Style

This project follows PEP 8 style guidelines. To check your code:

```bash
flake8 .
```

### Logging

Logs are stored in the `logs` directory with the following levels:
- INFO: General application flow
- WARNING: Non-critical issues
- ERROR: Critical issues requiring attention

