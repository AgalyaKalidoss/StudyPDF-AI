import os
from dotenv import load_dotenv

# Load variables from .env

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
"GOOGLE_API_KEY is missing. "
"Please add your Gemini API key to the .env file."
)
