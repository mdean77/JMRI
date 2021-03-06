# Script DetectDecoder.py to read the decoder
# J. Michael Dean, MD
# September 27 2018

import jmri
class Mike1(jmri.jmrit.automat.AbstractAutomaton):
	def init(self):
		print("Inside init self")
		self.DecoderMap = {141:"Tsunami", 129:"Digitrax", 153:"TCS", 11:"NCE", 113: "QSI/BLI", 99:"Lenz Gen 5", 151:"ESU", 127:"Atlas/Lenz XF"}
		self.DecoderType = "Default"
		return

    	def readDecoder(self):
		print ("Reading Locomotive...")
		self.val29 = self.readServiceModeCV("29")
		print ("CV 29 = ", self.val29)
		self.val1 = self.readServiceModeCV("1")
		print ("CV 1 = ", self.val1)
		self.val17 = self.readServiceModeCV("17")
		print ("CV 17 = ", self.val17)
		self.val18 = self.readServiceModeCV("18")
		print ("CV 18 = ", self.val18)
		self.val7 = self.readServiceModeCV("7")
		print ("CV 7 = ", self.val7)
		self.val8 = self.readServiceModeCV("8")
		print ("CV 8 = ", self.val8)
		self.val105 = self.readServiceModeCV("105")
		print ("CV 105 = ", self.val105)
		self.val106 = self.readServiceModeCV("106")
		print ("CV 106 = ", self.val106)

		# Determine if this locomotive uses a long address
		if ((self.val29 & 32) == 32) :
			self.long = True
			self.address = (self.val17 - 192) * 256 + self.val18
		else :
			self.long = False
			self.address = self.val1

		# get the manufacturer so we can adjust for decoder-specific settings
		
		self.mfrID = self.val8
		self.mfrVersion = self.val7
		
		if (self.DecoderMap.has_key(self.mfrID)):
			self.DecoderType = self.DecoderMap[self.mfrID]
		else:
			self.DecoderType = "Unknown"
            
        	return

	def attachProgrammer(self):
		self.programmer = addressedProgrammers.getAddressedProgrammer(self.long, self.address)
		return

	def myCVListener(self, value, status) :
		self.writeLock = False
		return
	
 	def testbedWriteCV(self, cv, value) :
		self.writeLock = True
		self.programmer.writeCV(cv, value, self.myCVListener)
		while (self.writeLock) :	# will be set to False by myCVListener()
			pass
		return
 
	def attachThrottle(self):
		self.throttle = self.getThrottle(self.address, self.long)
		if (self.throttle == None) :
			print ("ERROR: Couldn't assign throttle!")
		else :
			print ("Trottle assigned to locomotive: ", self.address)
		return

	def warmUpEngine(self):
		self.attachThrottle()
		self.throttle.setIsForward(True)
		self.throttle.setSpeedSetting(1.0)
		self.waitMsec(10000)
		self.throttle.setSpeedSetting(0)
		return
	
	      
	def handle(self):

		self.readDecoder()	
		print ("The Locomotive Address is: ", self.address)
		print ("The Manufacturer is: ", self.DecoderType)
		print ("The Manufacturer ID is: ", self.mfrID)
		print ("The Manufacturer Version is: ", self.mfrVersion)
		print ("The Current Private ID is ", self.val105, ", ", self.val106)
		#self.warmUpEngine()
		#self.readDecoder()
		self.attachThrottle()
		self.attachProgrammer()
		self.throttle.setIsForward(True)
		self.throttle.setSpeedSetting(1.0)
		self.waitMsec(5000)
		self.testbedWriteCV(94, 250)

		self.waitMsec(5000)
		self.testbedWriteCV(94, 100)

		self.waitMsec(5000)
		self.testbedWriteCV(94, 50)

		self.waitMsec(5000)
		self.throttle.setSpeedSetting(0)
		return False
		
Mike1().start()

