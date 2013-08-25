# coding=UTF-8
"""
@author    thomas
@date    2013-08-24
@desc
    ftp download to local, recursively, use curl.exe
@change
    init ------------------------------------- 2013.08.24
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
    parser.add_argument('-u','--remoteUrl', action='store', default='', dest='remoteUrl', help='remote url for download, must be folder')
    parser.add_argument('-l','--localPath', action='store', default=conf.package_folder, dest='localPath', help='local path to store, must be folder')
    parser.add_argument('-nr','--not-recursive', action='store_true', default=False, dest='nrecursive', help='not to download recursively')
    parser.add_argument('-a', '--fetch-all', action='store_true', default=False, dest='fetchAll', help='whether to fetch all')
    args = parser.parse_args()
    logging.info('remoteUrl : ' + args.remoteUrl)
    logging.info('localPath : ' + args.localPath)
    logging.info('resursive : ' + str(not args.nrecursive))
    logging.info('fetchAll : ' + str(args.fetchAll))
    
    #do work
    strR = ' ' if args.nrecursive else ' -r '
    remoteUrl = ''
    if args.fetchAll:
        remoteUrl = conf.ftp_host+':'+conf.ftp_port+conf.ftp_subdir
    else:
        remoteUrl =  args.remoteUrl
    if remoteUrl != '':
        command = conf.wget_exe + conf.wget_args + strR + remoteUrl + ' -P ' + args.localPath + ' --ftp-user=' + conf.ftp_user + ' --ftp-password=' + conf.ftp_password
        logging.info('command' + ' : ' + command)
        os.system(command)

if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))
