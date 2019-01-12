# Script MikeWarmUp.py to run on my test track.
# J. Michael Dean, MD
# January 11, 2019
#
# Hardware requirements are relatively minimal:
#	NCE Powercab system
#	NCE AIU to connect occupancy detectors to the NCE bus
#	NCE USB to connect the NCE bus to a computer
#	Computer with JMRI.  I am using Raspberry Pi 3 B+


import java
import jmri
import sys

class DCCDecoderCalibration(jmri.jmrit.automat.AbstractAutomaton):
	def init(self):
		self.long = False
		self.addr = 0
		self.warmupLaps = 3		#Usually should be 5 but 3 for train club demonstration
		self.throttle = None
		self.homesensor = sensors.provideSensor("Block 12")
		return

	def readDecoderAddress(self):
		print ("Reading Locomotive Address...")
		self.val29 = self.readServiceModeCV("29")
		print ("	CV 29 = %s." % self.val29)
		self.val1 = self.readServiceModeCV("1")
		print ("	CV 1 = %s." % self.val1)
		self.val17 = self.readServiceModeCV("17")
		print ("	CV 17 = %s." % self.val17)
		self.val18 = self.readServiceModeCV("18")
		print ("	CV 18 = %s." % self.val18)
		print("")
		
		# Determine if this locomotive uses a long address
		if ((self.val29 & 32) == 32) :
			self.long = True
			self.address = (self.val17 - 192) * 256 + self.val18
		else :
			self.long = False
			self.address = self.val1
			
		print ("The Locomotive Address is: %s." % self.address)
		print("")
		return
	
 	def waitNextActiveSensor(self, sensorlist) :
		inactivesensors = []		
		if (len(sensorlist) == 1) :
			if (sensorlist[0].getKnownState() == sensorlist[0].ACTIVE) :
				self.waitSensorInactive(sensorlist)
			inactivesensors.append(sensorlist[0])
		else :
			for s in sensorlist:
				if s.getKnownState() == s.INACTIVE :
					inactivesensors.append(s)
		self.waitSensorActive(inactivesensors)
		return
	
	def fullThrottleLaps(self):
		sys.stdout.write("Starting the locomotive warmup laps: ")
		self.throttle.setSpeedSetting(1.0)
		self.waitNextActiveSensor([self.homesensor])
		for x in range (0, self.warmupLaps) :
			sys.stdout.write("%s " % x)
			self.waitNextActiveSensor([self.homesensor])
		sys.stdout.write("\n")
		
	def warmUpForward(self):
		print ("Engine warmup in forward direction.")
		self.throttle.setIsForward(True)
		self.fullThrottleLaps()
		
	def warmUpReverse(self):
		print ("Engine warmup in reverse direction.")
		self.throttle.setIsForward(False)
		self.fullThrottleLaps()		
					
	def handle(self):
		self.readDecoderAddress()
		self.throttle = self.getThrottle(self.address, self.long)
		self.warmUpForward()
		self.throttle.setSpeedSetting(0.0)
		self.warmUpReverse()
		self.throttle.setSpeedSetting(0.0)
		return False

####################################################################################
#
# Instantiate the automation class and start it up
#
####################################################################################
a = DCCDecoderCalibration()
a.start()


