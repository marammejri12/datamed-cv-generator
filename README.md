# DataMed CV Anonymizer

Application de génération automatique de CVs anonymes avec Intelligence Artificielle pour DataMed ESN.

## Description

Cette application permet aux ingénieurs de DataMed de :
1. **Importer** un CV de consultant (PDF ou DOCX)
2. **Extraire automatiquement** 100% du contenu avec l'IA Gemini
3. **Générer** un CV anonyme professionnel au format DataMed ou FastorGie
4. **Exporter** en PDF ou Word

L'application extrait TOUT le contenu du CV (formations, certifications, compétences, expériences) et le rend anonyme (supprime nom, prénom, email, adresse)

## ✨ Fonctionnalités

- 📄 **Import automatique** - Glissez-déposez votre CV (PDF ou DOCX)
- 🤖 **Extraction intelligente avec IA** - Parsing automatique avec Google Gemini
- 🔒 **Anonymisation complète** - Suppression de toutes les données personnelles
- 🎨 **Templates professionnels** - DataMed (Bleu Marine) & FastorGie (Rouge)
- 📤 **Formats multiples** - Export PDF et Word (.docx)
- ⚡ **Ultra rapide** - Génération en quelques secondes
- 💻 **Interface web moderne** - Accessible partout, sur tous les appareils

## Prérequis

- Python 3.8+
- Clé API Google Gemini (obligatoire pour extraction IA)

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Configurer la clé API Gemini :
   - Créer un fichier `.env` à la racine
   - Ajouter : `GEMINI_API_KEY=votre_cle_api`

## Utilisation - Application Desktop (PyQt6)

Lancer l'application graphique :
```bash
python main.py
```

### Étapes :
1. Choisir le template (DataMed ou FastorGie)
2. Choisir le format d'export (PDF ou Word)
3. Glisser-déposer le CV ou cliquer pour parcourir
4. Cliquer sur "Générer le CV Anonyme"
5. Attendre 30-60 secondes (extraction IA)
6. Le CV anonyme est généré !

## Utilisation - Application Web (Streamlit) - Optionnel

```bash
streamlit run app_streamlit.py
```

## Structure du Projet

```
cv_anonymizer/
├── main.py                    # Point d'entrée application desktop
├── app_streamlit.py          # Point d'entrée application web (optionnel)
├── config.py                 # Configuration
├── .env                      # Clé API (à créer)
├── requirements.txt          # Dépendances
│
├── parsers/
│   ├── ai_cv_parser.py      # Parser IA avec Gemini (extraction 100%)
│   └── cv_parser.py         # Parser basique (fallback)
│
├── templates/
│   ├── datamed_template.py       # Template DataMed (bleu marine)
│   ├── fastorgie_template.py    # Template FastorGie (rouge)
│   └── advanced_professional_template.py  # Template avancé
│
├── generators/
│   ├── pdf_generator.py     # Générateur PDF
│   └── word_generator.py    # Générateur Word
│
├── ui/
│   ├── main_window.py       # Interface graphique PyQt6
│   └── styles.py            # Styles de l'interface
│
└── utils/
    └── anonymizer.py        # Anonymisation des données
```

## Templates Disponibles

### 1. DataMed - Advanced Professional (Bleu Marine)
- Logo DataMed
- Sections : Diplômes, Certifications, Compétences, Langues, Expériences
- Couleur principale : Bleu marine (#1e3a5f)

### 2. FastorGie - Professional (Rouge)
- Logo FastorGie
- Même structure que DataMed
- Couleur principale : Rouge

## Extraction IA - 100% du Contenu

Le parser IA (Gemini 1.5 Pro) extrait :
- **Tous les diplômes** avec année, titre, établissement
- **Toutes les certifications** (AWS, Azure, Oracle, etc.)
- **Toutes les compétences techniques** classifiées intelligemment
- **Toutes les langues** avec niveaux
- **Toutes les expériences** avec TOUS les détails :
  - Entreprise (vrai nom conservé)
  - Période exacte
  - Poste complet
  - Projets détaillés
  - TOUS les bullet points (réalisations)
  - Environnement technique complet

## Formats d'Export

- **PDF** : Format professionnel avec mise en page optimisée
- **Word (DOCX)** : Format éditable pour modifications ultérieures

## Anonymisation

L'application anonymise automatiquement:
- Nom et prénom → "Nom & Prénom"
- Email → Supprimé
- Téléphone → Supprimé
- Adresse → Supprimée

**Conservé (pour le CV anonyme):**
- Compétences techniques complètes
- Technologies utilisées
- Expériences professionnelles détaillées (avec vrai nom entreprise)
- Diplômes et formations
- Langues et niveaux

## Dépannage

### Erreur "GEMINI_API_KEY not found"
- Vérifier que le fichier `.env` existe
- Vérifier que la clé API est correcte

### Extraction incomplète
- Vérifier la version de `google-generativeai`
- L'IA extrait maintenant 100% du contenu (améliorations récentes)

### Erreur PyQt6
- Installer PyQt6 : `pip install PyQt6`

## Support

Pour toute question, contacter l'équipe DataMed.
