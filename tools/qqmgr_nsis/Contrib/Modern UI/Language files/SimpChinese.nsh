;NSIS Modern User Interface - Language File
;Compatible with Modern UI 1.68

;Language: 'Chinese (Simplified)' (2052)
;Translator: Kii Ali <kiiali@cpatch.org>
;Revision date: 2003-12-29
;Revision date: 2004-11-27
;--------------------------------

!insertmacro MUI_LANGUAGEFILE_BEGIN "SimpChinese"

  !define MUI_LANGNAME "Chinese (Simplified)" ;(以语言本身的方式，写下语言名称) Use only ASCII characters (if this is not possible, use the English name)
  
  !define MUI_TEXT_WELCOME_INFO_TITLE "欢迎使用 $(^NameDA) 安装向导"
  !define MUI_TEXT_WELCOME_INFO_TEXT "这个向导将指引您完成 $(^NameDA) 的安装进程。\r\n\r\n在开始安装之前，建议先关闭其他所有应用程序。这将允许安装程序更新指定的系统文件，而不需要重新启动您的计算机。\r\n\r\n$_CLICK"
  
  !define MUI_TEXT_LICENSE_TITLE "许可协议"
  !define MUI_TEXT_LICENSE_SUBTITLE "在安装 $(^NameDA) 之前，请仔细阅读许可协议。"
  !define MUI_INNERTEXT_LICENSE_TOP "要阅读许可协议的其余部分，请按 Page Down 往下翻页。"
  !define MUI_INNERTEXT_LICENSE_BOTTOM "如果您接受许可协议，点击“我同意”继续安装。如果您选择“取消”，安装程序将会关闭。您必须接受协议才能安装 $(^NameDA) 。"
  !define MUI_INNERTEXT_LICENSE_BOTTOM_CHECKBOX "如果您接受许可协议，点击下方的单选框。您必须接受协议才能安装 $(^NameDA)。$_CLICK"
  !define MUI_INNERTEXT_LICENSE_BOTTOM_RADIOBUTTONS "如果您接受许可协议，选择下方第一个选项。您必须接受协议才能安装 $(^NameDA)。$_CLICK"

  !define MUI_TEXT_COMPONENTS_TITLE "选择组件"
  !define MUI_TEXT_COMPONENTS_SUBTITLE "选择 $(^NameDA) 当中您想要安装的功能。"
  !define MUI_INNERTEXT_COMPONENTS_DESCRIPTION_TITLE "描述"
  !ifdef NSIS_CONFIG_COMPONENTPAGE_ALTERNATIVE
	!define MUI_INNERTEXT_COMPONENTS_DESCRIPTION_INFO "鼠标点击组件，便可见到它的描述。"
  !else
	!define MUI_INNERTEXT_COMPONENTS_DESCRIPTION_INFO "移动您的鼠标指针到组件之上，便可见到它的描述。"
  !endif
  
  !define MUI_TEXT_DIRECTORY_TITLE "选择安装位置" 
  !define MUI_TEXT_DIRECTORY_SUBTITLE "选择 $(^NameDA) 要安装的文件夹。"

  !define MUI_TEXT_INSTALLING_TITLE "正在安装"
  !define MUI_TEXT_INSTALLING_SUBTITLE "$(^NameDA) 正在安装，请等候..."
  
  !define MUI_TEXT_FINISH_TITLE "安装完成"
  !define MUI_TEXT_FINISH_SUBTITLE "安装程序已成功运行完毕。"
  
  !define MUI_TEXT_ABORT_TITLE "安装己中止"
  !define MUI_TEXT_ABORT_SUBTITLE "安装程序并未成功运行完毕。"
  
  !define MUI_BUTTONTEXT_FINISH "完成(&F)"
  !define MUI_TEXT_FINISH_INFO_TITLE "完成 $(^NameDA) 安装向导"
  !define MUI_TEXT_FINISH_INFO_TEXT "$(^NameDA) 已在您的系统安装。\r\n单击 [完成(F)] 关闭此向导。"
  !define MUI_TEXT_FINISH_INFO_REBOOT "您的系统需要重新启动，以便完成 $(^NameDA) 的安装。现在要重新启动吗？"
  !define MUI_TEXT_FINISH_REBOOTNOW "是，现在重新启动(&Y)"
  !define MUI_TEXT_FINISH_REBOOTLATER "否，我稍后再自行重新启动(&N)"
  !define MUI_TEXT_FINISH_RUN "运行 $(^NameDA)(&R)"
  !define MUI_TEXT_FINISH_SHOWREADME "显示说明文件(&M)"
  
  !define MUI_TEXT_STARTMENU_TITLE "选择开始菜单文件夹"
  !define MUI_TEXT_STARTMENU_SUBTITLE "选择开始菜单文件夹，用于程序的快捷方式。"
  !define MUI_INNERTEXT_STARTMENU_TOP "选择开始菜单文件夹，以便创建程序的快捷方式。您也可以输入名称，创建新文件夹。"
  !define MUI_INNERTEXT_STARTMENU_CHECKBOX "不要创建快捷方式(&N)"
  
  !define MUI_TEXT_ABORTWARNING "您确实要退出 $(^Name) 安装程序？"
  

  !define MUI_UNTEXT_WELCOME_INFO_TITLE "欢迎使用 $(^NameDA) 卸载向导"
  !define MUI_UNTEXT_WELCOME_INFO_TEXT "这个向导将全程指引您进行 $(^NameDA) 的卸载进程。\r\n\r\n在开始卸载之前，确认 $(^NameDA) 并未运行。\r\n\r\n$_CLICK"
 
  !define MUI_UNTEXT_CONFIRM_TITLE "卸载 $(^NameDA)"
  !define MUI_UNTEXT_CONFIRM_SUBTITLE "从您的计算机中卸载 $(^NameDA) 。"
  
  !define MUI_UNTEXT_LICENSE_TITLE "许可协议"
  !define MUI_UNTEXT_LICENSE_SUBTITLE "在卸载 $(^NameDA) 之前，请先阅读许可协议。"
  !define MUI_UNINNERTEXT_LICENSE_BOTTOM "如果您接受许可协议，点击“我同意”继续卸载。如果您选择“取消”，安装程序将会关闭。您必须接受协议才能卸载 $(^NameDA) 。"
  !define MUI_UNINNERTEXT_LICENSE_BOTTOM_CHECKBOX "如果您接受许可协议，点击下方的单选框。您必须接受协议才能卸载 $(^NameDA)。$_CLICK"
  !define MUI_UNINNERTEXT_LICENSE_BOTTOM_RADIOBUTTONS "如果您接受许可协议，选择下方第一个选项。您必须接受协议才能卸载 $(^NameDA)。$_CLICK"
  
  !define MUI_UNTEXT_COMPONENTS_TITLE "选择组件"
  !define MUI_UNTEXT_COMPONENTS_SUBTITLE "选择 $(^NameDA) 当中您想要卸载的功能。"
  
  !define MUI_UNTEXT_DIRECTORY_TITLE "选择卸载位置" 
  !define MUI_UNTEXT_DIRECTORY_SUBTITLE "选择 $(^NameDA) 要卸载的文件夹。"

  !define MUI_UNTEXT_UNINSTALLING_TITLE "正在卸载"
  !define MUI_UNTEXT_UNINSTALLING_SUBTITLE "$(^NameDA) 正在卸载，请等候..."
    
  !define MUI_UNTEXT_FINISH_TITLE "卸载已完成"
  !define MUI_UNTEXT_FINISH_SUBTITLE "卸载程序已成功运行完毕。"
  
  !define MUI_UNTEXT_ABORT_TITLE "卸载已中止"
  !define MUI_UNTEXT_ABORT_SUBTITLE "卸载程序并未成功运行完毕。"
  
  !define MUI_UNTEXT_FINISH_INFO_TITLE "正在完成 $(^NameDA) 卸载向导"
  !define MUI_UNTEXT_FINISH_INFO_TEXT "$(^NameDA) 已从您的计算机卸载。\r\n\r\n点击“完成”关闭来向导。"
  !define MUI_UNTEXT_FINISH_INFO_REBOOT "计算机需要重新启动，以便完成 $(^NameDA) 的卸载。现在想要重新启动吗？"

  !define MUI_UNTEXT_ABORTWARNING "您确实要退出 $(^Name) 的卸载吗？"  
  
!insertmacro MUI_LANGUAGEFILE_END
