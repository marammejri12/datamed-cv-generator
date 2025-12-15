@echo off
REM DataMed CV Generator - Script de lancement
REM Ce script vérifie Python et lance l'application

echo ========================================
echo DataMed CV Generator
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH!
    echo.
    echo Veuillez installer Python 3.10 ou supérieur depuis:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Cochez "Add Python to PATH" pendant l'installation!
    echo.
    pause
    exit /b 1
)

echo Python détecté:
python --version
echo.

REM Vérifier si les dépendances sont installées
echo Vérification des dépendances...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installation des dépendances nécessaires...
    echo Cela peut prendre quelques minutes...
    echo.
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERREUR: Échec de l'installation des dépendances!
        pause
        exit /b 1
    )
)

REM Vérifier le fichier .env
if not exist ".env" (
    echo.
    echo ATTENTION: Fichier .env non trouvé!
    echo Création d'un fichier .env à partir de .env.example...
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo.
        echo IMPORTANT: Éditez le fichier .env et ajoutez votre clé API Gemini!
        echo Ouvrez .env avec Notepad et remplacez "your_api_key_here" par votre vraie clé.
        echo.
    ) else (
        echo GEMINI_API_KEY=your_api_key_here > .env
        echo.
        echo IMPORTANT: Éditez le fichier .env et ajoutez votre clé API Gemini!
        echo.
    )
)

echo.
echo Lancement de l'application...
echo.

REM Lancer l'application
python main.py

REM Si l'application se ferme avec une erreur
if errorlevel 1 (
    echo.
    echo L'application s'est fermée avec une erreur.
    pause
)
