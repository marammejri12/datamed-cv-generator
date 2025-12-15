@echo off
REM DataMed CV Generator - Installation des dépendances
REM Ce script installe toutes les dépendances Python nécessaires

echo ========================================
echo DataMed CV Generator
echo Installation des dépendances
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé!
    echo.
    echo Téléchargez et installez Python depuis:
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

echo Mise à jour de pip...
python -m pip install --upgrade pip
echo.

echo Installation des dépendances...
echo Cela peut prendre plusieurs minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERREUR: L'installation a échoué!
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo Installation terminée avec succès!
    echo ========================================
    echo.
    echo Vous pouvez maintenant lancer l'application.
    echo.
    pause
)
