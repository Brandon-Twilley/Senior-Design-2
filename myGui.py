from Tkinter import *
import PIL.Image
import PIL.ImageTk
import socket
import json
import os, os.path
#from threading import Thread



class GUI(Frame):
    
    def initGui(self):
        global label
        global newNum
        global oldNum
        newNum = 0
        oldNum = 0
        image1 = PIL.ImageTk.PhotoImage(PIL.Image.open("/home/pi/Desktop/stops/0/0.png"))
        
        label = Label(self.root, image=image1)
        label.place(x=0, y=0, relwidth=1, relheight=1)

            #creates buttons
        self.back = Button(self.root, text="<",width=1, command=lambda: self.goBack())
        self.skip = Button(self.root, text="skip", command=lambda: self.goSkip()) 
        self.forward = Button(self.root, text=">",width=1, command=lambda: self.goForward())
        self.quit = Button(self.root, fg="red", text="Q", width=1, command=lambda: self.goDie())

        self.back.place(x=-5, y=100)
        self.skip.place(x=130, y=210)
        self.forward.place(x=290, y=100)
        self.quit.place(x=295, y=215)
            
        self.manageGui(0)
        self.changeLoc()
    
    def changeLoc(self):
        global newNum
        global oldNum
        if newNum != oldNum:
            self.manageGui(newNum)
            oldNum = newNum
        root.after(500, self.changeLoc)

    def manageGui(self, Location):
        global image1
        global imageNum
        global label
        global imageName
        
        global imageList
        global stopNum
        global myLoc
        
        myLoc = Location
        
        imageList = []
        imageNum = 0
        
        stopNum = str(Location)
        #print ""
        #print "Location is: "
        #print Location
        #print ""
        global address
        address = ("/home/pi/Desktop/stops/" + str(Location))
        global fileCount
        
        #print("the number of files is:")
        fileCount = len([name for name in os.listdir(address) if os.path.isfile(os.path.join(address, name))])
        #print fileCount 
        #print

        if (int(Location) > 0):
            for x in range(0, int(fileCount)):
                imageName = str(x)
                image1 = PIL.ImageTk.PhotoImage(PIL.Image.open(address + "/" + imageName + ".jpg"))
                imageList.append(image1)

            image1 = imageList.pop(0)
            imageList.insert(0, image1)
            label.configure(image = image1)

            self.back.place(x=-5, y=100)
            self.skip.place(x=130, y=210)
            self.forward.place(x=290, y=100)

        else:
            image1 = PIL.ImageTk.PhotoImage(PIL.Image.open("/home/pi/Desktop/stops/0/0.png"))
            label.configure(image = image1)

            self.forward.place_forget()
            self.back.place_forget()
            self.skip.place_forget()  

    def goDie(self):
        command = "/usr/bin/sudo /sbin/shutdown -P now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output
        
    def goBack(self):
        global imageNum
        global label
        global imageList
        global fileCount

        #print "entering B ImageNum:"
        #print imageNum
        if imageNum == 0 :
            imageNum = fileCount - 1

        else:
            imageNum -= 1
            
        newImage = imageList.pop(imageNum)
        imageList.insert(imageNum, newImage)
        label.configure(image = newImage)
        #print "leaving B ImageNum:"
        #print imageNum
        #print ""
        
    def goSkip(self):
        global newNum
        global imageNum
        global label
        global imageList
        global myLoc
        
        #print "skipped"
        target = open('/home/pi/Desktop/test.txt','w')
        target.truncate()
        target.write('0')
        target.write('\n')
        target.write('0')
        target.write('\n')
        target.close()
        
    def goForward(self):
        global imageNum
        global label
        global imageList
        #print "entering F ImageNum:"
        #print imageNum

        if imageNum == fileCount - 1 :
            imageNum = 0

        else:
            imageNum += 1
            
        newImage = imageList.pop(imageNum)
        imageList.insert(imageNum, newImage)
        label.configure(image = newImage)
        #print "leaving F ImageNum:"
        #print imageNum
        #print ""
        

    def startGui(self):
        self.root.mainloop()

    def __init__(self, parent):
        self.root = parent
        self.initGui()

host = '127.0.0.1'
PORT = 5006
BUFFER_SIZE = 1024

global s   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, PORT))
s.listen(1)

conn, addr = s.accept()

socketTime = 500
    
def get_text():
    # RECEIVE MESSAGE FROM SOCKET
    data = conn.recv(BUFFER_SIZE)
    #print("RECEIVED: "+data.decode("utf-8"))
    #s.close()
    return data.decode("utf-8")

def check():
    global newNum
    newNum = get_text()
    #print "newNum: "
    #print newNum
    root.after(socketTime, check)

root = Tk()

def main():
    
    root.geometry("320x240")
    
    root.attributes('-fullscreen', True)
        
    myGui = GUI(root)
    root.after(500, check)
    myGui.startGui()
    
if __name__ == '__main__':
    main()
