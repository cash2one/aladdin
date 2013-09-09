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
import rename_package
import 

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
    
def getSoftidFileName(softid):
    dom = xml.dom.minidom.parse(conf.aladdin_package_folder + softid + '\\' + softid + '.xml')
    root = dom.documentElement
    return root.getElementsByTagName('FileName')[0].childNodes[0].data

def buildPackage(softid, type):
    '''
    type
        baidusd, qqmgr, nobind
    ''' 
    
    #redelete nsis folder and copy
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
    nshInfo = '!define FILENAME softsetup.exe'
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
        
        #build
        command = nsis_exe + ' /X"SetCompressor /FINAL /SOLID lzma" ' + conf.task_pool_nsis_folder + 'stub\\aladin.nsi'
        logging.info(command)
        os.system(command.encode(sys.getfilesystemencoding()))
        
        #copy to archives
        if item.lower() == 'baidusd_nobind' or item.lower() == 'qqmgr_nobind':
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
            #init single task installer folder
            if not os.path.isdir(conf.aladdin_installer_folder + 'bind\\' + softid):
                os.mkdir(conf.aladdin_installer_folder + 'bind\\' + softid)
            command = 'copy /Y ' + conf.task_pool_nsis_folder + 'stub\\AladinDemo.exe ' + conf.aladdin_installer_folder + 'bind\\' + softid + '\\Setup.exe'
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
            command = 'copy /Y ' + conf.task_pool_nsis_folder + 'task.xml ' + conf.aladdin_installer_folder + 'bind\\' + softid + '\\task.xml'
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
            
            #init single task installer folder
            if not os.path.isdir(conf.aladdin_installer_folder + 'bind1\\' + softid):
                os.mkdir(conf.aladdin_installer_folder + 'bind1\\' + softid)
            command = 'copy /Y ' + conf.task_pool_nsis_folder + 'stub\\AladinDemo.exe ' + conf.aladdin_installer_folder + 'bind1\\' + softid + '\\Setup.exe'
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
            command = 'copy /Y ' + conf.task_pool_nsis_folder + 'task.xml ' + conf.aladdin_installer_folder + 'bind1\\' + softid + '\\task.xml'
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
            
            #init single task installer folder
            if not os.path.isdir(conf.aladdin_installer_folder + 'bind2\\' + softid):
                os.mkdir(conf.aladdin_installer_folder + 'bind2\\' + softid)
            command = 'copy /Y ' + conf.task_pool_nsis_folder + 'stub\\AladinDemo.exe ' + conf.aladdin_installer_folder + 'bind2\\' + softid + '\\Setup.exe'
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
            command = 'copy /Y ' + conf.task_pool_nsis_folder + 'task.xml ' + conf.aladdin_installer_folder + 'bind2\\' + softid + '\\task.xml'
            logging.info(command)
            os.system(command.encode(sys.getfilesystemencoding()))
        
        #copy src packages
        #init single task installer folder
            if not os.path.isdir(conf.aladdin_installer_folder + 'src\\' + softid):
                os.mkdir(conf.aladdin_installer_folder + 'src\\' + softid)
        command = 'copy /Y ' + conf.task_pool_nsis_folder + 'task.xml ' + conf.aladdin_installer_folder + 'src\\' + softid + '\\task.xml'
        logging.info(command)
        os.system(command.encode(sys.getfilesystemencoding()))
        command = 'copy /Y ' + conf.task_pool_nsis_folder + 'softsetup.exe ' + conf.aladdin_installer_folder + 'src\\' + softid + '\\Setup.exe'
        logging.info(command)
        os.system(command.encode(sys.getfilesystemencoding()))
    
