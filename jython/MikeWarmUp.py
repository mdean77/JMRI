# Script MikeSpeedScript.py to run on my test track.
# J. Michael Dean, MD
# September 27 2018
#
# Hardware requirements are relatively minimal:
#	NCE Powercab system
#	NCE AIU to connect occupancy detectors to the NCE bus
#	NCE USB to connect the NCE bus to a computer
#	Computer with JMRI.  I am using Raspberry Pi 3 B+
#	Kato track - N scale 19" radius Unitrack, 24 pieces - optional susbstitute a Kato wye for one of the pieces
#		The wye allows connection to a straight track to facilitate putting locomotive on the track.
#	Kato unitrack isolator joiners (black) and drop lead sets (12 and six, the leads can be pulled apart)
#	Occupancy detectors MRCS cpOD from Chuck Catania and Seth Neumann (12)
#	All cables and wiring are on the underside, and all circuitry is on top so I could adjust the pots on the cpOD.
#
#	Note for the naive carpenter - I built a 40" X 40" table thinking that would leave 2 inches spare on the
#	diameter, but track radius is measured from middle of track, so I have barely 0.5 inch margin on the four
#	sides.  Would be much much better if I had built 44" X 44" table!
#
#	This script is completely non-original and is based on work by Phil Klein from 2010 and Erich Whitney 2017 to present.
#	My goal has been to rewrite the script from scratch so that I understand it, and it is highly simplified from their
#	previous work because of several simplifications:
#
#		This only has one track, which is N scale.  I do not need to determine which track is being used.
#		The NCE Powercab only has one output that can be changed between programmer (service) and ops mode.
#		There is no need, therefore, for a complicated method of switching outputs on the DCC command station.
#

import java
import javax.swing
import jmri
import sys

class DCCDecoderCalibration(jmri.jmrit.automat.AbstractAutomaton):
	def init(self):
		self.long = False
		self.addr = 0
		self.warmupLaps = 5
		self.programmer = None
		self.throttle = None
		self.homesensor = sensors.provideSensor("Block 12")
		return

	def readDecoder(self):
		print ("Reading Locomotive...")
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
	
	def attachThrottle(self):
		self.throttle = self.getThrottle(self.address, self.long)
		if (self.throttle == None) :
			print ("ERROR: Couldn't assign throttle!")
		else :
			print ("Throttle assigned to locomotive: %s." % self.address)
			self.throttle.setF0(True)
			self.throttle.setF8(True)
		return
	
	def stopLocomotive(self):
		print ("Stop the locomotive")
		self.throttle.setSpeedSetting(0.0)
		self.waitMsec(2000)
		return
	
	def fullThrottleLaps(self):
		sys.stdout.write("Starting the locomotive warmup laps: ")
		self.throttle.setSpeedSetting(1.0)
		self.waitMsec(1000)
		self.waitNextActiveSensor([self.homesensor])
		for x in range (0, self.warmupLaps) :
			sys.stdout.write("%s " % x)
			self.waitNextActiveSensor([self.homesensor])
		sys.stdout.write("\n")
		
	def warmUpForward(self):
		print ("Engine warmup in forward direction.")
		self.throttle.setIsForward(True)
		self.waitMsec(500)
		self.fullThrottleLaps()
		
	def warmUpReverse(self):
		print ("Engine warmup in reverse direction.")
		self.throttle.setIsForward(False)
		self.waitMsec(500)
		self.fullThrottleLaps()		
					
	def handle(self):
		self.readDecoder()
		self.attachThrottle()
		self.warmUpForward()
		self.stopLocomotive()
		self.warmUpReverse()
		return False



####################################################################################
#
# Instantiate the automation class and start it up
#
####################################################################################
a = DCCDecoderCalibration()

# This brings up the dialog box that will call self.start()
a.start()


