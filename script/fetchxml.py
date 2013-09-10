# coding=UTF-8
"""
@author    thomas
@date    2013-08-24
@desc
    fetch the latest xml file from hao123 website
@change
    init ------------------------------------- 2013.09.06
"""

import os
import sys
import logging
import argparse
import codecs
import comm
import conf

def convert_encoding(filename, target_encoding):
    # convert file from the source encoding to target encoding
    logging.info('converting %s to utf-8 file format' % filename)
    content = codecs.open(filename, 'r').read()
    content = content.decode('gbk') #.encode(source_encoding)
    codecs.open(filename, 'w', encoding=target_encoding).write(content)
    ctx = comm.getMsg(filename)
    ctx = ctx.replace('encoding="gbk"', 'encoding="utf-8"')
    comm.saveFile(filename, ctx)

def main(argc, argv):
    #set sysencoding to utf-8
    reload(sys)
    sys.setdefaultencoding('utf-8')
    os.chdir(sys.path[0])
    
    #init logging system, it's told logging is threadsafe, so do NOT need to sync
    logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG, stream = sys.stdout)
    
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--download-full-xml-file', action='store_true', default=False, dest='bUpdateFull', help='download the latest full xml file')
    parser.add_argument('-d', '--download-daily-xml-file', action='store_true', default=False, dest='bUpdateDaily', help='download the latest daily xml file')
    parser.add_argument('-t', '--translate-to-utf8', action='store_true', default=False, dest='bTranslate', help='auto translate the xml file to utf-8 file format')
    parser.add_argument('-b', '--autostart-build', action='store_true', default=False, dest='bBuild', help='auto trigle the switch to build')
    args = parser.parse_args()
    logging.info('-----------------------------------------')
    logging.info('download-full-xml : ' + str(args.bUpdateFull))
    logging.info('download-daily-xml : ' + str(args.bUpdateDaily))
    logging.info('auto-translate : ' + str(args.bTranslate))
    logging.info('auto-build : ' + str(args.bBuild))
    
    command = ''
    try:
        if args.bUpdateFull:
            command = conf.wget_exe + ' ' + conf.url_full_xml + ' -O ' + conf.aladdin_xml_full
            logging.info(command)
            os.system(command)
            if args.bTranslate:
                convert_encoding(conf.aladdin_xml_full, 'utf-8')
        if args.bUpdateDaily:
            command = conf.wget_exe + ' ' + conf.url_daily_xml + ' -O ' + conf.aladdin_xml_daily
            logging.info(command)
            os.system(command)
            if args.bTranslate:
                convert_encoding(conf.aladdin_xml_daily, 'utf-8')
        if args.bBuild:
            comm.saveFile(conf.watchdog_notify_ready_file, conf.ready_string)
    except Exception, e:
        comm.saveFile(conf.watchdog_notify_ready_file, str(e))
        
if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))
    