import socket
import os


def listFilesInDir(conn):
    dir = os.getcwd()
    filesInDir = os.listdir(dir)
    returnVal = "\n".join(filesInDir)
    conn.sendall(returnVal.encode())

def storeFile(conn, fileName, fileSize):


    file = open(fileName, "wb")
    data = conn.recv(int(fileSize), socket.MSG_WAITALL)
    file.write(data) 
    file.close()

    conn.sendall("File was stored on Server".encode())


def retrieveFile(conn, fileName):
    # Error checking to see if file exists
    try:
        sizeOfFile = os.path.getsize("./" + fileName)
    except:
        print("Cannot find file")
        conn.sendall("Could not find file".encode())
        return

    # send filesize across so receiver knows how big it is.
    conn.sendall(str(sizeOfFile).encode())
    # As the file exists, open it up, load it into data and send it
    file = open(fileName, 'rb')

    # easy way to set both Data and line to collect the correct encoded bytes
    Line = file.read(1024)
    Data = Line
    while(Line):
        Line = file.read(1024)
        Data += Line
    conn.sendall(Data)
    file.close()






# CODE ENTERS HERE
# 127.0.0.1 is local host
host = "127.0.0.1"
port = 1000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
print("SERVER IS RUNNING")
conn, client = s.accept()
with conn:
    while(True):
        Data = conn.recv(1024).decode()
        print("DATA RECEIVED FROM CLIENT: ", Data)
        #split data so we can access different parts of the command
        Data = Data.split(" ")
        if Data[0] == '':
            continue

        if Data[0] == "QUIT":
            print("ENDING SESSION")
            conn.sendall("\nENDING SESSION".encode())
            break
        elif Data[0] == "LIST":
            listFilesInDir(conn)
        elif Data[0] == "STORE":
                storeFile(conn, Data[1], Data[2])
        elif Data[0] == "RETRIEVE":
                retrieveFile(conn, Data[1])   
        else:
            conn.sendall("Command must be: QUIT, LIST, STORE or RETRIEVE".encode())