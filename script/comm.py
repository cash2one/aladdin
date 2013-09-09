# coding=UTF-8
"""
@date 2011-12-15
@brief common function 
@author thomas
"""

import xml.dom.minidom
import conf
import datetime, logging

def saveFile(fname, ctx):
    f=open(fname,"w")
    f.write(ctx)
    f.close()

def getMsg(fname):
    f=open(fname,"r")
    ret = f.read()
    f.close()
    return ret

def getFileBuf(fname):
    f = open(fname,'rb')
    ret = f.read()
    f.close()
    return ret

def setBuildNumber(product,num,bDailybuild = True,bUpdate = False):
    v4 = ''
    try:
        dom = xml.dom.minidom.parse('buildswitch/misc.xml')
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.getAttribute('name') == 'v4':
                v4 = node.getAttribute('value')
                break
    except Exception,e:
        logging.error("error occers when parsing xml or run command:")
        logging.error(e)
    if v4 != '$auto' and v4 != '' and not bUpdate:
        if not bDailybuild:
            v4 = str(int(v4)-1)
        if product == 'bdm':
            saveFile(conf.buildIdFile,v4)
        elif product == 'bdkv':
            saveFile(conf.kvBuildIdFile,v4)
        return v4
    elif not bUpdate:
        if not bDailybuild:
            if product == 'bdm':
                v4 = str(int(getMsg(conf.buildIdFile))-1)
                saveFile(conf.buildIdFile,v4)
            elif product == 'bdkv':
                v4 = str(int(getMsg(conf.kvBuildIdFile))-1)
                saveFile(conf.kvBuildIdFile,v4)
        return num
    elif bUpdate:
        return num

def getInstallerVersion(product):
    v1 = v2 = v3 = v4 = ''
    try:
        dom = xml.dom.minidom.parse('buildswitch/misc.xml')
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.getAttribute('name') == 'v1':
                v1 = node.getAttribute('value')
            elif node.getAttribute('name') == 'v2':
                v2 = node.getAttribute('value')
            elif node.getAttribute('name') == 'v3':
                v3 = node.getAttribute('value')
    except Exception,e:
        logging.error("error occers when parsing xml or run command:")
        logging.error(e)
    if v1 == '':
        v1 = '1'
    if product == 'bdm':
        v4 = getMsg(conf.buildIdFile)
        if v2 == '':
            v2 = '0'
    elif product == 'bdkv':
        v4 = getMsg(conf.kvBuildIdFile)
        if v2 == '':
            v2 = '1'
    if v3 == '':
        v3 = '0'
    if v4 == '':
        v4 = '0'
    return '%s.%s.%s.%s' % (v1,v2,v3,v4)

def getInstallerFullName(product):
    prefix = ''
    postfix = ''
    try:
        dom = xml.dom.minidom.parse('buildswitch/misc.xml')
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.getAttribute('name') == 'prefix':
                prefix = node.getAttribute('value')
            elif node.getAttribute('name') == 'postfix':
                postfix = node.getAttribute('value')
    except Exception,e:
        logging.error("error occers when parsing xml or run command:")
        logging.error(e)
    prefix = prefix.replace("$prefix","")
    postfix = postfix.replace("$postfix","")
    mainFix = ''
    if product == 'bdm':
        mainFix = 'BaiduAn_Setup_'
    elif product == 'bdkv':
        mainFix = 'Baidusd_Setup_'
    return '%s%s%s%s' % (mainFix,prefix,getInstallerVersion(product),postfix)

def getArchiveRoot(product):
    archive = ''
    try:
        dom = xml.dom.minidom.parse('buildswitch/misc.xml')
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.getAttribute('name') == 'archive':
                archive = node.getAttribute('value')
    except Exception,e:
        logging.error("error occers when parsing xml or run command:")
        logging.error(e)
    #archive = str(archive)
    archive = archive.replace("/","\\")
    archive = archive.replace("$share",conf.ftp_default_archive)
    archive = archive.replace("$version",getInstallerVersion(product))
    subdir = '%d-%d-%d' % (datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)
    archive = archive.replace("$date",subdir)
    if archive[-1] == '\\':
        archive = archive[:-1]
    if len(archive) <= 2:
        return ''
    elif archive[0] == '\\' and archive[1] == '\\':
        index = archive[2:].find('\\')
        return archive[0:index+2]
    
def getArchiveFullPath(product):
    archive = ''
    try:
        dom = xml.dom.minidom.parse('buildswitch/misc.xml')
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.getAttribute('name') == 'archive':
                archive = node.getAttribute('value')
    except Exception,e:
        logging.error("error occers when parsing xml or run command:")
        logging.error(e)
    #archive = str(archive)
    archive = archive.replace('/','\\')
    archive = archive.replace("$share",conf.ftp_default_archive)
    archive = archive.replace("$version",getInstallerVersion(product))
    subdir = '%d-%d-%d' % (datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)
    archive = archive.replace("$date",subdir)
    if archive[-1] == '\\':
        archive = archive[:-1]
    return archive

