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
import datetime

class DCCDecoderCalibration(jmri.jmrit.automat.AbstractAutomaton):
	def init(self):
	    	
	    	# individual block section length (scale feet)
		self.scriptversion = 3.0
		self.block = float(132.65)  # 132.65 feet Erich's Speed Matching Track Kato Unitrack 19" Radius - 12 Sections / 24 Pieces
		self.NumSpeedMeasurements = 5
		self.long = False
		self.addr = 0
		self.warmupLaps = 5
		self.programmer = None
		self.throttle = None
		self.writeLock = False
		self.fullSpeed = 100
		self.stepValueList = [0]
		self.outputFileName = "SpeedOutput " + str(datetime.datetime.now()) + ".txt"
		
		# JMD:  I changed the sensor numbering since I will only have 12 blocks.
		self.sensor1 = sensors.provideSensor("Block 1")
		self.sensor2 = sensors.provideSensor("Block 2")
		self.sensor3 = sensors.provideSensor("Block 3")
		self.sensor4 = sensors.provideSensor("Block 4")
		self.sensor5 = sensors.provideSensor("Block 5")
		self.sensor6 = sensors.provideSensor("Block 6")
		self.sensor7 = sensors.provideSensor("Block 7")
		self.sensor8 = sensors.provideSensor("Block 8")
		self.sensor9 = sensors.provideSensor("Block 9")
		self.sensor10 = sensors.provideSensor("Block 10")
		self.sensor11 = sensors.provideSensor("Block 11")
		self.sensor12 = sensors.provideSensor("Block 12")
		self.homesensor = sensors.provideSensor("Block 12")
		
		# Different block sizes for different speeds or it would take
		# forever to do the low speed if loco had to circle whole track
		# for every measurement.
		
		self.HighSpeedNBlocks = 12
		self.MediumSpeedNBlocks = 3
		self.LowSpeedNBlocks = 1
		
		self.HighSpeedArrayN = [self.homesensor]
		
		self.MediumSpeedArrayN= (
				self.sensor1,
				self.sensor4,
				self.sensor7,
				self.sensor10)
		
		self.LowSpeedArrayN = (
				self.sensor1,
				self.sensor2,
				self.sensor3,
				self.sensor4,
				self.sensor5,
				self.sensor6,
				self.sensor7,
				self.sensor8,
				self.sensor9,
				self.sensor10,
				self.sensor11,
				self.sensor12)
		
		self.MediumSpeedThreshold = 45
		self.HighSpeedThreshold = 85
		
		self.DecoderMap = {141:"Tsunami", 129:"Digitrax", 153:"TCS", 11:"NCE", 113: "QSI/BLI", 99:"Lenz Gen 5", 151:"ESU", 127:"Atlas/Lenz XF"}
		self.DecoderType = "Default"
		
		#	These seven speed steps are measured.  All others are calculated.
		#	CV			70	74	78	82	86	90	94
		#	Speedsteps	 4	 8	12	16	20	24	28
		#	This list contains percentages of full speed, 1/7 per step
		self.stepList = [14.3, 28.5, 42.9, 57, 71.5, 85.7, 100]
		return

	def printSave(self, aString):
		print(aString)
		f = open(self.outputFileName, 'a')
		f.write(aString+"\n")
		f.close()

	def readDecoder(self):
		self.printSave ("Reading Locomotive...")
		self.val29 = self.readServiceModeCV("29")
		self.printSave ("	CV 29 = %s." % self.val29)
		self.val1 = self.readServiceModeCV("1")
		self.printSave ("	CV 1 = %s." % self.val1)
		self.val17 = self.readServiceModeCV("17")
		self.printSave ("	CV 17 = %s." % self.val17)
		self.val18 = self.readServiceModeCV("18")
		self.printSave ("	CV 18 = %s." % self.val18)
		self.mfrID = self.readServiceModeCV("8")
		self.printSave ("	CV 8 = %s." % self.mfrID)
		self.printSave("")
		
		# Determine if this locomotive uses a long address
		if ((self.val29 & 32) == 32) :
			self.long = True
			self.address = (self.val17 - 192) * 256 + self.val18
		else :
			self.long = False
			self.address = self.val1
		
		# get the manufacturer so we can adjust for decoder-specific settings
		if (self.DecoderMap.has_key(self.mfrID)):
			self.DecoderType = self.DecoderMap[self.mfrID]
		else:
			self.DecoderType = "Unknown"
			
		self.printSave("The Locomotive Address is: %s." % self.address)
		self.printSave("The Manufacturer is: %s."  % self.DecoderType)
		self.printSave("The Manufacturer ID is: %s."  % self.mfrID)
		self.printSave("")
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

	
	def setDecoderKnownState(self):
		self.testbedWriteCV(62, 0) # Turn off verbal reporting on QSI decoders
		self.testbedWriteCV(25, 0) # Turn off manufacture defined speed tables
		self.testbedWriteCV(19, 0) # Clear Consist Address in locomotive
		
		if self.long == True :			#turn off speed tables
			self.testbedWriteCV(29, 34)
		else:
			self.testbedWriteCV(29, 2)
		
		self.testbedWriteCV(2, 0)	#Start Voltage off
		self.testbedWriteCV(3, 0)	#Acceleration off
		self.testbedWriteCV(4, 0)	#Deceleration off
		self.testbedWriteCV(5, 0)	#Maximum Voltage off
		self.testbedWriteCV(6, 0)	#Mid Point Voltage off
		self.testbedWriteCV(66, 0) 	#Turn off Forward Trim
		self.testbedWriteCV(95, 0) 	#Turn off reverse Trim
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
		
		
####################################################################################
#
# self.measureTime() is used as part of the speed measurement
#
# This has been rewritten to first get the set of only the inactive sensors then
# wait just on a list of those sensors until one of them goes active.
#
# This should eliminate the false triggering of the block sensors that have a long
# timeout delay when they go from active to inactive.
#
####################################################################################
	def measureTime(self, sensorlist, starttime, stoptime) :
		
		"""Measures the time between virtual blocks"""
        
        # At the start of a measurement loop, we have to get the start time at the beginning
        # of the block then measure the time for the block.
        #
        # Otherwise, we take the stop time from the previous block, make it the start time
        # for this block and measure this block.
		
		if (starttime == 0):
			self.waitNextActiveSensor(sensorlist)
			stoptime = java.lang.System.currentTimeMillis()
		
		starttime = stoptime
		
		self.waitNextActiveSensor(sensorlist)
		stoptime = java.lang.System.currentTimeMillis()
		
		runtime = stoptime - starttime
		return runtime, starttime, stoptime
		

