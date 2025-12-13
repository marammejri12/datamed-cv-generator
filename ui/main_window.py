"""
Main Window for CV Anonymizer Application
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QProgressBar,
    QFileDialog, QTextEdit, QFrame, QMessageBox, QRadioButton, QButtonGroup,
    QScrollArea, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont, QPalette, QColor, QPixmap, QIcon
from parsers.cv_parser import CVParser
from parsers.ai_cv_parser import AICVParser
from generators.pdf_generator import PDFGenerator, CVGenerator
import os
import sys

# Add parent directory to path for config
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from config import GEMINI_API_KEY
except:
    GEMINI_API_KEY = ''


class CVProcessingThread(QThread):
    """Background thread for CV processing"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_file, output_file, template_type, export_format='pdf'):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.template_type = template_type
        self.export_format = export_format

    def run(self):
        try:
            # Step 1: Parse CV with AI
            self.status.emit("🤖 Analyse intelligente du CV avec IA...")
            self.progress.emit(10)

            # Try AI parser first
            if GEMINI_API_KEY:
                self.status.emit("🤖 Extraction avec Gemini AI...")
                parser = AICVParser(api_key=GEMINI_API_KEY)
            else:
                self.status.emit("📄 Extraction basique (pas d'API key)...")
                parser = CVParser()

            self.progress.emit(30)
            data = parser.parse_cv(self.input_file)

            # Step 2: Anonymize
            self.status.emit("🔒 Anonymisation des données...")
            self.progress.emit(60)

            # Step 3: Generate CV (PDF or WORD)
            format_name = "PDF" if self.export_format == 'pdf' else "Word"
            self.status.emit(f"📝 Génération du CV professionnel ({format_name})...")
            self.progress.emit(80)
            generator = CVGenerator()
            output_path = generator.generate_cv(data, self.output_file, self.template_type, self.export_format)

            # Complete
            self.progress.emit(100)
            self.status.emit("✅ CV généré avec succès!")
            self.finished.emit(output_path)

        except Exception as e:
            self.error.emit(str(e))


