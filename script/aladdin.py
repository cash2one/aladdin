# coding=UTF-8
"""
@author    thomas
@date    2013-08-24
@desc
    analyze specific xml supplied by hao123, translate it into tasks, and build them
@change
    init ------------------------------------- 2013.09.06
"""

import sys
import os
import logging
import argparse
import conf
import xml.dom.minidom
import base64
import hashlib
import io
import datetime
import rename_package
import sign
import comm
import codecs
import random
import struct
import tempfile

class SoftIDError(Exception):
    def __str__(self):
        return "multiple softid keyword found."

def calcFileMd5(afile):
    m = hashlib.md5()
    file = io.FileIO(afile,'r')
    bytes = file.read(1024)
    while(bytes != b''):
        m.update(bytes)
        bytes = file.read(1024)
    file.close()
    md5value = m.hexdigest()
    return md5value

def randomVersion():
    return '1.0.%d.%d' %(random.randint(0,100), random.randint(0,500))

def regenerateBind():
    #update folder first
    command = 'svn update --non-interactive --no-auth-cache --username buildbot --password bCRjzYKzk ..\\..\\sharemem\\basic\\tools'
    os.system(command)

    randName = tempfile.mktemp()
    randName = randName[randName.rfind('\\')+1:]
    for item in range(0,10000):
        if os.path.isfile(conf.aladdin_kvnetinstallhelper_folder + 'kvnetinstallhelper_%d.dll' % item):
            command = 'copy /Y ' + conf.aladdin_kvnetinstallhelper_folder + 'kvnetinstallhelper_%d.dll ..\\..\\sharemem\\basic\\tools\\nsis\\plugins\\%s.dll' % (item,randName)
            os.system(command)
            command = 'del /Q /S ' + conf.aladdin_kvnetinstallhelper_folder + 'kvnetinstallhelper_%d.dll' % item
            os.system(command)
            break

    #change outfile to bind.exe
    nsiFile = conf.sharemem_tools_folder + 'kvnetinstall\\kvnetinstall.nsi'
    file_r = open(nsiFile)
    lines = file_r.readlines()
    file_r.close()
    for index in range(len(lines)):
        if lines[index].find('OutFile') != -1:
            lines[index] = 'OutFile "..\\..\\..\\..\\autopack\\res\\baidusd\\bind.exe"\r\n'
        if lines[index].find('VIProductVersion') != -1:
            lines[index] = 'VIProductVersion "%s"\r\n' % randomVersion()
        if lines[index].find('KVNetInstallHelper') != -1:
            lines[index] = lines[index].replace('KVNetInstallHelper',randName)
    file_w = open(nsiFile, "w")
    file_w .writelines(lines)
    file_w .close()

    icoFile = conf.sharemem_tools_folder + 'kvnetinstall\\res\\setup.ico'
    
    #backup ico
    command = 'copy /Y ' + icoFile + ' ' + icoFile + '.bk'
    os.system(command)
    
    #change ico
    command = conf.modify_icon_exe + ' ' + icoFile + ' ' + icoFile
    os.system(command)

    #create random.dat(64k~512k random data)
    createRandomData(conf.sharemem_tools_folder + 'kvnetinstall\\res\\random.dat')

    #build bind.exe
    command = conf.sharemem_tools_folder + 'nsis\\makensis.exe ' + ' /X"SetCompressor /FINAL /SOLID lzma" ' + conf.sharemem_tools_folder + 'kvnetinstall\\kvnetinstall.nsi'
    os.system(command)
    
    #recover nsi
    file_r = open(nsiFile)
    lines = file_r.readlines()
    file_r.close()
    for index in range(len(lines)):
        if lines[index].find(randName) != -1:
            lines[index] = lines[index].replace(randName,'KVNetInstallHelper')
    file_w = open(nsiFile, "w")
    file_w .writelines(lines)
    file_w .close()

    #recover ico
    command = 'copy /Y ' + icoFile + '.bk ' + icoFile
    os.system(command)
    command = 'del /Q /S ' + icoFile + '.bk'
    os.system(command)

    #remove random.dat
    command = 'del /Q /S ' + conf.sharemem_tools_folder + 'kvnetinstall\\res\\random.dat'
    os.system(command)

    #modify bind pe
    #command = conf.modify_pe_exe + ' ..\\res\\baidusd\\bind.exe'
    #os.system(command)

    #sign driver sign
    command = conf.sign_driver_exe + ' /s ..\\res\\baidusd\\bind.exe'
    os.system(command)

    #sign kav sign
    command = conf.sign_kav_exe + ' /s"..\\res\\baidusd\\bind.exe" /u"..\\tools\\bin\\keys\\PrivateKey.sgn"'
    os.system(command)

    #sign baidu sign
    sign.main(3, ['sign.py', 'bdkv', conf.baidusd_res_folder])

    #auto modify last byte of bind.exe
    #fp = open('..\\res\\baidusd\\bind.exe', 'r+b')
    #fp.seek(-1, os.SEEK_END)
    #fp.write(struct.pack('c', chr(random.randint(1,255))))
    #fp.close()

    #overwrite bind.xml
    md5Value = calcFileMd5(conf.baidusd_res_folder + '\\bind.exe')
    try:
        dom = xml.dom.minidom.parse(conf.baidusd_res_folder + '\\bind.xml')
        root = dom.documentElement
        tsoftMD5 = root.getElementsByTagName('SoftMD5')[0]
        tsoftMD5.childNodes[0].data = md5Value

        writer = open(conf.baidusd_res_folder + '\\bind.xml', 'w')
        dom.writexml(writer)
        writer.close()
    except Exception, e:
        logging.error('error when update bind.xml')
        logging.error(e)

