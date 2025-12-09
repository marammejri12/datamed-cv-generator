"""
DataMed CV Generator - Application Web Streamlit
Version hébergée en ligne - Accès par lien URL uniquement
"""
import streamlit as st
import os
import tempfile
from datetime import datetime
from parsers.ai_cv_parser import AICVParser
from generators.pdf_generator import CVGenerator
from generators.word_generator import WordGenerator
from utils.anonymizer import Anonymizer
import base64

# Configuration de la page
st.set_page_config(
    page_title="DataMed CV Generator",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour le style DataMed
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        background-color: #1a365d;
        color: white;
        border-radius: 10px;
        padding: 15px 30px;
        font-size: 16px;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0f2847;
    }
    h1 {
        color: #1a365d;
        text-align: center;
    }
    h3 {
        color: #475569;
    }
    .success-box {
        padding: 20px;
        background-color: #d1fae5;
        border-radius: 10px;
        border-left: 5px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# Header avec logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("📄 DataMed CV Generator")
    st.markdown("**Anonymisation intelligente de CVs avec IA**")
    st.markdown("---")

# Instructions
with st.expander("ℹ️ Comment utiliser cette application"):
    st.markdown("""
    **Étapes:**
    1. Choisissez un template (DataMed ou FastorGie)
    2. Choisissez le format d'export (PDF ou Word)
    3. Uploadez votre CV (PDF ou DOCX)
    4. Cliquez sur "Générer le CV Anonyme"
    5. Téléchargez le résultat

    **L'application:**
    - Supprime: nom, email, téléphone, adresse
    - Préserve: formations, expériences, compétences
    - Utilise l'IA Gemini pour extraction intelligente
    """)

# Configuration
st.markdown("### ⚙️ Configuration")

col1, col2 = st.columns(2)

with col1:
    template = st.selectbox(
        "🎨 Template",
        ["DataMed - Bleu Marine", "FastorGie - Rouge"],
        index=0
    )
    template_type = 'advanced' if 'DataMed' in template else 'fastorgie'

with col2:
    format_export = st.selectbox(
        "📤 Format d'export",
        ["PDF", "Word (.docx)"],
        index=0
    )
    export_format = 'pdf' if format_export == "PDF" else 'word'

st.markdown("---")

# Upload du CV
st.markdown("### 📥 Importer le CV")
uploaded_file = st.file_uploader(
    "Glissez-déposez ou cliquez pour parcourir",
    type=['pdf', 'docx'],
    help="Formats supportés: PDF, DOCX"
)

if uploaded_file is not None:
    st.success(f"✅ Fichier chargé: {uploaded_file.name}")

    # Bouton de génération
    st.markdown("---")
    if st.button("🚀 Générer le CV Anonyme", type="primary"):

        with st.spinner("⏳ Traitement en cours... (10-30 secondes)"):
            try:
                # Créer un fichier temporaire pour l'input
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_input:
                    tmp_input.write(uploaded_file.read())
                    input_path = tmp_input.name

                # Afficher la progression
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Étape 1: Extraction
                status_text.text("📖 Extraction du contenu avec IA Gemini...")
                progress_bar.progress(20)

                parser = AICVParser()
                data = parser.parse_cv(input_path)

                progress_bar.progress(50)
                status_text.text("🤖 Anonymisation des données...")

                # Étape 2: Anonymisation
                anonymizer = Anonymizer()
                anonymized_data = anonymizer.anonymize_data(data)

                progress_bar.progress(70)
                status_text.text(f"📝 Génération du CV {format_export}...")

                # Étape 3: Génération
                extension = '.pdf' if export_format == 'pdf' else '.docx'
                output_filename = f"cv_anonyme_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"

                with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_output:
                    output_path = tmp_output.name

                generator = CVGenerator()
                result_path = generator.generate_cv(
                    anonymized_data,
                    output_path,
                    template_type,
                    export_format
                )

                progress_bar.progress(100)
                status_text.text("✅ Génération terminée!")

                # Lire le fichier généré
                with open(result_path, 'rb') as f:
                    file_data = f.read()

                # Bouton de téléchargement
                st.markdown("---")
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success("🎉 CV anonyme généré avec succès!")

                mime_type = 'application/pdf' if export_format == 'pdf' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

                st.download_button(
                    label=f"📥 Télécharger le CV Anonyme ({format_export})",
                    data=file_data,
                    file_name=output_filename,
                    mime=mime_type
                )
                st.markdown('</div>', unsafe_allow_html=True)

                # Nettoyage
                os.unlink(input_path)
                os.unlink(result_path)

            except Exception as e:
                error_msg = str(e)
                st.error(f"❌ Erreur lors de la génération: {error_msg}")

                # Messages d'aide spécifiques
                if "Flowable" in error_msg or "too large" in error_msg:
                    st.warning("⚠️ Le CV contient trop de contenu pour le format PDF. Essayez:")
                    st.info("✅ Exporter en format **Word** au lieu de PDF")
                    st.info("✅ Ou réduire le contenu du CV avant de l'uploader")
                elif "API" in error_msg or "key" in error_msg:
                    st.info("🔑 Vérifiez que votre clé API Gemini est configurée dans config.py")
                else:
                    st.info("💡 Essayez d'utiliser le format Word ou un CV plus court")

else:
    st.info("👆 Commencez par uploader un CV")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 12px;'>
    <p>© 2024 DataMed Consulting - Tous droits réservés</p>
    <p>Propulsé par Gemini AI | Support: support@datamed-consulting.com</p>
</div>
""", unsafe_allow_html=True)
