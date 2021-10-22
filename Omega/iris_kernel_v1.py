import cv2
import numpy as np
import socket
import threading
import pickle



cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cam_w = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
cam_h = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
cam_res = cam_w*cam_h

cam_center = (int(cam_w/2), int(cam_h/2))

search = False
analyze = False
scan = False
request = False
stop = False

previous = [0,0,0,0]

N = 13
M = 13

email = 'joelroihe@gmail.com'
    
request = False

def send_array(omega, array):
    
    HEADERSIZE = 10
    
    package = pickle.dumps(array)
    package = bytes(f"{len(package):<{HEADERSIZE}}", 'utf-8')+package
    
    omega.send(package)
    
def ask_for_request(omega):
    
    omega.send('REQUEST'.encode('ascii'))
    
    
def wait_for_instructions(omega, array):

    package = omega.recv(1024).decode('ascii') 
    
    if package == "SEND_CONTACT":
        
        print("Contact petition received!")
        
        send_email(omega, email)
        
    if package == "SEND_ARRAY":
        
        print("Array petition received!")
        
        send_array(omega, email)
        
        request = False
        

def send_email(omega, email):
    
     email_package = 'EMAIL:'+email
     omega.send(email_package.encode('ascii'))

        
def process(array):
    
    print(array)
    
    omega = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    omega_IP = '192.168.1.141'
    omega.connect((omega_IP, 55555))
    
    ask_for_request(omega)
    
    while request:
        
        wait_for_instructions(omega, array)
        
    
        
       
        
        
        


def search_array(frame, previous):
    
    array = -1
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
    blur = cv2.GaussianBlur(gray, (5,5), 0)
      
    thresh1 = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
      
    contours, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                
    best_cnt = -1
    max_area = 0
    
    for i in contours:
                
        area = cv2.contourArea(i)
        
        if area > cam_res*0.1:
            
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
          
    return array, previous
        

def build_array(frame, array, N, M):
    
    X,Y,W,H = cv2.boundingRect(array)  
    
    built_array = array[Y:Y+H, X:X+W]
    
    built_array = cv2.cvtColor(built_array, cv2.COLOR_GRAY2BGR)

    w = h = 39
    
    blur = cv2.GaussianBlur(array, (5,5), 0)
     
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 5, 2)
                
    array_results = np.zeros((N,M),np.uint8)  
 
    for j in range(M):
        for i in range(N): 
            
            cell = thresh[j*h:j*h+h, i*w:i*w+w]
            
            cv2.rectangle(built_array, (i*w, j*h), (i*w + w, j*h + h), (255,165,0), 2)
                                          
            if np.sum(cell) > 100000:
                
                array_results[j,i] = 1
                cv2.rectangle(built_array, (i*w, j*h), (i*w + w, j*h + h), (0,165,255), 3)
                 
    return thresh, built_array, array_results
                    




def control(scan, request, stop):
    
            
    k = cv2.waitKey(1) & 0xFF
        
    if k & 0xFF == ord('s'):
        if scan:
            scan = False
        else:
            scan = True
            
    if k & 0xFF == ord('c'):
        request = True
        
    if k & 0xFF == ord('q'):
        stop = True    
        
    return scan, request, stop

   

while True:

    _, frame = cam.read()
        
    array, previous = search_array(frame, previous)
    
    built_array = array
    
    if isinstance(array, np.ndarray):
                    
        thresh, built_array, array = build_array(frame, array, N, M)
        
        cv2.imshow('Array', built_array)
                      
    x_g, y_g = cam_center[0], cam_center[1]
    
    ROI_fract = 0.4
    
    if cam_w < cam_h:
        w_g, h_g = int(cam_w*ROI_fract), int(cam_w*ROI_fract)
    else:
        w_g, h_g = int(cam_h*ROI_fract), int(cam_h*ROI_fract)
        
        
    x = x_g - w_g
    y = y_g - h_g
    w = 2*w_g
    h = 30
     
    overlay = frame.copy()
    output = frame.copy()
        
    cv2.rectangle(output, (x_g - w_g, y_g - h_g), (x_g + w_g, y_g + h_g), (255,165,0), 3)
    cv2.circle(output, cam_center, 3, (255,165,0), 2)
    
    a = 0.5

    cv2.rectangle(overlay, (x, y-h), (x + w, y), (255,165,0), -1)
    cv2.addWeighted(overlay, a, output, 1-a, 0, output)
        
    cv2.putText(output, " This is the top of the array", (x+15,y-h+int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,165,255), 1)
    cv2.imshow('Camera',output)
    

    scan, request, stop = control(scan, request, stop)
    
    if request:
        process(array)
        request = False
    
    if stop:
        break
    


cam.release()
cv2.destroyAllWindows()


