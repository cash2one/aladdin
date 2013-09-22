# coding=UTF-8
"""
@author thomas
@date	2013-04-12
@desc
	main configuration file
	
@brief
	
"""

import userconf

svn_url = 'http://s.a.iyuntian.com/client/'
svn_conf_file = './buildswitch/SVN.xml'
markup_conf_file = './buildswitch/MarkupCode.xml'

bdm_mail_file = '../output/mail/mail.txt'
bdkv_mail_file = '../output/mail/kvmail.txt'

buildver_headerfile = "../../basic/include/CommonInclude/BuildVer.h"
buildver_definefile = "../../basic/include/CommonInclude/BDMVersion.h"

#cerf_addr='m1-scm-cluster-test03.m1.baidu.com:8111'
#cerf_addr='m1-win2003k32-scm-winbuild05.vm.baidu.com'
cerf_addr='sign.baidu.com'
#cerf_addr='m1-win2003k32-scm-winbuild05.vm.baidu.com'
#cerf_addr='m1-scm-git03.m1.baidu.com:8008'
cerf_login_server='uuap.baidu.com'

local_cerf_addr = 'qa1.basic.baidu.com:8000'
local_cerf_url = '/zpadmin/api/monitor/json_get_sig_by_sig_baidu_com/liuheng/1qaz@WSX'

sign_file_exts='*.exe,*.dll'
sign_file_product=u'百度卫士'
kvsign_file_product=u'百度杀毒'
sign_conf_file='./buildswitch/Signature.xml'
kvsign_conf_file='./buildswitch/KVSignature.xml'

verify_log_file = '..\\output\\verifylog\\BinVerify.txt'
kvverify_log_file = '..\\output\\verifylog\\KVBinVerify.txt'

exist_verify_file = './verifylist/FileVerify.xml'
kvexist_verify_file = './verifylist/KVFileVerify.xml'

verify_md5_file = '..\\output\\verifylog\\installer_md5.txt'

verify_path = '../output/verifylog/'

checklog_file = "./conf/checklog.conf"
kvchecklog_file = "./conf/kvchecklog.conf"

debug_path='../../basic/Output/binDebug/'
kvdebug_path="../../basic/binDebug/"
debugList=["*.exe","*.dll","plugins","res","*.xml","*.png"]

bin_path='../../basic/Output/binRelease/'
kvbin_path='../../basic/KVOutput/binRelease/'
binList=["*.exe","*.dll","plugins","res","*.xml","*.png"]
pdbList=["*.pdb"]
logList=["*.log","*.txt"]

original_kvsetup_path = '../../basic/tools/kvsetup/'
original_setup_path = '../../basic/tools/setup/'
kvsetup_path='../output/kvsetup/'
setup_path='../output/setup/'
setupList=["*.exe"]

log_path="../output/err/"
kvlog_path="../output/kverr/"

ftp_default_archive = '\\\\10.52.174.35'

ftpPathNameR= '\\\\'+'10.52.174.35'+'\\' + 'public' + '\\' + 'DailyBuild' +'\\' 
ftpKVPathNameR= '\\\\'+'10.52.174.35'+'\\' + 'public' + '\\' + 'KVDailyBuild' +'\\' 
ftpVersionPathNameR = '\\\\'+'10.52.174.35'+'\\' + 'public' + '\\' + 'VersionBuild' +'\\'
ftpVersionKVPathNameR = '\\\\'+'10.52.174.35'+'\\' + 'public' + '\\' + 'KVVersionBuild' +'\\'

#The following two lines DO NOT have spelling errors,merging daily and custom builds
ftpCustomPathNameR = '\\\\'+'10.52.174.35'+'\\' + 'public' + '\\' + 'DailyBuild' +'\\'
ftpCustomKVPathNameR = '\\\\'+'10.52.174.35'+'\\' + 'public' + '\\' + 'KVDailyBuild' +'\\'

ftpPathNameD= '\\'+'Debug' +'\\'
ftpPathNameRR= '\\'+'Release' +'\\'
ftpPathNameLog= '\\'+'Log' +'\\'

buildIdFile="../../basic/tools/AutoBuild/buildId.txt"
kvBuildIdFile="../../basic/tools/AutoBuild/kvbuildId.txt"
versionBuildIdFile="../../basic/tools/AutoBuild/versionBuildId.txt"
kvVersionBuildIdFile="../../basic/tools/AutoBuild/kvVersionBuildId.txt"

