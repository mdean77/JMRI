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
        
	def handle(self):

		self.readDecoder(self)	
		print ("The Locomotive Address is: ", self.address)
		print ("The Manufacturer is: ", self.DecoderType)
		print ("The Manufacturer ID is: ", self.mfrID)
		print ("The Manufacturer Version is: ", self.mfrVersion)
		print ("The Current Private ID is ", self.val105, ", ", self.val106)


		return False
		
Mike1().start()

