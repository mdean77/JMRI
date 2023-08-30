#Start Amtrak train out of SW track 3; returning to SW track 3.
import jarray
import jmri

class StartSWAmtrak(jmri.jmrit.automat.AbstractAutomaton):

    MasterFunctions = jmri.util.FileUtil.getExternalFilename("scripts:MikeMasterFunctions.py")
    execfile(MasterFunctions)

    def init(self):
        print("Inside init")
        memories.provideMemory("Train Done").setValue("No")
        self.getTableData()
        return

    def handle(self):
        print("This program will start up engine Amtrak on SW track 3,")
        print("and circle the layout one time.  It will then back the train into")
        print("SW Staging Track 3.")
        print("==================================================================")
        #Open staging via track 3
        self.openSWTrack3()
        self.throttle = self.getThrottle(16, True)
        if (self.throttle == None) :
            print ("ERROR: Couldn't assign throttle!")
        else :
            print ("Throttle assigned to locomotive: %s." % 16)
        print("Starting Amtrak train run out of staging")
        self.throttle.setIsForward(True)
        self.throttle.setF0(True)
        self.throttle.setSpeedSetting(0.25)
        print("Waiting for west NW sensor to become active")
        self.waitSensorActive([self.westNWSensor])
        print("Sensor active.  Waiting for inactive west NW sensor")
        self.waitSensorInactive([self.westNWSensor])
        print("Sensor inactive.  Closing staging.")
        self.closeSWStaging()
        self.throttle.setSpeedSetting(0.3)
        self.waitSensorActive([self.southSensor1])
        self.waitSensorActive([self.westSWSensor])
        self.throttle.setSpeedSetting(0.2)
        self.waitSensorInactive([self.westSWSensor])
        self.throttle.setSpeedSetting(0.0)
        self.openSWTrack3()
        self.throttle.setIsForward(False)
        self.throttle.setSpeedSetting(0.15)
        self.waitSensorInactive([self.westNWSensor])
        print("Sensor inactive - will drive for 20 seconds at 15%")
        self.waitMsec(20100)
        print("Throttle speed zero")
        self.throttle.setSpeedSetting(0)
        self.throttle.setF0(False)

        self.closeSWStaging()
        memories.provideMemory("Train Done").setValue("Yes")
        return False	# to continue
	
# end of class definition

# create one of these
a = StartSWAmtrak()

# and start it running
a.start()