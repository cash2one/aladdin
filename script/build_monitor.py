# coding=UTF-8
"""
@author    thomas
@date    2013-08-24
@desc
    watcher
@change
    init ------------------------------------- 2013.09.06
"""

import sys
import time
import logging
import conf
import comm
import aladdin
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AladdinEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.bReady = False
    def on_any_event(self, event):
        logging.info('%s, %s' % (event.event_type, event.src_path))
        if str(event.src_path).lower() == conf.watchdog_notify_ready_file:
            msg = comm.getMsg(conf.watchdog_notify_ready_file)
            if msg.lower() == conf.ready_string:
                self.bReady = True
                comm.saveFile(conf.watchdog_notify_ready_file, conf.not_ready_string)
                logging.info('-----------------------------------------')
                logging.info('start building aladdin installers')
                
                #top20 bind1 always build, using full xml
                aladdin.buildAladdinPackage(xmlFile=conf.aladdin_xml_full, bDownload=False, bBuild=True, bindType='baidusd', bForce=False, bAll=False, packInfoFile=conf.baidusd_packinfo_file, o_softId='', bCopy=True, o_xsoftId='', xpackInfoFile='', bNoBuild=False, bNoCopyToUpdate=False)
                
                #top20 bind1 always build, using daily xml
                aladdin.buildAladdinPackage(xmlFile=conf.aladdin_xml_daily, bDownload=False, bBuild=True, bindType='baidusd', bForce=False, bAll=False, packInfoFile=conf.baidusd_packinfo_file, o_softId='', bCopy=True, o_xsoftId='', xpackInfoFile='', bNoBuild=False, bNoCopyToUpdate=False)
                
                ############################################################################################################################
                
                #top20 unbind update build, using full xml
                aladdin.buildAladdinPackage(xmlFile=conf.aladdin_xml_full, bDownload=False, bBuild=False, bindType='baidusd_nobind', bForce=False, bAll=False, packInfoFile=conf.baidusd_packinfo_file, o_softId='', bCopy=True, o_xsoftId='', xpackInfoFile='', bNoBuild=False, bNoCopyToUpdate=False)
                
                #top20 unbind update build, using daily xml
                aladdin.buildAladdinPackage(xmlFile=conf.aladdin_xml_daily, bDownload=False, bBuild=False, bindType='baidusd_nobind', bForce=False, bAll=False, packInfoFile=conf.baidusd_packinfo_file, o_softId='', bCopy=True, o_xsoftId='', xpackInfoFile='', bNoBuild=False, bNoCopyToUpdate=False)
                
                ############################################################################################################################
                
                #top20-80 unbind update build, using full xml
                aladdin.buildAladdinPackage(xmlFile=conf.aladdin_xml_full, bDownload=False, bBuild=False, bindType='baidusd_nobind', bForce=False, bAll=False, packInfoFile=conf.baidusd_packinfo_20_80_file, o_softId='', bCopy=True, o_xsoftId='', xpackInfoFile=conf.baidusd_packinfo_20_80_excluded_file, bNoBuild=False, bNoCopyToUpdate=False)
                
                #top20-80 unbind update build, using daily xml
                aladdin.buildAladdinPackage(xmlFile=conf.aladdin_xml_daily, bDownload=False, bBuild=False, bindType='baidusd_nobind', bForce=False, bAll=False, packInfoFile=conf.baidusd_packinfo_20_80_file, o_softId='', bCopy=True, o_xsoftId='', xpackInfoFile=conf.baidusd_packinfo_20_80_excluded_file, bNoBuild=False, bNoCopyToUpdate=False)
                
                logging.info('-----------------------------------------')
                logging.info('build complete')
                self.bReady = False
            

def main(argc, argv):
    #set sysencoding to utf-8
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    #init logging system, it's told logging is threadsafe, so do NOT need to sync
    logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG, stream = sys.stdout)
    
    event_handler = AladdinEventHandler()
    observer = Observer()
    for item in conf.watchdog_notify_list:
        observer.schedule(event_handler, item, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))
    
