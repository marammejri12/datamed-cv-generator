"""
AI-Powered CV Parser using Google Gemini
Intelligent extraction and classification of CV data
"""
import google.generativeai as genai
import pdfplumber
import docx
import json
import os
from typing import Dict, List


class AICVParser:
    """AI-powered CV parser with Gemini for intelligent extraction"""

    def __init__(self, api_key: str = None):
        """
        Initialize AI parser with Gemini API key

        Args:
            api_key: Google Gemini API key (or set GEMINI_API_KEY env var)
        """
        # Get API key
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use Pro model for maximum accuracy and detail extraction
            self.model = genai.GenerativeModel(
                'models/gemini-2.5-flash',
                generation_config={
                    "temperature": 0.1,  # Very low for precision
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,  # Allow long responses
                }
            )
            self.ai_enabled = True
            print("✅ Gemini AI Pro activé - Extraction COMPLÈTE et PRÉCISE!")
        else:
            self.ai_enabled = False
            print("⚠️ Gemini API key not found. Using basic parsing.")

    def parse_cv(self, file_path: str) -> Dict:
        """
        Parse CV with AI-powered extraction

        Args:
            file_path: Path to CV file (PDF or DOCX)

        Returns:
            Structured CV data
        """
        # Extract raw text
        text = self._extract_text(file_path)

        if not text or len(text) < 50:
            raise ValueError("CV text is too short or empty")

        # Use AI to extract structured data
        if self.ai_enabled:
            return self._ai_extract(text)
        else:
            # Fallback to basic extraction
            return self._basic_extract(text)

    def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX"""
        if file_path.lower().endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        elif file_path.lower().endswith(('.docx', '.doc')):
            return self._extract_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")

    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text

    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")

    def _ai_extract(self, text: str) -> Dict:
        """
        Use Gemini AI to extract and classify CV data intelligently
        """
        prompt = f"""Extrais TOUT le contenu du CV en JSON. Ne résume rien, copie tout tel quel.

CV:
{text}

Format JSON (COMPLETE AVANT D'ARRÊTER):
{{
  "titre_professionnel": "Titre professionnel (ex: Business Analyste Salesforce)",
  "diplomes": [{{"annee": "2020", "diplome": "...", "etablissement": "..."}}],
  "certifications": [{{"annee": "2021", "nom": "...", "organisme": "..."}}],
  "competences_groups": [{{"categorie": "...", "competences": ["..."]}},
  "langues": [{{"langue": "...", "niveau": "..."}}],
  "experiences": [{{
    "entreprise": "...",
    "periode": "...",
    "poste": "...",
    "lieu": "...",
    "projets": ["..."],
    "realisations": ["..."],
    "environnement": ["..."]
  }}]
}}

RÈGLES:
- Extrais TOUS les diplômes/certifications/expériences
- Pour expériences: garde nom réel entreprise, TOUS les bullet points
- Groupe compétences par catégorie intelligente
- IMPORTANT: Ferme tous les tableaux et objets avant de terminer
- Retourne UNIQUEMENT JSON valide, pas de texte avant/après
"""

        try:
            response = self.model.generate_content(prompt)
            json_text = response.text.strip()

            # SAVE RAW JSON TO FILE FOR DEBUGGING - Use temp directory to avoid permission issues
            import tempfile
            debug_file = os.path.join(tempfile.gettempdir(), 'datamed_gemini_response.json')
            try:
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(json_text)
            except Exception:
                pass  # Ignore if can't write debug file
            print(f"📁 JSON brut sauvegardé dans: {debug_file}")

            # Clean markdown code blocks if present
            if json_text.startswith('```json'):
                json_text = json_text[7:]
            if json_text.startswith('```'):
                json_text = json_text[3:]
            if json_text.endswith('```'):
                json_text = json_text[:-3]

            json_text = json_text.strip()

            # Additional cleaning - remove any text before first { or after last }
            first_brace = json_text.find('{')
            last_brace = json_text.rfind('}')
            if first_brace != -1 and last_brace != -1:
                json_text = json_text[first_brace:last_brace+1]

            # Parse JSON
            data = json.loads(json_text)

            # Add titre_professionnel field if not present (extract from CV)
            if 'titre_professionnel' not in data:
                # Try to extract job title from text
                import re
                # Look for common patterns
                title_patterns = [
                    r'(?i)consultant\s+(\w+(?:\s+\w+){0,3})',
                    r'(?i)(data\s+\w+)',
                    r'(?i)(développeur\s+\w+)',
                    r'(?i)(architecte\s+\w+)',
                ]
                for pattern in title_patterns:
                    match = re.search(pattern, text)
                    if match:
                        data['titre_professionnel'] = match.group(0).title()
                        break
                else:
                    data['titre_professionnel'] = 'Consultant IT'

            return data

        except Exception as e:
            print(f"⚠️ AI extraction failed: {str(e)}")
            print("Falling back to basic extraction...")
            return self._basic_extract(text)

    def _basic_extract(self, text: str) -> Dict:
        """
        Fallback: Basic extraction without AI
        Extracts ALL text content even if structure is imperfect
        """
        import re

        lines = text.split('\n')

        # Extract everything as-is
        data = {
            'diplomes': [],
            'competences': {
                'langages': [],
                'api_normes': [],
                'frameworks': [],
                'sgbdr': [],
                'modelisation': [],
                'ide': [],
                'serveurs_applications': [],
                'serveurs_web': [],
                'integration_continue': [],
                'gestion_versions': [],
                'tests_unitaires': [],
                'cloud': [],
                'systemes': [],
                'methodes_outils': []
            },
            'langues': [],
            'experiences': []
        }

        # Try to extract diplomas
        for i, line in enumerate(lines):
            year_match = re.search(r'\b(19|20)\d{2}\b', line)
            if year_match and any(kw in line.lower() for kw in ['master', 'licence', 'diplôme', 'école', 'université']):
                data['diplomes'].append({
                    'annee': year_match.group(0),
                    'diplome': line.strip(),
                    'etablissement': lines[i+1].strip() if i+1 < len(lines) else ''
                })

        # Extract ALL technologies mentioned
        tech_patterns = {
            'langages': r'\b(Java|Python|JavaScript|TypeScript|C\+\+|C#|PHP|Ruby|Go|Rust|Kotlin|Swift|Scala)\b',
            'frameworks': r'\b(Angular|React|Vue|Spring|Django|Flask|Express|Hibernate|JPA)\b',
            'sgbdr': r'\b(Oracle|MySQL|PostgreSQL|MongoDB|Redis|Cassandra|SQL Server)\b',
            'cloud': r'\b(AWS|Azure|GCP|Cloud|Kubernetes|Docker)\b',
        }

        for category, pattern in tech_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            data['competences'][category] = list(set(matches))

        # Extract experiences with ALL content
        exp_sections = re.split(r'(?i)(expérience|experience)', text)
        if len(exp_sections) > 1:
            exp_text = exp_sections[-1]
            # Split by company or date patterns
            companies = re.split(r'\n(?=\d{4}|\w+\s+\d{4})', exp_text)

            for company_block in companies:
                if len(company_block.strip()) > 20:  # Skip small chunks
                    data['experiences'].append({
                        'entreprise': 'ENTREPRISE',
                        'periode': '',
                        'poste': '',
                        'projets': [company_block.strip()],  # Keep ALL text
                        'realisations': company_block.split('\n'),  # All lines
                        'environnement': []
                    })

        return data
