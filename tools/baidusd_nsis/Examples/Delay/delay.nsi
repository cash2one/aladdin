Name                 "Delay"
OutFile              "demo.exe"
Caption              "Delay the next button"
SetCompressor        lzma
ShowInstDetails      show

!AddPluginDir        ".\"
!include             MUI.nsh

!define MUI_CUSTOMFUNCTION_ABORT OnUserAbort

!define MUI_PAGE_CUSTOMFUNCTION_SHOW LicensePage
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE LicensePageLeave
!insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_LANGUAGE English

Section
	DetailPrint "Do nothing..."
SectionEnd


Function LicensePage
	GetDlgItem $0 $HWNDPARENT 1
	
	;NOTE: Plugins must be keep loaded while count, else installer may crash. (학션학션)
	;SYNTAX: Delay::DelayButton /NOUNLOAD HWND DELAY_COUNT DISPLAY_STRING
	;left DISPLAY_STRING empty to use default string
	Var /GLOBAL PageDone
	IntCmp $PageDone 1 free
	Delay::DelayButton /NOUNLOAD $0 5 ""
	StrCpy $PageDone 1
	Goto end
	free:
	Delay::Free
	end:
FunctionEnd

Function LicensePageLeave
	;Case installer unload the plugins after this command
	Delay::Free
FunctionEnd

Function OnUserAbort
	;If user press Cancel button when count not finish.
	;Case installer unload the plugins after this command
	Delay::Free
FunctionEnd


