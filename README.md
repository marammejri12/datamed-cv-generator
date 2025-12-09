# 🚀 DataMed CV Generator

**Application web d'anonymisation intelligente de CVs avec IA Gemini**

## 🌐 Accès en Ligne

L'application est accessible directement dans votre navigateur sans installation:
**[Accéder à l'application](#)** *(lien disponible après déploiement)*

## ✨ Fonctionnalités

- 📄 **Import automatique** - Glissez-déposez votre CV (PDF ou DOCX)
- 🤖 **Extraction intelligente avec IA** - Parsing automatique avec Google Gemini
- 🔒 **Anonymisation complète** - Suppression de toutes les données personnelles
- 🎨 **Templates professionnels** - DataMed (Bleu Marine) & FastorGie (Rouge)
- 📤 **Formats multiples** - Export PDF et Word (.docx)
- ⚡ **Ultra rapide** - Génération en quelques secondes
- 💻 **Interface web moderne** - Accessible partout, sur tous les appareils

## 📋 Prérequis

- Python 3.8 ou supérieur
- Windows 10/11 (ou Linux/Mac avec adaptations mineures)

## 🔧 Installation

### Installation automatique (Recommandée)

```bash
# 1. Cloner ou télécharger le projet
cd cv_anonymizer

# 2. Exécuter le script d'installation
install.bat
```

### Installation manuelle

```bash
# 1. Créer un environnement virtuel
python -m venv venv

# 2. Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

## 🚀 Utilisation

### Lancer l'application

```bash
# Windows
python main.py

# Ou double-cliquer sur run.bat
```

### Étapes d'utilisation

1. **Choisir le template** - Sélectionnez "DataMed - Professionnel"
2. **Importer le CV** - Glissez-déposez le fichier ou cliquez pour parcourir
3. **Générer** - Cliquez sur "🚀 Générer CV Anonyme"
4. **Enregistrer** - Choisissez l'emplacement de sauvegarde
5. **Terminé!** - Votre CV anonyme est prêt!

## 📁 Structure du Projet

```
cv_anonymizer/
├── main.py                      # Point d'entrée principal
├── requirements.txt             # Dépendances Python
├── ui/
│   ├── main_window.py          # Interface graphique principale
│   └── styles.py               # Styles CSS modernes
├── parsers/
│   └── cv_parser.py            # Extraction automatique des CVs
├── templates/
│   └── datamed_template.py     # Template DataMed professionnel
├── generators/
│   └── pdf_generator.py        # Génération PDF
└── utils/
    └── anonymizer.py           # Logique d'anonymisation
```

## 🎨 Templates Disponibles

### DataMed - Professionnel ✅
- ✅ Design exact DataMed
- ✅ Tableaux structurés
- ✅ Logo et header
- ✅ Sections: Diplômes, Compétences, Langues, Expériences
- ✅ Anonymisation complète

### Templates à venir
- DataMed - Minimal
- Format Standard

## 🔒 Anonymisation

L'application anonymise automatiquement:

- ✅ Nom et prénom → "Nom & Prénom"
- ✅ Email → Supprimé
- ✅ Téléphone → Supprimé
- ✅ Adresse → Supprimée
- ✅ Noms d'entreprises → "ENTREPRISE"
- ✅ Informations de localisation

**Conservé:**
- ✅ Compétences techniques
- ✅ Technologies utilisées
- ✅ Expériences (anonymisées)
- ✅ Diplômes et formations
- ✅ Langues et niveaux

## 🐛 Dépannage

### L'application ne se lance pas
```bash
# Vérifier l'installation de Python
python --version

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Erreur lors de la génération
- Vérifiez que le CV est bien au format PDF ou DOCX
- Assurez-vous que le fichier n'est pas corrompu
- Consultez les logs dans l'interface

## 📝 Notes Techniques

### Formats supportés
- **Entrée:** PDF, DOCX, DOC
- **Sortie:** PDF professionnel

### Extraction intelligente
L'application utilise:
- **pdfplumber** pour l'extraction PDF
- **python-docx** pour les fichiers Word
- **Regex avancés** pour le parsing structuré
- **ReportLab** pour la génération PDF professionnelle

## 🎯 Cas d'Usage

### Pour les ESN / Cabinets de recrutement
- Anonymiser les CVs avant envoi aux clients
- Respecter les réglementations RGPD
- Standardiser le format des CVs
- Gain de temps considérable

### Pour les Recruteurs
- Éviter les biais de recrutement
- Focus sur les compétences techniques
- Process de recrutement conforme

## 🚀 Améliorations Futures

- [ ] Support OCR pour CVs scannés
- [ ] Templates personnalisables
- [ ] Export multiple (Word, JSON)
- [ ] Traitement par lot
- [ ] API REST
- [ ] Intégration Boond

## 📧 Contact & Support

Pour toute question ou problème:
- 📧 Email: support@consultingdatamed.com
- 🌐 Website: www.consultingdatamed.com

## 📄 Licence

© 2024 DataMed Consulting. Tous droits réservés.

---

**Développé avec ❤️ pour simplifier votre workflow de recrutement**
