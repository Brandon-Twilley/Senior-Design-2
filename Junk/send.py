# !/usr/bin/env python
import socket
import json
import time
class MCU:
	timeInterval = 3 #seconds
	
	TCP_IP = '127.0.0.1'
	IMAGE_PORT = 5006
	BUFFER_SIZE = 1024
	MESG = '{"change_database":"1","object":{"template_file": "TEMPLATE_TEST.jpg","screen_file":"SCREEN_TEST.jpg"}}'
	MESG2 = '{"change_database":"0","object":[{"sign_number":"1","distance":".67"},{"sign_number":"2","distance":".67"},{"sign_number":"3","distance":".20"},{"sign_number":"4","distance":".67"}]}'

	def send_marker(MARKER):

		json.dumps()
		send_text(MARKER)

	def init_send_conn(PORT):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((TCP_IP, IMAGE_PORT))
		print("SOCKET "+str(IMAGE_PORT)+" INITIALIZED.")
		return s

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
		print("Sending: "+str(theLoc))
		a.send(str(theLoc))
    
	#def check_Location(ARUCO_ID, ORB_Id)
	#	global theLoc
	#	if(ARUCO_ID == ORB_Id)
	#		theLoc = ARUCO_ID
	#		print ("theLoc = "+ str(theLoc))
			#send_text(theLoc, IMAGE_PORT)
			#do USB communication
			#wait for return screen message
	#	else
	#		return False

	#def Compare_Distance(ARUCO_Dis, ORB_Dis)
	#	distance = (ARUCO_Dis + ORB_Dis) / 2
	#	print ("Distance = " + str(distance))
	#	return distance
		
	#def main():
	#	global theLoc
	#	theLoc = 0
	#	send_text()
	#	t = 0
		#send_text('{"window": {"title": "Sample Konfabulator Widget","name": "main_window","width": 500,"height": 500}}', TCP_PORT)
	#	while 1:
		#	
		#	themsg = t
		#	theLoc = t
	#		send_text()
		#	send_text(themsg, IMAGE_PORT)
		#	if t==4:
		#		t = 0
		#	else:
		#		t += 1
	#		time.sleep(timeInterval)
		#a.close()    

if __name__ == "__main__":
        mytest = MCU()
        global theLoc
        timeInterval = 8
        theLoc = 0
        t = 0
        while 1:
                theLoc = t
                mytest.send_text()
                if t==4:
			t = 0
		else:
			t += 1
		time.sleep(timeInterval)
                
