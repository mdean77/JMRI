# BackAndForth.py adapted by Mike Dean January 2019
# This is an example script for a JMRI "Automat" in Python
#
# It listens to two sensors, running a locomotive back and 
# forth between them by changing its direction when a sensor
# detects the engine. You need to set the speed of the engine
# using a throttle.
#
# Author: Bob Jacobsen, copyright 2004, 2005
# Part of the JMRI distribution

import jarray
import jmri

class BackAndForth(jmri.jmrit.automat.AbstractAutomaton) :
	def init(self):
		# get the sensors
		self.fwdSensor = sensors.provideSensor("Block 1")
		self.revSensor = sensors.provideSensor("Block 11")
		print ("Reading Locomotive Address...")
		self.val1 = self.readServiceModeCV("1")
		print ("	CV 1 = %s." % self.val1)
		self.val17 = self.readServiceModeCV("17")
		print ("	CV 17 = %s." % self.val17)
		self.val18 = self.readServiceModeCV("18")
		print ("	CV 18 = %s." % self.val18)
		self.val29 = self.readServiceModeCV("29")
		print ("	CV 29 = %s." % self.val29)
		print("")
		
		# Determine if this locomotive uses a long address
		if ((self.val29 & 32) == 32) :
			self.long = True
			self.address = (self.val17 - 192) * 256 + self.val18
		else :
			self.long = False
			self.address = self.val1			
		print ("The Locomotive Address is: %s." % self.address)
		
		self.throttle = self.getThrottle(self.address, self.long)
		return

	def handle(self):

		# set loco to forward
		self.throttle.setIsForward(True)
		self.throttle.setSpeedSetting(0.4)
		
		# wait for sensor in forward direction to trigger
		self.waitSensorActive(self.fwdSensor)
		
		# set loco to reverse
		self.throttle.setIsForward(False)
		
		# wait for sensor inactive, meaning loco has reversed out
		# (prevent infinite loop if both sensors go active in the overlap)
		self.waitSensorInactive(self.fwdSensor)

		# wait for sensor in reverse direction to trigger
		self.waitSensorActive(self.revSensor)
		
		# and continue around again
		return True	# to continue
	
# end of class definition

# create one of these
a = BackAndForth()

# and start it running
a.start()

