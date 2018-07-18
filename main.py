#coding:utf8
import re
try:
    import requests
except ImportError:
    print "[!] Modul Requests tidak ditemukan [!]"
    pass
import sys
import socket
import os
import time
reload(sys)
sys.setdefaultencoding('utf8')
W  = '\033[0m'  # white (default)
R  = '\033[31m' # red
G  = '\033[1;32m' # green bold
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray

#LogFile
file = "/storage/emulated/0/ProxyLog.txt"
def slowprint(s):
    os.system("clear")
    print P+"Proxy Checker & Grab Proxy sslproxies.org"+W
    for c in s + '\n':
        sys.stdout.write(c)
        sys.stdout.flush() # defeat buffering
        time.sleep(2./90)
def pepong():
    cek = requests.session()
    dic = {}
    url = "https://www.sslproxies.org/"
    print "--- MENGUNJUNGI SITE ---"
    print url
    print "\n--- Mencari Proxy:Port ---"
    page = cek.get(url).text
    proxy = re.findall(r"\d+\.\d+\.\d+\.\d+",page)
    port = re.findall(r"\**<td>\d+</td>", page)
    for i in range(len(proxy)):
        ports = port[i].replace("<td>", "").replace("</td>", "")
        print B+proxy[i]+":"+str(ports)+W
        dic.update({proxy[i]:str(ports)})        
    return dic
def test(proxy, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(int(timeout))
    print "\r\n[*] --- Analisa Proxy --- [*]"
    try:
        print "Connect to Proxy: "+O+proxy+":"+str((port))+W
        sock.connect((proxy,port))
        print "Get to Host: ", host
        payload = "CONNECT http://%s HTTP/1.1\r\nHost: %s\r\n\r\n" % (host, host)
        sock.sendall(payload)
        resp = sock.recv(9000).split("\r\n")[0]        
        if resp in ['HTTP/1.1 200 OK', 'HTTP/1.1 200 Connection established', 'HTTP/1.0 200 Connection established' ]:
            print "Status Code: ", G+resp+W
            print "Proxy disalin ke: ", file
            save = open(file, "a+")
            save.write("%s:%s\n" % (proxy,str(port)))
            save.close()
        else:
            print C+resp+W
    except socket.timeout:
        print R+"[!] TIME OUT [!]"+W
    except socket.error:
        print R+"[!] Cek Jaringan [!]"+W
    except IOError:
        print R+"[!]{}[!]\n[!]Tidak diketahui[!]".format(file)+W
    print "[*] ---------------------------- [*]"
def scan_all():
    for proxy,port in pepong().items():
        test(proxy,int(port))
    print "Selesai"    
def files_txt(o):
    proxy_list = []
    print "Membuka List"
    with open(o) as proxy_port:
        for list_proxy in proxy_port.readlines():
            proxy_list.append(list_proxy.split("\n")[0])
    for proxy in proxy_list:
        proxy = proxy.split(":")
        test(proxy[0], int(proxy[1]))
def ops():
    while True:
        print "\n----- [ MENU ] -----\n1. Grab Proxy Online\n2. Proxy Checker\n3. Proxy Checker List (*.txt)\n--------------------\r\n"
        try:
            opt = int(raw_input(C+"Masukkan Pilihan: "+W))
            if opt == 1:
                print "[*]------[ Scraping Proxy ]-----[*]"
                scan_all()
            elif opt == 3:
                print "[*]------[ Proxy Checker List ]------[*]"
                ask = raw_input(C+"Insert Your file txt: "+W)
                files_txt(ask)
            elif opt == 2:
                print "[*]------[ Proxy Checker ]------[*]"
                print "[?] Masukkan Proxy:port, Contoh: %s [?]" % (R+"127.0.0.1:8080"+W)
                t = raw_input(C+"Inser Proxy:Port: "+W)
                proxy = t.split(":")
                test(proxy[0], int(proxy[1]))
            else:
                print R+"[!] Masukkan Pilihan dengan Benar [!]"+W
                continue
        except IndexError:
            print R+"[!] Kesalahan Memasukkan Proxy [!]"+W
            continue
        except ValueError:
            print R+"[!] Pilihan Tidak Diketahui [!]"+W
            continue
        except:
            print R+"[!] Bodo Amat Ulang [!]"+W
            continue
        
        break
if __name__ == "__main__":
    slowprint("""
    	Author: """+R+
    		"""QIUBY """+W+
    			"""ZHUKHI"""+O+
    				"""\n\t-= [PBM] =- TEAM"""+W)
    print O+"[?] Delay memekai hitungan Detik\n[?] [Enter] jika 3 Detik"+W
    timeout = raw_input(C+"Delay : "+W)
    if timeout == '':
        timeout = 3
    print O+"[?] Contoh Akses Proxy ke google.com, ping.eu atau cmyip.com\n[?] [Enter] Jika ga mau repot"+W
    host = raw_input(C+"Akses Proxy ke Site: http://"+W)
    if host == '':
        host = "google.com"    
    ops()
