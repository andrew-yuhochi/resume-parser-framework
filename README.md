# Resume Parsing Framework

This project implements a production-ready, pluggable Resume Parsing framework designed to extract structured data from multiple file formats using field-specific extraction strategies. 

The framework is built with a strict adherence to Object-Oriented Design (OOD) principles, allowing it to easily scale to support new file types and extraction methods without modifying core orchestration logic. It successfully parses resumes into a standardized JSON format containing the candidate's name, email, and skills.

## Architecture & Object-Oriented Design

The system relies heavily on the Dependency Inversion Principle to decouple orchestration from implementation details:

* **File Parsing (`FileParser`):** An abstract base class defining the contract for text extraction. Concrete implementations (`PDFParser`, `WordParser`) handle `.pdf` and `.docx` files respectively.
* **Field Extraction (`FieldExtractor`):** An abstract base class for specific parsing strategies. 
    * `EmailExtractor`: Utilizes a robust Regular Expression strategy.
    * `NameExtractor`: Utilizes a Named Entity Recognition (NER) model via `spaCy`.
    * `SkillsExtractor`: Utilizes a Large Language Model (LLM) strategy via the Google Gemini API with deterministic configuration and retry logic.
* **Orchestration:** The `ResumeExtractor` coordinates the individual field extractors, returning a strongly typed `ResumeData` dataclass. The `ResumeParserFramework` provides the unified `parse_resume()` entry point.

## Prerequisites

* Python 3.9+
* A valid Google Gemini API Key

## Setup & Installation

**1. Clone the repository and navigate to the project directory:**
```bash
git clone https://github.com/andrew-yuhochi/resume-parser-framework.git
cd resume-parser-framework
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
```

**4. Download the required spaCy NER model:**
```bash
python -m spacy download en_core_web_sm
```

**5. Set your API Key securely:**
```bash
export LLM_API_KEY="your_actual_api_key_here"
```

## Usage Examples
The `main.py` script serves as an end-to-end integration example, demonstrating how to parse both a Word document and a PDF document using the field-specific extractors.

Ensure you have valid resume files located at `sample_resumes/jane_doe_resume.docx` and `sample_resumes/john_smith_resume.pdf`, then run:

```bash
python main.py
```

### Expected Output Structure:
```json
{
    "name": "Jane Doe",
    "email": "jane.doe@gmail.com",
    "skills": [
        "Python",
        "Machine Learning"
    ]
}
```

## Testing Strategy
The codebase is heavily unit-tested using `pytest`. The test suite isolates core logic by actively mocking the LLM API client, ensuring that tests execute instantaneously without making live network calls or requiring active API credentials.

To run the test suite:
```bash
pytest -v
```

## Notes on Extraction Accuracy

While the Object-Oriented orchestration reliably routes and extracts data, the accuracy of the deterministic extractors (like the NER-based `NameExtractor`) is highly dependent on the input file's layout. 

For example, standard PDF parsing often strips layout formatting and newline characters, which can cause adjacent text (e.g., a candidate's location) to be concatenated with their name if the NER model fails to isolate the entity. In a production environment, this would be mitigated by replacing the heuristic fallback with a dedicated LLM extraction call before text extraction.