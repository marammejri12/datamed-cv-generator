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
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')  # Modèle mis à jour!
            self.ai_enabled = True
            print("✅ Gemini AI activé - Extraction intelligente!")
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
        prompt = f"""
Tu es un expert en extraction de CVs. Ta mission: extraire **100% DU CONTENU** sans RIEN perdre.

RÈGLES CRITIQUES:
1. Lis TOUT le CV mot par mot
2. N'omets AUCUN détail - même le plus petit
3. Extrais CHAQUE diplôme, CHAQUE certification, CHAQUE compétence, CHAQUE expérience
4. Pour les expériences: extrais TOUTES les lignes de réalisations
5. Liste TOUTES les technologies mentionnées
6. CLASSIFIE intelligemment les compétences par catégories logiques

CV COMPLET À ANALYSER:
{text}

Retourne un JSON avec cette structure EXACTE:

{{
    "diplomes": [
        {{
            "annee": "année du diplôme",
            "diplome": "titre complet du diplôme",
            "etablissement": "nom complet de l'établissement avec ville et pays"
        }}
    ],
    "certifications": [
        {{
            "annee": "année de certification",
            "nom": "nom complet de la certification",
            "organisme": "organisme délivrant (AWS, Microsoft, Oracle, etc.)"
        }}
    ],
    "competences_groups": [
        {{
            "categorie": "nom de la catégorie (ex: Langages de Programmation, Big Data & Analytics, Cloud & DevOps, etc.)",
            "competences": ["liste des compétences dans cette catégorie"]
        }}
    ],
    "langues": [
        {{
            "langue": "nom de la langue",
            "niveau": "niveau (Professionnel, Bilingue, Courant, etc.)"
        }}
    ],
    "experiences": [
        {{
            "entreprise": "nom de l'entreprise (garder le vrai nom!)",
            "periode": "période exacte (ex: Mars 2022 - ce jour)",
            "poste": "titre exact du poste",
            "lieu": "ville et pays si mentionné",
            "projets": ["description COMPLÈTE de chaque projet"],
            "realisations": ["TOUTES les réalisations, tâches, responsabilités - une par ligne"],
            "environnement": ["TOUS les outils, technologies, frameworks utilisés"]
        }}
    ]
}}

INSTRUCTIONS ABSOLUES - NE SAUTE RIEN:

DIPLÔMES:
- Extrais CHAQUE diplôme mentionné avec année, titre complet et établissement
- Si plusieurs diplômes → tous dans le tableau
- Garde les noms exacts des écoles/universités

CERTIFICATIONS:
- Extrais TOUTES les certifications professionnelles (AWS, Azure, Google Cloud, Oracle, etc.)
- Avec année et organisme délivrant
- Si aucune certification trouvée → tableau vide []

COMPÉTENCES - CLASSIFICATION INTELLIGENTE:
- Cherche dans TOUT le CV: sections compétences, expériences, projets
- CLASSIFIE automatiquement chaque technologie/outil dans des groupes logiques
- Exemples de catégories intelligentes:
  * "Langages de Programmation": Java, Python, JavaScript, TypeScript, C++, C#, Scala, etc.
  * "Big Data & Analytics": Hadoop, Spark, Kafka, Hive, Elasticsearch, etc.
  * "Cloud & DevOps": AWS, Azure, GCP, Docker, Kubernetes, Terraform, Ansible, etc.
  * "Bases de Données": Oracle, PostgreSQL, MySQL, MongoDB, Redis, Cassandra, etc.
  * "Frameworks Backend": Spring Boot, Django, Flask, Express, Hibernate, etc.
  * "Frameworks Frontend": Angular, React, Vue, Next.js, etc.
  * "Data Architecture & Modeling": UML, Merise, Data Warehouse, ETL, Data Lake, etc.
  * "CI/CD & Build Tools": Jenkins, GitLab CI, Maven, Gradle, npm, etc.
  * "Testing & Quality": JUnit, Mockito, Selenium, SonarQube, etc.
  * "Méthodologies": Agile, Scrum, Kanban, DevOps, etc.
  * "Outils & IDE": IntelliJ, VSCode, Eclipse, Jira, Confluence, etc.
- Crée des catégories ADAPTÉES au profil du candidat
- Si profil Data → crée catégories: "Big Data", "Data Engineering", "Data Modeling"
- Si profil DevOps → crée catégories: "Cloud", "Containerization", "Orchestration"
- Si profil Web → crée catégories: "Frontend", "Backend", "Full Stack"

LANGUES:
- Si langues mentionnées: extrais toutes avec niveaux
- Si rien: mets au moins [{{"langue": "Français", "niveau": "Langue maternelle"}}]

EXPÉRIENCES:
- Pour CHAQUE expérience:
  * Nom entreprise (garder le vrai nom!)
  * Période exacte (format: "Mois Année - Mois Année")
  * Poste exact
  * Lieu si mentionné
  * Projets: description COMPLÈTE (2-3 lignes minimum)
  * Réalisations: CHAQUE bullet point = une entrée dans le tableau
  * Environnement: TOUTES les technos mentionnées pour ce poste

CRITIQUE: Si le CV mentionne 15 technologies, tu DOIS en extraire 15, pas 5!

Retourne UNIQUEMENT le JSON valide, rien d'autre.
"""

        try:
            response = self.model.generate_content(prompt)
            json_text = response.text.strip()

            # Clean markdown code blocks if present
            if json_text.startswith('```json'):
                json_text = json_text[7:]
            if json_text.startswith('```'):
                json_text = json_text[3:]
            if json_text.endswith('```'):
                json_text = json_text[:-3]

            json_text = json_text.strip()

            # Parse JSON
            data = json.loads(json_text)
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
