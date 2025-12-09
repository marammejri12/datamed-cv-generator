"""
Professional CV Template - Navy Blue Design
Beautiful, structured, and comprehensive CV generation
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import os


class ProfessionalTemplate:
    """Generate beautiful professional CVs with navy blue design"""

    def __init__(self, output_path: str):
        self.output_path = output_path
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()

        # Navy blue color scheme
        self.navy_blue = colors.HexColor('#1a365d')
        self.light_blue = colors.HexColor('#2563eb')
        self.lighter_blue = colors.HexColor('#3b82f6')
        self.gray = colors.HexColor('#4a5568')
        self.light_gray = colors.HexColor('#e2e8f0')

        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'Title',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=self.navy_blue,
            spaceAfter=8,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'Subtitle',
            fontSize=12,
            textColor=self.gray,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica'
        )

        # Section header style (navy blue background)
        self.section_header_style = ParagraphStyle(
            'SectionHeader',
            fontSize=14,
            textColor=colors.white,
            spaceAfter=10,
            spaceBefore=15,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            leading=18
        )

        # Subsection style
        self.subsection_style = ParagraphStyle(
            'Subsection',
            fontSize=11,
            textColor=self.navy_blue,
            spaceAfter=5,
            fontName='Helvetica-Bold'
        )

        # Normal text
        self.normal_style = ParagraphStyle(
            'Normal',
            fontSize=10,
            textColor=self.gray,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=14
        )

        # Bold text
        self.bold_style = ParagraphStyle(
            'Bold',
            fontSize=10,
            textColor=self.navy_blue,
            fontName='Helvetica-Bold'
        )

        # Bullet point style
        self.bullet_style = ParagraphStyle(
            'Bullet',
            fontSize=10,
            textColor=self.gray,
            leftIndent=20,
            fontName='Helvetica',
            leading=14
        )

    def generate(self, data: dict):
        """Generate complete CV PDF"""
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=1.5*cm,
            bottomMargin=2*cm
        )

        story = []

        # Header with logo
        story.extend(self._create_header())

        # Title
        story.append(Paragraph("Nom & Prénom", self.title_style))
        story.append(Paragraph("Profil Professionnel", self.subtitle_style))
        story.append(Spacer(1, 0.5*cm))

        # Diplomes
        if data.get('diplomes'):
            story.extend(self._create_diplomes_section(data['diplomes']))

        # Competences
        if data.get('competences'):
            story.extend(self._create_competences_section(data['competences']))

        # Langues
        if data.get('langues'):
            story.extend(self._create_langues_section(data['langues']))

        # Page break before experiences
        story.append(PageBreak())

        # Header on second page
        story.extend(self._create_header())
        story.append(Spacer(1, 0.5*cm))

        # Experiences
        if data.get('experiences'):
            story.extend(self._create_experiences_section(data['experiences']))

        # Footer
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph(
            '<font size=9 color="#718096">www.consultingdatamed.com</font>',
            ParagraphStyle('Footer', alignment=TA_CENTER)
        ))

        # Build PDF
        doc.build(story)

    def _create_header(self):
        """Create header with DataMed logo"""
        elements = []

        # Try to load logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image', 'datamed_consulting_logo.png')

        if os.path.exists(logo_path):
            try:
                logo_img = Image(logo_path, width=4*cm, height=2*cm)
                logo_table = Table([[logo_img]], colWidths=[17*cm])
                logo_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                elements.append(logo_table)
                elements.append(Spacer(1, 0.3*cm))
            except:
                # Fallback
                logo_text = Paragraph(
                    '<font size=16 color="#1a365d"><b>DATAMED</b></font><br/><font size=10 color="#4a5568">consulting</font>',
                    ParagraphStyle('Logo', alignment=TA_LEFT)
                )
                elements.append(logo_text)
                elements.append(Spacer(1, 0.3*cm))
        else:
            # Text logo fallback
            logo_text = Paragraph(
                '<font size=16 color="#1a365d"><b>DATAMED</b></font><br/><font size=10 color="#4a5568">consulting</font>',
                ParagraphStyle('Logo', alignment=TA_LEFT)
            )
            elements.append(logo_text)
            elements.append(Spacer(1, 0.3*cm))

        return elements

    def _create_section_header(self, title: str):
        """Create beautiful section header with navy blue background"""
        header_para = Paragraph(f"  {title}", self.section_header_style)
        header_table = Table([[header_para]], colWidths=[17*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.navy_blue),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('ROUNDEDCORNERS', [5, 5, 5, 5]),
        ]))
        return header_table

    def _create_diplomes_section(self, diplomes: list):
        """Create diplomas section with beautiful formatting"""
        elements = []

        # Section header
        elements.append(self._create_section_header("DIPLÔMES & FORMATIONS"))
        elements.append(Spacer(1, 0.4*cm))

        for diplome in diplomes:
            # Year in bold navy blue
            annee = diplome.get('annee', '')
            diplome_text = diplome.get('diplome', '')
            etablissement = diplome.get('etablissement', '')

            # Create a nice box for each diploma
            data = [[
                Paragraph(f'<b><font color="#1a365d" size=12>{annee}</font></b>', self.bold_style),
                Paragraph(f'<b>{diplome_text}</b><br/><font size=9 color="#718096">{etablissement}</font>', self.normal_style)
            ]]

            diploma_table = Table(data, colWidths=[2.5*cm, 14.5*cm])
            diploma_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('BOX', (0, 0), (-1, -1), 1, self.light_gray),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))

            elements.append(diploma_table)
            elements.append(Spacer(1, 0.2*cm))

        return elements

    def _create_competences_section(self, competences: dict):
        """Create comprehensive skills section"""
        elements = []

        # Section header
        elements.append(self._create_section_header("COMPÉTENCES TECHNIQUES"))
        elements.append(Spacer(1, 0.4*cm))

        # Mapping of categories
        categories = [
            ('Langages de Programmation', 'langages'),
            ('API & Normes', 'api_normes'),
            ('Frameworks', 'frameworks'),
            ('Bases de Données (SGBDR)', 'sgbdr'),
            ('Modélisation', 'modelisation'),
            ('IDE & Environnements', 'ide'),
            ("Serveurs d'Applications", 'serveurs_applications'),
            ('Serveurs Web', 'serveurs_web'),
            ('Intégration Continue (CI/CD)', 'integration_continue'),
            ('Gestion de Versions', 'gestion_versions'),
            ('Tests Unitaires', 'tests_unitaires'),
            ('Cloud & Infrastructure', 'cloud'),
            ('Systèmes d\'Exploitation', 'systemes'),
            ('Méthodologies & Outils', 'methodes_outils'),
        ]

        table_data = []

        for label, key in categories:
            skills = competences.get(key, [])
            if skills:
                skill_text = ', '.join(skills) if isinstance(skills, list) else str(skills)
            else:
                skill_text = '-'

            # Create row with nice formatting
            label_para = Paragraph(f'<b><font color="#1a365d">{label}</font></b>', self.bold_style)
            skill_para = Paragraph(skill_text, self.normal_style)
            table_data.append([label_para, skill_para])

        if table_data:
            comp_table = Table(table_data, colWidths=[5.5*cm, 11.5*cm])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
                ('BOX', (0, 0), (-1, -1), 1, self.light_gray),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(comp_table)

        elements.append(Spacer(1, 0.3*cm))
        return elements

    def _create_langues_section(self, langues: list):
        """Create languages section"""
        elements = []

        # Section header
        elements.append(self._create_section_header("LANGUES"))
        elements.append(Spacer(1, 0.4*cm))

        table_data = []
        for langue in langues:
            lang_name = langue.get('langue', '')
            niveau = langue.get('niveau', '')

            lang_para = Paragraph(f'<b><font color="#1a365d">{lang_name}</font></b>', self.bold_style)
            niveau_para = Paragraph(niveau, self.normal_style)
            table_data.append([lang_para, niveau_para])

        if table_data:
            lang_table = Table(table_data, colWidths=[5.5*cm, 11.5*cm])
            lang_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
                ('BOX', (0, 0), (-1, -1), 1, self.light_gray),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(lang_table)

        elements.append(Spacer(1, 0.3*cm))
        return elements

    def _create_experiences_section(self, experiences: list):
        """Create professional experiences section with beautiful design"""
        elements = []

        # Section header
        elements.append(self._create_section_header("EXPÉRIENCES PROFESSIONNELLES"))
        elements.append(Spacer(1, 0.4*cm))

        for idx, exp in enumerate(experiences):
            # Company header with light blue background
            entreprise = exp.get('entreprise', 'ENTREPRISE')
            periode = exp.get('periode', '')
            poste = exp.get('poste', '')

            # Header row
            header_data = [[
                Paragraph(f'<b><font color="white" size=11>{entreprise}</font></b>',
                         ParagraphStyle('CompanyName', fontName='Helvetica-Bold', textColor=colors.white)),
                Paragraph(f'<font color="white" size=10>{periode}</font>',
                         ParagraphStyle('Period', alignment=TA_RIGHT, textColor=colors.white))
            ]]

            header_table = Table(header_data, colWidths=[11*cm, 6*cm])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.light_blue),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(header_table)

            # Position
            if poste:
                elements.append(Spacer(1, 0.2*cm))
                elements.append(Paragraph(
                    f'<b><font color="#1a365d" size=11>{poste}</font></b>',
                    self.subsection_style
                ))

            # Projects
            if exp.get('projets'):
                elements.append(Spacer(1, 0.2*cm))
                for projet in exp['projets']:
                    elements.append(Paragraph(
                        f'<b>Projet :</b> {projet}',
                        self.normal_style
                    ))

            # Realizations
            if exp.get('realisations'):
                elements.append(Spacer(1, 0.2*cm))
                elements.append(Paragraph('<b>Réalisations :</b>', self.bold_style))
                for real in exp['realisations']:
                    elements.append(Paragraph(
                        f'• {real}',
                        self.bullet_style
                    ))

            # Technical environment
            if exp.get('environnement'):
                elements.append(Spacer(1, 0.2*cm))
                env_text = ', '.join(exp['environnement']) if isinstance(exp['environnement'], list) else str(exp['environnement'])
                elements.append(Paragraph(
                    f'<b>Environnement technique :</b> {env_text}',
                    self.normal_style
                ))

            # Spacing between experiences
            if idx < len(experiences) - 1:
                elements.append(Spacer(1, 0.5*cm))

        return elements
