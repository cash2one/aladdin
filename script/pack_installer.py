# coding=UTF-8
"""
@author    thomas
@date    2013-08-24
@desc
    
@change

"""

import sys
import os
import logging



def main(argc, argv):
    #init logging system, it's told logging is threadsafe, so do NOT need to sync
    logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG, stream = sys.stdout)



if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))
