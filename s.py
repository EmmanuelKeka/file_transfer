import socket
import threading

from time import gmtime, strftime
import time
import hashlib
import os


HOST = '127.0.0.1'        
PORT = 50007              
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))


  
    
# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""   

# custom say hello command
def sayHello():
    print ("----> The hello function was called")
    

# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a 
# command it will then need to extract the command.
def parseInput(data, con):
    print("parsing...")
    print(str(data))
    
    # Checking for commands 
    if "<getservertime>" in str(data):
        print("command in data..")

    elif "<get" in str(data):
        parts = str(data).split('-')
        print(parts[0]) # command
        print(parts[1]) # filename   <get-chunk0.mp3>
        filename = str(parts[1])[0:-3] # cut the last 3 chars off
        print(filename)
        f = open(filename, 'rb')
        content = f.read()
        con.sendall(content)
        f.close()

    elif "<addsong" in str(data):
        print("adding song....")
        items = data.split('-')
        print(items[0])
        print(items[1])
        print(items[2])
        f = open("server/" + str(items[2]), 'wb')
        filedata = con.recv(500)
        while filedata:
            print(filedata)
            f.write(filedata)
            if 'END' in str(filedata):
                f.close()
                break
            filedata = con.recv(500)

        f.close()
        con.close()
    elif "<listall" in str(data):
        files = os.listdir(path='server/.')
        justMp3s = list()
        for onefile in files:
            if ".mp3" in onefile:
                print(onefile)
                justMp3s.append(onefile)
        con.send(str(justMp3s).encode())
        

    elif "<hash" in str(data):
        m = hashlib.sha256()
        #read in the file
        file = open('chunk0.mp3', 'rb')
        content = file.read()
        # get the hash
        m.update(content)
        res = m.digest()
        print(res)
        file.close()
        
    
# we a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.
    
def manageConnection(conn, addr):
    global buffer
    print('Connected by', addr)
    
    
    data = conn.recv(1024)
    
    parseInput(str(data), conn)# Calling the parser, passing the connection
    
    print("rec:" + str(data))
    buffer += str(data)
    
    #conn.send(str(buffer))
        
    conn.close()


while 1:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args = (conn,addr))
    
    t.start()
    
    


