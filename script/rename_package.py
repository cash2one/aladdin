# coding=UTF-8
"""
@author    thomas
@date    2013-08-31
@desc
    remove all file exclud softsetup.exe and task.xml,
    rename softsetup to Setup.exe
@change
    init ------------------------------------- 2013.08.31
"""

import sys
import os
import logging
import argparse
import glob
import xml.dom.minidom

def FileOperation(dir,op,fileType,excluded_dir=[]):
    #root dir
    for type in fileType:
        destPath = dir + type
        for file in glob.glob(destPath): 
            excluded = False
            for exdir in excluded_dir:
                if file.lower().find(exdir) != -1:
                    excluded = True
                    break
            if not excluded:
                op(file)
    for root, folders,files in os.walk(dir): 
        for type in fileType:    
            for folder in folders:
                if root[-1] == '\\':
                    destPath = root + folder + '\\' + type
                else:
                    destPath = root + '\\' + folder + '\\' + type
                for file in glob.glob(destPath): 
                    excluded = False
                    for exdir in excluded_dir:
                        if file.lower().find(exdir) != -1:
                            excluded = True
                            break
                    if not excluded:
                        op(file)


def getOriginalName(file):
    try:
        dom = xml.dom.minidom.parse(file)
        root = dom.documentElement
        nodes = root.getElementsByTagName('FileName')
        for node in nodes:
            return str(node.childNodes[0].data)
    except Exception, e:
        logging.error("error occers when parsing : " + file)
        logging.error(e)

def renameExe(file):
    if len(file) > 4 and file[-4:] == '.xml':
        exe = file[0:-8] + 'setup.exe'
        command = 'rename ' + exe + ' ' + getOriginalName(file)
        logging.info(command)
        os.system(command)

def main(argc, argv):
    #init logging system, it's told logging is threadsafe, so do NOT need to sync
    logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG, stream = sys.stdout)

    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--trip-directory', action='store', default='d:\\aladdin\\softicons\\products', dest='dir', help='dir to handle with')
    args = parser.parse_args()
    logging.info('trip-directory : ' + args.dir)
    
    #do work
    FileOperation(args.dir,renameExe,'*.xml')

if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))

