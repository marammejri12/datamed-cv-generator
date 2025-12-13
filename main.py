"""
CV Anonymizer - Main Application Entry Point
Generate anonymous professional CVs automatically

Author: DataMed Solutions
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
from ui.styles import MAIN_STYLE


def main():
    """Main application entry point"""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("CV Anonymizer")
    app.setOrganizationName("DataMed")

    # Apply stylesheet
    app.setStyleSheet(MAIN_STYLE)

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
