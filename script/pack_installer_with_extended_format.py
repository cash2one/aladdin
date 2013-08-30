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
import xml.dom.minidom
import hashlib

def getPkgInfo(pkgName):
    fp = open(conf.packdetail_file)
    lines = fp.readlines()
    fp.close()
    strName = ''
    for item in lines:
        if item.find(pkgName) != -1:
            return item.split('\t')
    return []

def generagePkgInfo(pkgName, bindSoft):
    
    pkgInfo = getPkgInfo(pkgName)
    ctx = ''
    
    doc = xml.dom.minidom.parse(conf.task_pool_nsis_folder + 'task.xml')
    root = doc.documentElement
    
    taskid = doc.createElement('TaskID')
    if len(pkgInfo) == 0:
        ctx = '1'
    else:
        ctx = pkgInfo[0]
    taskid.appendChild(doc.createTextNode(ctx))
    root.appendChild(taskid)

    filename = doc.createElement('FileName')
    filename.appendChild(doc.createTextNode(pkgName + '.exe'))
    root.appendChild(filename)
    
    if len(pkgInfo) == 0:
        ctx = ''
    else:
        ctx = pkgInfo[1]
    name = doc.createElement('Name')
    name.appendChild(doc.createTextNode(ctx))
    root.appendChild(name)

    if len(pkgInfo) == 0:
        ctx = ''
    else:
        ctx = pkgInfo[8]
    title = doc.createElement('Title')
    title.appendChild(doc.createTextNode(ctx))
    root.appendChild(title)

    version = doc.createElement('Verision')
    if len(pkgInfo) == 0:
        ctx = '1.0'
    else:
        ctx = pkgInfo[4]
    version.appendChild(doc.createTextNode(ctx))
    root.appendChild(version)

    size = doc.createElement('Size')
    if len(pkgInfo) == 0:
        ctx = ''
    else:
        ctx = pkgInfo[5]
    size.appendChild(doc.createTextNode(ctx))
    root.appendChild(size)

    updateTime = doc.createElement('UpdateTime')
    if len(pkgInfo) == 0:
        ctx = '2013-08-25'
    else:
        ctx = pkgInfo[6]
    updateTime.appendChild(doc.createTextNode(ctx))
    root.appendChild(updateTime)

    systemRequire = doc.createElement('SystemRequire')
    if len(pkgInfo) == 0:
        ctx = ''
    else:
        ctx = pkgInfo[7]
    systemRequire.appendChild(doc.createTextNode(ctx))
    root.appendChild(systemRequire)

    softURL = doc.createElement('SoftURL')
    if len(pkgInfo) == 0:
        ctx = 'ftp://10.52.175.51:8021/softs/' + pkgName
    else:
        ctx = pkgInfo[3]
    softURL.appendChild(doc.createTextNode(ctx))
    root.appendChild(softURL)

    mCalc = hashlib.md5()
    inputFile = open(conf.package_folder + pkgName + '\\' + pkgName + '.exe', 'rb')
    strRead = ''
    while True:
        strRead = inputFile.read(8096)
        if not strRead:
            break
        mCalc.update(strRead)
    inputFile.close()
    strMd5 = mCalc.hexdigest()
    softMd5 = doc.createElement('SoftMD5')
    softMd5.appendChild(doc.createTextNode(strMd5))
    root.appendChild(softMd5)

    logoUrl = doc.createElement('LogoURL')
    logoUrl.appendChild(doc.createTextNode('please give me a url'))
    root.appendChild(logoUrl)

    mCalc = hashlib.md5()
    inputFile = open(conf.package_folder + pkgName + '\\logo_32.png', 'rb')
    strRead = ''
    while True:
        strRead = inputFile.read(8096)
        if not strRead:
            break
        mCalc.update(strRead)
    inputFile.close()
    strMd5 = mCalc.hexdigest()
    logoMd5 = doc.createElement('LogoMD5')
    logoMd5.appendChild(doc.createTextNode(strMd5))
    root.appendChild(logoMd5)

    logoUrl2 = doc.createElement('LogoURL2')
    logoUrl2.appendChild(doc.createTextNode('please give me a url 2'))
    root.appendChild(logoUrl2)

    mCalc = hashlib.md5()
    inputFile = open(conf.package_folder + pkgName + '\\logo_48.png', 'rb')
    strRead = ''
    while True:
        strRead = inputFile.read(8096)
        if not strRead:
            break
        mCalc.update(strRead)
    inputFile.close()
    strMd5 = mCalc.hexdigest()
    logoMd5_2 = doc.createElement('LogoMD52')
    logoMd5_2.appendChild(doc.createTextNode(strMd5))
    root.appendChild(logoMd5_2)

    softId = doc.createElement('SoftID')
    softId.appendChild(doc.createTextNode('1'))
    root.appendChild(softId)

    mCalc = hashlib.md5()
    inputFile = open(conf.package_folder + pkgName + '\\' + pkgName + '.exe', 'rb')
    strRead = ''
    while True:
        strRead = inputFile.read(8096)
        if not strRead:
            break
        mCalc.update(strRead)
    inputFile.close()
    strMd5 = mCalc.hexdigest()
    packMd5 = doc.createElement('PackMD5')
    packMd5.appendChild(doc.createTextNode(strMd5))
    root.appendChild(packMd5)

    writer = open(conf.task_pool_nsis_folder + 'task.xml', 'w')
    doc.writexml(writer, '\n', ' ', '')
    writer.close()

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

