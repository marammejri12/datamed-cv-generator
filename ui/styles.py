"""
Modern styling for CV Anonymizer application
"""

MAIN_STYLE = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #1e3c72, stop:1 #2a5298);
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #2c3e50;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 15px 30px;
    font-size: 14px;
    font-weight: bold;
    min-width: 200px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #764ba2, stop:1 #667eea);
    transform: translateY(-2px);
}

QPushButton:pressed {
    background: #5a67d8;
}

QPushButton:disabled {
    background: #cccccc;
    color: #666666;
}

QLabel {
    color: white;
    font-size: 14px;
}

QLabel#title {
    font-size: 32px;
    font-weight: bold;
    color: white;
    margin: 20px;
}

QLabel#subtitle {
    font-size: 16px;
    color: #e0e0e0;
    margin-bottom: 30px;
}

QComboBox {
    background: white;
    border: 2px solid #667eea;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    min-width: 300px;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox::down-arrow {
    image: url(down_arrow.png);
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background: white;
    border: 2px solid #667eea;
    selection-background-color: #667eea;
    selection-color: white;
}

QProgressBar {
    border: 2px solid white;
    border-radius: 10px;
    background: white;
    text-align: center;
    color: #2c3e50;
    font-weight: bold;
    min-height: 30px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
    border-radius: 8px;
}

QFrame#dropArea {
    background: rgba(255, 255, 255, 0.1);
    border: 3px dashed white;
    border-radius: 15px;
    min-height: 200px;
}

QFrame#dropArea:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: #ffd700;
}

QTextEdit {
    background: white;
    border: 2px solid #667eea;
    border-radius: 10px;
    padding: 10px;
    font-size: 12px;
}
"""