####################################################################################
#
# self.stripMinMax() is a generator that yields all values in a list that are
# NOT minimum or maximum values in the list.
#
####################################################################################
	def stripMinMax(self, speedlist):
		for speed in speedlist:
			if speed == max(speedlist):
				continue
			if speed == min(speedlist):
				continue
			yield speed
			
####################################################################################
#
# self.getSpeed() is used as part of the speed measurement
#
# This takes several speed measurements and returns an average value. If more than
# 3 values are given, the min and max values are omitted from the average.
# The final speed value returned is an average of the remaining values.
#
####################################################################################	
	def getSpeed(self, speedlist):
		if(self.NumSpeedMeasurements > 3):
			trimmedValues = []
			for speed in self.stripMinMax(speedlist):
				trimmedValues.append(speed)
		else:
			trimmedValues = speedlist
		return sum(trimmedValues)/len(trimmedValues)
		
####################################################################################
#
# self.measureSpeed() performs the speed measurement algorithm
#
# Given which track loop and the length of a block, we can measure the speed by
# measuring the time through each block. This version takes several measurements and
# averaging them, throwing out the high and low values.
#
# The targetspeed parameter is used to select the appropriate sensor array
####################################################################################
	def measureSpeed(self, targetspeed) :
		"""converts time to speed, ft/sec - scale speed"""
		starttime = stoptime = 0	# Needed when using every block
		speed = 0.0
		speedlist = []
		num_measurements = self.NumSpeedMeasurements
		num_blocks = 1
		sensor_array = []
		
		if (int(targetspeed) >= self.HighSpeedThreshold) :
			num_blocks = self.HighSpeedNBlocks
			sensor_array = self.HighSpeedArrayN
			print ("Measuring speed using the high speed array (%s block(s))." % num_blocks)
		elif (int(targetspeed) >= self.MediumSpeedThreshold) :
			num_blocks = self.MediumSpeedNBlocks
			sensor_array = self.MediumSpeedArrayN
			print ("Measuring speed using the medium speed array (%s block(s))." % num_blocks)
		else:
			num_blocks = self.LowSpeedNBlocks
			sensor_array = self.LowSpeedArrayN
			print ("Measuring speed using the low speed array (%s block(s))." % num_blocks)
		
		# Calculate the length of the selected block
		blocklength = self.block * num_blocks
        
        # Measure the speed a number of times and put those speeds into a list
		
		for z in range(0,self.NumSpeedMeasurements) : # make 5 speed measurements
			duration, starttime, stoptime = self.measureTime(sensor_array,starttime,stoptime)
			
			if duration == 0 :
				print ("Error: Got a zero for duration") # this should not happen
				speed = 0.0
			else :
				speed = (blocklength / (duration / 1000.0)) * (3600.0 / 5280)
				self.printSave("	Measurement %s: Speed = %s MPH" % (z+1, str(round(speed,3))))
				speedlist.append(speed)
		
		speed = self.getSpeed(speedlist)
		return speed
		
	def findMaximumForwardSpeed(self) :
		print ("Finding the maximum forward speed over %s laps." % self.NumSpeedMeasurements)
		self.throttle.setIsForward(True)
		self.waitMsec(500)
		self.throttle.setSpeedSetting(1.0)
		self.waitMsec(1000)
		speed = self.measureSpeed(self.fullSpeed)
		self.printSave ("Maximum forward speed found = %s MPH." % round(speed))
		print("")
		self.waitNextActiveSensor([self.homesensor])
		self.stopLocomotive()
		return speed		

	def findMaximumReverseSpeed(self) :
		print ("Finding the maximum reverse speed over %s laps/" % self.NumSpeedMeasurements)
		self.throttle.setIsForward(False)
		self.waitMsec(500)
		self.throttle.setSpeedSetting(1.0)
		self.waitMsec(1000)
		speed = self.measureSpeed(self.fullSpeed)
		self.printSave ("Maximum reverse speed found = %s MPH." % round(speed))
		print("")
		self.waitNextActiveSensor([self.homesensor])
		self.stopLocomotive()
		return speed
		
