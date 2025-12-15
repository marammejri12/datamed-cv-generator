; Script Inno Setup pour DataMed CV Generator
; Version 1.0.0
; Créé pour générer un installateur .exe professionnel

#define MyAppName "DataMed CV Generator"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "DataMed Consulting"
#define MyAppURL "https://www.consultingdatamed.com"
#define MyAppExeName "lancer_app.bat"

[Setup]
; Informations de l'application
AppId={{A5E8F9C3-2D4B-4E6A-9F1C-8D7E6A5B4C3D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Chemins d'installation
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Sortie
OutputDir=C:\Users\Maram Mejri\Desktop
OutputBaseFilename=DataMed-CV-Generator-Setup-v{#MyAppVersion}
SetupIconFile=C:\Users\Maram Mejri\cv_anonymizer\image\app_icon.ico

; Compression
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes

; Interface
WizardStyle=modern

; Privilèges (pas besoin d'admin)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Désinstallation
UninstallDisplayIcon={app}\image\app_icon.ico
UninstallDisplayName={#MyAppName}

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le Bureau"; GroupDescription: "Raccourcis additionnels:"; Flags: unchecked

[Files]
; Application Python - TOUS les fichiers sauf temporaires
Source: "C:\Users\Maram Mejri\cv_anonymizer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "__pycache__,*.pyc,*.pyo,*.tmp,*.log,nul,gemini_response_raw.json,.git,.gitignore"

; Copier le .env AVEC la clé API (partagée pour tous les collègues)
Source: "C:\Users\Maram Mejri\cv_anonymizer\.env"; DestDir: "{app}"; Flags: ignoreversion confirmoverwrite

[Icons]
; Menu Démarrer
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\image\app_icon.ico"; Comment: "Lancer DataMed CV Generator"
Name: "{group}\Installer les dépendances Python"; Filename: "{app}\install_dependencies.bat"; IconFilename: "{sys}\imageres.dll"; IconIndex: 76; Comment: "Installer les bibliothèques Python nécessaires"
Name: "{group}\Désinstaller {#MyAppName}"; Filename: "{uninstallexe}"; Comment: "Désinstaller l'application"

; Bureau (optionnel)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\image\app_icon.ico"; Tasks: desktopicon; Comment: "Lancer DataMed CV Generator"

[Run]
; Proposer de lancer l'application après installation
Filename: "{app}\{#MyAppExeName}"; Description: "Lancer {#MyAppName} maintenant"; Flags: nowait postinstall skipifsilent shellexec

[Code]
var
  PythonPage: TOutputMsgWizardPage;

procedure InitializeWizard;
begin
  // Page d'information Python uniquement
  PythonPage := CreateOutputMsgPage(wpWelcome,
    'Pré-requis: Python',
    'Python 3.10 ou supérieur est requis pour faire fonctionner l''application',
    'Si Python N''EST PAS encore installé sur cet ordinateur:' + #13#10 + #13#10 +
    '  1. Téléchargez Python depuis: https://www.python.org/downloads/' + #13#10 +
    '  2. IMPORTANT: Cochez "Add Python to PATH" pendant l''installation' + #13#10 +
    '  3. Redémarrez l''ordinateur après installation de Python' + #13#10 + #13#10 +
    'Si Python est déjà installé, cliquez simplement sur Suivant.' + #13#10 + #13#10 +
    'NOTE: La clé API Gemini est déjà configurée dans l''application.');
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  MsgResult: Integer;
begin
  // Demander si on doit supprimer les fichiers générés
  if CurUninstallStep = usUninstall then
  begin
    MsgResult := MsgBox('Voulez-vous également supprimer les CVs générés et les fichiers de configuration (.env)?',
                        mbConfirmation, MB_YESNO or MB_DEFBUTTON2);
    if MsgResult = IDYES then
    begin
      // Supprimer les fichiers générés
      DeleteFile(ExpandConstant('{app}\.env'));
      DeleteFile(ExpandConstant('{app}\gemini_response_raw.json'));
      DelTree(ExpandConstant('{app}\output'), True, True, True);
      DelTree(ExpandConstant('{app}\__pycache__'), True, True, True);
    end;
  end;
end;
