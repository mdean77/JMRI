# BackAndForthTwoEngines.py adapted by Mike Dean January 2019
# This is an example script for a JMRI "Automat" in Python
#
# It listens to four sensors, running two locomotives back and 
# forth between them by changing its direction when a sensor
# detects the engine. 
#

import jarray
import jmri

class BackAndForth(jmri.jmrit.automat.AbstractAutomaton) :
	def init(self):
		# get the sensors
		self.fwdSensor1 = sensors.provideSensor("Block 1")
		self.revSensor1 = sensors.provideSensor("Block 6")
		self.fwdSensor2 = sensors.provideSensor("Block 7")
		self.revSensor2 = sensors.provideSensor("Block 12")
		
		self.throttle1 = self.getThrottle(5327, True)
		return

	def handle(self):

		# set loco to forward
		self.throttle1.setIsForward(True)
		self.throttle1.setSpeedSetting(0.4)
		
		# wait for sensor in forward direction to trigger
		self.waitSensorActive(self.fwdSensor1)
		
		# set loco to reverse
		self.throttle1.setIsForward(False)
		
		# wait for sensor inactive, meaning loco has reversed out
		# (prevent infinite loop if both sensors go active in the overlap)
		self.waitSensorInactive(self.fwdSensor1)

		# wait for sensor in reverse direction to trigger
		self.waitSensorActive(self.revSensor1)
		
		# and continue around again
		return True	# to continue
	
# end of class definition

# create one of these
a = BackAndForth()

# and start it running
a.start()

