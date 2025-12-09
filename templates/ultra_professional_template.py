"""
Ultra Professional CV Template
Magnifique design avec extraction complète du contenu
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


class UltraProfessionalTemplate:
    """Template ultra professionnel avec design magnifique"""

    def __init__(self, output_path: str):
        self.output_path = output_path
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()

        # Navy blue color scheme - MAGNIFIQUE!
        self.navy_dark = colors.HexColor('#0f172a')      # Très foncé
        self.navy_main = colors.HexColor('#1e293b')      # Principal
        self.navy_light = colors.HexColor('#334155')     # Clair
        self.blue_accent = colors.HexColor('#3b82f6')    # Accent
        self.gray_text = colors.HexColor('#64748b')      # Texte gris
        self.gray_bg = colors.HexColor('#f1f5f9')        # Fond gris

        self._setup_styles()

    def _setup_styles(self):
        """Setup custom styles"""
        # Title
        self.title_style = ParagraphStyle(
            'Title',
            fontSize=26,
            textColor=self.navy_main,
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=30
        )

        # Subtitle
        self.subtitle_style = ParagraphStyle(
            'Subtitle',
            fontSize=11,
            textColor=self.gray_text,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica'
        )

        # Section header
        self.section_style = ParagraphStyle(
            'SectionHeader',
            fontSize=13,
            textColor=colors.white,
            spaceAfter=12,
            spaceBefore=16,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            leftIndent=10,
            leading=16
        )

        # Normal
        self.normal_style = ParagraphStyle(
            'Normal',
            fontSize=9,
            textColor=self.gray_text,
            fontName='Helvetica',
            leading=13,
            spaceAfter=4
        )

        # Bold
        self.bold_style = ParagraphStyle(
            'Bold',
            fontSize=9,
            textColor=self.navy_main,
            fontName='Helvetica-Bold'
        )

        # Large bold
        self.large_bold_style = ParagraphStyle(
            'LargeBold',
            fontSize=10,
            textColor=self.navy_main,
            fontName='Helvetica-Bold',
            spaceAfter=4
        )

    def generate(self, data: dict):
        """Generate CV"""
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            rightMargin=1.8*cm,
            leftMargin=1.8*cm,
            topMargin=1.5*cm,
            bottomMargin=1.8*cm
        )

        story = []

        # Logo
        story.extend(self._create_logo())

        # Title
        story.append(Paragraph("Nom & Prénom", self.title_style))
        story.append(Paragraph("Consultant IT", self.subtitle_style))
        story.append(Spacer(1, 0.4*cm))

        # Diplomes
        if data.get('diplomes'):
            story.extend(self._create_diplomes(data['diplomes']))

        # Competences
        if data.get('competences'):
            story.extend(self._create_competences(data['competences']))

        # Langues
        if data.get('langues'):
            story.extend(self._create_langues(data['langues']))

        # Page break
        story.append(PageBreak())
        story.extend(self._create_logo())
        story.append(Spacer(1, 0.3*cm))

        # Experiences
        if data.get('experiences'):
            story.extend(self._create_experiences(data['experiences']))

        # Footer
        story.append(Spacer(1, 0.8*cm))
        footer = Paragraph(
            '<font size=9 color="#94a3b8">www.consultingdatamed.com</font>',
            ParagraphStyle('Footer', alignment=TA_CENTER)
        )
        story.append(footer)

        doc.build(story)

    def _create_logo(self):
        """Logo DataMed"""
        elements = []
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image', 'datamed_consulting_logo.png')

        if os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=4.5*cm, height=2.2*cm)
                elements.append(logo)
                elements.append(Spacer(1, 0.4*cm))
            except:
                pass

        return elements

    def _create_section_header(self, title: str):
        """Beautiful section header"""
        para = Paragraph(f" {title}", self.section_style)
        table = Table([[para]], colWidths=[17.4*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.navy_main),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ]))
        return table

    def _create_diplomes(self, diplomes: list):
        """Diplomas section"""
        elements = []
        elements.append(self._create_section_header("DIPLÔMES & FORMATIONS"))
        elements.append(Spacer(1, 0.3*cm))

        for dip in diplomes:
            annee = dip.get('annee', '')
            diplome = dip.get('diplome', '')
            etablissement = dip.get('etablissement', '')

            data = [[
                Paragraph(f'<b><font color="#1e293b" size=11>{annee}</font></b>', self.bold_style),
                Paragraph(f'<b>{diplome}</b><br/><font size=8 color="#64748b">{etablissement}</font>', self.normal_style)
            ]]

            table = Table(data, colWidths=[2.5*cm, 14.9*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('BOX', (0, 0), (-1, -1), 0.5, self.gray_bg),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.15*cm))

        elements.append(Spacer(1, 0.2*cm))
        return elements

    def _create_competences(self, competences: dict):
        """Competences section - TOUTES les catégories!"""
        elements = []
        elements.append(self._create_section_header("COMPÉTENCES TECHNIQUES"))
        elements.append(Spacer(1, 0.3*cm))

        categories = [
            ('Langages de Programmation', 'langages'),
            ('API & Normes', 'api_normes'),
            ('Frameworks & Librairies', 'frameworks'),
            ('Bases de Données', 'sgbdr'),
            ('Modélisation', 'modelisation'),
            ('IDE & Environnements', 'ide'),
            ("Serveurs d'Applications", 'serveurs_applications'),
            ('Serveurs Web', 'serveurs_web'),
            ('Intégration Continue', 'integration_continue'),
            ('Gestion de Versions', 'gestion_versions'),
            ('Tests & Qualité', 'tests_unitaires'),
            ('Cloud & Infrastructure', 'cloud'),
            ('Systèmes d\'Exploitation', 'systemes'),
            ('Méthodologies & Outils', 'methodes_outils'),
        ]

        rows = []
        for label, key in categories:
            skills = competences.get(key, [])
            skill_text = ', '.join(skills) if skills else '-'

            label_para = Paragraph(f'<b><font color="#1e293b">{label}</font></b>', self.bold_style)
            skill_para = Paragraph(skill_text, self.normal_style)
            rows.append([label_para, skill_para])

        table = Table(rows, colWidths=[5.8*cm, 11.6*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.gray_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, self.gray_bg),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*cm))
        return elements

    def _create_langues(self, langues: list):
        """Languages section"""
        elements = []
        elements.append(self._create_section_header("LANGUES"))
        elements.append(Spacer(1, 0.3*cm))

        rows = []
        for langue in langues:
            nom = langue.get('langue', '')
            niveau = langue.get('niveau', '')

            nom_para = Paragraph(f'<b><font color="#1e293b">{nom}</font></b>', self.bold_style)
            niveau_para = Paragraph(niveau, self.normal_style)
            rows.append([nom_para, niveau_para])

        table = Table(rows, colWidths=[5.8*cm, 11.6*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.gray_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, self.gray_bg),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*cm))
        return elements

    def _create_experiences(self, experiences: list):
        """Experiences - TOUT le contenu!"""
        elements = []
        elements.append(self._create_section_header("EXPÉRIENCES PROFESSIONNELLES"))
        elements.append(Spacer(1, 0.4*cm))

        for idx, exp in enumerate(experiences):
            entreprise = exp.get('entreprise', '')
            periode = exp.get('periode', '')
            poste = exp.get('poste', '')
            lieu = exp.get('lieu', '')

            # Header
            header_data = [[
                Paragraph(f'<b><font color="white" size=11>{entreprise}</font></b>',
                         ParagraphStyle('Company', fontName='Helvetica-Bold', textColor=colors.white)),
                Paragraph(f'<font color="white" size=10>{periode}</font>',
                         ParagraphStyle('Period', alignment=TA_RIGHT, textColor=colors.white))
            ]]

            header_table = Table(header_data, colWidths=[10.5*cm, 6.9*cm])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.blue_accent),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(header_table)

            # Poste & Lieu
            if poste:
                elements.append(Spacer(1, 0.2*cm))
                elements.append(Paragraph(
                    f'<b><font color="#1e293b" size=10>{poste}</font></b>',
                    self.large_bold_style
                ))
            if lieu:
                elements.append(Paragraph(
                    f'<font size=9 color="#64748b"><i>{lieu}</i></font>',
                    self.normal_style
                ))

            # Projets
            if exp.get('projets'):
                elements.append(Spacer(1, 0.25*cm))
                for projet in exp['projets']:
                    elements.append(Paragraph(
                        f'<b>Projet:</b> {projet}',
                        self.normal_style
                    ))

            # Réalisations
            if exp.get('realisations'):
                elements.append(Spacer(1, 0.25*cm))
                elements.append(Paragraph('<b>Réalisations:</b>', self.bold_style))
                elements.append(Spacer(1, 0.1*cm))
                for real in exp['realisations']:
                    if real.strip():  # Only non-empty
                        elements.append(Paragraph(
                            f'• {real}',
                            ParagraphStyle('Bullet', fontSize=9, leftIndent=15, textColor=self.gray_text, leading=13)
                        ))

            # Environnement
            if exp.get('environnement'):
                elements.append(Spacer(1, 0.25*cm))
                env_text = ', '.join(exp['environnement']) if isinstance(exp['environnement'], list) else str(exp['environnement'])
                elements.append(Paragraph(
                    f'<b>Environnement technique:</b> {env_text}',
                    self.normal_style
                ))

            # Spacing
            if idx < len(experiences) - 1:
                elements.append(Spacer(1, 0.5*cm))

        return elements
