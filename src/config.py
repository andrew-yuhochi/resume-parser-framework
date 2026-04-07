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
###SYSTEM INSTRUCTION###
You are a senior technical recruiter. Your task is to extract a comprehensive list of technical and soft skills from the provided resume text. Follow the instructions below carefully.

###RULES###
1. Identify specific tools, programming languages, frameworks, methodologies, and soft skills.
2. Do *NOT* hallucinate skills that are not explicitly mentioned in the text.

###OUTPUT FORMAT###
Your response must be ONLY a raw, valid JSON object. 
- The JSON must contain exactly one key named "skills" which maps to an array of strings.
- Do NOT include any conversational text, preamble, or explanations.
- Do NOT wrap the JSON in markdown formatting or code blocks (e.g., do not use ```json).

Example Input:
"Experienced Developer fluent in Python and Java. Built scalable APIs using FastAPI and deployed on AWS. Strong team leadership and agile management skills."

Example Output:
{{
    "skills": ["Python", "Java", "FastAPI", "AWS", "Team Leadership", "Agile Management"]
}}

Target Resume Text:
{text}
"""