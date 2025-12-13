"""
Configuration file for CV Anonymizer
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Configuration (from .env file)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Template par défaut
DEFAULT_TEMPLATE = 'advanced'  # DataMed Advanced

# Logo path
LOGO_PATH = 'image/datamed_consulting_logo.png'
