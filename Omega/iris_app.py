from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import time
import cv2
import numpy as np

Window.clearcolor = (1, 1, 1, 1)
screen_size = Window.size

print(screen_size)

# from android.permissions import request_permissions, Permission
# request_permissions([
#     Permission.CAMERA,
#     Permission.WRITE_EXTERNAL_STORAGE,
#     Permission.READ_EXTERNAL_STORAGE,
#     Permission.INTERNET
# ])


class Scanner():
    
     def __init__(self, app):
    
        self.app = app
        self.scanner_on = False
        self.scanner_size = [500,500]
        self.scan_requested = False
        self.fps = 30
        self.scan_view = Image()
        self.scan_frame = np.zeros([self.scanner_size[1],self.scanner_size[0],3],dtype=np.uint8)
        self.scan_frame.fill(250)
        buffer = cv2.flip(self.scan_frame,0).tostring()
        texture = Texture.create(size = (self.scan_frame.shape[1], self.scan_frame.shape[0]), colorfmt = 'bgr')
        texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
        self.scan_view.texture = texture
    
     
     def scan(self, *args):
    
        if self.scanner_on:    
            
            if self.scan_input.isOpened():
        
                _, self.scan_frame = self.scan_input.read()
            
                buffer = cv2.flip(self.scan_frame,0).tobytes()
                texture = Texture.create(size = (self.scan_frame.shape[1],self.scan_frame.shape[0]), colorfmt = 'bgr')
                texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
                self.scan_view.texture = texture
            
                if self.scan_requested:
                    
                    self.app.frame = self.scan_frame
                    self.app.analysis_request = True
                    #cv2.imwrite("/sdcard/IMG_{}.png".format(time.strftime("%Y%m%d_%H%M%S")), self.scan_frame)
                    self.scan_requested = False
            else:
                print("Camera not ready yet")
                
            if self.scan_input.isOpened() == False:    
                self.scan_input.open(0)
        else:
        
            self.scan_requested = False
            
     def control(self, *args):
    
        if self.scanner_on:
        
            self.scanner_on = False   
            self.scan_input.release()
            self.scan_frame = np.zeros([self.scanner_size[1],self.scanner_size[0],3],dtype=np.uint8)
            self.scan_frame.fill(255)
            buffer = cv2.flip(self.scan_frame,0).tostring()
            texture = Texture.create(size = (self.scan_frame.shape[1], self.scan_frame.shape[0]), colorfmt = 'bgr')
            texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
            self.scan_view.texture = texture
            
        else:
            
            self.scanner_on = True
            self.scan_input = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            
     def request(self, *args):
    
        self.scan_requested = True


class Processor():
    
     def __init__(self, app):
         
         self.app = app
     
     def analyze(self, *args):
         
         if self.app.analysis_request:
             
            squares = self.find(self.app.frame)
            self.show(squares)   
            self.app.analysis_request = False
      
     def angle_cos(p0, p1, p2):
         d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
         return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )
     
     def find(self, img):

        img = cv2.GaussianBlur(img, (5, 5), 0)
        squares = []
        for gray in cv2.split(img):
            for thrs in range(0, 255, 26):
                if thrs == 0:
                    bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                    bin = cv2.dilate(bin, None)
                else:
                    _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
                bin, contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                    if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                        cnt = cnt.reshape(-1, 2)
                        max_cos = np.max([self.angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                        #print(cnt)
                        a = (cnt[1][1] - cnt[0][1])
    
                        if max_cos < 0.1 and a < img.shape[0]*0.8:
    
                            squares.append(cnt)
        return squares
    
    
     def show(self, *args, img, squares):
        
        cv2.drawContours(img, squares, -1, (0, 255, 0), 3)
        

class Iris(MDApp):

    def build(self):   
     
        self.analysis_request = False 
        self.frame = 0
        
        self.theme_cls.theme_style = "Light"
        
        self.scanner = Scanner(self)
        self.processor = Processor(self)

        self.search_button = MDRectangleFlatButton(text="Search", pos_hint = {"center_x": 0.2, "center_y": 0.2})
        self.scan_button = MDRectangleFlatButton(text="Scan", pos_hint = {"center_x": 0.5, "center_y": 0.2})
        self.close_button = MDRectangleFlatButton(text="Close", pos_hint = {"center_x": 0.8, "center_y": 0.2})

        self.search_button.bind(on_press=self.scanner.control)
        self.scan_button.bind(on_press=self.scanner.request)  
        self.close_button.bind(on_press=self.stop_app)
            
        screen = MDBoxLayout(orientation = 'vertical')
        buttons = RelativeLayout()
   
        buttons.add_widget(self.search_button)  
        buttons.add_widget(self.scan_button)  
        buttons.add_widget(self.close_button)  
        
        screen.add_widget(self.scanner.scan_view)
        screen.add_widget(buttons)
        
        Clock.schedule_interval(self.scanner.scan, 1.0/self.scanner.fps)
        Clock.schedule_interval(self.processor.analyze, 1.0/self.scanner.fps)

        return screen
                
            
    def stop_app(self, *args):
        
        if self.scanner.scanner_on:
            self.scanner.scan_input.release()
        
        self.get_running_app().stop()
        Window.close()
 


Iris().run()