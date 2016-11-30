import os, sys
import numpy as np
import cv2
import time
import serial
import multiprocessing
import socket
import json
from joblib import Parallel, delayed

sys.path.append('/usr/include/opencv2')
start_time = time.time()

# function to implement SURF like algorithm to dectect matches in a scene to a template 
def image_pro(img, img2):

  # Initiate ORB detector
  orb = cv2.ORB()
   
  # compute the descriptors with ORB
  kp, des = orb.detectAndCompute(img, None)
  kp2, des2 = orb.detectAndCompute(img2,None)

  # create BFMatcher object
  bf = cv2.BFMatcher()
  
  # Match descriptors.
  matches = bf.knnMatch(des,des2, k = 2)

  # creates an array of matches 	
  good = []
  for m,n in matches:
      if m.distance < 0.75*n.distance:
          good.append(m)

  # gets length of the array created previously and returns the number of matches found for each picture
  match = len(good)
  return match

# uses number of matches returned from first function to approximate distance and location. 
def distance(match):
  if max(match) >= 20 and max(match) == match[0]: 
      return [1,1]
  elif max(match) >= 20 and max(match) == match[1]:  
      return [1,2]
  elif max(match) >= 20 and max(match) == match[2]: 
      return [1,3]
  elif max(match) >= 20 and max(match) == match[3]: 
      return [1,4]
  elif max(match) < 15 and max(match) >= 10 and max(match) == match[0]: 
      return [3,1]
  elif max(match) < 15 and max(match) >= 10 and max(match) == match[1]:  
      return [3,2]
  elif max(match) < 15 and max(match) >= 10 and max(match) == match[2]: 
      return [3,3]
  elif max(match) < 15 and max(match) >= 10 and max(match) == match[3]: 
      return [3,4]
  elif max(match) < 20 and max(match) >= 15 and max(match) == match[0]: 
      return [2,1]
  elif max(match) < 20 and max(match) >= 15 and max(match) == match[1]:  
      return [2,2]
  elif max(match) < 20 and max(match) >= 15 and max(match) == match[2]: 
      return [2,3]
  elif max(match) < 20 and max(match) >= 15 and max(match) == match[3]: 
      return [2,4]
  else: 
      return [0,0]

def img_Main():
        
	try:

		data = []
                #reads in file and appends it to the array
		with open('/home/pi/Desktop/test.txt') as f: 
				for line in f: 
					data.append([int(val) for val in line.split()])	#returns two independant arrays (list)	

		data = data[0] + data[1] #concantinates list to singular one

		#img = the images to look for / img2 = scene to be searched 
		img = [cv2.imread('/home/pi/Desktop/1.png',1), cv2.imread('/home/pi/Desktop/2.png',1), cv2.imread('/home/pi/Desktop/3.png',1), cv2.imread('/home/pi/Desktop/4.png',1)]
		img2 = cv2.imread('/home/pi/Desktop/scene.jpg')

		# gets cpu core count for use in a later function 
		cores = multiprocessing.cpu_count()

		# input range 
		inputs = range(len(img))

		#runs loop in parallel on multiple cores to reduce computation time on raspberry pi
		match = Parallel(n_jobs = cores, backend = 'threading' )(delayed(image_pro)(img[i], img2) for i in inputs)

		# outputs "distance and approximate "location"
		output = distance(match) 

		data.append(output[0])
		data.append(output[1])

                #os.remove('test.txt')
        
		return data
		
	except:
               pass
      
	      
class MCU:
	timeInterval = 0.5 #seconds
	
	TCP_IP = '127.0.0.1'
	IMAGE_PORT = 5006
	BUFFER_SIZE = 1024

        global a
	a = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
		a.connect((TCP_IP, IMAGE_PORT))
	except:
		time.sleep(0.2)
		a.connect((TCP_IP, IMAGE_PORT))
    
	def send_text(self):
		global theLoc
		global a
		#print("Sending: "+str(theLoc))
		a.send(str(theLoc))
    
	def check_Location(self, ARUCO_ID, ORB_Id):
		global theLoc
		if(ARUCO_ID == ORB_Id):
			theLoc = ARUCO_ID
			#print ("theLoc = "+ str(theLoc))
		else:
			return False

	def Compare_Distance(self,ARUCO_Dis, ORB_Dis):
		distance = (ARUCO_Dis + ORB_Dis) / 2
		#print ("Distance = " + str(distance))
		return distance
		
global theLoc
theLoc = 0
myMain = MCU()
#ser = serial.Serial('/dev/ttyACM0',9600)

while (1) :
        
        data = img_Main()
        #print(img_Main())

        #if statement to control skip button to return to default picture
        #try:
	if( data[0] != 0 and data[1] != 0):
		myMain.send_text()
          #ser.write(str(theLoc))
          
		myMain.check_Location(data[0], data[3])
		myMain.Compare_Distance(data[1], data[2])
          #print("%s" % str((time,time.time() - start_time)))
          #myMain.user_response()
		time.sleep(.5)
	else:
		data[2] = 0
		data[3] = 0 
		myMain.send_text()
		myMain.check_Location(data[0], data[3])
		myMain.Compare_Distance(data[1], data[2])
		time.sleep(.5)
          #except 