class DropArea(QFrame):
    """Drag and drop area for files"""
    file_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setObjectName("dropArea")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)

        # Modern clean style
        self.setStyleSheet("""
            QFrame#dropArea {
                background-color: #f8fafc;
                border: 3px dashed #cbd5e1;
                border-radius: 12px;
                min-height: 180px;
            }
            QFrame#dropArea:hover {
                border-color: #2563eb;
                background-color: #dbeafe;
                border-width: 3px;
            }
        """)

        # Icon
        icon_label = QLabel("📄")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(50)
        icon_label.setFont(font)

        # Text
        text_label = QLabel("Glissez-déposez le CV ici\nou cliquez pour parcourir")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("color: #0f2847; font-size: 15px; font-weight: 600; line-height: 1.8;")

        # Supported formats
        format_label = QLabel("Formats supportés: PDF, DOCX")
        format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        format_label.setStyleSheet("color: #94a3b8; font-size: 12px; margin-top: 8px;")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addWidget(format_label)

        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            file_path = files[0]
            if file_path.lower().endswith(('.pdf', '.docx', '.doc')):
                self.file_dropped.emit(file_path)

    def mousePressEvent(self, event):
        # Open file dialog on click
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un CV",
            "",
            "Documents (*.pdf *.docx *.doc)"
        )
        if file_path:
            self.file_dropped.emit(file_path)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.current_file = None
        self.processing_thread = None
        self.init_ui()

    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("DataMed CV Generator")
        self.setGeometry(100, 100, 1100, 800)
        self.setMinimumSize(950, 700)

        # Set DataMed logo as window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image', 'app_icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            print(f"Icon loaded successfully from: {icon_path}")
        else:
            # Try alternative path
            icon_path_alt = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image', 'datamed_consulting_logo.ico')
            if os.path.exists(icon_path_alt):
                self.setWindowIcon(QIcon(icon_path_alt))
                print(f"Icon loaded from alternative path: {icon_path_alt}")
            else:
                print(f"Warning: Icon file not found at {icon_path}")

        # Set AMAZING professional style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QScrollArea {
                background-color: #f5f7fa;
                border: none;
            }
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #0f2847;
                letter-spacing: 0.5px;
            }
            QLabel#subtitle {
                font-size: 13px;
                color: #64748b;
                font-style: italic;
            }
            QLabel#section_title {
                font-size: 12px;
                font-weight: bold;
                color: #475569;
                text-transform: uppercase;
                letter-spacing: 1px;
                padding: 8px 0px;
            }
            QPushButton {
                background-color: #001a3d;
                color: #ffffff !important;
                border: 2px solid #002855;
                padding: 16px 32px;
                font-size: 17px;
                font-weight: bold;
                border-radius: 10px;
                min-height: 50px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4), 0 4px 8px rgba(0, 0, 0, 0.25);
            }
            QPushButton:hover {
                background-color: #003d73;
                color: #ffffff !important;
                border-color: #004d8f;
                box-shadow: 0 14px 28px rgba(0, 26, 61, 0.6), 0 8px 16px rgba(0, 0, 0, 0.3);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #00112b;
                color: #ffffff !important;
                border-color: #001a3d;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
            }
            QPushButton:disabled {
                background-color: #cbd5e1;
                color: #94a3b8 !important;
            }
            QComboBox {
                background-color: white;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #0f2847;
                min-height: 45px;
                font-weight: 500;
            }
            QComboBox:hover {
                border-color: #2563eb;
            }
            QComboBox:focus {
                border-color: #2563eb;
                border-width: 2px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 7px solid #2563eb;
            }
            QRadioButton {
                font-size: 14px;
                color: #0f2847;
                padding: 10px 16px;
                font-weight: 500;
                spacing: 10px;
                background-color: white;
                border-radius: 8px;
            }
            QRadioButton::indicator {
                width: 22px;
                height: 22px;
                border-radius: 11px;
                border: 2px solid #cbd5e1;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                background-color: #2563eb;
                border: 2px solid #2563eb;
            }
            QRadioButton::indicator:hover {
                border-color: #2563eb;
            }
            QProgressBar {
                border: none;
                border-radius: 10px;
                text-align: center;
                background-color: #e2e8f0;
                min-height: 30px;
                font-weight: bold;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #2563eb;
                border-radius: 10px;
            }
            QTextEdit {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 16px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                color: #1f2937;
                line-height: 1.6;
            }
            QFrame#card {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """)

        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f5f7fa;")

        scroll.setWidget(central_widget)
        self.setCentralWidget(scroll)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(60, 40, 60, 40)

        # ============ HEADER WITH LOGO ============
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)

        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image', 'datamed_consulting_logo.jfif')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setFixedSize(70, 70)

        # Title and subtitle container
        title_container = QVBoxLayout()
        title_container.setSpacing(5)

        title = QLabel("DataMed CV Generator")
        title.setObjectName("title")

        subtitle = QLabel("Génération automatique de CVs anonymes avec Intelligence Artificielle")
        subtitle.setObjectName("subtitle")

        title_container.addWidget(title)
        title_container.addWidget(subtitle)

        header_layout.addWidget(logo_label)
        header_layout.addLayout(title_container)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # ============ CONFIGURATION CARD ============
        config_card = QFrame()
        config_card.setObjectName("card")
        config_card_layout = QVBoxLayout()
        config_card_layout.setContentsMargins(30, 25, 30, 25)
        config_card_layout.setSpacing(20)
        config_card.setLayout(config_card_layout)

        # Grid for options
        options_grid = QGridLayout()
        options_grid.setHorizontalSpacing(30)
        options_grid.setVerticalSpacing(20)

        # Template selector
        template_section_label = QLabel("CHOIX DU TEMPLATE")
        template_section_label.setObjectName("section_title")

        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "DataMed - Advanced Professional (Bleu Marine)",
            "FastorGie - Professional (Rouge)"
        ])
        self.template_combo.setCurrentIndex(0)

        # Format selector
        format_section_label = QLabel("FORMAT D'EXPORT")
        format_section_label.setObjectName("section_title")

        format_container = QHBoxLayout()
        format_container.setSpacing(15)

        self.format_group = QButtonGroup()
        self.pdf_radio = QRadioButton("📄 PDF")
        self.word_radio = QRadioButton("📝 Word (.docx)")
        self.pdf_radio.setChecked(True)

        self.format_group.addButton(self.pdf_radio)
        self.format_group.addButton(self.word_radio)

        format_container.addWidget(self.pdf_radio)
        format_container.addWidget(self.word_radio)
        format_container.addStretch()

        # Add to grid (0=row, 0=column, 1=rowspan, 1=colspan)
        options_grid.addWidget(template_section_label, 0, 0)
        options_grid.addWidget(self.template_combo, 1, 0)
        options_grid.addWidget(format_section_label, 0, 1)
        options_grid.addLayout(format_container, 1, 1)

        config_card_layout.addLayout(options_grid)

        main_layout.addWidget(config_card)

        # ============ UPLOAD CARD ============
        upload_card = QFrame()
        upload_card.setObjectName("card")
        upload_card_layout = QVBoxLayout()
        upload_card_layout.setContentsMargins(30, 25, 30, 25)
        upload_card_layout.setSpacing(15)
        upload_card.setLayout(upload_card_layout)

        upload_section_label = QLabel("IMPORTER LE CV")
        upload_section_label.setObjectName("section_title")
        upload_card_layout.addWidget(upload_section_label)

        # Drop area
        self.drop_area = DropArea()
        self.drop_area.file_dropped.connect(self.on_file_selected)
        upload_card_layout.addWidget(self.drop_area)

        # File info
        self.file_label = QLabel("Aucun fichier sélectionné")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet("color: #64748b; font-size: 13px; font-weight: 500; padding: 10px;")
        upload_card_layout.addWidget(self.file_label)

        main_layout.addWidget(upload_card)

        # ============ PROGRESS SECTION ============
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #1f2937; font-size: 13px; font-weight: 600; padding: 8px;")

        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_label)

        # ============ ACTION BUTTONS ============
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        # Generate button
        self.generate_btn = QPushButton("🚀 Générer le CV Anonyme")
        self.generate_btn.setEnabled(False)
        self.generate_btn.clicked.connect(self.on_generate_clicked)
        self.generate_btn.setMinimumHeight(55)

        # Open folder button
        self.open_folder_btn = QPushButton("📁 Ouvrir le Dossier")
        self.open_folder_btn.setVisible(False)
        self.open_folder_btn.clicked.connect(self.on_open_folder_clicked)
        self.open_folder_btn.setMinimumHeight(55)

        buttons_layout.addWidget(self.generate_btn, 2)
        buttons_layout.addWidget(self.open_folder_btn, 1)

        main_layout.addLayout(buttons_layout)

        # ============ LOG SECTION ============
        log_card = QFrame()
        log_card.setObjectName("card")
        log_card_layout = QVBoxLayout()
        log_card_layout.setContentsMargins(20, 20, 20, 20)
        log_card_layout.setSpacing(10)
        log_card.setLayout(log_card_layout)

        log_section_label = QLabel("JOURNAL D'ACTIVITÉ")
        log_section_label.setObjectName("section_title")
        log_card_layout.addWidget(log_section_label)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMinimumHeight(120)
        self.log_area.setMaximumHeight(180)
        log_card_layout.addWidget(self.log_area)

        log_card.setVisible(False)
        main_layout.addWidget(log_card)
        self.log_card = log_card

        main_layout.addStretch()

        central_widget.setLayout(main_layout)

    def on_file_selected(self, file_path: str):
        """Handle file selection"""
        self.current_file = file_path
        file_name = os.path.basename(file_path)
        self.file_label.setText(f"✓ Fichier sélectionné: {file_name}")
        self.generate_btn.setEnabled(True)
        self.log(f"📄 Fichier chargé: {file_name}")

    def on_generate_clicked(self):
        """Handle generate button click"""
        if not self.current_file:
            return

        # Get export format
        export_format = 'word' if self.word_radio.isChecked() else 'pdf'
        extension = '.docx' if export_format == 'word' else '.pdf'

        # Get output path
        output_dir = os.path.dirname(self.current_file)
        input_filename = os.path.splitext(os.path.basename(self.current_file))[0]

        # Get template name for filename
        template_name = "DATAMED" if self.template_combo.currentIndex() == 0 else "FASTORGIE"
        output_path = os.path.join(output_dir, f"{input_filename}_ANONYME_{template_name}{extension}")

        # Ask user for save location
        file_filter = "Word Files (*.docx)" if export_format == 'word' else "PDF Files (*.pdf)"
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le CV anonyme",
            output_path,
            file_filter
        )

        if not output_path:
            return

        # Start processing
        self.start_processing(output_path, export_format)

    def start_processing(self, output_path: str, export_format: str = 'pdf'):
        """Start CV processing in background thread"""
        # UI state
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.log_card.setVisible(True)
        self.open_folder_btn.setVisible(False)

        # Get template type based on selection
        template_index = self.template_combo.currentIndex()
        if template_index == 0:
            template_type = 'advanced'  # DataMed Advanced
        elif template_index == 1:
            template_type = 'fastorgie'  # FastorGie
        else:
            template_type = 'advanced'  # Default

        # Create and start thread
        self.processing_thread = CVProcessingThread(
            self.current_file,
            output_path,
            template_type,
            export_format
        )
        self.processing_thread.progress.connect(self.on_progress_update)
        self.processing_thread.status.connect(self.on_status_update)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.error.connect(self.on_processing_error)
        self.processing_thread.start()

        self.log("🚀 Démarrage de la génération...")

    def on_progress_update(self, value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)

    def on_status_update(self, status: str):
        """Update status label"""
        self.status_label.setText(status)
        self.log(status)

    def on_processing_finished(self, output_path: str):
        """Handle successful processing"""
        self.generate_btn.setEnabled(True)
        self.open_folder_btn.setVisible(True)
        self.output_path = output_path

        self.log(f"✅ CV généré avec succès!")
        self.log(f"📁 Emplacement: {output_path}")

        # Show success message
        QMessageBox.information(
            self,
            "Succès!",
            f"Le CV anonyme a été généré avec succès!\n\n{output_path}"
        )

    def on_processing_error(self, error: str):
        """Handle processing error"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        self.log(f"❌ Erreur: {error}")

        QMessageBox.critical(
            self,
            "Erreur",
            f"Une erreur est survenue lors de la génération:\n\n{error}"
        )

    def on_open_folder_clicked(self):
        """Open folder containing generated CV"""
        if hasattr(self, 'output_path'):
            folder = os.path.dirname(self.output_path)
            os.startfile(folder)

    def log(self, message: str):
        """Add message to log area"""
        self.log_area.append(message)
