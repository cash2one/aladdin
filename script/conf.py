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

#url
url_full_xml = 'http://adminsoft.hao123.com:8080/source/api/pack_all_1.xml'
url_daily_xml = 'http://adminsoft.hao123.com:8080/source/api/pack_today_1.xml'

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

aladdin_archive_folder = '\\\\10.52.174.35\\public\\aladdin\\installers\\'
aladdin_update_pool_folder = '..\\output\\aladdin\\installers\\update\\'
aladdin_update_list_file = '..\\output\\aladdin\\installers\\update_list.txt'

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
                        'd:\\autopack\\info\\',
                        'd:\\autopack\\res\\baidusd\\',
                        'd:\\autopack\\res\\nobind\\',
                        'd:\\autopack\\res\\qqmgr\\',
                        'd:\\autopack\\tools\\bdnsis\\',
                        'd:\\autopack\\tools\\bdnsis_nobind\\',
                        'd:\\autopack\\tools\\qqnsis\\',
                        'd:\\autopack\\tools\\qqnsis_nobind\\',
                        ]
watchdog_notify_ready_file = 'd:\\autopack\\info\\pack_ready.txt'
ready_string = 'i am ready'
not_ready_string = 'i am not ready'

#wget -r -nH --cut-dirs=1 ftp://10.52.175.51:8021/softs/ -P . --ftp-user=soft_mgr_edit --ftp-password=soft_mgr_pass
 
