"""
CV Generator - Orchestrates CV generation (PDF & WORD)
"""
from templates.advanced_professional_template import AdvancedProfessionalTemplate
from templates.fastorgie_template import FastorGieTemplate
from generators.word_generator import WordGenerator
from utils.anonymizer import Anonymizer
import os


class CVGenerator:
    """Generate anonymous CVs in PDF or WORD format"""

    def __init__(self):
        self.anonymizer = Anonymizer()

    def generate_cv(self, data: dict, output_path: str, template_type: str = 'advanced', export_format: str = 'pdf'):
        """
        Generate CV with specified template and format

        Args:
            data: Parsed CV data
            output_path: Output file path
            template_type: Template to use (advanced, fastorgie)
            export_format: Export format (pdf or word)
        """
        # Anonymize data
        anonymized_data = self.anonymizer.anonymize_data(data)

        # Ensure correct extension
        base_path = os.path.splitext(output_path)[0]

        if export_format.lower() == 'word':
            output_path = base_path + '.docx'
            # Generate WORD
            word_gen = WordGenerator(template_type=template_type)
            word_gen.generate_cv(anonymized_data, output_path)
        else:
            output_path = base_path + '.pdf'
            # Generate PDF
            if template_type == 'fastorgie':
                template = FastorGieTemplate(output_path)
            else:  # advanced (default)
                template = AdvancedProfessionalTemplate(output_path)

            template.generate(anonymized_data)

        return output_path


# Backward compatibility
class PDFGenerator(CVGenerator):
    """Alias for backward compatibility"""
    pass
