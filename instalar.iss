[Setup]
AppName=Policlinico
AppVersion=1.0
DefaultDirName={pf}\Policlinico
OutputDir=C:\Users\Yo\Desktop\Clinica\Instalador
OutputBaseFilename=Policlinico_Setup
Compression=lzma
SolidCompression=yes
ChangesAssociations=yes
CreateAppDir=no
DefaultGroupName=Policlinico
DisableProgramGroupPage=yes
DisableDirPage=yes
DisableReadyPage=yes
UninstallDisplayIcon={app}\Policlinico.exe
UninstallDisplayName=Policlinico
UninstallDisplaySizeMB=5
WizardImageFile=wizard-small.bmp
WizardSmallImageFile=wizard-small.bmp
ArchitecturesAllowed=x64

[Files]
Source: "C:\Users\Yo\Desktop\Clinica\historiaMedica\dist\Policlinico.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yo\Desktop\Clinica\historiaMedica\imagenes\logo.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yo\Desktop\Clinica\historiaMedica\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{commondesktop}\Policlinico"; Filename: "{app}\Policlinico.exe"; WorkingDir: "{app}"; IconFilename: "{app}\logo.ico"

[Run]
Filename: "{app}\Policlinico.exe"; Description: "Launch Policlinico"; Flags: postinstall shellexec skipifsilent
