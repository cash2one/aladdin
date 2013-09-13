OutFile services.exe
Section
  Services::IsProcessUserAdministrator
  Pop $0
  MessageBox MB_OK|MB_ICONINFORMATION 'Admin? $0'
  Services::IsServiceRunning 'beep'
  Pop $0
  MessageBox MB_OK|MB_ICONINFORMATION 'Running? $0'
  Services::IsServiceInstalled 'beep'
  Pop $0
  MessageBox MB_OK|MB_ICONINFORMATION 'Installed? $0'
  Services::RemoveLogonAsAService 'username'
  Pop $0
  MessageBox MB_OK|MB_ICONINFORMATION 'Removed? $0'
  Services::GrantLogonAsAService 'username'
  Pop $0
  MessageBox MB_OK|MB_ICONINFORMATION 'Granted? $0'
  Services::HasLogonAsAService 'username'
  Pop $0
  MessageBox MB_OK|MB_ICONINFORMATION 'Has Grant? $0'
  Services::SendServiceCommand 'stop' 'beep'
  Pop $0
  MessageBox MB_OK|MB_ICONINFORMATION 'Stopped? $0'
SectionEnd
