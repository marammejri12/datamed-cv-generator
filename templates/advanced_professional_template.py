"""
Advanced Professional CV Template
Beautiful design with dynamic AI-classified skills
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


class AdvancedProfessionalTemplate:
    """Advanced professional template with AI-classified skills"""

    def __init__(self, output_path: str):
        self.output_path = output_path
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()

        # DataMed color palette - Navy Blue Professional
        self.primary_blue = colors.HexColor('#1a365d')      # Navy blue (DataMed)
        self.dark_blue = colors.HexColor('#0f2847')         # Dark navy
        self.light_blue = colors.HexColor('#e6f2ff')        # Light blue background
        self.text_dark = colors.HexColor('#1f2937')         # Dark text
        self.text_gray = colors.HexColor('#6b7280')         # Gray text
        self.bg_light = colors.HexColor('#f8fafc')          # Light background
        self.accent_green = colors.HexColor('#2c7a7b')      # Teal accent

        self._setup_styles()

    def _setup_styles(self):
        """Setup custom styles"""
        # Title
        self.title_style = ParagraphStyle(
            'Title',
            fontSize=28,
            textColor=self.dark_blue,  # Navy blue for title
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=32
        )

        # Subtitle
        self.subtitle_style = ParagraphStyle(
            'Subtitle',
            fontSize=12,
            textColor=self.text_gray,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica'
        )

        # Section number
        self.section_number_style = ParagraphStyle(
            'SectionNumber',
            fontSize=16,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        )

        # Section header
        self.section_style = ParagraphStyle(
            'SectionHeader',
            fontSize=14,
            textColor=colors.white,
            spaceAfter=12,
            spaceBefore=16,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            leftIndent=10,
            leading=18
        )

        # Normal
        self.normal_style = ParagraphStyle(
            'Normal',
            fontSize=9.5,
            textColor=self.text_gray,
            fontName='Helvetica',
            leading=14,
            spaceAfter=4
        )

        # Bold
        self.bold_style = ParagraphStyle(
            'Bold',
            fontSize=10,
            textColor=self.text_dark,
            fontName='Helvetica-Bold',
            leading=13
        )

        # Large bold
        self.large_bold_style = ParagraphStyle(
            'LargeBold',
            fontSize=11,
            textColor=self.text_dark,
            fontName='Helvetica-Bold',
            spaceAfter=5
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
        story.append(Spacer(1, 0.5*cm))

        # Section counter
        section_num = 1

        # 1. FORMATION
        if data.get('diplomes'):
            story.extend(self._create_section_header(section_num, "FORMATION"))
            story.extend(self._create_diplomes(data['diplomes']))
            section_num += 1

        # 2. CERTIFICATIONS
        if data.get('certifications'):
            story.extend(self._create_section_header(section_num, "CERTIFICATIONS"))
            story.extend(self._create_certifications(data['certifications']))
            section_num += 1

        # 3. COMPÉTENCES (Dynamic AI-classified)
        if data.get('competences_groups'):
            story.extend(self._create_section_header(section_num, "COMPÉTENCES TECHNIQUES"))
            story.extend(self._create_dynamic_competences(data['competences_groups']))
            section_num += 1

        # 4. LANGUES
        if data.get('langues'):
            story.extend(self._create_section_header(section_num, "LANGUES"))
            story.extend(self._create_langues(data['langues']))
            section_num += 1

        # Page break before experiences
        story.append(PageBreak())
        story.extend(self._create_logo())
        story.append(Spacer(1, 0.4*cm))

        # 5. EXPÉRIENCES
        if data.get('experiences'):
            story.extend(self._create_section_header(section_num, "EXPÉRIENCES PROFESSIONNELLES"))
            story.extend(self._create_experiences(data['experiences']))

        # Footer
        story.append(Spacer(1, 1*cm))
        footer = Paragraph(
            '<font size=10 color="#6b7280">www.consultingdatamed.com</font>',
            ParagraphStyle('Footer', alignment=TA_CENTER)
        )
        story.append(footer)

        doc.build(story)

    def _create_logo(self):
        """Logo DataMed"""
        elements = []
        # Try multiple possible logo paths and formats
        base_path = os.path.dirname(os.path.dirname(__file__))
        possible_paths = [
            os.path.join(base_path, 'image', 'datamed_consulting_logo.jfif'),
            os.path.join(base_path, 'image', 'datamed_consulting_logo.png'),
            os.path.join(base_path, 'image', 'LO-removebg-preview.png'),
            os.path.join(base_path, 'image', 'datamed_consulting_logo.jpg'),
        ]

        for logo_path in possible_paths:
            if os.path.exists(logo_path):
                try:
                    # Try to load and add logo
                    logo = Image(logo_path, width=5*cm, height=2.5*cm)
                    elements.append(logo)
                    elements.append(Spacer(1, 0.5*cm))
                    print(f"✓ Logo chargé: {logo_path}")
                    break
                except Exception as e:
                    print(f"⚠ Erreur chargement logo {logo_path}: {e}")
                    continue

        if not elements:
            print("⚠ Aucun logo trouvé dans le dossier image/")

        return elements

    def _create_section_header(self, number: int, title: str):
        """Beautiful numbered section header"""
        elements = []

        # Create header with number
        number_cell = Paragraph(f"<b>{number}</b>", self.section_number_style)
        title_cell = Paragraph(f"<b>{title}</b>", self.section_style)

        data = [[number_cell, title_cell]]
        table = Table(data, colWidths=[1.2*cm, 16.2*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.dark_blue),
            ('BACKGROUND', (1, 0), (1, 0), self.primary_blue),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.3*cm))
        return elements

    def _create_diplomes(self, diplomes: list):
        """Diplomas section"""
        elements = []

        for dip in diplomes:
            annee = dip.get('annee', '')
            diplome = dip.get('diplome', '')
            etablissement = dip.get('etablissement', '')

            data = [[
                Paragraph(f'<b><font color="#1a365d" size=12>{annee}</font></b>', self.bold_style),
                Paragraph(f'<b>{diplome}</b><br/><font size=9 color="#6b7280">{etablissement}</font>', self.normal_style)
            ]]

            table = Table(data, colWidths=[2.8*cm, 14.6*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('BOX', (0, 0), (-1, -1), 1, self.light_blue),
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

    def _create_certifications(self, certifications: list):
        """Certifications section"""
        elements = []

        for cert in certifications:
            annee = cert.get('annee', '')
            nom = cert.get('nom', '')
            organisme = cert.get('organisme', '')

            data = [[
                Paragraph(f'<b><font color="#10b981" size=12>{annee}</font></b>', self.bold_style),
                Paragraph(f'<b>{nom}</b><br/><font size=9 color="#6b7280">{organisme}</font>', self.normal_style)
            ]]

            table = Table(data, colWidths=[2.8*cm, 14.6*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1fae5')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.2*cm))

        elements.append(Spacer(1, 0.3*cm))
        return elements

    def _create_dynamic_competences(self, competences_groups: list):
        """Dynamic AI-classified competences"""
        elements = []

        for group in competences_groups:
            categorie = group.get('categorie', '')
            competences = group.get('competences', [])

            if not competences:
                continue

            skill_text = ' • '.join(competences)

            # Create group
            label_para = Paragraph(f'<b>{categorie}</b>', self.bold_style)
            skill_para = Paragraph(skill_text, self.normal_style)

            data = [[label_para, skill_para]]
            table = Table(data, colWidths=[5.5*cm, 11.9*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), self.light_blue),
                ('BACKGROUND', (1, 0), (1, 0), colors.white),
                ('BOX', (0, 0), (-1, -1), 1, self.light_blue),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.15*cm))

        elements.append(Spacer(1, 0.3*cm))
        return elements

    def _create_langues(self, langues: list):
        """Languages section"""
        elements = []

        rows = []
        for langue in langues:
            nom = langue.get('langue', '')
            niveau = langue.get('niveau', '')

            nom_para = Paragraph(f'<b>{nom}</b>', self.bold_style)
            niveau_para = Paragraph(niveau, self.normal_style)
            rows.append([nom_para, niveau_para])

        table = Table(rows, colWidths=[5.5*cm, 11.9*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.light_blue),
            ('BOX', (0, 0), (-1, -1), 1, self.light_blue),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*cm))
        return elements

    def _create_experiences(self, experiences: list):
        """Experiences - Complete extraction!"""
        elements = []

        for idx, exp in enumerate(experiences):
            entreprise = exp.get('entreprise', '')
            periode = exp.get('periode', '')
            poste = exp.get('poste', '')
            lieu = exp.get('lieu', '')

            # Header with gradient-like effect
            header_data = [[
                Paragraph(f'<b><font color="white" size=12>{entreprise}</font></b>',
                         ParagraphStyle('Company', fontName='Helvetica-Bold', textColor=colors.white)),
                Paragraph(f'<font color="white" size=11>{periode}</font>',
                         ParagraphStyle('Period', alignment=TA_RIGHT, textColor=colors.white))
            ]]

            header_table = Table(header_data, colWidths=[10.5*cm, 6.9*cm])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.primary_blue),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(header_table)

            # Content box
            content_elements = []

            # Poste & Lieu
            if poste:
                content_elements.append(Paragraph(
                    f'<b><font color="#1f2937" size=11>{poste}</font></b>',
                    self.large_bold_style
                ))
            if lieu:
                content_elements.append(Paragraph(
                    f'<font size=9 color="#6b7280"><i>📍 {lieu}</i></font>',
                    self.normal_style
                ))
                content_elements.append(Spacer(1, 0.2*cm))

            # Projets
            if exp.get('projets'):
                content_elements.append(Paragraph('<b>Projets:</b>', self.bold_style))
                content_elements.append(Spacer(1, 0.1*cm))
                for projet in exp['projets']:
                    if projet.strip():
                        content_elements.append(Paragraph(
                            f'{projet}',
                            self.normal_style
                        ))
                content_elements.append(Spacer(1, 0.2*cm))

            # Réalisations
            if exp.get('realisations'):
                content_elements.append(Paragraph('<b>Réalisations:</b>', self.bold_style))
                content_elements.append(Spacer(1, 0.1*cm))
                for real in exp['realisations']:
                    if real.strip():
                        content_elements.append(Paragraph(
                            f'✓ {real}',
                            ParagraphStyle('Bullet', fontSize=9.5, leftIndent=15, textColor=self.text_gray, leading=14, spaceAfter=3)
                        ))
                content_elements.append(Spacer(1, 0.2*cm))

            # Environnement
            if exp.get('environnement'):
                env_text = ' • '.join(exp['environnement']) if isinstance(exp['environnement'], list) else str(exp['environnement'])
                content_elements.append(Paragraph(
                    f'<b>Environnement technique:</b> {env_text}',
                    self.normal_style
                ))

            # Wrap content in box
            content_box = Table([[content_elements]], colWidths=[17.4*cm])
            content_box.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('BOX', (0, 0), (-1, -1), 1, self.light_blue),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Allow content to flow
            ]))
            elements.append(content_box)

            # Spacing
            if idx < len(experiences) - 1:
                elements.append(Spacer(1, 0.5*cm))

        return elements
