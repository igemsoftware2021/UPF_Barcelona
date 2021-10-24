
from kivy.config import Config
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.textfield import MDTextField
import cv2
import numpy as np
import socket
import threading
import pickle
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import re   
  
# This is the pattern for valid email identification.
email_expression = '[^@]+@[^@]+\.[^@]+'  

# This is a fixed size to ensure the scan view is properly visualized.
Window.size = (1280, 720)


"""
This is the Communication Subsystem, intended to implent the 
client-side of the Omega Architecture protocol. It includes a 
manager to answer OmegaServer's commands transmit the array data 
for subsequent processing and inference, and an initiation module to
establish connection with OmegaServer, start requests and initiate 
management threads.

"""
class Communication():
    
    # Client-side protocol management.
    def manager(email):
        
        print("Manager active")
        while True:
            
            try:
                message = Communication.client.recv(1024).decode('ascii')
                    
                if message == 'SEND_CONTACT':
                    email_packet = 'EMAIL:'+email
                    Communication.client.send(email_packet.encode('ascii'))
                    print("Contact data sent!")
                    
                elif message == 'SEND_ARRAY':
                    print("Question for array received.")
                    HEADERSIZE = 10
                    packet = pickle.dumps(Communication.array)
                    packet = bytes(f"{len(packet):<{HEADERSIZE}}", 'utf-8')+packet
                    Communication.client.send(packet)
                    print("Array data sent!")
                    
                elif message == 'DONE':
                    print("Request completed, finishing connection.")
                    Communication.client.send('DONE'.encode('ascii'))
                    Communication.client.close()
                    break
               
            except:
                print("An error occured")
                Communication.client.close()
                break
            
        print("Management finished")
      
    # Client-side protocol management.         
    def send_data(array, EMAIL):
        
        Communication.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        omega_IP = 'OMEGA_SERVER_IP'
        Communication.client.connect((omega_IP, 55555))
        Communication.array = array
        print("Communication established")
        
        message = 'REQUEST'
        Communication.client.send(message.encode('ascii'))
        print("Request sent")

        Communication.receptor_thread = threading.Thread(target=Communication.manager(EMAIL))
        print("Reception prepared")
        Communication.receptor_thread.start()
        print("Reception started")
        
 
        
