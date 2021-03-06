
!include ..\soft.nsh

Name "AladinDemo"
OutFile "AladinDemo.exe"



RequestExecutionLevel admin
#RequestExecutionLevel user

SetCompressor  LZMA
Icon ..\setup.ico

Page instfiles  "" showwindow
var repair

Function showwindow
;	绘制界面：显示准备中...	
	AladdinInstallHelper::CreateAladdinWnd /NOUNLOAD
    BDMSDWrench::CallRepair /NOUNLOAD
    pop $repair
    AladdinInstallHelper::OnRepairResult /NOUNLOAD $repair
FunctionEnd
;第三方软件释放地址 %temp%\TimeStamp\filename
Var str3rdPath 

Function .onInit
	InitPluginsDir
;拷贝所需文件
	SetOutPath "$PLUGINSDIR"
	File "..\BDMSkin.dll"	
	File "..\AladdinWnd.zip"
	File "..\task.xml"
;	File "..\bind.xml"
	File "..\logo.png"
	File "..\setup.ico"


	File "..\BDMDownload.dll"
	File "..\dl.dll"
	File "..\BDMNet.dll"
	File "..\BDMReport.dll"
	File /oname=$PLUGINSDIR\st.tmp "..\st.dll"
	#File /oname=$PLUGINSDIR\bind.tmp "..\bind.exe"

;得到软件释放地址
	AladdinInstallHelper::GetUpackPath /NOUNLOAD "$PLUGINSDIR" 
	pop $str3rdPath
FunctionEnd

Section
  SetOverwrite try
  File  /oname=$str3rdPath ..\softsetup.exe
;通知界面：软件释放完毕，可以 立即安装
	AladdinInstallHelper::UpackComplete /NOUNLOAD  
SectionEnd

 