####################################################################################
# setCalibrateDirection() checks to see in what direction the locomotive is slower
# and sets the throttle appropriately.  Goal is to set up speed tables for a 
# diesel locomotive in the slower direction.
####################################################################################		
	def setCalibrateDirection(self, fwdmaxspeed, revmaxspeed):
		if (fwdmaxspeed > revmaxspeed) :
			self.printSave ("Locomotive %s is faster in the forward direction." % self.address)
		elif (revmaxspeed > fwdmaxspeed) :
			self.printSave ("Locomotive %s is faster in the reverse direction." % self.address)
		else :
			self.printSave ("Locomotive %s runs equally well in both directions." % self.address)
		self.throttle.setIsForward(fwdmaxspeed > revmaxspeed)
		self.waitMsec(500)
			
					
	def handle(self):
		self.printSave("Speed Table Script Version %s." % self.scriptversion)
		self.printSave("")
		startProgramTime = java.lang.System.currentTimeMillis()
		topspeed = float(self.MaxSpeed.text)/100
		self.printSave("Top Target Speed is %s MPH" % self.MaxSpeed.text)
		self.printSave("")
		
		self.readDecoder()
		self.attachThrottle()
		self.attachProgrammer()
		self.setDecoderKnownState()
		self.attachThrottle()
		self.waitMsec(2000)
		
		self.warmUpForward()
		fwdmaxspeed = self.findMaximumForwardSpeed()
		
		
		if self.Locomotive.getSelectedItem() <> "Steam" :
			self.warmUpReverse()
			revmaxspeed = self.findMaximumReverseSpeed()
		else:
			self.printSave("Not checking speeds in reverse direction because this is a steam locomotive.")
			self.printSave("")
			revmaxspeed = 0
		
		self.setCalibrateDirection(fwdmaxspeed, revmaxspeed)	

			#Find throttle setting that gives desired speed

		
		throttlesetting = 35	# starting throttle setting(determined by lots of testing)
		lowthrottle = 0
		badlocomotive = False

		for speedvalue in self.stepList :

			targetspeed = round(speedvalue * topspeed)		

			print
			self.printSave ("Target Speed is %s." % targetspeed)
			print

			self.stepValueList.extend([0,0,0]) #create spots in list for calculated speed steps

			#initializing all variables for next measured speed step
			Done = False
			speed = 1000
			minimumdifference = 20
			beenupone = False
			beendownone = False
			lowspeed = 0	
			hispeed = 1000
			hithrottle = 127

            #05/21/10
			if ((self.Locomotive.getSelectedItem() == "Diesel") and (targetspeed > revmaxspeed)) or targetspeed > fwdmaxspeed :
				print
				self.printSave ("Locomotive can not reach %s MPH." % targetspeed)
				print
				Done = True
				throttlesetting = 127

			while Done == False:

				# Fraction of throttle per 126 steps is 1/126 = 0.0079365
				self.throttle.setSpeedSetting(.0079365 * throttlesetting)
				self.waitMsec(100)
				print
				self.printSave ("Throttle Setting %s" % throttlesetting)
				speed = self.measureSpeed(targetspeed)
 
				# compare it to desired speed and decide whether or not to test a different throttle setting
				difference = targetspeed - speed
				self.printSave ("Measured Speed = %s.  Difference = %s at throttle setting %s." % (round(speed,3), round(difference ,3),throttlesetting))

				#Coarse Measurement
				if difference < -10 and targetspeed < 20 and throttlesetting > 15 : #started at 35 want to drop fast to reduce time
					hithrottle = throttlesetting
					throttlesetting = throttlesetting - 10
					if throttlesetting < lowthrottle :
						self.printSave ("Throttlesetting %s is too slow." % throttlesetting)
						throttlesetting = lowthrottle + 1
						if hithrottle-lowthrottle < 2 :
							Done = True
							if (hispeed - targetspeed) > (targetspeed - lowspeed) :
								throttlesetting = lowthrottle
							else :
								throttlesetting = hithrottlesetting

				elif difference < -13 and throttlesetting > 15 : # keep throttle setting > 0
					hithrottle = throttlesetting
					throttlesetting = throttlesetting - 6	 # and don't want drastic changes
					if throttlesetting < lowthrottle :
						self.printSave ("Throttlesetting %s is too slow." % throttlesetting)
						throttlesetting = lowthrottle + 1
						if hithrottle-lowthrottle < 2 :
							Done = True
							if (hispeed - targetspeed) > (targetspeed - lowspeed) :
								throttlesetting = lowthrottle
							else :
								throttlesetting = hithrottlesetting

				elif difference < -8 and throttlesetting > 6 : # keep throttle setting > 0
					hithrottle = throttlesetting
					throttlesetting = throttlesetting - 3
					if throttlesetting < lowthrottle :
						self.printSave ("Throttlesetting %s is too slow." % throttlesetting)
						throttlesetting = lowthrottle + 1
						if hithrottle-lowthrottle < 2 :
							Done = True
							if (hispeed - targetspeed) > (targetspeed - lowspeed) :
								throttlesetting = lowthrottle
							else :
								throttlesetting = hithrottlesetting

				elif difference > 13 and throttlesetting < 121 : # keep throtte setting < 128
					lowthrottle = throttlesetting
					throttlesetting = throttlesetting + 7
					if throttlesetting > hithrottle :
						self.printSave ("Throttlesetting %s is too fast." % throttlesetting)
						throttlesetting = hithrottle - 1
						
				elif difference > 8 and throttlesetting < 123 : # keep throtte setting < 128
					lowthrottle = throttlesetting
					throttlesetting = throttlesetting + 4
					if throttlesetting > hithrottle :
						self.printSave ("Throttlesetting %s is too fast." % throttlesetting)
						throttlesetting = hithrottle - 1
						
				elif difference > 5 and targetspeed < 20 and throttlesetting > 10 : #for motors that need a lot at the beginning
					lowthrottle = throttlesetting
					throttlesetting = throttlesetting + 5
					if throttlesetting > hithrottle :
						self.printSave ("Throttlesetting %s is too fast." % throttlesetting)
						throttlesetting = hithrottle - 1

				else :
					#Fine Measurement
					if minimumdifference > abs(difference) :
						minimumdifference = abs(difference)
						savethrottlesetting = throttlesetting
					elif beenupone == True and beendownone == True :
						throttlesetting = savethrottlesetting
						lowthrottle = throttlesetting + 1
						self.printSave ("Closest throttle setting is %s." % throttlesetting)
						Done = True

					if difference < 0  and Done != True :
						throttlesetting = throttlesetting - 1
						beendownone = True
					elif difference > 0 and Done != True :
						throttlesetting = throttlesetting + 1
						lowthrottle = throttlesetting
						beenupone = True
					else :
						Done = True
						throttlesetting = savethrottlesetting
						lowthrottle = throttlesetting + 1

				if throttlesetting < 1 :
					print
					self.printSave ("Cannot create speedtable")
					self.printSave ("Locomotive has mechanical or decoder problem")
					print
					Done = True
					badlocomotive = True
					throttlesetting = 1

	
				if throttlesetting > 127 :
					print
					self.printSave ("Locomotive can not reach %s MPH." % targetspeed)
					print
					Done = True
					throttlesetting = 127

			lowthrottle = throttlesetting
			if difference < -5 :
				self.stepValueList.append(int(round((throttlesetting - .5) * 2)))
			elif difference > 5 :
				self.stepValueList.append(int(round((throttlesetting + .5) * 2)))
			else :
				self.stepValueList.append(int(round(throttlesetting * 2)))
			throttlesetting = throttlesetting + 10 	# no need test a value already in the table
										# time to do the next speed step
                                            #09/17/09	had instance where prior statment set speed to 128
			if throttlesetting > 127 :
				throttlsetting = 127

			# Stop locomotive

			self.throttle.setSpeedSetting(0.0)
			self.waitMsec(3000)

			#Calculate speed step values inbetween measured ones

		if badlocomotive == False :
			print
			self.printSave ("Measured Values")
			self.printSave ("%s" % self.stepValueList)

			if self.stepValueList[4] < 4 :
				self.stepValueList[4] = 4

			self.stepValueList[0] = self.stepValueList[4] - (self.stepValueList[8] - self.stepValueList[4]) #trying to improve the bottom end performance

			# making sure none of the speedsteps are < 1
			if ((self.stepValueList[4] - self.stepValueList[0]) / 4) + self.stepValueList[0] < 1 :
				self.stepValueList[0] = 0

			for  z in range (4, 29, 4) :
				# To prevent speedsteps from having the same value
				# decided it was better to error faster than slower
				if self.stepValueList[z] - self.stepValueList[z - 4] < 4 :
					self.stepValueList[z] = self.stepValueList[z - 4] + 4

				if self.stepValueList[z] > 255 :	#can't have a value greater than 255
					self.stepValueList[z] = 255
 

				# Create calculated speed steps
				y = self.stepValueList[z] - self.stepValueList[z - 4]
				x = (y/4)
				self.stepValueList[z -3] = self.stepValueList[z] - round(x * 3)
				self.stepValueList[z -2] = self.stepValueList[z] - round(x * 2)
				self.stepValueList[z -1] = self.stepValueList[z] - round(x)

			print
			self.printSave ("All Values")
			self.printSave ("%s" % self.stepValueList)
			self.attachProgrammer()

			self.printSave("Writing Speed table to locomotive")
			# Write Speed Table to locomotive
			for z in range (67, 95) :
				self.printSave("Writing CV: %s with value %s." % (z, self.stepValueList[z - 66]))
				self.testbedWriteCV(z, int(self.stepValueList[z - 66]))
				print(self.readServiceModeCV(str(z)))

			# Turn on speed table
			print("Turning on speed table")
			if self.long == True :
				self.testbedWriteCV(29, 50)
			else:
				self.testbedWriteCV(29, 18)

			# Turn on acceleration and deceleration
			self.testbedWriteCV(3, 1)	#Acceleration on
			self.testbedWriteCV(4, 1)	#Deceleration on

			self.printSave("Done")
		else :
				print("Done - Locomotive has decoder or mechanical problem; cannot create speed table")

		stopProgramTime = java.lang.System.currentTimeMillis()
		timeElapsed = (stopProgramTime - startProgramTime)/60000
		
		self.printSave("Handle Procedure Done - required %s minutes." % timeElapsed)
		
		return False

