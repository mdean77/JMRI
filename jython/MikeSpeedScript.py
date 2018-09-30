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

		# JMD:  I changed the sensor numbering since I will only have 12 blocks.
		self.sensor1 = sensors.provideSensor("Block:1")
		self.sensor2 = sensors.provideSensor("Block:2")
		self.sensor3 = sensors.provideSensor("Block:3")
		self.sensor4 = sensors.provideSensor("Block:4")
		self.sensor5 = sensors.provideSensor("Block:5")
		self.sensor6 = sensors.provideSensor("Block:6")
		self.sensor7 = sensors.provideSensor("Block:7")
		self.sensor8 = sensors.provideSensor("Block:8")
		self.sensor9 = sensors.provideSensor("Block:9")
		self.sensor10 = sensors.provideSensor("Block:10")
		self.sensor11 = sensors.provideSensor("Block:11")
		self.sensor12 = sensors.provideSensor("Block:12")
		self.homesensor = sensors.provideSensor("Block:12")

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

		#	These speed steps are measured.  All others are calculated
		#	CV		70	74	78	82	86	90	94
		#	Speedsteps	 4	 8	12	16	20	24	28

		#	These lists are percentages of full speed
		self.DigitraxStepList = [10, 22, 35, 47, 60, 72, 85]
		self.Lenz5GenStepList = [17, 30, 44, 57, 71, 84, 98]
		self.LenzXFStepList = [11, 26, 40.5, 55, 70, 84, 98.5]
		self.NCEStepList = [10.5, 25, 39.5, 54,	68, 83,	98]
		self.OldTCSStepList = [14.5, 28.5, 42.5, 57, 71.5, 86, 99]
		self.NewTCSStepList = [13, 25.5, 38, 50.5, 63, 75.5, 88]
		self.QSIStepList = [11,	26,	41,	55,	70,	85,	99]
		self.SoundtraxxDSDStepList = [14,	28,	42,	56,	70,	84,	99]
		self.TsunamiStepList = [14.5,	28.5,	42.5,	57,	71,	85,	99]
		self.ESUStepList = [12,	27,	41,	56,	70,	85,	99]
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
			print ("Trottle assigned to locomotive: ", self.address)
		return

	def warmUpEngine(self):
		self.attachThrottle()

		print ("Warming up Locomotive")
		self.throttle.setIsForward(True)

		#01/09/09	TCS decoder would not move when setting throttle to 1.0
 
 		print ("Set the throttle to 1.0")

		self.throttle.setSpeedSetting(.99)
		self.waitMsec(250)
		self.throttle.setSpeedSetting(1.0)

		print ("Wait for the locomotive to get to block", self.homesensor_num, "after", self.warmupLaps, "laps...")

		for x in range (0, self.warmupLaps) :
			self.waitNextActiveSensor([self.homesensor])

		print ("Stop the locomotive")
		self.throttle.setSpeedSetting(0.0)
		self.waitMsec(2000)
		
		# Warm up 5 laps reverse

		if self.Locomotive.getSelectedItem() <> "Steam" :
			self.throttle.setIsForward(False)
			self.throttle.setSpeedSetting(1.0)

			print ("Warming up in the reverse direction for", self.warmupLaps, "laps...")
			for x in range (0, self.warmupLaps) :
				self.waitNextActiveSensor([self.homesensor])

		return
	
	      
	def handle(self):
		topspeed = float(self.MaxSpeed.text)/100
		print ("Top Target Speed is ", self.MaxSpeed.text, "MPH")
		self.status.text = "Locomotive Setup"

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


