

x18servicesV0.1.zip
-------------------

Version 0.0, first alpha, 10th June 2002 by Ximon Eighteen.
Version 0.1, added GetServiceNameFromDisplayName(), 5th June 2003 by Ximon Eighteen.


这是什么？
----------------------

如果你曾经需要启动、停止、移除或其它操作 Windows NT 服务你就会发现这是多么的有用。这各插件所提供的一系列函数就可以用于实现上面的操作。

如果你不知道上面说的是什么那么你肯定不需要它，很简单。

大部分代码基于微软知识文库和 MSDN Platform SDK 文档上找到的信息。

在相当长的时间里我已经没有发布过任何作品了，所以如果我忘了什么或者搞糟了什么请务必告诉我。

把你的意见、建议、BUG 修正发送到 ximon_eighteen@3b2.com (用英文)。

我会尽我所能的回答任何的问题，但我不能对使用可能产生的问题负责，请自行承担风险。如果你什么地方搞砸了我会尽力的帮助你，但是我认为这很可能是 RPWT ;-)

---

Ximon Eighteen aka Sunjammer


已知的 BUG、问题 :
-------------------

  - 我认为 SendServiceCommand 并不支持真正的删除操作
    所以，应该把它作为分开的函数？
  - 没有其它的已知问题。


函数文档 : 
---------------------

GetServiceNameFromDisplayName:
  描述: 在所有服务里查找服务的名称，完整的名称就如你在服务控制面板里看到的那样，包含已给出的名称或名称片断 (不区分大小写)。     输入: 把显示的名称或名称片断压入堆栈。
  返回: 一个或多个值返回到堆栈里。第一个应该是找到匹配的数量。第二个应该是未找到的原因或者第一个匹配。第三个或更多的是剩余的一直到匹配的数量为止。
  使用: 参考 FindServices.nsi。

IsProcessUserAdministrator:
  描述: 找出用户 (当前进程的所有者) 是不是属于本地计算机上的管理员组 (不是在域上)。
  输入: 把服务名称压入堆栈。
  返回: Pop 结果到堆栈。如果没什么问题结果应该是 Yes 或 No，如果出现了问题则返回失败的原因。
  使用: 像这样 -
        Services::IsProcessUserAdministrator
        Pop $0
        ; $0 现在包含 Yes 或 No 或错误描述

HasLogonAsAService:
  描述: 找出当前用户 (当前进程的所有者) 是否拥有 LSA (Local Security Authority) 权限 SeServiceLogonRight。
  返回: Pop 结果到堆栈。如果没什么问题结果应该是 Yes 或 No，如果出现了问题则返回失败的原因。
  使用: 像这样 -
        Services::HasLogonAsAService '3B2\Ximon_Eighteen'
        Pop $0
        ; $0 现在包含 Yes 或 No 或错误描述

GrantLogonAsAService:
  描述: 给予当前用户 (当前进程的所有者) LSA (Local Security Authority) 权限 SeServiceLogonRight。
  返回: Pop 结果到堆栈。如果没什么问题结果应该是 OK，如果出现了问题则返回失败的原因。
  使用: 像这样 -
        Services::GrantLogonAsAService '3B2\Ximon_Eighteen'
        Pop $0
        ; $0 现在包含 OK 或错误描述

RemoveLogonAsAService:
  描述: 拒绝当前用户 (当前进程的所有者) LSA (Local Security Authority) 权限 SeServiceLogonRight。
  返回: Pop 结果到堆栈。如果没什么问题结果应该是 OK，如果出现了问题则返回失败的原因。
  使用: 像这样 -
        Services::RemoveLogonAsAService '3B2\Ximon_Eighteen'
        Pop $0
        ; $0 现在包含 OK 或错误描述

IsServiceInstalled:
  描述: 找出服务是否已安装。
  输入: 把服务的名称压入堆栈。
  返回: Pop 结果到堆栈。如果没什么问题结果应该是 Yes 或 No，如果出现了问题则返回失败的原因。
  使用: 像这样 -
        Services::IsServiceInstalled 'MyServiceName'
        Pop $0
        ; $0 现在包含 Yes 或 No 或错误描述

IsServiceRunning
  描述: 找出服务是否已安装并运行。
  输入: 把服务的名称压入堆栈。
  返回: Pop 结果到堆栈。如果没什么问题结果应该是 Yes 或 No，如果出现了问题则返回失败的原因。
  使用: 像这样 -
        Services::IsServiceRunning 'MyServiceName'
        Pop $0
        ; $0 现在包含 Yes 或 No 或错误描述

SendServiceCommand:
  描述: 发送一个命令 (Start, Stop, Pause, Continue 或 Delete) 给服务控制管理器 (SCM)。
  输入: 把要发送的命令压入堆栈。
  输入: 把服务的名称压入堆栈。
  返回: Pop 结果到堆栈。如果没什么问题结果应该是 OK，如果出现了问题则返回失败的原因。
  使用: 像这样 -
        Services::SendServiceCommand 'start' 'MyServiceName'
        Pop $0
        StrCmp $0 'Ok' success
        MessageBox MB_OK|MB_ICONSTOP '发送命令失败，原因: $0'
        Abort
        success:
