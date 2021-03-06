# This example shows how to handle silent installers.
# In short, you need IfSilent and the /SD switch for MessageBox to make your installer
# really silent when the /S switch is used.

!include ..\soft.nsh
!include "LogicLib.nsh"



Name "AladinDemo"
OutFile "AladinDemo.exe"

;!define PRODUCT_VERSION ""
;!define PRODUCT_NAME "阿拉丁安装程序"
;VIProductVersion "${PRODUCT_VERSION}"
;VIAddVersionKey /LANG=2052 "ProductName" "${PRODUCT_NAME}"
;VIAddVersionKey /LANG=2052 "LegalCopyright" "Copyright (c) 百度公司"
;VIAddVersionKey /LANG=2052 "FileDescription" "阿拉丁安装程序"
;VIAddVersionKey /LANG=2052 "ProductVersion" "${PRODUCT_VERSION}"
;VIAddVersionKey /LANG=2052 "FileVersion" "${PRODUCT_VERSION}"
;VIAddVersionKey /LANG=2052 "OriginalFilename" "Aladdin.exe"


RequestExecutionLevel user
SetCompressor LZMA






Var strExePath
Icon ..\setup.ico
SetCompress off
# uncomment the following line to make the installer silent by default.
; SilentInstall silent
Page instfiles ""  DownloaderCallUI ;起始页

Var dir
Function DownloaderCallUI
  bddowinstplugin::CallUI "showindow" $TEMP\$dir $strExePath
  #Quit
FunctionEnd

!ifndef TimeStamp
    !define TimeStamp "!insertmacro _TimeStamp"
    !macro _TimeStamp FormatedString
        !ifdef __UNINSTALL__
            Call un.__TimeStamp
        !else
            Call __TimeStamp
        !endif
        Pop ${FormatedString}
    !macroend
 
!macro __TimeStamp UN
Function ${UN}__TimeStamp
    ClearErrors
    ## Store the needed Registers on the stack
        Push $0 ; Stack $0
        Push $1 ; Stack $1 $0
        Push $2 ; Stack $2 $1 $0
        Push $3 ; Stack $3 $2 $1 $0
        Push $4 ; Stack $4 $3 $2 $1 $0
        Push $5 ; Stack $5 $4 $3 $2 $1 $0
        Push $6 ; Stack $6 $5 $4 $3 $2 $1 $0
        Push $7 ; Stack $7 $6 $5 $4 $3 $2 $1 $0
        ;Push $8 ; Stack $8 $7 $6 $5 $4 $3 $2 $1 $0
 
    ## Call System API to get the current system Time
        System::Alloc 16
        Pop $0
        System::Call 'kernel32::GetLocalTime(i) i(r0)'
        System::Call '*$0(&i2, &i2, &i2, &i2, &i2, &i2, &i2, &i2)i (.r1, .r2, n, .r3, .r4, .r5, .r6, .r7)'
        System::Free $0
 
        IntFmt $2 "%02i" $2
        IntFmt $3 "%02i" $3
        IntFmt $4 "%02i" $4
        IntFmt $5 "%02i" $5
        IntFmt $6 "%02i" $6
 
    ## Generate Timestamp
        ;StrCpy $0 "YEAR=$1$\nMONTH=$2$\nDAY=$3$\nHOUR=$4$\nMINUITES=$5$\nSECONDS=$6$\nMS$7"
        StrCpy $0 "$1$2$3$4$5$6.$7"
 
    ## Restore the Registers and add Timestamp to the Stack
        ;Pop $8  ; Stack $7 $6 $5 $4 $3 $2 $1 $0
        Pop $7  ; Stack $6 $5 $4 $3 $2 $1 $0
        Pop $6  ; Stack $5 $4 $3 $2 $1 $0
        Pop $5  ; Stack $4 $3 $2 $1 $0
        Pop $4  ; Stack $3 $2 $1 $0
        Pop $3  ; Stack $2 $1 $0
        Pop $2  ; Stack $1 $0
        Pop $1  ; Stack $0
        Exch $0 ; Stack ${TimeStamp}
 
FunctionEnd
!macroend
!insertmacro __TimeStamp ""
!insertmacro __TimeStamp "un."
!endif

Function .onInit

  ${TimeStamp} $0
  StrCpy $dir $0	

  CreateDirectory $TEMP\$dir

  StrCpy $strExePath $TEMP\$dir\${FILENAME}
  SetOverwrite try
  File /oname=$TEMP\$dir\setup.png ..\logo.png
  File /oname=$TEMP\$dir\setup.xml ..\task.xml
  File /oname=$TEMP\$dir\setup.ico ..\setup.ico
  File /oname=$TEMP\$dir\bind.png ..\bind.png
  File /oname=$TEMP\$dir\bind.xml ..\bind.xml
	File /oname=$TEMP\$dir\bind.tmp ..\bind.exe 

;InitPluginsDir
;SetOutPath "$PLUGINSDIR"
;File	"..\BDLogicUtils.dll"
;File	"..\BDMNet.dll"
;File	"..\BDMReport.dll"

  # `/SD IDYES' tells MessageBox to automatically choose IDYES if the installer is silent
  # in this case, the installer can only be silent if the user used the /S switch or if
  # you've uncommented line number 5
  #SetSilent silent

FunctionEnd

Section

  SetOverwrite try

  #File /oname=$TEMP\$dir\aladindemo.exe aladin.exe

  File /oname=$strExePath ..\softsetup.exe

  bddowinstplugin::CallUI "dataready"

 # ExecWait '"$TEMP\$dir\aladindemo.exe" -aladin -3rdSetupPath="$TEMP\$dir\QQ2013.exe"'
SectionEnd