#The following two lines DO NOT have spelling errors,merging daily and custom builds
customBuildIdFile="../../basic/tools/AutoBuild/buildId.txt"
kvCustomBuildIdFile="../../basic/tools/AutoBuild/kvbuildId.txt"

bdm_nsifile_daily="../../basic/Tools/SetupScript/BDM_setup.nsi"
bdm_nsifile_version="../../basic/Tools/SetupScript/BDM_setup.nsi"
bdm_nsifile_partial="../../basic/Tools/SetupScript/BDM_setup.nsi"
bdm_nsifile_buildline="../../basic/Tools/SetupScript/include/buildline.nsi"

bdkv_nsifile_daily="../../basic/Tools/KVSetupScript/BDKV_setup.nsi"
bdkv_nsifile_version="../../basic/Tools/KVSetupScript/BDKV_setup.nsi"
bdkv_nsifile_partial="../../basic/Tools/KVSetupScript/BDKV_setup.nsi"
bdkv_nsifile_buildline="../../basic/Tools/KVSetupScript/include/buildline.nsi"

bdm_netinstall_file="../../basic/Tools/BDMNetInstall/BDMNetInstall.nsi"
bdkv_netinstall_file="../../basic/Tools/KVNetInstall/KVNetInstall.nsi"
bdm_netinstall_silent_file="../../basic/Tools/BDMNetInstall/BDMNetInstall.nsi"
bdkv_netinstall_silent_file="../../basic/Tools/KVNetInstall/KVNetInstall.nsi"
bdm_install_silent_file="../../basic/Tools/SetupScript/include/BDM_Install.nsi"
bdkv_install_silent_file="../../basic/Tools/KVSetupScript/include/KV_Install.nsi"

fromaddr="liuheng@baidu.com"
toaddr=["liuheng@baidu.com"]

smtp_host="proxy-in.baidu.com"

ver_company_name = u'百度在线网络技术（北京）有限公司'
ver_legal_trademarks = u'Baidu'
ver_copyright = u'Copyright (C) 2013 Baidu Inc.'
ver_product_manager = u'百度卫士'
ver_product_antivirus = u'百度杀毒'

rclist_file = './conf/rcdef.xml'
kv_rclist_file = './conf/kvrcdef.xml'

svn_remote_info_file = '../output/svn/svn_remote.info'

mgr_official_sign_excluded_dir = ['..\\..\\basic\\output\\binrelease\\microsoft.vc80.atl\\',
								'..\\..\\basic\\output\\binrelease\\microsoft.vc80.crt\\',
                                '..\\..\\basic\\output\\binrelease\\vcredist_x86.exe',
                                '..\\..\\basic\\output\\binrelease\\uninst.exe',]

kv_official_sign_excluded_dir = ['..\\..\\basic\\kvoutput\\binrelease\\kav\\',
								'..\\..\\basic\\kvoutput\\binrelease\\kavdrivers\\',
								'..\\..\\basic\\kvoutput\\binrelease\\microsoft.vc80.atl\\',
								'..\\..\\basic\\kvoutput\\binrelease\\microsoft.vc80.crt\\',
                                '..\\..\\basic\\kvoutput\\binrelease\\bdmantivirus\\kavupdate\\',
                                '..\\..\\basic\\kvoutput\\binrelease\\uninst.exe',]

kv_load_sign_excluded_dir = ['..\\..\\basic\\kvoutput\\binrelease\\kav\\',
								'..\\..\\basic\\kvoutput\\binrelease\\kavdrivers\\',
								'..\\..\\basic\\kvoutput\\binrelease\\microsoft.vc80.atl\\',
								'..\\..\\basic\\kvoutput\\binrelease\\microsoft.vc80.crt\\',
                                '..\\..\\basic\\kvoutput\\binrelease\\bdmantivirus\\kavupdate\\',]

kvsign_excluded_dir = ['..\\..\\basic\\kvoutput\\binrelease\\kavdrivers\\udinstaller32.exe',
                      '..\\..\\basic\\kvoutput\\binrelease\\kavdrivers\\udinstaller64.exe',
                      '..\\..\\basic\\output\\binrelease\\vcredist_x86.exe',
                      '..\\..\\basic\\output\\binrelease\\uninst.exe',
                      '..\\..\\basic\\kvoutput\\binrelease\\uninst.exe',]