def packInstaller(pkgName, bindSoft):
    command = 'del /Q ' + conf.task_pool_nsis_folder + '\\softsetup.exe'
    logging.info(command)
    os.system(command)
    command = 'copy /Y ' + conf.package_folder + pkgName + '\\' + pkgName + '.exe ' + conf.task_pool_nsis_folder + 'softsetup.exe'
    logging.info(command)
    os.system(command)
    
    command = 'del /Q ' + conf.task_pool_nsis_folder + '\\logo_32.png '
    logging.info(command)
    os.system(command)
    command = 'copy /Y ' + conf.package_folder + pkgName + '\\logo_32.png ' + conf.task_pool_nsis_folder + 'logo.png'
    logging.info(command)
    os.system(command)
    
    command = 'del /Q ' + conf.task_pool_nsis_folder + '\\logo_48.png '
    logging.info(command)
    os.system(command)
    command = 'copy /Y  ' + conf.package_folder + pkgName + '\\logo_48.png ' + conf.task_pool_nsis_folder + 'logo2.png'
    logging.info(command)
    os.system(command)
    
    command = 'del /Q ' + conf.task_pool_nsis_folder + '\\setup.ico '
    logging.info(command)
    os.system(command)
    command = 'copy /Y  ' + conf.ico_folder + pkgName.replace('.','') + '.ico ' + conf.task_pool_nsis_folder + 'setup.ico'
    logging.info(command)
    os.system(command)
    
    fp = open(conf.task_pool_nsis_folder + 'soft.nsh','w')
    nshInfo = '!define FILENAME ' + pkgName + '.exe'
    fp.write(nshInfo)
    fp.close()
    logging.info('soft.nsh : ' + nshInfo)
    
    generagePkgInfo(pkgName, bindSoft)

    nsis_exe = ''
    if bindSoft == 'baidusd':
        nsis_exe = conf.baidusd_nsis_exe
    elif bindSoft == 'qqmgr':
        nsis_exe = conf.qqmgr_nsis_exe
    command = nsis_exe + ' /X"SetCompressor /FINAL /SOLID lzma" ' + conf.task_pool_nsis_folder + 'stub\\aladin.nsi'
    logging.info(command)
    os.system(command)
    
    command = 'del /Q /S ' + conf.installer_folder + pkgName
    logging.info(command)
    os.system(command)
    
    command = 'mkdir ' + conf.installer_folder + pkgName
    logging.info(command)
    os.system(command)
    
    command = 'copy /Y  ' + conf.task_pool_nsis_folder + 'stub\\AladinDemo.exe ' + conf.installer_folder + pkgName + '\\Setup.exe'
    logging.info(command)
    os.system(command)
    
    command = 'copy /Y  ' + conf.task_pool_nsis_folder + 'task.xml ' + conf.installer_folder + pkgName + '\\task.xml'
    logging.info(command)
    os.system(command)
    

def main(argc, argv):
    #init logging system, it's told logging is threadsafe, so do NOT need to sync
    logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG, stream = sys.stdout)

    #utf-8 encoding
    reload(sys)
    sys.setdefaultencoding('utf-8')

    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputSoft', action='store', dest='inputSoft', default='', help='third party software name')
    parser.add_argument('-l', '--outputDir', action='store', default=conf.installer_folder, dest='outputDir', help='binded installer folder, must be folder')
    parser.add_argument('-b', '--bindSoft', action='store', dest='bindSoft', default='baidusd', help='binded soft, baidusd[default] or qqmgr')
    parser.add_argument('-a', '--packAll', action='store_true', default=False, dest='packAll', help='whether to pack all installers')
    
    args = parser.parse_args()
    
    logging.info('inputSoft' + ' : ' + args.inputSoft)
    logging.info('outputDir' + ' : ' + args.outputDir)
    logging.info('bindSoft' + ' : ' + args.bindSoft)
    logging.info('packAll' + ' : ' + str(args.packAll))

    if args.inputSoft == '' and (not args.packAll):
        return

    packinfoFile = ''
    resFolder = ''
    bindSoft = args.bindSoft.lower()
    if bindSoft.lower() == 'baidusd':
        packinfoFile = conf.baidusd_packinfo_file
        resFolder = conf.baidusd_res_folder
    elif bindSoft.lower() == 'qqmgr':
        packinfoFile = conf.qqmgr_packinfo_file
        resFolder = conf.qqmgr_res_folder

    #redelete nsis folder
    command = 'del /Q /S ' + conf.task_pool_nsis_folder
    logging.info(command)
    os.system(command)
    command = 'xcopy /Y /E /S ' + resFolder + ' ' + conf.task_pool_nsis_folder
    logging.info(command)
    os.system(command)
    
    if (not args.packAll):
        packInstaller(args.inputSoft, bindSoft)
    else:
        fp = open(packinfoFile)
        lines = fp.readlines()
        fp.close()
        for item in lines:
            logging.info('------------------------------------------')
            pkgName = item[item.find('\t')+1:-1]
            if checkPackage(pkgName):
                logging.info('packing ' + pkgName + ' ... ')
                packInstaller(pkgName, bindSoft)
            else:
                logging.error('check package ' + pkgName + ' failed')
                continue
        

if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))