####################################################################################
	def whenMyButtonClicked(self,event) :
		self.start()
		# we leave the button off
		self.startButton.enabled = False
		
		return

####################################################################################
#
# This method creates the user input panel, starting the whole process
# the panel collects input parameters from the user
#
####################################################################################
	
	def setup(self):
		# create a frame to hold the button, set up for nice layout
		f = javax.swing.JFrame("Testbed Input Panel")		# argument is the frames title
		f.setLocation(300,200)
		f.contentPane.setLayout(javax.swing.BoxLayout(f.contentPane, javax.swing.BoxLayout.Y_AXIS))
		
		# create the start button
		self.startButton = javax.swing.JButton("Start")
		self.startButton.actionPerformed = self.whenMyButtonClicked
		self.status = javax.swing.JLabel("Press start when ready")
		
		templabel = javax.swing.JLabel("", javax.swing.JLabel.CENTER)
		templabel.setText("Select Locomotive Type")
		
		self.Locomotive = javax.swing.JComboBox()
		self.Locomotive.addItem("Diesel")
		#self.Locomotive.addItem("Electric")
		self.Locomotive.addItem("Steam")
		
		self.MaxSpeed = javax.swing.JTextField(3)
		
		temppanel3 = javax.swing.JPanel()
		temppanel3.add(javax.swing.JLabel("Maximum Speed (MPH)"))
		temppanel3.add(self.MaxSpeed)
		
		temppanel2 = javax.swing.JPanel()
		f.contentPane.add(templabel)
		f.contentPane.add(self.Locomotive)
		f.contentPane.add(temppanel3)
		temppanel2.add(self.startButton)
		f.contentPane.add(temppanel2)
		f.contentPane.add(self.status)
		f.pack()
		f.show()
		
		return

####################################################################################
#
# Instantiate the automation class and start it up
#
####################################################################################
a = DCCDecoderCalibration()

# This brings up the dialog box that will call self.start()
a.setup()


