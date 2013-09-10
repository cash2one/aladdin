import sys
import time
import logging
import conf
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AladdinEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        logging.info('%s, %s' % (event.event_type, event.src_path))

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
    