# coding=UTF-8
"""
@author    thomas
@date    2013-08-24
@desc
    configuration file
@change
    init --------------------------------- 2013.08.24
    add aladdin support ------------------ 2013.09.06
"""

#exe
curl_exe = '..\\tools\\bin\\curl.exe'
wget_exe = '..\\tools\\bin\\wget.exe'
wget_args = ' -nH --cut-dirs=1 '

baidusd_nsis_exe = '..\\tools\\bdnsis\\makensis.exe'
baidusd_nsis_nobind_exe = '..\\tools\\bdnsis_nobind\\makensis.exe'
qqmgr_nsis_exe = '..\\tools\\qqnsis\\makensis.exe'
qqmgr_nsis_nobind_exe = '..\\tools\\qqnsis_nobind\\makensis.exe'

extract_icon_exe = '..\\tools\\bin\\extracticon.exe'

#config files
baidusd_packinfo_file = '..\\info\\packinfo_baidusd.txt'
qqmgr_packinfo_file = '..\\info\\packinfo_qqmgr.txt'
packdetail_file = '..\\info\\packdetail.txt'

aladdin_xml_full = '..\\info\\pack_all_1.xml'
aladdin_xml_daily = '..\\info\\pack_today_1.xml'

packinfo_aladdin_file = '..\\info\\packinfo_aladdin.txt'

#folders
package_folder = '..\\output\\packages\\'
aladdin_package_folder = '..\\output\\aladdin\\packages\\'
installer_folder = '..\\output\\installers\\'
aladdin_installer_folder= '..\\output\\aladdin\\installers\\'
ico_folder = '..\\output\\ico\\'
aladdin_ico_folder = '..\\output\\aladdin\\ico\\'

baidusd_res_folder = '..\\res\\baidusd'
qqmgr_res_folder = '..\\res\\qqmgr'
nobind_res_folder = '..\\res\\nobind'

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

watchdog_notify_list = [
                        'D:\\autopack\\info\\',
                        'D:\\autopack\\res\\baidusd\\',
                        'D:\\autopack\\res\\nobind\\',
                        'D:\\autopack\\res\\qqmgr\\',
                        'D:\\autopack\\tools\\bdnsis\\',
                        'D:\\autopack\\tools\\bdnsis_nobind\\',
                        'D:\\autopack\\tools\\qqnsis\\',
                        'D:\\autopack\\tools\\qqnsis_nobind\\',
                        ]

#wget -r -nH --cut-dirs=1 ftp://10.52.175.51:8021/softs/ -P . --ftp-user=soft_mgr_edit --ftp-password=soft_mgr_pass
