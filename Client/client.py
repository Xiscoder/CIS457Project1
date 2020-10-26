import socket
import os
import sys

class FTPConnection():

    #constructor for class that sets connection to false
    def __init__(self):
        self.connected = False

    def connect(self, address, port):
        self.connected = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, port))


    def listFilesInDir(self):
        self.sock.sendall("LIST".encode())
        print(self.sock.recv(1024).decode())
    


    def storeFile(self, fileName):
        
        # Error checking to see if file exists
        try:
            sizeOfFile = os.path.getsize("./" + fileName)
        except:
            print("Cannot find file")
            return

        self.sock.sendall(("STORE " + fileName  + " " + str(sizeOfFile)).encode())

        file = open(fileName, 'rb')

        # easy way to set both Data and line to collect the correct encoded bytes
        Line = file.read(1024)
        Data = Line
        while(Line):
            Line = file.read(1024)
            Data += Line
        self.sock.sendall(Data)
        file.close()
        
        print(self.sock.recv(1024).decode())
          
    
    def retrieveFile(self, fileName):
        #Send the initial
        self.sock.sendall(("RETRIEVE " + fileName).encode())

        #get filesize from server
        fileSize = self.sock.recv(1024).decode()
 
        file = open(fileName, "wb")
        data = sock.recv(int(fileSize), socket.MSG_WAITALL)
        file.write(data) 
        file.close()
        print("File Retrieved")

    def quit(self):    
        self.sock.sendall("QUIT".encode())
        print(self.sock.recv(1024).decode())
        self.sock.close()
    

# CODE ENTERS HERE
connection = FTPConnection()
try:
    # for a nice clean CLI for each command
    cli = "\nClientCLI> "
    while (True):
        ## read in input from terminal and split it for sending to functions and make upper case for comparison reasons
        inputs = str(input(cli))
        inputs = inputs.split(" ")
        inputs[0] = inputs[0].upper() 

        ## if we are not connected yet, try and connect
        if connection.connected == False:
            if inputs[0] == "CONNECT":
                try:
                    connection.connect(inputs[1], int(inputs[2]))
                    print("Connected to host: " + inputs[1] + " at port: " + inputs[2])
                except:
                    connection = FTPConnection()
                    print("Error with connection")
            else:
                print("Use CONNECT <host><PORT> to connect to a server")
        else:
            if inputs[0] == "LIST":
                connection.listFilesInDir()
            elif inputs[0] == "RETRIEVE":
                connection.retrieveFile(inputs[1])
            elif inputs[0] == "STORE":
                connection.storeFile(inputs[1])
            elif inputs[0] == "QUIT":
                connection.quit()
                connection = FTPConnection()
                break
            else:
                print("Command must be: QUIT, LIST, STORE or RETRIEVE")
            
except:
    connection.quit()