#!/usr/bin/env python
from optparse import OptionParser
from socket import *
import sys
import time
import random

'''
class MyWriter(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
'''
def h2ip(host):
    try:
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
        output("[+] Connected to %s:%d"%(host, port))
        #try:
        #    cop = bg
        #except NameError:
        #    bg = False
        if bg:
            banner=bgrabber(sock)
            if banner:
                output("[+] Banner: %s"%banner)
            else:
                output("[!] Can't grab the target banner")
            sock.close() # Done

    else:
        output("[!] Can't connect to %s:%d"%(host, port))
        
def output(text):
    global write_to_file
    print(text)
    #if write_to_file == False:
    #    print(text)
    #else:
        #with open(write_to_file,"a") as s:
        #    #original = sys.stdout
        #    sys.stdout = MyWriter(sys.stdout, s)
        #    print(text)


if __name__=="__main__":
    parser=OptionParser()
    parser.set_defaults(bg=True)
    parser.add_option("-t", "--target", dest="host", type="string",
                      help="enter host name", metavar="hede.com")
    parser.add_option("-p", "--port", dest="ports", type="string",
                      help="port you want to scan separated by comma", metavar="PORT")
    parser.add_option("-P", "--port-list", dest="portsfile", type="string",
                      help="ports file you want to scan separated one line", metavar="/tmp/portfile")
    parser.add_option("-T", "--target-list", dest="targetsfile", type="string",
                      help="file that contains targets one line", metavar="/tmp/hostlist")
    parser.add_option("-i", "--interval", dest="interval", type="string",
                      help="scanning time interval, default is 1 sec", metavar="")
    parser.add_option("-b", "--print-banner", action="store_true", dest="bg", default=False,
                      help="Grab the banner")
    parser.add_option("-f", "--print-output", type="string", dest="write_to_file",
                      help="Write output to file also", metavar="/tmp/outputfile")
    (options, args)=parser.parse_args()
    bg=options.bg

    if options.interval == None:
        interval = 1
    else:
        interval = options.interval

    if options.write_to_file == None:
        write_to_file = False
    else:
        write_to_file = options.write_to_file

    if options.ports==None or (options.targetsfile==None and options.host==None):
        parser.print_help()
    else:
        if options.host==None:
            with open(options.targetsfile) as f:
                hosts = f.readlines()
                random.shuffle(hosts)
        elif options.targetsfile==None:
            host = options.host
        else:
            parser.print_help()
            sys.exit()
        if options.portsfile==None:
            ports=(options.ports).split(",")
        else:
            with open(options.portsfile) as f:
                ports = f.readlines()
        random.shuffle(ports)

        try:
            ports=list(filter(int, ports))
            random.shuffle(ports)
            c=len(ports)
            try:
                for host in hosts:
                    ip=h2ip(host)
                    if ip:
                        output("[+] Running scan on %s"%host)
                        output("[+] Target IP: %s"%ip)
                        scan(ip, int(ports[c-1]))
                        c-=1
                        time.sleep(float(interval))
                        output("")

                    else:
                        output("[!] Invalid host %s"%host)
            except NameError:
                ip=h2ip(host)
                if ip:
                    output("[+] Running scan on %s"%host)
                    output("[+] Target IP: %s"%ip)
                    c=len(ports)
                    for port in ports:
                        scan(ip, int(port))
                        c-=1
                        if c>=1:
                            time.sleep(float(interval))
                else:
                    output("[!] Invalid host %s"%host)


        except KeyboardInterrupt:
            output("Interrupted by User")
            sys.exit()