kvsign_kav_excluded_dir = ['..\\..\\basic\\kvoutput\\binrelease\\kavdrivers\\udinstaller32.exe',
                          '..\\..\\basic\\kvoutput\\binrelease\\kavdrivers\\udinstaller64.exe',
                          '..\\..\\basic\\output\\binrelease\\vcredist_x86.exe',
                          '..\\..\\basic\\output\\binrelease\\uninst.exe',
                          '..\\..\\basic\\kvoutput\\binrelease\\uninst.exe',]

mgr_verify_excluded_dir = ['..\\..\\basic\\output\\binrelease\\microsoft.vc80.atl\\',
						  '..\\..\\basic\\output\\binrelease\\microsoft.vc80.crt\\',
						  userconf.mgr_install_dir + 'microsoft.vc80.atl\\',
						  userconf.mgr_install_dir + 'microsoft.vc80.crt\\',]

kv_verify_excluded_dir = ['..\\..\\basic\\kvoutput\\binrelease\\kav\\',
						 '..\\..\\basic\\kvoutput\\binrelease\\kavdrivers\\',
						 '..\\..\\basic\\kvoutput\\binrelease\\microsoft.vc80.atl\\',
						 '..\\..\\basic\\kvoutput\\binrelease\\microsoft.vc80.crt\\',
                         '..\\..\\basic\\kvoutput\\binrelease\\bdmantivirus\\kavupdate\\',
                         userconf.kv_install_dir + 'kav\\',
                         userconf.kv_install_dir + 'kavdrivers\\',
                         userconf.kv_install_dir + 'microsoft.vc80.atl\\',
                         userconf.kv_install_dir + 'microsoft.vc80.crt\\',
                         userconf.kv_install_dir + 'bdmantivirus\\kavupdate\\',]

mgr_file_exist_excluded_dir = ['.pdb','.exp','.lib',]

kv_file_exist_excluded_dir = ['.pdb','.exp','.lib',]

#总的工程根目录
sln_root = '..\\..\\'
byp_bin_path = '.\\AutoBuild\\'

#每个sln的配置文件
bdkv_conf_files = {
	'commonlib':'BDMCommonLib',
	'commondll':'BDMCommonDll',
	'skin':'BDMSkin',
	'logicmisc':'BDMLogicMisc',
	'logicutils':'BDLogicUtils',
	'client':'BDMClient',
	'avcommon':'AVCommon',
	'filemon':'FileMon',
	'avhips':'AVHips',
	'drivermanager':'DriverManager',
	'sysrepair':'SYSRepair',
	'antivirus':'BDMAntiVirus',
	'bdkv':'BDKV',
	'bd0001':'BD0001',
	'defense':'SDWrench',
    'attack':'AttackDefense',
    'repair':'baiduRepair',
    'bdkitUtils':'BDKitUtils',
    'websafe':'WebSafe',
}

bdm_conf_files = {
	'commonlib':'BDMCommonLib',
	'commondll':'BDMCommonDll',
	'skin':'BDMSkin',
	'logicmisc':'BDMLogicMisc',
	'logicutils':'BDLogicUtils',
	'client':'BDMClient',
	'qmlib':'QMlib',
	'bdnd':'BDND',
	'syscleanerlib':'SYSCleanerLib',
	'luaVM':'SYSCleanerLuaVM',
	'syscleaner':'SYSCleaner',
	'sysaccelerator':'BDMSYSAccelerator',
	'soacceleratorlib':'BDMSOAcceleratorLib',
	'soacceleratorplugin':'BDMSOAcceleratorPlugin',
	'socleanerplugin':'BDMSOCleanerPlugin',
	'somanager':'BDMSOManager',
	'soshortcutplugin':'BDMSOShortcutPlugin',
	'swmanager':'BDMSWManager',
	'qmgarbagecleaner':'QMGarbageCleaner',
	'homepageplugins':'BDMHomePagePlugins',
	'mainframeplugins':'BDMMainFramePlugins',
	'main':'BDMMain',
    'trojanscan':'BDMTrojanScan',
    'antivirusGJ':'BDMAntiVirus_GJ',
    'drivermanager':'DriverManager',
    'avhips':'AVHips',
    'bd0001':'BD0001',
    'patcher':'patcher',
    'attack':'AttackDefense',
    'bdkitUtils':'BDKitUtils',
}

build_conf_files = {
	'杀毒': bdkv_conf_files,
	'卫士': bdm_conf_files,
}

default_installer_supplyid = ['m10001','n10000','n50000','f10015']