def signPackage(softid, type):
    
    
def renamePackage(softid, type):
    
    
def main(argc, argv):
    #set sysencoding to utf-8
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    #init logging system, it's told logging is threadsafe, so do NOT need to sync
    logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG, stream = sys.stdout)

    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--xml-file', action='store', default='..\\info\\pack_today_1.xml', dest='xmlFile', help='hao123 xml file location')
    parser.add_argument('-d', '--auto-download', action='store_true', default=False, dest='bDownload', help='auto download original packages')
    parser.add_argument('-b', '--auto-build', action='store_true', default=False, dest='bBuild', help='auto build packages')
    parser.add_argument('-t', '--bind-type', action='store', default='baidusd;baidusd_nobind', dest='bindType', help='bind type')
    parser.add_argument('-F', '--force-update', action='store_true', default=False, dest='bForce', help='force updating everything')
    parser.add_argument('-a', '--analyze-all', action='store_true', default=False, dest='bAll', help='analyze all tasks')
    parser.add_argument('-p', '--packinfo-file', action='store', default='', dest='packInfoFile', help='packlist maintain list file')
    args = parser.parse_args()
    logging.info('xml-file : ' + args.xmlFile)
    logging.info('auto-download : ' + str(args.bDownload))
    logging.info('auto-build : ' + str(args.bBuild))
    logging.info('bind-type : ' + args.bindType)
    logging.info('force-update : ' + str(args.bForce))
    logging.info('analyze-all : ' + str(args.bAll))
    
    error_summary = []
    
    #get all maintain list
    packInfoFile = conf.packinfo_aladdin_file
    if args.packInfoFile != '':
        packInfoFile = args.packInfoFile
    
    aladdin_maintain_list = []
    try:
        bdlist_file = open(packInfoFile, 'r')
        for line in bdlist_file.readlines():
            bdsd_maintain_list.append(line.strip('\r\n \t'))
        bdlist_file.close()
    except Exception, e:
        logging.error('error when get softid maintain list')
        logging.error(e)
        return
    
    #do it
    #1.update all hao123softid single xmls
    try:
        dom = xml.dom.minidom.parse(conf.aladdin_xml_full)
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            #softid
            nsoftid = node.getElementsByTagName('SoftID')
            if len(nsoftid) != 1:
                raise SoftIDError()
            softid = nsoftid[0].firstChild.wholeText
            logging.info('parsing softid %s' % softid)
            
            #if not in maintain list, ignore
            if (softid not in aladdin_maintain_list) and (not args.bAll):
                logging.info('%s is not in the maintain list, ignored' % softid)
                continue
            
            #if force update, delete the xml file first
            if args.bForce:
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
                    tfilename.appendChild(tdom.createTextNode(filename))
                else:
                    pass
                tsofturl = troot.getElementsByTagName('SoftURL')[0]
                if tsofturl.childNodes[0].data != downloadLink:
                    bUpdate = True
                    tsofturl.appendChild(tdom.createTextNode(downloadLink))
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
                    tname.appendChild(tdom.createTextNdoe(name))
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
                    ttitle.appendChild(tdom.createTextNdoe(title))
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
                tversion = troot.getElementsByTagName('Version')[0]
                if tversion.childNodes[0].data != version:
                    bUpdate = True
                    tversion.appendChild(tdom.createTextNdoe(version))
                else:
                    pass
            else:
                tversion = tdom.createElement('Version')
                tversion.appendChild(tdom.createTextNode(version))
                troot.appendChild(tversion)
            
            #Size
            nsize = node.getElementsByTagName('content3')
            size = nsize[0].firstChild.wholeText[5:]
            if bInited:
                tsize = troot.getElementsByTagName('Size')[0]
                if tsize.childNodes[0].data != size:
                    bUpdate = True
                    tsize.appendChild(tdom.createTextNdoe(size))
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
                    tupdateTime.appendChild(tdom.createTextNdoe(updateTime))
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
                    tsystemRequire.appendChild(tdom.createTextNdoe(update))
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
                    ticon.appendChild(tdom.createTextNdoe(iconAddr))
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
                #if bDownload is set, also download soft、ico, and update softmd5、logomd5、softid
                if args.bDownload:
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
                tdom.writexml(writer, '\n', ' ', '')
                writer.close()
                
                #build specific package
                if args.bBuild:
                    buildPackage(softid, args.bindType)
                    signPackage(softid, args.bindType)
                    renamePackage(softid, args.bindType)
                
            else:
                if args.bDownload:
                    if not os.path.isfile(conf.aladdin_package_folder + softid + '\\' + filename):
                        #soft
                        command = conf.wget_exe + ' ' + downloadLink + ' -O ' + conf.aladdin_package_folder + softid + '\\' + filename
                        os.system(command.encode(sys.getfilesystemencoding()))
                    if not os.path.isfile(conf.aladdin_package_folder + softid + '\\' + softid + '.png'):
                        #ico
                        command = conf.wget_exe + ' ' + iconAddr + ' -O ' + conf.aladdin_package_folder + softid + '\\' + softid + '.png'
                        os.system(command.encode(sys.getfilesystemencoding()))
                
    except Exception, e:
        logging.error('error occers while parsing aladdin full xml')
        logging.error(e)
        return
    
    #2.
    

if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))
    
    