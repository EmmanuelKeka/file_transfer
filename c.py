
# Echo client program
import socket
import os

HOST = '127.0.0.1'    # The remote host
PORT = 50007          # The same port as used by the server



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("type input:")
justMp3s = list()
text = input()

# when we send data to the server, we are using a colon
# at the end of a sentence to mark the end of the current sentence
# later when the input comes back, we will then be breaking the input
# into individual parts using the colon : to separate the lines
s.sendall((text + ":").encode())

def findAllSong():
    i = 0;
    files = os.listdir(path='client/.')
    for onefile in files:
        if ".mp3" in onefile:
            i = i + 1;
            print(str(i) + ". " + onefile)
            justMp3s.append(onefile)

if "<addsong" in text:
    print("getting ready to send file....")
    # read in the file chunk
    print("list of all user songs")
    findAllSong()
    print("pick a song:")
    pick = input()
    chunk = open("client/" + justMp3s[int(pick)-1], 'rb')
    content = chunk.read()
    chunk.close()
    # start
    # send
    s.sendall(content)
    s.sendall(str('END').encode())

elif "<get" in text:
    f = open('part.mp3','wb')
    output = s.recv(1000)
    while filedata:
        f.write(output)
        filedata = s.recv(1000)
    f.close()

elif "<hash" in text:
    ans = s.recv(1000)
    print(ans)
    print("Response:" + str(ans))

elif "<listall" in text:
    ans = s.recv(1000)
    print(ans)
    print("Response:" + str(ans))
    
s.close()
