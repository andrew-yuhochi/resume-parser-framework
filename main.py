import os
import warnings

from src.extractors import EmailExtractor, NameExtractor, SkillsExtractor
from src.framework import ResumeParserFramework
from src.gemini_client import GeminiClient

warnings.filterwarnings("ignore")


def main() -> None:
    print("Initializing Resume Parsing Framework...\n")

    try:
        llm_client = GeminiClient()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please set your Gemini API key using: export LLM_API_KEY='your_key'")
        return

    extractors = {
        "name": NameExtractor(),
        "email": EmailExtractor(),
        "skills": SkillsExtractor(llm_client=llm_client)
    }

    framework = ResumeParserFramework(extractors=extractors)

    word_resume_path = "sample_resumes/jane_doe_resume.docx"
    pdf_resume_path = "sample_resumes/john_smith_resume.pdf"

    if os.path.exists(word_resume_path):
        print(f"--- Parsing Word Document: {word_resume_path} ---")
        print(framework.parse_resume(word_resume_path).to_json())
    else:
        print(f"Warning: Word resume not found at {word_resume_path}")

    if os.path.exists(pdf_resume_path):
        print(f"\n--- Parsing PDF Document: {pdf_resume_path} ---")
        print(framework.parse_resume(pdf_resume_path).to_json())
    else:
        print(f"\nWarning: PDF resume not found at {pdf_resume_path}")


if __name__ == "__main__":
    main()