"""
This is the Computer Vision System per se. It includes:

- A configuration function called before action to set all 
  the necessary parameters.
  
- A general processing function that is executed in real-time,
  provided that the CAPTURE MODE is active. It takes the general
  frame captured, passes to a search function, and if the array is 
  found, it is send to an analysis function intended to analyze
  the array cells content. Apart from that, this is also
  drawing a capture guide to assist the user during capture.
  
- A search function that detects the array in the general frame,
  and extracts it as a corrected and preprocessed mask.
  
- An analysis function that transforms the preprocessed mask
  into a binary matrix, encoding the positive and negative markers.
  
- A stop function to release the camera and finish processing.

"""
class Processor():
         
      def start():
        
        Processor.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        Processor.cam_w = Processor.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        Processor.cam_h = Processor.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        Processor.cam_res = Processor.cam_w*Processor.cam_h
        
        Processor.cam_center = (int(Processor.cam_w/2), int(Processor.cam_h/2))
        
        Processor.active = True
        Processor.search = False
        Processor.analyze = False
        Processor.scan = False
        Processor.request = False
            
        Processor.request = False
             
      
      def search_array(frame):
        
        array = -1
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      
        blur = cv2.GaussianBlur(gray, (5,5), 0)
          
        thresh1 = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
          
        contours, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    
        best_cnt = -1
        max_area = 0
        
        for i in contours:
                    
            area = cv2.contourArea(i)
            
            if area > Processor.cam_res*0.1:
                
                if area > max_area:
                    
                    (X,Y), (W, H), ang = cv2.minAreaRect(i)
                
                    ar = W/float(H)
                
                    if 0.8 <= ar <= 1.2:
                    
                        max_area = area
                        best_cnt = i
       
        mask = np.zeros((gray.shape),np.uint8)
    
        if isinstance(best_cnt, np.ndarray):
        
            (X,Y), (W, H), ang = cv2.minAreaRect(best_cnt)
            
            box = cv2.boxPoints(((X,Y), (W, H), ang))
            box = np.int0(box)
            cv2.drawContours(frame,[box],0,(255,255,255),2)
            
            ROI = np.array([[box[0], box[1], box[2], box[3]]], dtype=np.int32)
            cv2.fillPoly(mask, ROI, 255)
            array = cv2.bitwise_and(gray, mask)
    
            if W < H:
                ang = ang - 90;
    
            image_center = tuple(np.array(array.shape[1::-1]) / 2)
            rot_mat = cv2.getRotationMatrix2D(image_center, ang, 1.0)
            result = cv2.warpAffine(array, rot_mat, array.shape[1::-1], flags=cv2.INTER_LINEAR)
            
            X,Y,W,H = cv2.boundingRect(result)  
            array = result[Y:Y+H, X:X+W]       
            array = cv2.resize(array, (500,500), interpolation = cv2.INTER_AREA)
              
        return array
            
    
      def build_array(frame, array):
        
        X,Y,W,H = cv2.boundingRect(array)  
        
        built_array = array[Y:Y+H, X:X+W]
        
        built_array = cv2.cvtColor(built_array, cv2.COLOR_GRAY2BGR)
    
        w = h = int((500/Processor.N))
        
        blur = cv2.GaussianBlur(array, (5,5), 0)
         
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 5, 2)
                    
        array_results = np.zeros((Processor.N,Processor.M),np.uint8)  
     
        for j in range(Processor.M):
            for i in range(Processor.N): 
                
                cell = thresh[j*h:j*h+h, i*w:i*w+w]
                
                cv2.rectangle(built_array, (i*w, j*h), (i*w + w, j*h + h), (255,165,0), 2)
                                              
                if np.sum(cell) > 100000:
                    
                    array_results[j,i] = 1
                    cv2.rectangle(built_array, (i*w, j*h), (i*w + w, j*h + h), (0,165,255), 3)
                     
        return thresh, built_array, array_results
                        
    
      def process_frame(frame, REQUEST, EMAIL):
     
        ERROR = 0
        
        try: 
                        
            array = Processor.search_array(frame)
            
            built_array = array
            
            if isinstance(array, np.ndarray):
                            
                thresh, built_array, array = Processor.build_array(frame, array)
                
        except Exception as e:
            print("Error: could not process frame")
            print(e)
            ERROR = 1
                          
            
        try: 
            
            x_g, y_g = Processor.cam_center[0], Processor.cam_center[1]
            
            ROI_fract = 0.4
            
            if Processor.cam_w < Processor.cam_h:
                w_g, h_g = int(Processor.cam_w*ROI_fract), int(Processor.cam_w*ROI_fract)
            else:
                w_g, h_g = int(Processor.cam_h*ROI_fract), int(Processor.cam_h*ROI_fract)
                
                
            x = x_g - w_g
            y = y_g - h_g
            w = 2*w_g
            h = 30
             
            overlay = frame.copy()
            output = frame.copy()
                
            cv2.rectangle(output, (x_g - w_g, y_g - h_g), (x_g + w_g, y_g + h_g), (255,165,0), 3)
            cv2.circle(output, Processor.cam_center, 3, (255,165,0), 2)
            
            a = 0.5
        
            cv2.rectangle(overlay, (x, y-h), (x + w, y), (255,165,0), -1)
            cv2.addWeighted(overlay, a, output, 1-a, 0, output)
                
            cv2.putText(output, " This is the top of the array", (x+15,y-h+int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,165,255), 1)
            
        
        except Exception as e:
            print("Error: could not render capture guide")
            print(e)
            ERROR = 2


        if REQUEST:
            
            try:
                Communication.send_data(array, EMAIL)
            except Exception as e:
                print("Error: could not send data")
                print(e)
                ERROR = 3
                
        return output, built_array, ERROR
            
        
      def stop():
        
        Processor.cam.release()
        cv2.destroyAllWindows()




Window.clearcolor = (1, 1, 1, 1)
screen_size = Window.size


        
"""
This is the Scanner class. It acts as an interface
between the computer vision system and the app structure.
It contains:

- A setup function to prepare the scan view rendering and
  establish a link with the app structure.
- A scan function to manage inputs and outputs 
  to the computer vision system and render the scan
  views shown in the interface.
- A control function that changes that state of 
  the Scanner depending on its configuration 
  and user inputs.
- A request managing method.

Furthermore, the Scanner can create dialogs to notify erros during
processing, rendering and transmission.
 
"""