def getSoftidFileName(softid):
    dom = xml.dom.minidom.parse(conf.aladdin_package_folder + softid + '\\' + softid + '.xml')
    root = dom.documentElement
    return root.getElementsByTagName('FileName')[0].childNodes[0].data

def buildPackage(softid, type, bRepack, subfolder):
    '''
    type
        baidusd, qqmgr, nobind
    ''' 

    innerPackage = 'softsetup.exe'
    originalFileName = getSoftidFileName(softid)
    if originalFileName.lower().find('baiduplayernetsetup') != -1:
        innerPackage = 'BaiduPlayerNetSetup_103.exe'
    
    #delete nsis folder
    command = 'del /Q /S ' + conf.task_pool_nsis_folder
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    
    packageRootDir = conf.aladdin_package_folder + softid + '\\'
    
    command = 'del /Q ' + conf.task_pool_nsis_folder + 'softsetup.exe'
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    command = 'copy /Y ' + packageRootDir + getSoftidFileName(softid) + ' ' + conf.task_pool_nsis_folder + 'softsetup.exe'
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    
    command = 'del /Q ' + conf.task_pool_nsis_folder + 'logo.png'
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    command = 'copy /Y ' + packageRootDir + softid + '.png ' + conf.task_pool_nsis_folder + 'logo.png'
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    
    command = 'del /Q ' + conf.task_pool_nsis_folder + 'logo2.png'
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    command = 'copy /Y ' + packageRootDir + softid + '.png ' + conf.task_pool_nsis_folder + 'logo2.png'
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    
    command = 'del /Q ' + conf.task_pool_nsis_folder + 'setup.ico'
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    command = conf.extract_icon_exe + ' ' + conf.task_pool_nsis_folder + 'softsetup.exe ' + conf.task_pool_nsis_folder + 'setup.ico'
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    
    fp = open(conf.task_pool_nsis_folder + 'soft.nsh','w')
    nshInfo = '!define FILENAME ' + innerPackage
    fp.write(nshInfo)
    fp.close()
    logging.info('soft.nsh : ' + nshInfo)
    
    command = 'del /Q ' + conf.task_pool_nsis_folder + 'task.xml'
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    command = 'copy /Y ' + packageRootDir + softid + '.xml ' + conf.task_pool_nsis_folder + 'task.xml'
    logging.info(command)
    os.system(command.encode(sys.getfilesystemencoding()))
    
    for item in type.split(';'):
        #regenerate bind.exe and bind.xml
        if bRepack:
            regenerateBind()
        #copy res folder to nsis pool
        resFolder = ''
        nsis_exe = ''
        if item.lower() == 'baidusd':
            resFolder = conf.baidusd_res_folder
            nsis_exe = conf.baidusd_nsis_exe
        elif item.lower() == 'qqmgr':
            resFolder = conf.qqmgr_res_folder
            nsis_exe = conf.qqmgr_nsis_exe
        elif item.lower() == 'baidusd_nobind':
            resFolder = conf.nobind_res_folder
            nsis_exe = conf.baidusd_nsis_nobind_exe
        elif item.lower() == 'qqmgr_nobind':
            resFolder = conf.nobind_res_folder
            nsis_exe = conf.qqmgr_nsis_nobind_exe
        command = 'xcopy /Y /E /S ' + resFolder + ' ' + conf.task_pool_nsis_folder
        logging.info(command)
        os.system(command.encode(sys.getfilesystemencoding()))

        #change original filename in nsi file
        aladdinNsiFile = conf.task_pool_nsis_folder + 'stub\\aladin.nsi'
        infile = codecs.open(aladdinNsiFile,'r', encoding='utf-16-le')
        lines = infile.readlines()
        infile.close()
        for index in range(len(lines)):
            if lines[index].find('!define PRODUCT_FILENAME') != -1:
                lines[index] = '!define PRODUCT_FILENAME "' + getSoftidFileName(softid) + '"\r\n'
        outfile = codecs.open(aladdinNsiFile, 'w', encoding='utf-16-le')
        outfile.writelines(lines)
        outfile.close()
        
        #build
        command = nsis_exe + ' /X"SetCompressor /FINAL /SOLID lzma" ' + conf.task_pool_nsis_folder + 'stub\\aladin.nsi'
        logging.info(command)
        os.system(command.encode(sys.getfilesystemencoding()))
        
        #copy to archives
        if item.lower() == 'baidusd_nobind' or item.lower() == 'qqmgr_nobind':
            #delete output installer folder
            command = 'del /Q /S ' + conf.aladdin_installer_folder + 'unbind\\' + softid
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
            #init single task installer folder
            if not os.path.isdir(conf.aladdin_installer_folder + 'unbind\\' + softid):
                os.mkdir(conf.aladdin_installer_folder + 'unbind\\' + softid)
            command = 'copy /Y ' + conf.task_pool_nsis_folder + 'stub\\AladinDemo.exe ' + conf.aladdin_installer_folder + 'unbind\\' + softid + '\\Setup.exe'
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
            command = 'copy /Y ' + conf.task_pool_nsis_folder + 'task.xml ' + conf.aladdin_installer_folder + 'unbind\\' + softid + '\\task.xml'
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
        elif item.lower() == 'baidusd' or item.lower() == 'qqmgr':
            #delete output installer folder
            command = 'del /Q /S ' + conf.aladdin_installer_folder + subfolder + '\\' + softid
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
            #init single task installer folder
            if not os.path.isdir(conf.aladdin_installer_folder + subfolder + '\\' + softid):
                os.mkdir(conf.aladdin_installer_folder + subfolder + '\\' + softid)
            command = 'copy /Y ' + conf.task_pool_nsis_folder + 'stub\\AladinDemo.exe ' + conf.aladdin_installer_folder + subfolder + '\\' + softid + '\\Setup.exe'
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
            command = 'copy /Y ' + conf.task_pool_nsis_folder + 'task.xml ' + conf.aladdin_installer_folder + subfolder + '\\' + softid + '\\task.xml'
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
            
        #copy src packages
        #delete output installer folder
        command = 'del /Q /S ' + conf.aladdin_installer_folder + 'src\\' + softid
        logging.info(command)
        os.system(command.encode(sys.getfilesystemencoding()))

        #init single task installer folder
        if not os.path.isdir(conf.aladdin_installer_folder + 'src\\' + softid):
            os.mkdir(conf.aladdin_installer_folder + 'src\\' + softid)
        command = 'copy /Y ' + conf.task_pool_nsis_folder + 'task.xml ' + conf.aladdin_installer_folder + 'src\\' + softid + '\\task.xml'
        logging.info(command)
        os.system(command.encode(sys.getfilesystemencoding()))
        command = 'copy /Y ' + conf.task_pool_nsis_folder + 'softsetup.exe ' + conf.aladdin_installer_folder + 'src\\' + softid + '\\Setup.exe'
        logging.info(command)
        os.system(command.encode(sys.getfilesystemencoding()))
    
