# -*- coding: utf-8 -*-

import tensorflow.keras
import socket
import threading
import pickle
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import numpy as np


          
"""
In this first section, the connecton parameters are preapred.
This includes, for instance, to automatically extract the IP 
of the machine in which the server is executed, to define
the port, to start the listening connection and to define
the login data for the service address, that is, the email
from which the reports are going to be sent.
"""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host = s.getsockname()[0]

port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
addresses = []
port_mail = 465  
SENDER = "SERVICE_ADDRESS@PROVIDER.DOMAIN"
PASSWORD = 'SERVICE_ADDRESS_PASSWORD'


"""
This simple function is used to load the neural subunits
from the directory 'omegacore'. They are saved in a dictionary
by their name, so then can be used for inference.
"""

def load_omegacore():
    
     omegacore = {}
    
     subunits = os.listdir("omegacore")
     
     for subunit_name in subunits:
         
         omegacore[subunit_name] = tensorflow.keras.models.load_model(subunit_name)
         
     return omegacore
         
"""
The inference module is the one performing the analysis per se.
If there are neural subunits availables, the emergent behaviors associated
to those that provide a positive result are added to the report. 
If there are not, the system is in TEST MODE, so the report is just the 
number of positives per row.
"""
def inference(array, TEST_MODE):
    
     report = []
     
     if TEST_MODE:
         
        for row in array: 
            report.append(str(sum(row))+" positives")
            
     
        
     else:
         
        for key in omegacore.keys():
         
            CNN_input = np.expand_dims(array, axis=0)
          
            if omegacore[key].predict(CNN_input, verbose=1) > 0.5:
              
                report.append(key)   

         
     return report
              
         
"""
This modules constructs the report message and sends it to the
requester, both in text plane and html. Depending on the results
obtained, or if the system is in TEST MODE, the response
is adapted.
"""
def send_report(REQUESTER, REPORT, TEST_MODE, CLIENT):
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Omega Inference Demo"
    message["From"] = SENDER
    message["To"] = REQUESTER
    
    print(REPORT)
    diagnostic = "\n "
    for i in range(len(REPORT)-1):
        diagnostic += " " + REPORT[i].replace("_", " ") + ", "
    diagnostic += "  and  "+REPORT[len(REPORT)-1].replace("_", " ") +"."
  

    print("Message configured")
    
    text = '\n Hello there, \n'

    text += '\n This is Omega, one of the AI Systems belonging to ARIA.'
    
    text += '\n These are the results requested. \n'
    
    if TEST_MODE:
        
        text += '\n OmegaSever was in Test Mode, so here there is a description of the sample row by row. \n'
        text += '\n There are '
    
    else:
        
        if len(REPORT) == 0:
            text += "\n The sample sent was found to be clear, with no signs of dangerous behaviors."
        else:
            text += "\n Attention! The sample sent has been identified as potentially dangerous."
            
            text += "\n The markers detected imply  "
    
    text += diagnostic
    
    text += '\n\n Thank you for your interest in this technical demo.'
    
    text += '\n If you want to know more, visit our website.'
           
    text += '\n \n https://aria-igem.netlify.app/index.text'
    
    text += '\n \n Regards, '
    
    text += '\n \n Omega. '
    
    
    print("Text version prepared")
            
    
    html = '<html> \n <body> \n <p>'
    
    html += '\n Hello there, <br><br>'

    html += '\n This is Omega, one of the AI Systems belonging to ARIA.<br>'
    
    html += '\n These are the results requested. \n <br><br>'
    
    if TEST_MODE:
        
        html += '\n OmegaSever was in Test Mode, so here there is a description of the sample row by row.  <br> \n'
        html += '\n There are '
    
    else:
        
        if len(REPORT) == 0:
            html += "\n The sample sent was found to be clear, with no signs of dangerous behaviors. <br>"
        else:
            html += "\n Attention! The sample sent has been identified as potentially dangerous.  <br>"
            
            html += "\n The markers detected imply  "
        
    html += diagnostic
    
    html += '\n  <br><br>  Thank you for your interest in this technical demo. <br>'
    
    html += '\n If you want to know more, visit our website.  <br>'
    
    html += '\n <br> <a href="https://aria-igem.netlify.app/index.html">ARIA iGEM Project</a> <br>'
    
    html += '\n    <br> Regards, <br>'
    
    html += ' <br> \n Omega. \n <br> \n </p> \n </body> \n </html>'
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    print("HTML version prepared")

    message.attach(part1)
    message.attach(part2)
    
    print("Message built")
    
    context = ssl.create_default_context()

    try:
        
        with smtplib.SMTP_SSL("smtp.gmail.com", port_mail, context=context) as server:
            try:
                server.login(SENDER, PASSWORD)  
                try:
                    server.sendmail(SENDER, REQUESTER, message.as_string())
                    print("Successfully sent email")
                    CLIENT.send('DONE'.encode('ascii'))
                except: 
                    print("Failed to send the mail")
            except:
                print("Failed to login")
       
    except:
      
        print("Error: unable to send email")

    
         
