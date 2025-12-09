"""
Anonymizer utility for CV data
"""
import re
import random


class Anonymizer:
    """Anonymize personal information in CVs"""

    def __init__(self):
        self.anonymized_map = {}

    def anonymize_data(self, data: dict) -> dict:
        """
        Anonymize ONLY personal identifiers (name, email, phone, address)
        KEEP EVERYTHING ELSE: company names, locations, all details!
        """
        anonymized = data.copy()

        # Hide ONLY personal identifiers
        anonymized['nom'] = 'Nom & Prénom'
        anonymized['email'] = None
        anonymized['telephone'] = None
        anonymized['adresse'] = None
        anonymized['photo'] = None

        # KEEP EVERYTHING ELSE!
        # - Keep real company names in experiences
        # - Keep all locations (cities, countries)
        # - Keep all project details
        # - Keep all technical environment
        # - Keep all education details

        return anonymized

    def anonymize_text(self, text: str) -> str:
        """
        Anonymize text by removing emails, phones, addresses
        """
        # Remove emails
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)

        # Remove phone numbers
        text = re.sub(r'\b\d{2,3}[-.\s]?\d{2,3}[-.\s]?\d{2,3}[-.\s]?\d{2,3}\b', '[PHONE]', text)
        text = re.sub(r'\+\d{1,3}\s?\d{1,14}', '[PHONE]', text)

        # Remove specific addresses
        text = re.sub(r'\d+\s+[A-Za-z\s]+(?:rue|avenue|boulevard|place|street)[^,\n]+', '[ADDRESS]', text)

        return text

    def generate_anonymous_id(self) -> str:
        """Generate anonymous candidate ID"""
        return f"CAND-{random.randint(1000, 9999)}"
