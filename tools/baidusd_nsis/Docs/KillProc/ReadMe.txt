KillProcDLL ?003 by DITMan, based upon the KILL_PROC_BY_NAME function programmed by Ravi, reach him at: http://www.physiology.wisc.edu/ravi/


-> 介绍

  这个插件的唯一功能就是关闭任何正在运行的进程，不需要知道 Class 名，也不需要知道 Windows API TerminateProcess 或 ExitProcess 使用的窗口句柄，你只需要知道可执行文件名 .exe 文件即可。

    KillProc "可执行文件名.exe"

  参数 "可执行文件名.exe" 是通过堆栈传递的，并且返回值将会保存在 $R0 变量里。

返回值为下列之一:

   0   = 进程未能成功终结
   603 = 京城当前没有运行
   604 = 没有终结进程的权限
   605 = 无法载入 PSAPI.DLL
   602 = 由于其它原因而无法终结进程
   606 = 无法确定系统类型
   607 = 不支持的操作系统
   632 = 无效的进程名
   700 = 无法从 PSAPI.DLL 获得程序地址
   701 = 无法获取进程列表，EnumProcesses 失败
   702 = 无法载入 KERNEL32.DLL
   703 = 无法从 KERNEL32.DLL 获得程序地址
   704 = CreateToolhelp32Snapshot 失败


-> 使用

  使用如下方式来调用:

    KillProcDLL::KillProc "可执行文件名.exe"

或

     ; NSIS 2.0 以前的版本
    SetOutPath $TEMP
    GetTempFileName $8
    File /oname=$8 KillProcDLL.dll
    Push "可执行文件名.exe"
    CallInstDLL KillProc

  如果需要的话可以随后检测 $R0 返回值


-> 警告:
  根据 MSDN (MicroSoft Developers Network):
  
  TerminateProcess 是用来强制进程无条件退出的函数。请仅在极端的条件下才使用它。如果使用了 TerminateProces 而不是 ExitProcess 的话，动态链接库的全局数据维持状态将可能导致危险。

  所以这个插件请仅在最后逼不得已的关头才使用它 :)


-> 版权所有和所有的资源:

  The original source file for the KILL_PROC_BY_NAME function is provided, the file is: exam28.cpp, and it MUST BE in this zip file.

  You can redistribute this archive if you do it without changing anything on it, otherwise you're NOT allowed to do so.

  You may use this source code in any of your projects, while you keep all the files intact, otherwise you CAN NOT use this code.


-> 联系信息:

My homepage:
   http://petra.uniovi.es/~i6948857/index.php


-> 致谢:

  First of all, thanks to Ravi for his great function...
  Then all the winamp.com forums people who helped me doing this (kichik, Joost Verburg, Afrow UK...)
  Last but not least, I want to devote this source code to my Girl, Natalia... :)



Compiled in La Felguera, Spain, June-7th-2003
while listening to 'The Cure - Greatest Hits'
(in Winamp 2.91, of course :D)

?EOF- 