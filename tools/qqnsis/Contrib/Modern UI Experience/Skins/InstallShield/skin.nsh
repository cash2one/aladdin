!ifndef MUI_EXPERIENCE_SKIN
!verbose push
!verbose 3
!define MUI_EXPERIENCE_SKIN

!insertmacro MUI_UNSET MUI_SKIN_DIR
!define MUI_SKIN_DIR "${MUI_XP_DIR}\Skins\InstallShield"

!insertmacro MUI_DEFAULT MUI_UI "${MUI_SKIN_DIR}\installshield.exe"
!insertmacro MUI_DEFAULT MUI_UI_COMPONENTSPAGE_NODESC "${MUI_SKIN_DIR}\installshield_nodesc.exe"

!insertmacro MUI_DEFAULT MUI_WELCOMEFINISHPAGE_BITMAP "${MUI_SKIN_DIR}\LeftBranding.bmp"
!insertmacro MUI_DEFAULT MUI_HEADERIMAGE_BITMAP "${MUI_SKIN_DIR}\Header.bmp"
!insertmacro MUI_DEFAULT MUI_BOTTOMIMAGE_BITMAP "${MUI_SKIN_DIR}\Bottom.bmp"

!insertmacro MUI_DEFAULT MUI_TEXT_COLOR FFFFFF
!insertmacro MUI_DEFAULT MUI_TEXT_BGCOLOR 3D66AB




!insertmacro MUI_UNSET MUI_SKIN_DIR
!verbose pop
!else
	!warning `MUI_EXPERIENCE_SKIN already defined!`
!endif
