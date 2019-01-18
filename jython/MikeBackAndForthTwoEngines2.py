# BackAndForthTwoEngines.py adapted by Mike Dean January 2019
# This is an example script for a JMRI "Automat" in Python
#
# It listens to two sensors, running two locomotives back and 
# forth between them by changing its direction when a sensor
# detects the engine. 
# Run script 1, and let it run.  Place second loco and run script 2.
# Both scripts will remain active.
#

import jarray
import jmri

class BackAndForth2(jmri.jmrit.automat.AbstractAutomaton) :
	def init(self):
		# get the sensors
		self.fwdSensor = sensors.provideSensor("Block 6")
		self.revSensor = sensors.provideSensor("Block 1")
		self.throttle = self.getThrottle(5542, True)
		self.throttle.setIsForward(True)
		self.throttle.setSpeedSetting(0.15)
		return

	def handle(self):

		# set loco to forward
		self.throttle.setIsForward(True)

		
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
b = BackAndForth2()

# and start it running
b.start()