"""
This module is the core processing the data received from IRIS, 
and implementing the communication protocol between them.
If the message received is found to be an object, the inference-report
pipeline is started. If not, it is seen as a string and analyzed using
the command response structure. As a final note, it is also the one
closing the connection when the request is completed.
"""
def process(message, TEST_MODE, CLIENT):
    
    packet_object = False
    
    global REQUESTER
    
    try:
        
        packet = message.decode('ascii')
        
    except:
        
        packet = message
        packet_object = True

    if packet_object:
    
        
        print("Processing array data...")
        HEADERSIZE = 10
        array = pickle.loads(packet[HEADERSIZE:])
        print(array)
        
        REPORT = inference(array, TEST_MODE)
        
        print("Sending results to contact")
        
        
        try:
            send_report(REQUESTER, REPORT, TEST_MODE, CLIENT)
        except Exception as e:
            print("ERROR: There was a problem sending the report...")
            print(e)
            
        packet_object = ""
        
        
    else:
        
        if packet == 'REQUEST':
            print(str(addresses[clients.index(CLIENT)][0])+" is making a request.")
            print("Asking for contact...")
            CLIENT.send('SEND_CONTACT'.encode('ascii'))
        elif packet[:6] == 'EMAIL:':
            print(str(addresses[clients.index(CLIENT)][0])+"'s contact received.")
            REQUESTER = packet[6:]
            print(REQUESTER)
            CLIENT.send('SEND_ARRAY'.encode('ascii'))
        elif packet == 'DONE':
            index = clients.index(CLIENT)
            clients.remove(CLIENT)
            CLIENT.close()
            address = addresses[index]
            print('{} disconnected'.format(address).encode('ascii'))
            addresses.remove(address)

"""
The manager is a simple module that is loaded in multiple threads,
designed to control the interaction with one specific IRIS instance,
so the information can flow between both parts in an ordered and structured 
manner. Furthermore, it is able to stop the connection if a problem is detected,
as an additional mechanism if the request cannot be completed properly.
"""
def manager(client, TEST_MODE):
    while len(clients) != 0:
        try:
            message = client.recv(1024)
            process(message, TEST_MODE, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            address = addresses[index]
            print('{} disconnected'.format(address).encode('ascii'))
            addresses.remove(address)
            break

"""
The receptor is the listening function that constantly executes
when the server is active. It waits for IRIS instances to connect,
and when they do so, it saves them as current clients and start
a managing thread for them.
"""
            
def receptor(TEST_MODE):
    while True:
        
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        clients.append(client)
        addresses.append(address)
        
        thread = threading.Thread(target=manager, args=(client,TEST_MODE))
        thread.start()

        
"""
This is the system workflow.
1. The server search for the OmegaCore Subunits.
2. If they are available, they are loaded and prepared.
3. If not, a message is shown to the user explaining that inference is not possible
and that the system goes into TEST MODE.
4. One way or the other, the receptor is started.
"""
   
if __name__ == "__main__":
    
    print(" ")
    print(" ")
    print("        O M E G A    S E R V E R        ")
    print("----------------------------------------")
    print("OmegaServer is waiting for requests")
    
    omegacore = {}
    TEST_MODE = False
    
    try:
        omegacore = load_omegacore()
    except Exception as e:
        print("ERROR: The OmegaCore Subunits could not be loaded")
        print(e)
        TEST_MODE = True
        
    
    if len(omegacore) == 0:
        print(" ")
        print("Attention! There are not OmegaCore subunits available.")
        print("Inference is not possible, so Test Mode is activated.")
        print("------------------------------------------------------------------------")
        print("In test mode, OmegaServer can process requests and communicate via email.")
        print("However, the report sent will not show the diagnostic result, but a the number ")
        print("of positives per row in the array.")
        print(" ")
        TEST_MODE = True
  
    try:
        receptor(TEST_MODE)
    except Exception as e:
        print("ERROR: Communication failed")
        print(e)
            
    input("Press any key to close")
