#! usr/bin/python

from Tkinter import *
import ping, socket
import os, commands
import subprocess, multiprocessing
import easygui as eg

# ip_range = ["172.19.16.215", "172.19.10.235"]
ip_range = []
filePath = ''
user = ""
password = ""

def set_range(fromIP, toIP):
    from_ip = fromIP.get()
    to_ip = toIP.get()
    if not(len(from_ip)) and not(len(to_ip)):
        return
    suffix_start = int(from_ip.split(".").pop())
    suffix_end = int(to_ip.split(".").pop())
    prefix = from_ip.split(".")
    prefix.pop()
    temp=".".join(prefix)
    # ip_range=[]
    for i in range(suffix_start, suffix_end+1):
        ip_range.append(temp+"."+str(i))
    # ip_range = []

def pinger( job_q, results_q ):
    DEVNULL = open(os.devnull,'w')
    # while True:
    ip = job_q.get()
    if ip is None: 
        return 
        # break
    try:
        subprocess.check_call(['ping', '-c1', ip], stdout=DEVNULL)
        # subprocess.check_call(['ssh', 'sagar@'+ip], stdout=DEVNULL, stdin=filePath)
        # subprocess.check_call(['ssh', 'sagar@'+ip], stdout=DEVNULL)
        print ip, ": Reachable"
        results_q.put(ip)
    except:
        print ip, ": Not Reachable"
        pass

def test_connections():
    # for ip in ip_range:
    #     response = os.system("ping -c 1 " + ip)
    #     if response == 0:
    #         print ip, 'is up!'
    #     else:
    #         print ip, 'is down!'
    ###MULTIPROCESSING
    pool_size = 255
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()
    pool = [ multiprocessing.Process(target=pinger, args=(jobs,results))
             for i in range(pool_size) ]
    for p in pool:
        p.start()
    for ip in ip_range:
        jobs.put(ip)
        # jobs.put('192.168.1.{0}'.format(i))

def update_script(userEntry, passwordEntry, textArea):
    # path = str(eg.fileopenbox())
    # filePath = path
    user = userEntry.get()
    password = passwordEntry.get()
    text = textArea.get("1.0", END)
    text = text.split("\n")
    text = ";".join(text)
    # print "User: ", user 
    # print "Password: ", password
    # print "FilePath: ", path
    for ip in ip_range:
        command = "sshpass -p '"+ password+"' ssh -o StrictHostKeyChecking=no "+user+"@"+ip+" '"+text +"'"
        print command
        # command = "sshpass -p '"+ password+"' ssh -o StrictHostKeyChecking=no "+user+"@"+ip+" 'echo "+password+"| sudo -S apt-get -y install mpg321; export DISPLAY=:0; notify-send Installed!'"
        print commands.getoutput(command)
        print 'Done all IPs'
        # print command
        # command = "ssh " + user+"@"+ip+" < "+path
        # print command
    # file_open_path = open(path,'r')
    # textArea.insert('1.0',file_open_path.read())
    # print 'uploading script'

def main():
    global textArea
    root = Tk()

    userLabel = Label(root, text="Username: ")
    userLabel.pack(side='left')
    userEntry = Entry(root)
    userEntry.pack(side="left")

    passwdLabel = Label(root, text="Password: ")
    passwdLabel.pack(side="left")
    passwordEntry = Entry(root, show="*")
    passwordEntry.pack(side="left")

    fromLabel = Label(root, text="From: ")
    fromLabel.pack(side='left')
    fromEntry = Entry(root)
    fromEntry.pack(side="left")

    toLabel = Label(root, text="To: ")
    toLabel.pack(side="left")
    toEntry = Entry(root)
    toEntry.pack(side="left")
    
    setRange = Button(root, text='Range', command = lambda: set_range(fromEntry, toEntry))
    setRange.pack(side="left")

    testConnection = Button(root, text='Test Connections', command=test_connections)
    testConnection.pack(side="left")

    textArea = Text(root)
    textArea.pack(side='bottom', fill=X)

    updateScript = Button(root, text="Go!", command=lambda: update_script(userEntry, passwordEntry, textArea))
    updateScript.pack(side="left")

    # textArea.pack(side='bottom', expand=True, fill=X)
    
    root.mainloop()

if __name__ == '__main__':
    main()
