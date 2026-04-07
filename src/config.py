import os

# API Credentials
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

# LLM Parameters
LLM_MODEL_NAME = "gemini-3-flash-preview"
LLM_TEMPERATURE = 0.1
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 1.0

# Extraction Prompts
DEFAULT_SKILLS_PROMPT = """
You are an expert technical recruiter and resume parser.
Extract all technical and soft skills from the following resume text.
You must return ONLY a valid JSON object with a single key "skills" containing a list of strings.
Do not include any markdown formatting like ```json or ```.

Resume Text:
{text}
"""