# StartNW8997.py created by Mike Dean July 2021
# This script can be executed directly or called from another script.
#

import jarray
import jmri
#global trainDone
class StartNW8997(jmri.jmrit.automat.AbstractAutomaton):

    MasterFunctions = jmri.util.FileUtil.getExternalFilename("scripts:MikeMasterFunctions.py")
    execfile(MasterFunctions)

# Start up routines are unique for each train
    def startUpRoutines(self):
        print("Executing startup routine")
        self.throttle = self.getThrottle(8997, True)
        self.throttle.setF0(True)
        self.throttle.setSpeedSetting(0.01)
        self.waitMsec(200)
        self.throttle.setSpeedSetting(0)
        self.throttle.setF9(True)
        self.waitMsec(20000)
        self.LongHorn(1500, 1200,3)
        self.waitMsec(1000)
        print("Leaving startup routine")
        return
    
    def init(self):
        print("Inside init")
        memories.provideMemory("Train Done").setValue("No")
        self.getTableData()
        return

    def handle(self):
        print("This program will start up engine 8997 on NW Staging Track 6,")
        print("and circle the layout one time.  It will then back the train into")
        print("NW Staging Track 6 via the NW Bypass track, shutdown the engine,")
        print("and then restore the mainline, eliminating power to staging.")
        print("==================================================================")
        #Open staging via track 6
        self.openNWTrack6()
        print("Power should be on to track 6 caboose")
        self.throttle = self.getThrottle(8997, True)
        self.startUpRoutines()

        print("Starting main train run out of staging")
        self.throttle.setIsForward(True)
        self.throttle.setF0(True)
        self.throttle.setSpeedSetting(0.1)
        print("Waiting for west SW sensor to become active")
        self.waitSensorActive([self.westSWSensor])
        print("Sensor active.  Waiting for inactive west SW sensor")
        self.waitSensorInactive([self.westSWSensor])
        print("Sensor inactive.  Closing staging.")
        self.closeNWStaging()
        print("Throttle up")
        self.LongHorn(1200,500,3)
        self.throttle.setSpeedSetting(0.35)
        print("Straight through should already be set but will run routine anyway")
        self.straightThru.setRoute()
        print("Doing the first lap straight thru - no cross over at the interchange")
        print("Waiting for north sensor 1 to become active and will then toot horn")
        self.waitSensorActive([self.northSensor1])
        print("Sensor 1 active - toot horn")
        self.LongHorn(1200, 800,2)
        self.waitSensorInactive([self.eastSensor13])
        self.waitSensorActive([self.northSensor9])
        print("Slowing speed to 20%")
        self.throttle.setSpeedSetting(0.2)
        print("Now waiting to set west SW sensor on")
        self.waitSensorActive([self.westSWSensor])
        print("SW west is active - lowering speed to 15%")
        self.throttle.setSpeedSetting(0.15)
        print("Waiting for SW west to go inactive and will then stop")
        self.waitSensorInactive([self.westSWSensor])
        print("South west sensor inactive - will stop.")
        self.throttle.setSpeedSetting(0.0)
        self.waitMsec(10000)
        print("Now set reverse and open the bypass track")
        self.throttle.setIsForward(False)
        self.openNWBypass()
        print("Reverse speed at 15%")
        self.throttle.setSpeedSetting(0.15)
        self.throttle.setF1(True)
        self.waitSensorActive([self.westSWSensor])
        print("We SW sensor active")
        self.waitSensorInactive([self.westSWSensor])
        self.throttle.setSpeedSetting(0.1)
        print("Sensor inactive - will drive for 28 seconds at 10%")
        self.waitMsec(28000)
        print("Throttle speed zero")
        self.throttle.setSpeedSetting(0)
        self.throttle.setF1(False)
        self.throttle.setF0(False)
        print("Shutting down engine and closing staging")
        self.throttle.setF9(False)
        self.throttle.setF9(True)
        self.waitMsec(25000)
        self.closeNWStaging()
        memories.provideMemory("Train Done").setValue("Yes")
        #trainDone = memories.provideMemory("Train Done").getValue()
        #print(trainDone)
        return False	# to continue
	
# end of class definition

# create one of these
a = StartNW8997()

# and start it running
a.start()