def signPackage(softid, type, subfolder):
    for item in type.split(';'):
        if item.lower() == 'baidusd_nobind' or item.lower() == 'qqmgr_nobind':
            sign.main(3, ['sign.py', 'bdkv', conf.aladdin_installer_folder + 'unbind\\' + softid + '\\'])
        elif item.lower() == 'baidusd' or item.lower() == 'qqmgr':
            sign.main(3, ['sign.py', 'bdkv', conf.aladdin_installer_folder + subfolder + '\\' + softid + '\\'])
    
def renamePackage(softid, type, subfolder):
    for item in type.split(';'):
        if item.lower() == 'baidusd_nobind' or item.lower() == 'qqmgr_nobind':
            rename_package.FileOperation(conf.aladdin_installer_folder + 'unbind\\' + softid + '\\', rename_package.renameExe, '*.xml')
        elif item.lower() == 'baidusd' or item.lower() == 'qqmgr':
            rename_package.FileOperation(conf.aladdin_installer_folder + subfolder + '\\' + softid + '\\', rename_package.renameExe, '*.xml')
        rename_package.FileOperation(conf.aladdin_installer_folder + 'src\\' + softid + '\\', rename_package.renameExe, '*.xml')

def cleanUpdatePoolFolder(subfolder):
    command = 'rd /Q /S ' + conf.aladdin_update_pool_folder + subfolder + '\\'
    logging.info(command)
    os.system(command)
    command = 'rd /Q /S ' + conf.aladdin_update_pool_folder + 'src\\'
    logging.info(command)
    os.system(command)
    command = 'rd /Q /S ' + conf.aladdin_update_pool_folder + 'unbind\\'
    logging.info(command)
    os.system(command)
    command = 'rd /Q /S ' + conf.aladdin_update_pool_folder + 'changelist\\'
    logging.info(command)
    os.system(command)
    
def cleanArchiveFolder(subfolder):
    command = 'rd /Q /S ' + conf.aladdin_archive_update_folder + subfolder + '\\'
    logging.info(command)
    os.system(command)
    command = 'rd /Q /S ' + conf.aladdin_archive_update_folder + 'src\\'
    logging.info(command)
    os.system(command)
    command = 'rd /Q /S ' + conf.aladdin_archive_update_folder + 'unbind\\'
    logging.info(command)
    os.system(command)

