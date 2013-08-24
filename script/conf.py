# coding=UTF-8
"""
@author    thomas
@date    2013-08-24
@desc
    configuration file
@change
    init --------------------------------- 2013.08.24
    
"""

#exe
curl_exe = '..\\tools\\bin\\curl.exe'
wget_exe = '..\\tools\\bin\\wget.exe'
wget_args = ' -nH --cut-dirs=1 '
baidusd_nsis_exe = '..\\tools\\baidusd_nsis\\makensis.exe'

#config files
packinfo_file = '..\\info\\packinfo.txt'

#folders
package_folder = '..\\output\\packages\\'
installer_folder = '..\\output\\installers\\'
res_folder = '..\\res\\baidusd'
task_pool_folder = '..\\taskpool\\'
task_pool_nsis_folder = '..\\taskpool\\nsis\\'

#ftp config
ftp_host = 'ftp://10.52.175.51'
ftp_port = '8021'
ftp_user = 'soft_mgr_edit'
ftp_password = 'soft_mgr_pass'
ftp_subdir = '/softs/'

ftp_host_old = 'ftp://qa1.basic.baidu.com'
ftp_port_old = '8021'
ftp_user_old = 'soft_mgr_edit'
ftp_password_old = 'soft_mgr_pass'
ftp_subdir_old = '/softs/'

#wget -r -nH --cut-dirs=1 ftp://10.52.175.51:8021/softs/ -P . --ftp-user=soft_mgr_edit --ftp-password=soft_mgr_pass
