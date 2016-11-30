'''
Distance calculator for image processing

Written by: Joseph Rodenbaugh

Senior Design 2
'''


class Distance:
#Note replace every declared value with your specific camera values
	def CalcDistance(self,pixHeight):
		global focalLength
		global realHeight  
		global distance
		global objHeight
		global imageHeight_px
		
		focalLength = 30 #mm; unknown at time
		realHeight = 6 #feet or meter; whatever unit you want final answer as, inches in our case
		
		imageHeight_px = pixHeight #example 1050 pixels
		
		self.findSize()
		
		distance = float(realHeight)*float(focalLength)/float(objHeight) #same unit as realHeight (inches)
		
		print ("distance is:" + str(round(distance,2)))
		return round(distance,2)
		
	def findSize(self):
		global imageHeight_px
		global sensHeight_MM
		global sensHeight_PX
		global objHeight
		
		sensHeight_MM =4.59 #dependant on comera model, 4.59mm is approx ours
		sensHeight_PX = 3280 #dependant on comera model; 3280 is our pixel height
		
		objHeight = float(sensHeight_MM)*float(imageHeight_px)/float(sensHeight_PX) 
		
if __name__ == '__main__':
    myCalc = Distance()
    myCalc.CalcDistance(1050)

    with open('dist.txt') as f: \
         f.write(myCalc.CalcDistance(1050))