def copyPackageUpdate(softid, type, subfolder):
    for item in type.split(';'):
        if item.lower() == 'baidusd_nobind' or item.lower() == 'qqmgr_nobind':
            command = 'xcopy /Y /E /S /I ' + conf.aladdin_installer_folder + 'unbind\\' + softid + ' ' + conf.aladdin_update_pool_folder + 'unbind\\' + softid + ''
            logging.info(command)
            os.system(command)
            command = 'xcopy /Y /E /S /I ' + conf.aladdin_installer_folder + 'src\\' + softid + ' ' + conf.aladdin_update_pool_folder + 'src\\' + softid + ''
            logging.info(command)
            os.system(command)
        elif item.lower() == 'baidusd' or item.lower() == 'qqmgr':
            command = 'xcopy /Y /E /S /I ' + conf.aladdin_installer_folder + subfolder + '\\' + softid + ' ' + conf.aladdin_update_pool_folder + subfolder + '\\' + softid + ''
            logging.info(command)
            os.system(command)
            command = 'xcopy /Y /E /S /I ' + conf.aladdin_installer_folder + 'src\\' + softid + ' ' + conf.aladdin_update_pool_folder + 'src\\' + softid + ''
            logging.info(command)
            os.system(command)

def generateUpdateList(aladdin_update_list, type, subfolder):
    ctx = ''
    for item in aladdin_update_list:
        ctx += item + '\r\n'
    if ctx != '':
        clname = type.replace(';','_')
        clname += '-changelist_'
        clname += subfolder + '_'
        clname += str(datetime.datetime.now()).replace(':','-').replace(' ','-').replace('.','_')
        clname += '.txt'
        if not os.path.isdir(conf.aladdin_update_pool_folder + 'changelist'):
            os.mkdir(conf.aladdin_update_pool_folder + 'changelist')
        comm.saveFile(conf.aladdin_update_pool_folder + 'changelist\\' + clname, ctx)

def copyPackageToArchiveFolder(aladdin_update_list, type, bRemoveOld, subfolder):
    #clean old packages in archive folder
    if bRemoveOld:
        for item in type.split(';'):
            if item.lower() == 'baidusd_nobind' or item.lower() == 'qqmgr_nobind':
                for softid in aladdin_update_list:
                    #unbind
                    command = 'rd /Q /S ' + conf.aladdin_archive_folder + 'unbind\\' + softid
                    logging.info(command)
                    os.system(command)
                    #src
                    command = 'rd /Q /S ' + conf.aladdin_archive_folder + 'src\\' + softid
                    logging.info(command)
                    os.system(command)
            elif item.lower() == 'baidusd' or item.lower() == 'qqmgr':
                for softid in aladdin_update_list:
                    #subfolder
                    command = 'rd /Q /S ' + conf.aladdin_archive_folder + subfolder + '\\' + softid
                    logging.info(command)
                    os.system(command)
                    #src
                    command = 'rd /Q /S ' + conf.aladdin_archive_folder + 'src\\' + softid
                    logging.info(command)
                    os.system(command)
    command = conf.robo_copy_exe + ' ' + conf.aladdin_installer_folder[:-1] + ' ' + conf.aladdin_archive_folder + ' /E /XO /fft /W:0 '
    logging.info(command)
    os.system(command)
    
