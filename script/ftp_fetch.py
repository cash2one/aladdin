# coding=UTF-8
"""
@author    thomas
@date    2013-08-24
@desc
    ftp download to local, recursively, use curl.exe
@change

"""

import sys
import os
import logging
import argparse
import conf


def main(argc, argv):
    #init logging system, it's told logging is threadsafe, so do NOT need to sync
    logging.basicConfig(format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG, stream = sys.stdout)

    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--remoteUrl', action='store', default=conf.ftp_host+':'+conf.ftp_port+conf.ftp_subdir, dest='remoteUrl', help='remote url for download, must be folder')
    parser.add_argument('-l','--localPath', action='store', default=conf.package_folder, dest='localPath', help='local path to store, must be folder')
    parser.add_argument('-nr','--not-recursive', action='store_true', default=False, dest='nrecursive', help='not to download recursively')
    args = parser.parse_args()
    logging.info('remoteUrl' + ' : ' + args.remoteUrl)
    logging.info('localPath' + ' : ' + args.localPath) 
    logging.info('resursive' + ' : ' + str(not args.nrecursive))
    
    #do work
    strR = ' ' if args.nrecursive else ' -r '
    command = conf.wget_exe + conf.wget_args + strR + args.remoteUrl + ' -P ' + args.localPath + ' --ftp-user=' + conf.ftp_user + ' --ftp-password=' + conf.ftp_password
    logging.info('command' + ' : ' + command)
    os.system(command)

if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))
