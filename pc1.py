import socket , pickle
import time 
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5550))
server.listen(1)

server_socket, address = server.accept()
print ("Conencted to - " + str(address))

input("Press Enter to Connect...")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5553))


name = 'p1'

flag = False

token = []

inExecution = False

input('start')

server_socket.send(pickle.dumps(token))


def token_manager():
    while(1):
        data = client.recv(1024)
        global token
        token = pickle.loads(data)
        print("Token recived")
        global flag
        global inExecution
        flag=True
        time.sleep(5)
        if(token!=[]):
            if(token[0]==name):
                print("Starting execution")
                time.sleep(10)
                print("Done")
                token.remove(token[0])
                print(token)
        while(inExecution):
            time.sleep(1)
        flag=False   
        server_socket.send(pickle.dumps(token))
        


reciver_sender = threading.Thread(target=token_manager)
reciver_sender.start()

def demande_execution():
    while(1):
        demande = server_socket.recv(1024)
        if(flag==True):
            global token
            token.append(demande.decode())
            print("Demande of "+ str(demande.decode())+" has been added")
            print(token)
        else:
            client.send(demande)

demande_exec = threading.Thread(target=demande_execution)
demande_exec.start()

while(1):
    input("Press Enter to request execution\n")
    if(flag):
        if(not token):
            inExecution = True
            print("Starting execution")
            time.sleep(10)
            print("Done")
            inExecution = False
        else:
            token.append(name)
            print(token)
    else:
        client.send(name.encode())  