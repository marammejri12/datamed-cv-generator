"""
DataMed CV Template Generator
Creates professional CVs with exact DataMed styling
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import os


class DataMedTemplate:
    """Generate CV in DataMed format with professional styling"""

    def __init__(self, output_path: str):
        self.output_path = output_path
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a5f'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        # Profile link style
        self.profile_style = ParagraphStyle(
            'ProfileStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#3b82f6'),
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica'
        )

        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=11,
            textColor=colors.white,
            spaceAfter=6,
            spaceBefore=12,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#808080')
        )

        # Normal text style
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )

        # Bold style for table headers
        self.bold_style = ParagraphStyle(
            'BoldStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Bold'
        )

    def generate(self, data: dict):
        """Generate complete CV PDF"""
        # Create PDF document
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # Build content
        story = []

        # Add logo and header
        story.extend(self._create_header())

        # Add title with professional title
        story.append(Paragraph("Nom & Prénom", self.title_style))

        # Professional title from CV data
        titre_pro = data.get('titre_professionnel', 'Consultant IT')
        story.append(Paragraph(titre_pro, self.profile_style))
        story.append(Spacer(1, 0.3*cm))

        # Add Diplomes & Formations
        story.extend(self._create_diplomes_section(data.get('diplomes', [])))

        # Add Certifications (if any)
        if data.get('certifications'):
            story.extend(self._create_certifications_section(data.get('certifications', [])))

        # Add Competences Techniques (grouped by AI)
        story.extend(self._create_competences_section(data.get('competences_groups', [])))

        # Add Languages
        story.extend(self._create_langues_section(data.get('langues', [])))

        # Page break before experiences
        story.append(PageBreak())

        # Add header on second page
        story.extend(self._create_header())

        # Add Experiences
        story.extend(self._create_experiences_section(data.get('experiences', [])))

        # Build PDF
        doc.build(story)

    def _create_header(self):
        """Create header with logo"""
        elements = []

        # Try to load DataMed logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image', 'datamed_consulting_logo.png')

        if os.path.exists(logo_path):
            # Use actual logo image
            try:
                logo_img = Image(logo_path, width=3*cm, height=1.5*cm)
                logo_table = Table([[logo_img]], colWidths=[4*cm])
                logo_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                elements.append(logo_table)
            except:
                # Fallback to text if image fails
                logo_text = Paragraph(
                    '<font size=14 color="#1e3a5f"><b>DATAMED</b></font><br/><font size=8>consulting</font>',
                    ParagraphStyle('Logo', alignment=TA_LEFT, fontSize=10)
                )
                logo_table = Table([[logo_text]], colWidths=[4*cm])
                logo_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                elements.append(logo_table)
        else:
            # Fallback to text logo
            logo_text = Paragraph(
                '<font size=14 color="#1e3a5f"><b>DATAMED</b></font><br/><font size=8>consulting</font>',
                ParagraphStyle('Logo', alignment=TA_LEFT, fontSize=10)
            )
            logo_table = Table([[logo_text]], colWidths=[4*cm])
            logo_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(logo_table)

        elements.append(Spacer(1, 0.5*cm))
        return elements

    def _create_diplomes_section(self, diplomes: list):
        """Create diplomas section with table"""
        elements = []

        if not diplomes:
            return elements

        # Section header - BLEU MARINE
        header = Paragraph("<b>DIPLÔMES & FORMATIONS</b>", self.section_style)
        header_table = Table([[header]], colWidths=[17*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1e3a5f')),  # BLEU MARINE
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.4*cm))

        # Diplomes table
        table_data = []

        for diplome in diplomes:
            # Handle None values from JSON null
            annee_val = diplome.get('annee') or ''
            annee_val = str(annee_val).strip() if annee_val else ''

            # Only show year if it exists and is not empty/None
            if annee_val and annee_val.lower() not in ['none', '', 'null', 'non spécifié']:
                annee = Paragraph(f"<b>{annee_val}</b>", self.bold_style)
            else:
                annee = Paragraph("", self.bold_style)  # Empty if no year

            diplome_text = Paragraph(
                f"<b>{diplome.get('diplome', '')}</b><br/>"
                f"<font size=8>{diplome.get('etablissement', '')}</font>",
                self.normal_style
            )
            table_data.append([annee, diplome_text])

        if table_data:
            diplome_table = Table(table_data, colWidths=[2*cm, 15*cm])
            diplome_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(diplome_table)

        elements.append(Spacer(1, 0.5*cm))
        return elements

    def _create_certifications_section(self, certifications: list):
        """Create certifications section with table"""
        elements = []

        if not certifications:
            return elements

        # Section header - BLEU MARINE
        header = Paragraph("<b>CERTIFICATIONS</b>", self.section_style)
        header_table = Table([[header]], colWidths=[17*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1e3a5f')),  # BLEU MARINE
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.4*cm))

        # Certifications table
        table_data = []

        for cert in certifications:
            # Handle None values from JSON null
            annee_val = cert.get('annee') or ''
            annee_val = str(annee_val).strip() if annee_val else ''

            # Only show year if it exists and is not empty/None
            if annee_val and annee_val.lower() not in ['none', '', 'null', 'non spécifié']:
                annee = Paragraph(f"<b>{annee_val}</b>", self.bold_style)
            else:
                annee = Paragraph("", self.bold_style)  # Empty if no year

            # Handle organisme - don't show if None or empty
            organisme_val = cert.get('organisme') or ''
            organisme_val = str(organisme_val).strip() if organisme_val and str(organisme_val).lower() not in ['none', 'null'] else ''

            cert_name = cert.get('nom', '')
            if organisme_val:
                cert_text = Paragraph(
                    f"<b>{cert_name}</b><br/>"
                    f"<font size=8>{organisme_val}</font>",
                    self.normal_style
                )
            else:
                cert_text = Paragraph(f"<b>{cert_name}</b>", self.normal_style)
            table_data.append([annee, cert_text])

        if table_data:
            cert_table = Table(table_data, colWidths=[2*cm, 15*cm])
            cert_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(cert_table)

        elements.append(Spacer(1, 0.5*cm))
        return elements

    def _create_competences_section(self, competences_groups: list):
        """Create technical skills section with AI-grouped competences"""
        elements = []

        if not competences_groups:
            return elements

        # Section header - BLEU MARINE
        header = Paragraph("<b>COMPÉTENCES TECHNIQUES</b>", self.section_style)
        header_table = Table([[header]], colWidths=[17*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1e3a5f')),  # BLEU MARINE
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.4*cm))

        # Build table from AI-grouped competences
        table_data = []

        for group in competences_groups:
            categorie = group.get('categorie', '')
            competences = group.get('competences', [])

            if competences:
                skill_text = ', '.join(competences) if isinstance(competences, list) else str(competences)

                label_para = Paragraph(f"<b>{categorie}</b>", self.bold_style)
                skill_para = Paragraph(skill_text, self.normal_style)
                table_data.append([label_para, skill_para])

        if table_data:
            comp_table = Table(table_data, colWidths=[4.5*cm, 12.5*cm])
            comp_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(comp_table)

        elements.append(Spacer(1, 0.5*cm))
        return elements

    def _create_langues_section(self, langues: list):
        """Create languages section with table"""
        elements = []

        if not langues:
            return elements

        # Section header - BLEU MARINE
        header = Paragraph("<b>LANGUES</b>", self.section_style)
        header_table = Table([[header]], colWidths=[17*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1e3a5f')),  # BLEU MARINE
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.4*cm))

        # Languages table
        table_data = []

        for langue in langues:
            lang_para = Paragraph(f"<b>{langue.get('langue', '')}</b>", self.bold_style)
            niveau_para = Paragraph(langue.get('niveau', ''), self.normal_style)
            table_data.append([lang_para, niveau_para])

        if table_data:
            lang_table = Table(table_data, colWidths=[4.5*cm, 12.5*cm])
            lang_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(lang_table)

        elements.append(Spacer(1, 0.5*cm))
        return elements

    def _create_experiences_section(self, experiences: list):
        """Create professional experiences section"""
        elements = []

        if not experiences:
            return elements

        # Section header - BLEU MARINE
        header = Paragraph("<b>EXPÉRIENCES PROFESSIONNELLES</b>", self.section_style)
        header_table = Table([[header]], colWidths=[17*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1e3a5f')),  # BLEU MARINE
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.5*cm))

        for exp in experiences:
            # Company header with blue background
            company_header = Paragraph(
                f"<b>{exp.get('entreprise', 'ENTREPRISE')}</b>",
                ParagraphStyle('CompanyHeader', fontSize=10, textColor=colors.white, fontName='Helvetica-Bold')
            )
            period = Paragraph(
                exp.get('periode', ''),
                ParagraphStyle('Period', fontSize=10, textColor=colors.white, alignment=TA_CENTER)
            )

            header_table = Table([[company_header, period]], colWidths=[11*cm, 6*cm])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2563eb')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ]))
            elements.append(header_table)

            # Position
            position = Paragraph(
                f"<i>{exp.get('poste', '')}</i>",
                ParagraphStyle('Position', fontSize=9, fontName='Helvetica-Oblique', spaceAfter=6)
            )
            elements.append(Spacer(1, 0.2*cm))
            elements.append(position)

            # Project description
            if exp.get('projets'):
                project_text = '<br/>'.join([f"<b>Projet :</b> {p}" for p in exp['projets']])
                project_para = Paragraph(project_text, self.normal_style)
                elements.append(project_para)
                elements.append(Spacer(1, 0.2*cm))

            # Realisations
            if exp.get('realisations'):
                elements.append(Paragraph("<b>Réalisation :</b>", self.bold_style))
                for real in exp['realisations']:
                    real_para = Paragraph(f"• {real}", self.normal_style)
                    elements.append(real_para)
                elements.append(Spacer(1, 0.2*cm))

            # Technical environment
            if exp.get('environnement'):
                env_text = ', '.join(exp['environnement']) if isinstance(exp['environnement'], list) else exp['environnement']
                env_para = Paragraph(
                    f"<b>Environnement technique :</b> {env_text}",
                    self.normal_style
                )
                elements.append(env_para)

            elements.append(Spacer(1, 0.5*cm))

        # Footer
        footer = Paragraph(
            'www.consultingdatamed.com',
            ParagraphStyle('Footer', fontSize=9, alignment=TA_CENTER, textColor=colors.grey)
        )
        elements.append(Spacer(1, 1*cm))
        elements.append(footer)

        return elements
