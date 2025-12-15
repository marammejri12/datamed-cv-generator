"""
DataMed CV Generator - Système de mise à jour automatique
Télécharge les mises à jour depuis GitHub
"""

import os
import sys
import zipfile
import shutil
import requests
from pathlib import Path

class AutoUpdater:
    def __init__(self, github_repo_url, current_version="1.0.0"):
        """
        Initialise le système de mise à jour

        Args:
            github_repo_url: URL du repo GitHub (ex: "https://github.com/username/cv_anonymizer")
            current_version: Version actuelle de l'application
        """
        self.github_repo_url = github_repo_url.rstrip('/')
        self.current_version = current_version
        self.app_dir = Path(os.path.dirname(os.path.abspath(__file__)))

    def check_for_updates(self):
        """
        Vérifie s'il y a une nouvelle version disponible

        Returns:
            dict: {"available": bool, "latest_version": str, "download_url": str}
        """
        try:
            # Extraire le nom d'utilisateur et repo depuis l'URL
            parts = self.github_repo_url.replace('https://github.com/', '').split('/')
            if len(parts) < 2:
                return {"available": False, "error": "URL GitHub invalide"}

            owner = parts[0]
            repo = parts[1]

            # Appeler l'API GitHub pour obtenir la dernière release
            api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            response = requests.get(api_url, timeout=10)

            if response.status_code == 404:
                # Pas de releases, utiliser la branche main
                return {
                    "available": True,
                    "latest_version": "latest",
                    "download_url": f"{self.github_repo_url}/archive/refs/heads/main.zip",
                    "message": "Mise à jour disponible depuis la branche main"
                }

            if response.status_code != 200:
                return {"available": False, "error": f"Erreur API GitHub: {response.status_code}"}

            data = response.json()
            latest_version = data.get('tag_name', 'latest').lstrip('v')

            # Comparer les versions
            if latest_version != self.current_version:
                zipball_url = data.get('zipball_url')
                return {
                    "available": True,
                    "latest_version": latest_version,
                    "download_url": zipball_url,
                    "message": f"Nouvelle version disponible: {latest_version}"
                }

            return {
                "available": False,
                "latest_version": latest_version,
                "message": "Vous avez déjà la dernière version"
            }

        except requests.exceptions.RequestException as e:
            return {"available": False, "error": f"Erreur réseau: {str(e)}"}
        except Exception as e:
            return {"available": False, "error": f"Erreur: {str(e)}"}

    def download_and_install_update(self, download_url, progress_callback=None):
        """
        Télécharge et installe la mise à jour

        Args:
            download_url: URL du fichier ZIP à télécharger
            progress_callback: Fonction à appeler pour afficher la progression

        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            temp_dir = self.app_dir / "temp_update"
            temp_dir.mkdir(exist_ok=True)

            # Télécharger le fichier ZIP
            if progress_callback:
                progress_callback("📥 Téléchargement de la mise à jour...")

            zip_path = temp_dir / "update.zip"

            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size > 0:
                            percent = (downloaded / total_size) * 100
                            progress_callback(f"📥 Téléchargement: {percent:.1f}%")

            # Extraire le ZIP
            if progress_callback:
                progress_callback("📦 Extraction des fichiers...")

            extract_dir = temp_dir / "extracted"
            extract_dir.mkdir(exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            # Trouver le dossier principal (GitHub crée un sous-dossier)
            extracted_folders = list(extract_dir.iterdir())
            if len(extracted_folders) == 1 and extracted_folders[0].is_dir():
                source_dir = extracted_folders[0]
            else:
                source_dir = extract_dir

            # Sauvegarder le .env actuel (pour garder la clé API)
            env_backup = None
            if (self.app_dir / ".env").exists():
                env_backup = (self.app_dir / ".env").read_text(encoding='utf-8')

            # Liste des fichiers/dossiers à ne PAS écraser
            protected_items = {'.env', 'output', '__pycache__', 'temp_update'}

            # Copier les nouveaux fichiers
            if progress_callback:
                progress_callback("🔄 Installation de la mise à jour...")

            for item in source_dir.rglob('*'):
                if item.is_file():
                    # Calculer le chemin relatif
                    rel_path = item.relative_to(source_dir)

                    # Vérifier si le fichier est protégé
                    if any(protected in rel_path.parts for protected in protected_items):
                        continue

                    # Copier le fichier
                    dest_path = self.app_dir / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)

            # Restaurer le .env (pour garder la clé API)
            if env_backup:
                (self.app_dir / ".env").write_text(env_backup, encoding='utf-8')

            # Nettoyer les fichiers temporaires
            if progress_callback:
                progress_callback("🧹 Nettoyage...")

            shutil.rmtree(temp_dir, ignore_errors=True)

            if progress_callback:
                progress_callback("✅ Mise à jour terminée!")

            return {
                "success": True,
                "message": "Mise à jour installée avec succès! Redémarrez l'application."
            }

        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Erreur de téléchargement: {str(e)}"}
        except zipfile.BadZipFile:
            return {"success": False, "message": "Le fichier téléchargé est corrompu"}
        except Exception as e:
            return {"success": False, "message": f"Erreur d'installation: {str(e)}"}
        finally:
            # Nettoyer en cas d'erreur
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)

    def auto_update(self, progress_callback=None):
        """
        Vérifie et installe automatiquement les mises à jour

        Args:
            progress_callback: Fonction à appeler pour afficher la progression

        Returns:
            dict: Résultat de la mise à jour
        """
        if progress_callback:
            progress_callback("🔍 Recherche de mises à jour...")

        # Vérifier les mises à jour
        check_result = self.check_for_updates()

        if not check_result.get("available"):
            return {
                "success": True,
                "updated": False,
                "message": check_result.get("message", "Aucune mise à jour disponible")
            }

        # Télécharger et installer
        install_result = self.download_and_install_update(
            check_result["download_url"],
            progress_callback
        )

        if install_result["success"]:
            return {
                "success": True,
                "updated": True,
                "message": install_result["message"],
                "version": check_result.get("latest_version")
            }
        else:
            return {
                "success": False,
                "updated": False,
                "message": install_result["message"]
            }


# Configuration - URL du repo GitHub
GITHUB_REPO_URL = "https://github.com/marammejri12/datamed-cv-generator"
APP_VERSION = "1.0.0"


def main():
    """Test du système de mise à jour"""
    updater = AutoUpdater(GITHUB_REPO_URL, APP_VERSION)

    print("🔍 Vérification des mises à jour...")
    result = updater.auto_update(progress_callback=print)

    print("\n" + "="*50)
    print(f"Résultat: {result['message']}")

    if result.get('updated'):
        print("⚠️  Redémarrez l'application pour appliquer les changements")


if __name__ == "__main__":
    main()