def buildAladdinPackage(xmlFile, bDownload, bBuild, bindType, bForce, bAll, packInfoFile, o_softId, bCopy, o_xsoftId, xpackInfoFile, bNoBuild, bNoCopyToUpdate, bRemoveOld, bRepack, subfolder):
    bCleanArchive = False
    
    #always clean update pool folder
    cleanUpdatePoolFolder(subfolder)
    
    #get all maintain list
    i_packInfoFile = conf.packinfo_aladdin_file
    if packInfoFile != '':
        i_packInfoFile = packInfoFile
    
    aladdin_update_list = []
    aladdin_maintain_list = []
    xsoftList = []
    try:
        bdlist_file = open(i_packInfoFile, 'r')
        for line in bdlist_file.readlines():
            aladdin_maintain_list.append(line.strip('\r\n \t'))
        bdlist_file.close()
    except Exception, e:
        logging.error('error when get softid maintain list')
        logging.error(e)
        return

    try:
        if xpackInfoFile != '':
            xbdlist_file = open(xpackInfoFile, 'r')
            for line in xbdlist_file.readlines():
                item = line.strip('\r\n \t')
                xsoftList.append(item)
                if item in aladdin_maintain_list:
                    aladdin_maintain_list.remove(item)
            xbdlist_file.close()
    except Exception, e:
        logging.error('error when get softid excluded maintain list')
        logging.error(e)
        return
    
    #manual softid
    if o_softId != '':
        aladdin_maintain_list = []
        for item in o_softId.split(';'):
            aladdin_maintain_list.append(item)
    if o_xsoftId != '':
        for item in o_xsoftId.split(';'):
            xsoftList.append(item)
            if item in aladdin_maintain_list:
                aladdin_maintain_list.remove(item)
    
    #xml file to anylize
    i_xmlFile = conf.aladdin_xml_full
    if xmlFile != '':
        i_xmlFile = xmlFile
    
    #do it
    #1.update all hao123softid single xmls
    try:
        dom = xml.dom.minidom.parse(i_xmlFile)
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            #softid
            nsoftid = node.getElementsByTagName('SoftID')
            if len(nsoftid) != 1:
                raise SoftIDError()
            softid = nsoftid[0].firstChild.wholeText

            #if not in maintain list, ignore
            if (softid not in aladdin_maintain_list) and (not bAll):
                #logging.info('%s is not in the maintain list, ignored' % softid)
                continue
            if softid in xsoftList:
                #logging.info('%s is in ignored list, ignored' % softid)
                continue
            
            logging.info('parsing softid %s' % softid)
            
            #if force update, delete the xml file first
            if bForce:
                command = 'del /Q ' + conf.aladdin_package_folder + softid + '\\' + softid + '.xml'
                os.system(command.encode(sys.getfilesystemencoding()))
            
            #init single task xml
            if not os.path.isdir(conf.aladdin_package_folder + softid):
                os.mkdir(conf.aladdin_package_folder + softid)
            
            taskxml_file = conf.aladdin_package_folder + softid + '\\' + softid + '.xml'
            tdom = ''
            bInited = False
            bUpdate = False
            if os.path.isfile(taskxml_file):
                bUpdate = False
                bInited = True
                tdom = xml.dom.minidom.parse(taskxml_file)
            else:
                bUpdate = True
                bInited = False
                impl = xml.dom.minidom.getDOMImplementation()
                tdom = impl.createDocument(None, 'DOCUMENT', None)
            troot = tdom.documentElement
            if bInited:
                pass
            else:
                ttaskid = tdom.createElement('TaskID')
                ttaskid.appendChild(tdom.createTextNode(softid))
                troot.appendChild(ttaskid)
            
            #softurl and filename
            nButton = node.getElementsByTagName('button')
            buttonLink = nButton[0].getAttribute('buttonlink')
            downloadLink = base64.decodestring(buttonLink[buttonLink.find('f=')+2:])
            logging.info('downloadLink : ' + downloadLink)
            
            filename = downloadLink[downloadLink.rfind('/')+1:]
            if bInited:
                tfilename = troot.getElementsByTagName('FileName')[0]
                if tfilename.childNodes[0].data != filename:
                    bUpdate = True
                    tfilename.childNodes[0].data = filename
                else:
                    pass
                tsofturl = troot.getElementsByTagName('SoftURL')[0]
                if tsofturl.childNodes[0].data != downloadLink:
                    bUpdate = True
                    tsofturl.childNodes[0].data = downloadLink
                else:
                    pass
            else:
                tfilename = tdom.createElement('FileName')
                tfilename.appendChild(tdom.createTextNode(filename))
                troot.appendChild(tfilename)
                tsofturl = tdom.createElement('SoftURL')
                tsofturl.appendChild(tdom.createTextNode(downloadLink))
                troot.appendChild(tsofturl)
                
            #Name
            nname = node.getElementsByTagName('content1')
            name = nname[0].firstChild.wholeText
            if bInited:
                tname = troot.getElementsByTagName('Name')[0]
                if tname.childNodes[0].data != name:
                    bUpdate = True
                    tname.childNodes[0].data = name
                else:
                    pass
            else:
                tname = tdom.createElement('Name')
                tname.appendChild(tdom.createTextNode(name))
                troot.appendChild(tname)
            
            #Title
            ntitle = node.getElementsByTagName('title')
            title = ntitle[0].firstChild.wholeText
            if bInited:
                ttitle = troot.getElementsByTagName('Title')[0]
                if ttitle.childNodes[0].data != title:
                    bUpdate = True
                    ttitle.childNodes[0].data = title
                else:
                    pass
            else:
                ttitle = tdom.createElement('Title')
                ttitle.appendChild(tdom.createTextNode(title))
                troot.appendChild(ttitle)
                
            #Version
            nversion = node.getElementsByTagName('content2')
            version = nversion[0].firstChild.wholeText
            if bInited:
                tversion = troot.getElementsByTagName('Verision')[0]
                if tversion.childNodes[0].data != version:
                    bUpdate = True
                    tversion.childNodes[0].data = version
                else:
                    pass
            else:
                tversion = tdom.createElement('Verision')
                tversion.appendChild(tdom.createTextNode(version))
                troot.appendChild(tversion)
            
            #Size
            nsize = node.getElementsByTagName('content3')
            size = nsize[0].firstChild.wholeText[5:]
            if bInited:
                tsize = troot.getElementsByTagName('Size')[0]
                if tsize.childNodes[0].data != size:
                    bUpdate = True
                    tsize.childNodes[0].data = size
                else:
                    pass
            else:
                tsize = tdom.createElement('Size')
                tsize.appendChild(tdom.createTextNode(size))
                troot.appendChild(tsize)
            
            #UpdateTime
            nupdateTime = node.getElementsByTagName('content4')
            updateTime = nupdateTime[0].firstChild.wholeText[5:]
            if bInited:
                tupdateTime = troot.getElementsByTagName('UpdateTime')[0]
                if tupdateTime.childNodes[0].data != updateTime:
                    bUpdate = True
                    tupdateTime.childNodes[0].data = updateTime
                else:
                    pass
            else:
                tupdateTime = tdom.createElement('UpdateTime')
                tupdateTime.appendChild(tdom.createTextNode(updateTime))
                troot.appendChild(tupdateTime)
            
            
            #SystemRequire
            nsystemRequire = node.getElementsByTagName('content5')
            systemRequire = nsystemRequire[0].firstChild.wholeText[5:]
            if bInited:
                tsystemRequire = troot.getElementsByTagName('SystemRequire')[0]
                if tsystemRequire.childNodes[0].data != systemRequire:
                    bUpdate = True
                    tsystemRequire.childNodes[0].data = systemRequire
                else:
                    pass
            else:
                tsystemRequire = tdom.createElement('SystemRequire')
                tsystemRequire.appendChild(tdom.createTextNode(systemRequire))
                troot.appendChild(tsystemRequire)
            
            #SoftMD5 - only update it when bUpdate is set
            tsoftMD5 = None
            if bInited:
                tsoftMD5 = troot.getElementsByTagName('SoftMD5')[0]
                pass
            else:
                tsoftMD5 = tdom.createElement('SoftMD5')
                tsoftMD5.appendChild(tdom.createTextNode(''))
                troot.appendChild(tsoftMD5)
            
            #LogoUrl
            nicon = node.getElementsByTagName('icon')
            iconAddr = nicon[0].getAttribute('iconaddress')
            logging.info('LogoUrl : ' + iconAddr)
            if bInited:
                ticon = troot.getElementsByTagName('LogoUrl')[0]
                if ticon.childNodes[0].data != iconAddr:
                    bUpdate = True
                    ticon.childNodes[0].data = iconAddr
                else:
                    pass
            else:
                ticon = tdom.createElement('LogoUrl')
                ticon.appendChild(tdom.createTextNode(iconAddr))
                troot.appendChild(ticon)
            
            
            #LogoMD5 - only update it when bUpdate is set
            tlogoMD5 = None
            if bInited:
                tlogoMD5 = troot.getElementsByTagName('LogoMD5')[0]
                pass
            else:
                tlogoMD5 = tdom.createElement('LogoMD5')
                tlogoMD5.appendChild(tdom.createTextNode(''))
                troot.appendChild(tlogoMD5)
            
            
            #SoftID - only update it when bUpdate is set
            if bInited:
                pass
            else:
                tsoftID = tdom.createElement('SoftID')
                tsoftID.appendChild(tdom.createTextNode(softid))
                troot.appendChild(tsoftID)
            
            #PackMD5 - only update it when the pack is packed
            if bInited:
                pass
            else:
                tpackMD5 = tdom.createElement('PackMD5')
                tpackMD5.appendChild(tdom.createTextNode(''))
                troot.appendChild(tpackMD5)
            
            #if bUpdate, do some real work
            if bUpdate:
                
                #always download when bUpdate
                #soft
                command = conf.wget_exe + ' ' + downloadLink + ' -O ' + conf.aladdin_package_folder + softid + '\\' + filename
                os.system(command.encode(sys.getfilesystemencoding()))
                #ico
                command = conf.wget_exe + ' ' + iconAddr + ' -O ' + conf.aladdin_package_folder + softid + '\\' + softid + '.png'
                os.system(command.encode(sys.getfilesystemencoding()))
                #softmd5
                tsoftMD5.childNodes[0].data = calcFileMd5(conf.aladdin_package_folder + softid + '\\' + filename)
                #icomd5
                tlogoMD5.childNodes[0].data = calcFileMd5(conf.aladdin_package_folder + softid + '\\' + softid + '.png')
                
                #save to xml
                writer = open(taskxml_file, 'w')
                tdom.writexml(writer)
                writer.close()

                #always build when bUpdate
                if not bNoBuild:
                    
                    #mark clean archive
                    bCleanArchive = True
                    
                    #mark upadte
                    aladdin_update_list.append(softid)
                    
                    buildPackage(softid, bindType, bRepack, subfolder)
                    signPackage(str(softid), bindType, subfolder)
                    renamePackage(str(softid), bindType, subfolder)
                    if not bNoCopyToUpdate:
                        copyPackageUpdate(str(softid), bindType, subfolder)
                
            #if bDownload is set, also download soft、ico
            if bDownload and not bUpdate:
                #soft
                command = conf.wget_exe + ' ' + downloadLink + ' -O ' + conf.aladdin_package_folder + softid + '\\' + filename
                os.system(command.encode(sys.getfilesystemencoding()))
                #ico
                command = conf.wget_exe + ' ' + iconAddr + ' -O ' + conf.aladdin_package_folder + softid + '\\' + softid + '.png'
                os.system(command.encode(sys.getfilesystemencoding()))
            
            #build specific package
            if bBuild and not (bUpdate and not bNoBuild):
                
                #mark clean archive
                bCleanArchive = True
                    
                #mark upadte
                aladdin_update_list.append(softid)
                
                buildPackage(softid, bindType, bRepack, subfolder)
                signPackage(str(softid), bindType, subfolder)
                renamePackage(str(softid), bindType, subfolder)
                if not bNoCopyToUpdate:
                    copyPackageUpdate(str(softid), bindType, subfolder)
            
        #update list
        generateUpdateList(aladdin_update_list, bindType, subfolder)
        
        if bCopy:
            #clean update pool folder
            if bCleanArchive:
                cleanArchiveFolder(subfolder)
            copyPackageToArchiveFolder(aladdin_update_list, bindType, bRemoveOld, subfolder)
            
    except Exception, e:
        logging.error('error occers while parsing aladdin full xml')
        logging.error(e)
        print xsoftList
        return

