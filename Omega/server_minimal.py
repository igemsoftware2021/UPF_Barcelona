# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 15:47:00 2021

@author: JoelRH

"""
import socket
import threading
import pickle
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Connection Data
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host = s.getsockname()[0]

port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
addresses = []
requester = 'wadalibaba'
port_mail = 465  # For SSL
sender = "inference.omega@gmail.com"
password = 'omega_inference_pass'

def manage(message):
    
    packet_object = False
    
    global requester
    
    try:
        
        packet = message.decode('ascii')
        
    except:
        
        packet = message
        packet_object = True

    if packet_object:
        
        inference()
        
        print("Processing array data...")
        HEADERSIZE = 10
        array = pickle.loads(packet[HEADERSIZE:])
        print(array)
        
        print("Sending results to contact")
        print(requester)
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Omega Inference Demo"
        message["From"] = sender
        message["To"] = requester
        
        # Create the plain-text and HTML version of your message
        text = """\
        Hello there,
        
        This is Omega, one of the AI Systems belonging to ARIA.
        Thank you for your interest in this technical demo.
        
        If you want to know more, visit our website.
        
        aria-igem.netlify.app/index.html
        
        Regards, 
        
        Omega"""
        
        html = """\
        <html>
          <body>
            <p>Hello there,<br>
               <br>
               This is Omega, one of the AI Systems belonging to ARIA.<br>
               Thank you for your interest in this technical demo.<br>
               If you want to know more, visit our website.<br>
               <a href="https://aria-igem.netlify.app/index.html">ARIA iGEM Project</a> <br>
               <br>
               Regards, <br>
               <br>
               Omega.<br>
               
            </p>
          </body>
        </html>
        """
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)
        
        context = ssl.create_default_context()

        try:
            
            with smtplib.SMTP_SSL("smtp.gmail.com", port_mail, context=context) as server:
                try:
                    server.login(sender, password)  
                    try:
                        server.sendmail(sender, requester, message.as_string())
                        print("Successfully sent email")
                    except: 
                        print("Failed to send the mail")
                except:
                    print("Failed to login")
           
        except:
          
            print("Error: unable to send email")
        
    else:
        
        for i in range(len(clients)):
            
            if packet == 'REQUEST':
                print(str(addresses[i][0])+" is making a request.")
                print("Asking for contact...")
                clients[i].send('SEND_CONTACT'.encode('ascii'))
            elif packet[:6] == 'EMAIL:':
                print(str(addresses[i][0])+"'s contact received.")
                requester = packet[6:]
                print(requester)
                clients[i].send('SEND_ARRAY'.encode('ascii'))
            else:
                print("Unknown instruction, ignoring...")
                
def inference(client):
    pass
  

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            manage(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            address = addresses[index]
            manage('{} left!'.format(address).encode('ascii'))
            addresses.remove(address)
            break

# Receiving / Listening Function
def receive():
    while True:
        
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        clients.append(client)
        addresses.append(address)
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("O M E G A")
print("--------------------------------------")
print("Omega is waiting for a requests")

receive()