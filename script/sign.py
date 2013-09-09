# coding=UTF-8
"""
@author    thomas
@date    2013-02-22
@desc
    Sign pe files recursively in specific dir
@change
    
"""
import sys,fileop,sign_conf,xml.dom.minidom

def main(argc, argv):
    if argc != 3:
        print 'usage:python sign.py <product (bdm|bdkv)> <dir>'
        return
    
    argv[2] = argv[2].strip('"')
    if argv[2][-1] != '\\':
        argv[2] += '\\'
    
    try:
        done = False
        signId = '0'
        confFile = ''
        excluded_dir = []
        if argv[1].lower() == 'bdm':
            confFile = sign_conf.sign_conf_file
            excluded_dir = sign_conf.mgr_official_sign_excluded_dir
        elif argv[1].lower() == 'bdkv':
            confFile = sign_conf.kvsign_conf_file
            excluded_dir = sign_conf.kv_official_sign_excluded_dir
        dom = xml.dom.minidom.parse(confFile)
        root = dom.documentElement
        for node in root.childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.getAttribute('sign') != '1':
                continue
            if node.getAttribute('sign') == '1':
                if done:
                    #node.setAttribute('sign','0')
                    continue
                type = node.getAttribute('type')
                if type == 'baidu_cn':
                    signId = '1'
                elif type == 'baidu_bj_netcom':
                    signId = '2'
                elif type == 'baidu_jp':
                    signId = '3'
                #node.setAttribute('sign','0')
                done = True
        writer = open(confFile,'w')
        dom.writexml(writer)
        writer.close()
        
        #login
        #ret = fileop.loginSignServer(sign_conf.cerf_login_server)
        #print ret
        
        if done:
            fileop.FileOperationWithExtraPara(argv[2],fileop.SignBaidu,(argv[1].lower(),signId),sign_conf.sign_file_exts.split(','),excluded_dir)
    except fileop.SignBaiduException,e:
        print e
        raise e
    except Exception,e:
        print "error occers when parsing xml or run command:"
        print e


if "__main__" == __name__:
    sys.exit(main(len(sys.argv),sys.argv))
