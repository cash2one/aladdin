!ifndef MUI_EXPERIENCE_SKIN
!verbose push
!verbose 3
!define MUI_EXPERIENCE_SKIN

!insertmacro MUI_UNSET MUI_SKIN_DIR
!define MUI_SKIN_DIR "${MUI_XP_DIR}\Skins\InstallSpider"

;!define NO_HEADER_TEXT
!define NO_BOTTOMIMAGE
!define NO_LEFTIMAGE
!define NO_WIZARDIMAGE
!define NO_DEFAULT_TEXT_COLOR

!insertmacro MUI_DEFAULT MUI_UI "${MUI_SKIN_DIR}\InstallSpider.exe"
!insertmacro MUI_DEFAULT MUI_UI_COMPONENTSPAGE_NODESC "${MUI_SKIN_DIR}\InstallSpider_nodesc.exe"

!insertmacro MUI_DEFAULT MUI_HEADERIMAGE_BITMAP "${MUI_SKIN_DIR}\LeftBranding.bmp"
!insertmacro MUI_DEFAULT MUI_HEADERIMAGE_UNBITMAP "${MUI_SKIN_DIR}\UnLeftBranding.bmp"

!insertmacro MUI_DEFAULT MUI_ICON "${MUI_SKIN_DIR}\install.ico"
!insertmacro MUI_DEFAULT MUI_UNICON "${MUI_SKIN_DIR}\uninstall.ico"
!insertmacro MUI_DEFAULT MUI_COMPONENTSPAGE_CHECKBITMAP "${MUI_SKIN_DIR}\checks.bmp"
!insertmacro MUI_DEFAULT MUI_WELCOMEFINISHPAGE_INI "${MUI_SKIN_DIR}\ioSpecial.ini"

!macro MUI_WELCOME_MACROPRE
    !insertmacro MUI_INSTALLOPTIONS_WRITE "ioSpecial.ini" "Field 2" Top 10
    !insertmacro MUI_INSTALLOPTIONS_WRITE "ioSpecial.ini" "Field 2" Bottom 22

    !insertmacro MUI_INSTALLOPTIONS_WRITE "ioSpecial.ini" "Field 3" Top 34
!macroend

!macro MUI_WELCOME_MACROSHOW
    GetDlgItem $MUI_TEMP1 $MUI_HWND 1201
    CreateFont $MUI_TEMP2 $(^Font) $(^FontSize) 400
    SendMessage $MUI_TEMP1 ${WM_SETFONT} $MUI_TEMP2 0
!macroend

!macro MUI_FINISH_MACROPRE
    !insertmacro MUI_WELCOME_MACROPRE
!macroend

!macro MUI_FINISH_MACROSHOW
    !insertmacro MUI_WELCOME_MACROSHOW
    ;CreateFont $MUI_TEMP2 $(^Font) $(^FontSize) 400
    ;SendMessage $MUI_TEMP1 ${WM_SETFONT} $MUI_TEMP2 0
!macroend




!insertmacro MUI_UNSET MUI_SKIN_DIR
!verbose pop
!else
	!warning `MUI_EXPERIENCE_SKIN already defined!`
!endif
