#!/usr/bin/env python
from optparse import OptionParser
from socket import *
import sys
import time

def h2ip(host):
    try:
        #print host
        host=host.strip("\n \"\'")
        ip=gethostbyname(host)
        return ip
    except Exception as e:
        return None

def connecto(host, port):
    try:
        s=socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        return s
    except:
        s.close()
        return None

def bgrabber(sock):
    try:
        sock.send("GET / HTTP/1.0\r\n\r\n")
        banner=sock.recv(1024)
        return banner
    except:
        return None

def scan(host, port):
    global bg
    sock=connecto(host, port)
    setdefaulttimeout(2) # set default timeout to 5 sec
    if sock:
        print("[+] Connected to %s:%d"%(host, port))
        #try:
        #    cop = bg
        #except NameError:
        #    bg = False
        if bg:
            banner=bgrabber(sock)
            if banner:
                print("[+] Banner: %s"%banner)
            else:
                print("[!] Can't grab the target banner")
            sock.close() # Done

    else:
        print("[!] Can't connect to %s:%d"%(host, port))
        
        

if __name__=="__main__":
    parser=OptionParser()
    parser.set_defaults(bg=True)
    parser.add_option("-t", "--target", dest="host", type="string",
                      help="enter host name", metavar="hede.com")
    parser.add_option("-p", "--port", dest="ports", type="string",
                      help="port you want to scan separated by comma", metavar="PORT")
    parser.add_option("-T", "--target-list", dest="targetsfile", type="string",
                      help="file that contains targets one line", metavar="/tmp/hostlist")
    parser.add_option("-i", "--interval", dest="interval", type="string",
                      help="scanning time interval, default is 1 sec", metavar="")
    parser.add_option("-b", "--print-banner", action="store_true", dest="bg", default=False,
                      help="Grab the banner")
    (options, args)=parser.parse_args()
    bg=options.bg
    if options.interval == None:
        interval = 1
    else:
        interval = options.interval
    if options.ports==None or (options.targetsfile==None and options.host==None):
        parser.print_help()
    else:
        if options.host==None:
            with open(options.targetsfile) as f:
                hosts = f.readlines()
        elif options.targetsfile==None:
            host = options.host
        else:
            parser.print_help()
            sys.exit()
        ports=(options.ports).split(",")
        try:
            ports=list(filter(int, ports))
            try:
                ip=h2ip(host)
                if ip:
                    print("[+] Running scan on %s"%host)
                    print("[+] Target IP: %s"%ip)
                    for port in ports:
                        scan(ip, int(port))
                        time.sleep(float(interval))
                        print("")
                else:
                    print("[!] Invalid host %s"%host)
            except NameError:
                for host in hosts:
                    ip=h2ip(host)
                    #print("IP:%s"%ip)
                    if ip:
                        print("[+] Running scan on %s"%host)
                        print("[+] Target IP: %s"%ip)
                        c=len(ports)
                        for port in ports:
                            scan(ip, int(port))
                            c-=1
                            if c!=1:
                                time.sleep(float(interval))
                        print("")

                    else:
                        print("[!] Invalid host %s"%host)
        except Exception as e:
            print e
