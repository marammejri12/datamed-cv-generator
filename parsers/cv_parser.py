"""
CV Parser with AI extraction
"""
import pdfplumber
import docx
import re
from typing import Dict, List, Optional
import json


class CVParser:
    """Extract structured information from CVs"""

    def __init__(self):
        self.extracted_data = {}

    def parse_cv(self, file_path: str) -> Dict:
        """
        Parse CV and extract structured information
        """
        # Extract text based on file type
        text = self._extract_text(file_path)

        # Parse structured data
        data = {
            'diplomes': self._extract_diplomes(text),
            'competences': self._extract_competences(text),
            'langues': self._extract_langues(text),
            'experiences': self._extract_experiences(text),
        }

        return data

    def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX"""
        if file_path.lower().endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        elif file_path.lower().endswith(('.docx', '.doc')):
            return self._extract_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please use PDF or DOCX.")

    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
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

    def _extract_diplomes(self, text: str) -> List[Dict]:
        """Extract diplomas/education"""
        diplomes = []

        # Keywords for education section
        education_keywords = [
            'formation', 'diplôme', 'education', 'étude', 'master',
            'licence', 'bachelor', 'doctorat', 'université', 'école'
        ]

        # Split text into lines
        lines = text.split('\n')

        # Find education section
        in_education = False
        current_diplome = {}

        for i, line in enumerate(lines):
            line_lower = line.lower().strip()

            # Check if we're in education section
            if any(keyword in line_lower for keyword in education_keywords):
                in_education = True

            # Check for end of education section
            if in_education and any(keyword in line_lower for keyword in ['expérience', 'compétence', 'projet']):
                in_education = False
                if current_diplome:
                    diplomes.append(current_diplome)
                    current_diplome = {}

            # Extract year
            year_match = re.search(r'\b(19|20)\d{2}\b', line)
            if year_match and in_education:
                if current_diplome:
                    diplomes.append(current_diplome)
                current_diplome = {
                    'annee': year_match.group(0),
                    'diplome': line.strip(),
                    'etablissement': ''
                }

            # Try to extract establishment
            if current_diplome and ('université' in line_lower or 'école' in line_lower or 'institut' in line_lower):
                current_diplome['etablissement'] = line.strip()

        if current_diplome:
            diplomes.append(current_diplome)

        # If no diplomes found, create a default entry
        if not diplomes:
            diplomes = [{
                'annee': '2019',
                'diplome': 'Master 2 - À extraire manuellement',
                'etablissement': 'Université - À extraire manuellement'
            }]

        return diplomes

    def _extract_competences(self, text: str) -> Dict:
        """Extract technical skills"""
        competences = {
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
        }

        # Programming languages
        lang_patterns = [
            r'\bJava\b', r'\bPython\b', r'\bJavaScript\b', r'\bTypeScript\b',
            r'\bC\+\+\b', r'\bC#\b', r'\bPHP\b', r'\bRuby\b', r'\bGo\b',
            r'\bHTML\b', r'\bCSS\b', r'\bSQL\b', r'\bReact\b', r'\bAngular\b',
            r'\bVue\.js\b', r'\bNode\.js\b'
        ]

        for pattern in lang_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['langages'].extend(list(set(matches)))

        # Frameworks
        framework_patterns = [
            r'\bSpring\b', r'\bAngular\b', r'\bReact\b', r'\bVue\b',
            r'\bDjango\b', r'\bFlask\b', r'\bExpress\b', r'\bStruts\b',
            r'\bHibernate\b', r'\bJPA\b', r'\bMVC\b', r'\bLog4J\b'
        ]

        for pattern in framework_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['frameworks'].extend(list(set(matches)))

        # Databases
        db_patterns = [
            r'\bOracle\b', r'\bMySQL\b', r'\bPostgreSQL\b', r'\bMongoDB\b',
            r'\bJDBC\b', r'\bSQL\b'
        ]

        for pattern in db_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['sgbdr'].extend(list(set(matches)))

        # IDE
        ide_patterns = [
            r'\bEclipse\b', r'\bIntelliJ\b', r'\bVSCode\b', r'\bNetBeans\b',
            r'\bIDEA\b', r'\bVisual Studio\b'
        ]

        for pattern in ide_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['ide'].extend(list(set(matches)))

        # CI/CD & Version Control
        ci_patterns = [r'\bJenkins\b', r'\bMaven\b', r'\bNexus\b', r'\bSonarQube\b']
        for pattern in ci_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['integration_continue'].extend(list(set(matches)))

        vcs_patterns = [r'\bGit\b', r'\bGitLab\b', r'\bBitbucket\b', r'\bSVN\b']
        for pattern in vcs_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['gestion_versions'].extend(list(set(matches)))

        # Web Servers
        web_patterns = [r'\bApache\b', r'\bTomcat\b', r'\bNginx\b']
        for pattern in web_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['serveurs_web'].extend(list(set(matches)))

        # Testing
        test_patterns = [r'\bJUnit\b', r'\bJasmin\b', r'\bMockito\b', r'\bSelenium\b']
        for pattern in test_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['tests_unitaires'].extend(list(set(matches)))

        # Cloud
        cloud_patterns = [r'\bAWS\b', r'\bAzure\b', r'\bGCP\b', r'\bCloud\b']
        for pattern in cloud_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['cloud'].extend(list(set(matches)))

        # Systems
        os_patterns = [
            r'\bLinux\b', r'\bWindows\b', r'\bUNIX\b', r'\bMac OS\b',
            r'\bRed Hat\b', r'\bUbuntu\b'
        ]
        for pattern in os_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['systemes'].extend(list(set(matches)))

        # Methodologies
        method_patterns = [
            r'\bAgile\b', r'\bScrum\b', r'\bDevOps\b', r'\bCI/CD\b',
            r'\bGED\b', r'\bKanban\b'
        ]
        for pattern in method_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['methodes_outils'].extend(list(set(matches)))

        # APIs
        api_patterns = [r'\bREST\b', r'\bSOAP\b', r'\bGraphQL\b', r'\bAPI\b']
        for pattern in api_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                competences['api_normes'].extend(list(set(matches)))

        # Remove duplicates
        for key in competences:
            competences[key] = list(set(competences[key]))

        return competences

    def _extract_langues(self, text: str) -> List[Dict]:
        """Extract languages"""
        langues = []

        # Common languages and levels
        language_patterns = {
            'Anglais': r'\b(anglais|english)\b',
            'Français': r'\b(français|french)\b',
            'Arabe': r'\b(arabe|arabic)\b',
            'Espagnol': r'\b(espagnol|spanish)\b',
            'Allemand': r'\b(allemand|german)\b'
        }

        level_patterns = {
            'Professionnel': r'\b(professionnel|professional|fluent|courant)\b',
            'Bilingue': r'\b(bilingue|bilingual|natif|native)\b',
            'Intermédiaire': r'\b(intermédiaire|intermediate)\b',
            'Basique': r'\b(basique|basic|débutant)\b'
        }

        text_lower = text.lower()

        for lang, pattern in language_patterns.items():
            if re.search(pattern, text_lower):
                # Try to find level
                level = 'Professionnel'
                for lvl, lvl_pattern in level_patterns.items():
                    if re.search(lvl_pattern, text_lower):
                        level = lvl
                        break

                langues.append({
                    'langue': lang,
                    'niveau': level
                })

        # Default if no language found
        if not langues:
            langues = [{'langue': 'Anglais', 'niveau': 'Professionnel'}]

        return langues

    def _extract_experiences(self, text: str) -> List[Dict]:
        """Extract professional experiences"""
        experiences = []

        # Keywords for experience section
        exp_keywords = ['expérience', 'experience', 'projet', 'mission']

        lines = text.split('\n')
        in_experience = False
        current_exp = {}

        for line in lines:
            line_lower = line.lower().strip()

            # Check if we're in experience section
            if any(keyword in line_lower for keyword in exp_keywords):
                in_experience = True

            # Extract company and dates
            date_pattern = r'\b(19|20)\d{2}\b'
            dates = re.findall(date_pattern, line)

            if dates and in_experience:
                if current_exp:
                    experiences.append(current_exp)

                current_exp = {
                    'entreprise': 'ENTREPRISE',
                    'periode': f"{dates[0]} - " + (dates[1] if len(dates) > 1 else "ce jour"),
                    'poste': line.strip(),
                    'projets': [],
                    'realisations': [],
                    'environnement': []
                }

            # Extract project info
            if current_exp and ('projet' in line_lower or 'mission' in line_lower):
                if 'projets' not in current_exp:
                    current_exp['projets'] = []
                current_exp['projets'].append(line.strip())

        if current_exp:
            experiences.append(current_exp)

        # Create default experience if none found
        if not experiences:
            experiences = [{
                'entreprise': 'ENTREPRISE',
                'periode': 'Mars 2022 - ce jour',
                'poste': 'Développeur Full stack Java J2EE Angular',
                'projets': ['Projet : À extraire du CV original'],
                'realisations': ['Réalisations à extraire'],
                'environnement': []
            }]

        return experiences