def createRandomData(rFile):
    fp = open(rFile, 'w')
    iRandom = random.randint(64,512)
    iContent = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in range(0,iRandom):
        for j in range(0,1024):
            fp.write(iContent[random.randint(0,61)])
    fp.close()

def buildV1020Installer(bCopy, num, version):
    #clean local and remote folder
    online_subfolder = 'online'
    tools_folder = conf.v1020_tools_folder
    if version == '1020':
        online_subfolder = 'online_v1020'
        tools_folder = conf.v1020_tools_folder
    elif version == '1055':
        online_subfolder = 'online_v1055'
        tools_folder = conf.v1055_tools_folder
    elif version == '1092':
        online_subfolder = 'online_v1092'
        tools_folder = conf.v1092_tools_folder
        
    #update tools folder
    command = 'svn update --non-interactive --no-auth-cache --username buildbot --password bCRjzYKzk ' + tools_folder
    os.system(command)
        
    command = 'del /Q /S ..\\output\\aladdin\\installers\\' + online_subfolder + '\\*.exe'
    os.system(command)
    if bCopy:
        command = 'del /Q /S ' + conf.aladdin_archive_folder + online_subfolder + '\\*.exe'
        os.system(command)
    
    iNum = int(num)
    for i in range(0,iNum):
        #change outfile to online folder
        nsiFile = tools_folder + 'kvsetupscript\\BDKV_setup.nsi'
        file_r = open(nsiFile)
        lines = file_r.readlines()
        file_r.close()
        randomVer = randomVersion()
        installer = ''
        for index in range(len(lines)):
            if lines[index].find('OutFile') != -1:
                lines[index] = 'OutFile "..\\..\\..\\..\\autopack\\output\\aladdin\\installers\\' + online_subfolder + '\\Baidusd_Setup_%s.exe"\r\n' % randomVer
                installer = 'Baidusd_Setup_%s.exe' % randomVer
            if lines[index].find('VIProductVersion') != -1:
                lines[index] = 'VIProductVersion "%s"\r\n' % randomVer
            if lines[index].find('File /oname=$PLUGINSDIR\\BDMSkin.dll    			"res\\BDMSkin.dll"') != -1:
                lines[index] = lines[index] + '\r\n' + lines[index].replace('BDMSkin.dll','random.dat') + '\r\n'
        file_w = open(nsiFile, "w")
        file_w .writelines(lines)
        file_w .close()
        
        #create random.dat(64k~512k random data)
        createRandomData(tools_folder + 'kvsetupscript\\res\\random.dat')

        icoFile = tools_folder + 'kvsetupscript\\res\\setup.ico'
        
        #backup ico
        command = 'copy /Y ' + icoFile + ' ' + icoFile + '.bk'
        os.system(command)
        
        #change ico
        command = conf.modify_icon_exe + ' ' + icoFile + ' ' + icoFile
        os.system(command)

        #build installer
        command = tools_folder + 'nsis\\makensis.exe ' + ' /X"SetCompressor /FINAL /SOLID lzma" ' + tools_folder + 'kvsetupscript\\BDKV_setup.nsi'
        os.system(command)

        #recover nsh
        file_r = open(nsiFile)
        lines = file_r.readlines()
        file_r.close()
        randomVer = randomVersion()
        for index in range(len(lines)):
            if lines[index].find('File /oname=$PLUGINSDIR\\random.dat    			"res\\random.dat"') != -1:
                lines[index] = '\r\n'
        file_w = open(nsiFile, "w")
        file_w .writelines(lines)
        file_w .close()
        
        #remove random.dat
        command = 'del /Q /S ' + tools_folder + 'kvsetupscript\\res\\random.dat'
        os.system(command)

        #recover ico
        command = 'copy /Y ' + icoFile + '.bk ' + icoFile
        os.system(command)
        command = 'del /Q /S ' + icoFile + '.bk'
        os.system(command)

        #sign driver sign
        command = conf.sign_driver_exe + ' /s ..\\output\\aladdin\\installers\\' + online_subfolder + '\\' + installer
        os.system(command)

        #sign kav sign
        command = conf.sign_kav_exe + ' /s"..\\output\\aladdin\\installers\\' + online_subfolder + '\\' + installer + '" /u"..\\tools\\bin\\keys\\PrivateKey.sgn"'
        os.system(command)

    #sign baidu sign
    sign.main(3, ['sign.py', 'bdkv', '..\\output\\aladdin\\installers\\' + online_subfolder])