class Scanner():
    
     def setup(app):

        Scanner.app = app
        
        Scanner.EMAIL = ''
        Scanner.scanner_on = False
        Scanner.scanner_size = [800,800]
        Scanner.scan_requested = False
        Scanner.fps = 30
        Scanner.scan_view = Image()
        Scanner.array_view = Image()
        Scanner.scan_frame = np.zeros([Scanner.scanner_size[1],Scanner.scanner_size[0],3],dtype=np.uint8)
        Scanner.scan_array = np.zeros([500,500,3],dtype=np.uint8)
        
        Scanner.scan_frame.fill(250)
        buffer = cv2.flip(Scanner.scan_frame,0).tostring()
        texture = Texture.create(size = (Scanner.scan_frame.shape[1], Scanner.scan_frame.shape[0]), colorfmt = 'bgr')
        texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
        Scanner.scan_view.texture = texture
        Scanner.array_view.texture = texture
    
     
     def scan(*args):
    
        if Scanner.scanner_on:    
            
            if Processor.cam.isOpened():
        
                _, Scanner.scan_frame = Processor.cam.read()
             
                Scanner.scan_frame, Scanner.scan_array, ERROR = Processor.process_frame(Scanner.scan_frame, 
                                                                    Scanner.scan_requested, 
                                                                    Scanner.EMAIL)
               
                buffer = cv2.flip(Scanner.scan_frame,0).tobytes()
                texture = Texture.create(size = (Scanner.scan_frame.shape[1],Scanner.scan_frame.shape[0]), colorfmt = 'bgr')
                texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
                Scanner.scan_view.texture = texture
                
                if type(Scanner.scan_array) == int:
                    
                    Scanner.scan_array = np.zeros([500,500,3],dtype=np.uint8)
                    Scanner.scan_array.fill(250)
               
                buffer = cv2.flip(Scanner.scan_array,0).tobytes()
                texture = Texture.create(size = (Scanner.scan_array.shape[1],Scanner.scan_array.shape[0]), colorfmt = 'bgr')
                texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
                Scanner.array_view.texture = texture
            
            
                if Scanner.scan_requested:
                    if ERROR == 1:
                        Scanner.app.show_dialog("Sorry, there was a problem processing the frame.", "Processing Error")   
                    elif ERROR == 2: 
                        Scanner.app.show_dialog("Sorry, there was a problem rendering the capture guide.", "Render Error")       
                    elif ERROR == 3: 
                        Scanner.app.show_dialog("Sorry, the request was not completed.", "Connection Error")  
                    else:
                        Scanner.app.show_dialog("Omega is processing the data now. Check your email for results.", "Request Completed")   
                    Scanner.scan_requested = False
               
            else:
                print("Camera not ready yet")
                
            if Processor.cam.isOpened() == False:    
                Processor.cam.open(0)
                    
                         
        else:
        
            Scanner.scan_requested = False
            
     def control(*args):
    
        if Scanner.scanner_on:
        
            Scanner.scanner_on = False   
            Processor.stop()
            Scanner.scan_frame = np.zeros([Scanner.scanner_size[1],Scanner.scanner_size[0],3],dtype=np.uint8)
            Scanner.scan_frame.fill(250)
            buffer = cv2.flip(Scanner.scan_frame,0).tostring()
            texture = Texture.create(size = (Scanner.scan_frame.shape[1], Scanner.scan_frame.shape[0]), colorfmt = 'bgr')
            texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
            Scanner.scan_view.texture = texture
            Scanner.array_view.texture = texture
            
        else:
            
            Scanner.scanner_on = True
            Processor.start()
            
     def request(*args):
    
        Scanner.scan_requested = True


              
"""
This is a method to build the initial, system configuration screen. 
It allows the user to introduce both the contact address and 
the desired array size (square).
There are also two buttons, one to shift to capture mode and one to stop the 
appliaction execution.
Furthermore, the system can create dialogs to notify an invalid email
or array size. 
"""
class ConfigScreen(Screen, MDApp):
    
    def __init__(self, **kwargs):
    
        
        super(ConfigScreen, self).__init__(**kwargs)
    
        self.search_button = MDRectangleFlatButton(text="Search", pos_hint = {"center_x": 0.2, "center_y": 0.2})
        self.close_button = MDRectangleFlatButton(text="Close", pos_hint = {"center_x": 0.8, "center_y": 0.2})
    
        self.search_button.bind(on_press=self.to_capture)
        self.close_button.bind(on_press=self.stop_app)
        
        self.contact_input = MDTextField(hint_text='Contact Address', 
                                         mode = 'rectangle',  
                                         size_hint=(0.5, None), 
                                         pos_hint = {"center_x": 0.5, "center_y": 0.2},
                                         multiline=False)
        
        self.size_input = MDTextField(hint_text='Array Size', 
                                      mode = 'rectangle', 
                                      input_filter = 'int', 
                                      size_hint=(0.5, None),  
                                      pos_hint = {"center_x": 0.5, "center_y": 0.2},
                                      multiline=False)
            
        main_layout = MDBoxLayout(orientation = 'vertical')

        
        buttons = RelativeLayout()
     
        buttons.add_widget(self.search_button)  
        buttons.add_widget(self.close_button)  
        
        main_layout.add_widget(MDLabel(  text="IRIS App", 
                    text_color = (0, 0, 1, 1),
                    halign="center",
                    font_style='H4'))
        
        main_layout.add_widget(self.contact_input)
        main_layout.add_widget(self.size_input)

          
        main_layout.add_widget(buttons)
        
        self.add_widget(main_layout)
        
    def to_capture(self, *args):
        
       EMAIL = self.contact_input.text
   
       if(re.search(email_expression,EMAIL)):  
            
           print(self.size_input.text.isnumeric())
           print(self.size_input.text)
           if self.size_input.text.isnumeric():
                
                Scanner.EMAIL = EMAIL
                Processor.N = int(self.size_input.text)
                Processor.M = int(self.size_input.text)
                self.manager.current = 'Capture'
                Scanner.control()
                
             
                
           else:
                print("Array error")
                IRIS.show_dialog(self,"Sorry, the array size must be specified.", "Invalid Array Size")   
              
       else:
            
            IRIS.show_dialog(self,"Sorry, your email address is not correct.", "Invalid Email")   
 
             
    def stop_app(self, *args):
        
        self.get_running_app().stop()
        Window.close()
        
   
