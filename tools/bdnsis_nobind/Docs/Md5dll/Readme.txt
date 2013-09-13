计算文件或字串的 MD5 校验和。
NSIS 2.0 以上经过测试


来自 RSA Data Security, Inc. MD5 Message-Digest 算法

[Md5Dll]
Matthew "IGx89" Lieder
  -Original plugin Author

Sunjammer (12th May 2002)
  -Original usage notes and example script 

[Md5Dll.0.1]
KJD (2004)
  -Modified to reduce size and use exdll.h
   (reduced to about 6KB uncompressed, by removing CRTL dependency)

[Md5dll.0.2]
Davy Durham (2004)
  -MD5.cpp fix (correct for loop used to replace memset, exceeded bounds)

[Md5dll.0.3]
Shengalts Aleksander aka Instructor (2005)
  -New command: "GetMD5Random"
  -Changed names: "GetFileMD5" -> "GetMD5File", "GetMD5" -> "GetMD5String"
  -Fixed: string length error

[Md5dll.0.4]
KJD (2005)
  -Added dual name to exports for backwards compatibility


--------------------------------

使用:

Push $1 ;字串
CallInstDll "md5dll" GetMD5String
Pop $1 ;字串的 MD5 

-或者-

Push $1 ;文件名
CallInstDll "md5dll" GetMD5File
Pop $1 ;文件的 MD5

--------------------------------

NSIS 2.0 以上的版本用法例子

OutFile "md5test.exe"
Section ""
  #生成字串的 MD5 
  md5dll::GetMD5String "md5me"
  Pop $0
  DetailPrint "md5: [$0]"

  #生成文件的 MD5
  md5dll::GetMD5File "${NSISDIR}\makensis.exe"
  Pop $0
  DetailPrint "md5: [$0]"

  #生成随机的 MD5
  md5dll::GetMD5Random
  Pop $0
  DetailPrint "md5: [$0]"
SectionEnd
