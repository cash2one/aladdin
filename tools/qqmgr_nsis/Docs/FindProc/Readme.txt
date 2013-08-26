FindProcDLL ?003 by iceman_k (Sunil Kamath), based upon the FIND_PROC_BY_NAME function written by Ravi Kochhar (http://www.physiology.wisc.edu/ravi/)


1. 介绍

  这个插件可以根据可执行文件 .exe 来找出该进程是否在运行。

    FindProc "可执行文件名.exe"

  返回值保存在 $R0 变量里。 

返回值为下列之一:

   0   = 进程未找到
   1   = 找到进程
   605 = 无法搜索进程
   606 = 无法确定系统类型
   607 = 不支持的操作系统
   632 = 进程名称无效


2. 使用:

  只需要按下列方法来调用插件:

    FindProcDLL::FindProc "可执行文件名.exe"

或者

     ; NSIS 2.0 以前的语法
    SetOutPath $TEMP
    GetTempFileName $8
    File /oname=$8 FindProcDLL.dll
    Push "可执行文件名.exe"
    CallInstDLL FindProc

  $R0 将会保存返回值。

3. 版权所有:

  The original source file for the FIND_PROC_BY_NAME function is included in this distribution. The file name is: exam38.cpp, and it MUST BE in this zip file. Other than that, you may use or modify this source code as you wish in any of your projects. However, you MUST include this file as well as the exam38.cpp file if you are distributing the original or modified source to anyone or anywhere.

4. 致谢:
Ravi for the FIND_PROC_BY_NAME function.
DITMan for his KillProcDLL Manual NSIS Plugin which inspired this plugin.