def main(argc, argv):
    #set sysencoding to utf-8
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    #init logging system, it's told logging is threadsafe, so do NOT need to sync
    logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG, stream = sys.stdout)

    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--xml-file', action='store', default=conf.aladdin_xml_full, dest='xmlFile', help='hao123 xml file location, second considered')
    parser.add_argument('-d', '--auto-download', action='store_true', default=False, dest='bDownload', help='auto download original packages')
    parser.add_argument('-b', '--auto-build', action='store_true', default=False, dest='bBuild', help='auto build packages')
    parser.add_argument('-t', '--bind-type', action='store', default='baidusd', dest='bindType', help='bind type')
    parser.add_argument('-F', '--force-update', action='store_true', default=False, dest='bForce', help='force updating everything')
    parser.add_argument('-a', '--analyze-all', action='store_true', default=False, dest='bAll', help='analyze all tasks')
    parser.add_argument('-p', '--packinfo-file', action='store', default='', dest='packInfoFile', help='packlist maintain list file')
    parser.add_argument('-P', '--excluded-packinfo-file', action='store', default='', dest='xpackInfoFile', help='excluded packlist maintain list file')
    parser.add_argument('-s', '--soft-id', action='store', default='', dest='softId', help='use manual softid list, first considered')
    parser.add_argument('-x', '--excluded-softid', action='store', default='', dest='xsoftId', help='excluded softid list, first considered')
    parser.add_argument('-c', '--copyto-archive', action='store_true', default=False, dest='bCopy', help='also copy to archive folder')
    parser.add_argument('-B', '--nobuild-when-update', action='store_true', default=False, dest='bNoBuild', help='not build when update')
    parser.add_argument('-U', '--nocopy-to-update', action='store_true', default=False, dest='bCopyUpdate', help='not copy to update folder')
    parser.add_argument('-R', '--remove-old-pkgs', action='store_true', default=False, dest='bRemoveOldPkg', help='remove old packages in archive folder')
    parser.add_argument('-e', '--build-v1020-installer', action='store_true', default=False, dest='bInstaller1020', help='build v1020 installer')
    parser.add_argument('-n', '--numberof-v1020-installers', action='store', default='1', dest='numInstallers', help='number of v1020 installers')
    parser.add_argument('-r', '--repack', action='store_true', default=False, dest='bRepack', help='repack bind.exe')
    parser.add_argument('-v', '--repackVersion', action='store', default='1020', dest='repackVersion', help='repack version')
    parser.add_argument('-g', '--archive-subfolder', action='store', default='bind1', dest='archiveSubfolder', help='archive subfolder')


    args = parser.parse_args()
    logging.info('-----------------------------------------')
    logging.info('xml-file : ' + args.xmlFile)
    logging.info('auto-download : ' + str(args.bDownload))
    logging.info('auto-build : ' + str(args.bBuild))
    logging.info('bind-type : ' + args.bindType)
    logging.info('force-update : ' + str(args.bForce))
    logging.info('analyze-all : ' + str(args.bAll))
    logging.info('packinfo-file : ' + args.packInfoFile)
    logging.info('excluded-packinfo-file : ' + args.xpackInfoFile)
    logging.info('soft-id : ' + args.softId)
    logging.info('excluded-softid : ' + args.xsoftId)
    logging.info('copyto-archive : ' + str(args.bCopy))
    logging.info('nobuild-when-update : ' + str(args.bNoBuild))
    logging.info('nocopy-to-update : ' + str(args.bCopyUpdate))
    logging.info('remove-old-packages : ' + str(args.bRemoveOldPkg))
    logging.info('build-v1020-installer : ' + str(args.bInstaller1020))
    logging.info('number-v1020-installers : ' + args.numInstallers)
    logging.info('repack bind.exe : ' + str(args.bRepack))
    logging.info('repack version : ' + args.repackVersion)
    logging.info('archive subfolder : ' + args.archiveSubfolder)
    logging.info('-----------------------------------------')
    
    if args.bInstaller1020:
        buildV1020Installer(args.bCopy, args.numInstallers, args.repackVersion)
    
    buildAladdinPackage(args.xmlFile, args.bDownload, args.bBuild, args.bindType, args.bForce, args.bAll, args.packInfoFile, args.softId, args.bCopy, args.xsoftId, args.xpackInfoFile, args.bNoBuild, args.bCopyUpdate, args.bRemoveOldPkg, args.bRepack, args.archiveSubfolder)

if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))
    
    
