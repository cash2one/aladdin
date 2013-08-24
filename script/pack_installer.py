# coding=UTF-8
"""
@author    thomas
@date    2013-08-24
@desc
    pack installer
@change
    init ------------------------------------- 2013.08.24
"""

import sys
import os
import logging
import argparse
import conf

def checkPackage(pkgName):
    if not os.path.isdir(conf.package_folder + pkgName):
        logging.error('package ' + pkgName + ' folder not exist')
        return False
    elif not os.path.isfile(conf.package_folder + pkgName + '\\' + pkgName + '.exe'):
        logging.error('package ' + pkgName + ' missing ' + pkgName + '.exe')
        return False
    elif not os.path.isfile(conf.package_folder + pkgName + '\\logo_32.png'):
        logging.error('package ' + pkgName + ' missing logo_32.png')
        return False
    elif not os.path.isfile(conf.package_folder + pkgName + '\\logo_48.png'):
        logging.error('package ' + pkgName + ' missing logo_48.png')
        return False
    else:
        return True

def packInstaller(pkgName):
    command = 'del /Q ' + conf.task_pool_nsis_folder + '\\' + pkgName + '.exe'
    logging.info(command)
    os.system(command)
    command = 'echo F | xcopy /Y ' + conf.package_folder + pkgName + '\\' + pkgName + '.exe ' + conf.task_pool_nsis_folder + 'softsetup.exe'
    logging.info(command)
    os.system(command)
    
    command = 'del /Q ' + conf.task_pool_nsis_folder + '\\logo_32.png '
    logging.info(command)
    os.system(command)
    command = 'echo F | xcopy /Y ' + conf.package_folder + pkgName + '\\logo_32.png ' + conf.task_pool_nsis_folder + 'logo.png'
    logging.info(command)
    os.system(command)
    
    command = 'del /Q ' + conf.task_pool_nsis_folder + '\\logo_48.png '
    logging.info(command)
    os.system(command)
    command = 'echo F | xcopy /Y  ' + conf.package_folder + pkgName + '\\logo_48.png ' + conf.task_pool_nsis_folder + 'logo2.png'
    logging.info(command)
    os.system(command)
    
    fp = open(conf.task_pool_nsis_folder + 'soft.nsh','w')
    nshInfo = '!define FILENAME ' + pkgName + '.exe'
    fp.write(nshInfo)
    fp.close()
    logging.info('soft.nsh : ' + nshInfo)
    
    command = conf.baidusd_nsis_exe + ' /X"SetCompressor /FINAL /SOLID lzma" ' + conf.task_pool_nsis_folder + 'stub\\aladin.nsi'
    logging.info(command)
    os.system(command)
    
    command = 'del /Q /S ' + conf.installer_folder + pkgName
    logging.info(command)
    os.system(command)
    
    command = 'mkdir ' + conf.installer_folder + pkgName
    logging.info(command)
    os.system(command)
    
    command = 'echo F | xcopy /Y  ' + conf.task_pool_nsis_folder + 'stub\\AladinDemo.exe ' + conf.installer_folder + pkgName + '\\Setup.exe'
    logging.info(command)
    os.system(command)
    
    command = 'echo F | xcopy /Y  ' + conf.task_pool_nsis_folder + 'task.xml ' + conf.installer_folder + pkgName + '\\task.xml'
    logging.info(command)
    os.system(command)
    

def main(argc, argv):
    #init logging system, it's told logging is threadsafe, so do NOT need to sync
    logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG, stream = sys.stdout)

    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inputSoft', action='store', dest='inputSoft', default='', help='third party software name')
    parser.add_argument('-l','--outputDir', action='store', default=conf.installer_folder, dest='outputDir', help='binded installer folder, must be folder')
    parser.add_argument('-a','--packAll', action='store_true', default=False, dest='packAll', help='whether to pack all installers')
    args = parser.parse_args()
    logging.info('inputSoft' + ' : ' + args.inputSoft)
    logging.info('outputDir' + ' : ' + args.outputDir)
    logging.info('packAll' + ' : ' + str(args.packAll))
    
    #redelete nsis folder
    command = 'del /Q /S ' + conf.task_pool_nsis_folder
    logging.info(command)
    os.system(command)
    command = 'xcopy /Y /E /S ' + conf.res_folder + ' ' + conf.task_pool_nsis_folder
    logging.info(command)
    os.system(command)
    
    if not args.packAll:
        packInstaller(args.inputSoft)
    else:
        fp = open(conf.packinfo_file)
        lines = fp.readlines()
        fp.close()
        for item in lines:
            logging.info('------------------------------------------')
            pkgName = item[item.find('\t')+1:-1]
            if checkPackage(pkgName):
                logging.info('packing ' + pkgName + ' ... ')
                packInstaller(pkgName)
            else:
                logging.error('check package ' + pkgName + ' failed')
                continue
        

if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))
