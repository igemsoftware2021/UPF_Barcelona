import socket
import threading
import pickle
import numpy as np


class IRIS():
    
    

    def receptor():
        while True:
            try:
                message = IRIS.client.recv(1024).decode('ascii')
                    
                if message == 'SEND_CONTACT':
                    email = input("Question for contact received. Email?  ")
                    email_packet = 'EMAIL:'+email
                    IRIS.client.send(email_packet.encode('ascii'))
                    print("Contact data sent!")
                    
                elif message == 'SEND_ARRAY':
                    print("Question for array received.")
                    HEADERSIZE = 10
                    packet = pickle.dumps(IRIS.array)
                    packet = bytes(f"{len(packet):<{HEADERSIZE}}", 'utf-8')+packet
                    IRIS.client.send(packet)
                    print("Array data sent!")
                    IRIS.client.close()
                    break
                else:
                    pass
               
            except:
                print("An error occured!")
                IRIS.client.close()
                break
            
        print("Request completed")
      
           
    def writer():
        while True:
            message = input()
            IRIS.client.send(message.encode('ascii'))
            
            
    def start_communication(array):
        
        IRIS.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        omega_IP = '192.168.0.164'
        IRIS.client.connect((omega_IP, 55555))
        IRIS.array = array
            
        print("Welcome to IRIS")        
        print("Write 'REQUEST' to start communications with Omega")
        
        IRIS.receptor_thread = threading.Thread(target=IRIS.receptor)
        IRIS.receptor_thread.start()
        
        IRIS.writer_thread = threading.Thread(target=IRIS.writer)
        IRIS.writer_thread.start()
        
           
      
            
    
IRIS.start_communication(np.asarray([0,0,1,0,1,0,0,0,1]))