"""
This is a method to build the second, capture-oriented screen. 
It renders the general frame captured by the camera, and if 
an array is detected, a zoom, preprocessed and extracted render
of the target per se. Furthermore, it also includes three buttons: 
one to cancel the capture and return to the initial screen, 
one to capture the array, and one to stop the application execution.
"""

class CaptureScreen(Screen, MDApp):
    
     def __init__(self, **kwargs):
         
        super(CaptureScreen, self).__init__(**kwargs) 
        
        self.dialog = None
            
            
        main_layout = MDBoxLayout(orientation = 'vertical')
        
        main_layout.add_widget(MDLabel(  text="System ready. Please, follow the capture guide.", 
                   text_color = (0, 0, 1, 1),
                   halign="center",
                   size_hint = (1, None),
                   font_style='H5'))
        
        labels = RelativeLayout(size_hint = (1, None))
        
        labels.add_widget(MDLabel(  text="General Frame", 
                   pos_hint = {"center_x": 0.25, "center_y": 0.2},
                   halign="center",
                   font_style='H6'))
        
        labels.add_widget(MDLabel(  text="Extracted Array", 
                   pos_hint = {"center_x": 0.75, "center_y": 0.2},
                   halign="center",
                   font_style='H6'))
        
        main_layout.add_widget(labels)
        
        self.search_button = MDRectangleFlatButton(text="Cancel", pos_hint = {"center_x": 0.2, "center_y": 0.2})
        self.scan_button = MDRectangleFlatButton(text="Capture", pos_hint = {"center_x": 0.5, "center_y": 0.2})
        self.close_button = MDRectangleFlatButton(text="Close", pos_hint = {"center_x": 0.8, "center_y": 0.2})
    
        self.search_button.bind(on_press=self.to_config)
        self.scan_button.bind(on_press=Scanner.request)  
        self.close_button.bind(on_press=self.stop_app)
        
        buttons = RelativeLayout(size_hint=(1, None))
        
        displays = MDBoxLayout(orientation = 'horizontal')
        
        displays.add_widget(Scanner.scan_view)
        displays.add_widget(Scanner.array_view)
     
        buttons.add_widget(self.search_button)  
        buttons.add_widget(self.scan_button)  
        buttons.add_widget(self.close_button)  
        
        
        main_layout.add_widget(displays)
        
        
        main_layout.add_widget(buttons)
        
 
        self.add_widget(main_layout)
        
     def to_config(self, *args):
         
        Scanner.control()
        self.manager.current = 'Configuration'
        
             
     def stop_app(self, *args):
        
        if Scanner.scanner_on:
            Processor.stop()
        self.get_running_app().stop()
        Window.close()
   
"""
This is the screen-shifting mechanism.
"""

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)


"""
This is the application's main class.
"""

class IRIS(MDApp):

    """
    This method creates the interface for each screen,
    combines them, and starts the internal cyclic processes.
    """
    def build(self):   
        
                
        self.dialog = None
        self.analysis_request = False 
        self.frame = 0
        
        self.theme_cls.theme_style = "Light"
        
        Scanner.setup(self)

        app_structure = ScreenManagement(transition=SlideTransition())
        
        app_structure.add_widget(ConfigScreen(name='Configuration'))
        app_structure.add_widget(CaptureScreen(name='Capture' ))
        
        Clock.schedule_interval(Scanner.scan, 1.0/Scanner.fps)
        
        app_structure.current = 'Configuration'

        return app_structure
      
    # Auxiliar method to show dialogs with notifications over the interface.
    def show_dialog(self, message, header):
        
       
        button = MDFlatButton(
                    text="OK", text_color= self.theme_cls.primary_color
                )
            
        IRIS.dialog = MDDialog(
            title=header,
            text=message,
            buttons=[
                button,
            ],
        )
            
        button.bind(on_press=IRIS.dialog.dismiss)
            
        IRIS.dialog.open()
        

 
      
# IRIS is self-contained.
if __name__ == "__main__":
    
    IRIS().run()
