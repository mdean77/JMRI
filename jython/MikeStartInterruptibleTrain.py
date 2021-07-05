# Script to start up a train, send it out, and then have it stop.
# Then the script watches a memory variable to restart.
# In the meantime, I mess with the train, and get it ready to go.
# On restart, it returns to staging.

# J. Michael Dean, MD
# July 5, 2021

import jarray
import jmri

class StartTrainWithIntermediateActions(jmri.jmrit.automat.AbstractAutomaton):
    
    MasterFunctions = jmri.util.FileUtil.getExternalFilename("scripts:MikeMasterFunctions.py")
    execfile(MasterFunctions)
    
    def init(self):
        print("Inside init")
        memories.provideMemory("Intermediate Work Done").setValue("No")
        self.getTableData()
        return
    
    def handle(self):
        print("This will send out a train and stop it in South staging area,")
        print("and then when I set the flag Intermediate Work Done to Yes the")
        print("train will return to staging.")
        self.openNWTrack2()
        self.throttle = self.getThrottle(5542, True)
        self.throttle.setIsForward(True)
        self.throttle.setF0(True)
        self.throttle.setSpeedSetting(0.30)
        print("Waiting for west SW sensor to become active")
        self.waitSensorActive([self.westSWSensor])
        print("Sensor active.  Waiting for inactive west SW sensor")
        self.waitSensorInactive([self.westSWSensor])
        print("Sensor inactive.  Closing staging.")
        self.closeNWStaging()
        self.waitSensorActive([self.southSensor1])
        self.waitSensorInactive([self.southSensor1])
        self.throttle.setSpeedSetting(0.0)
        self.closeNWStaging()
        workDone = memories.provideMemory("Intermediate Work Done").getValue()
        while workDone != "Yes":
            self.waitMsec(10000)
            workDone = memories.provideMemory("Intermediate Work Done").getValue()
        print("Work done - escaped from loop")
        memories.provideMemory("Intermediate Work Done").setValue("No")
        
        self.throttle = self.getThrottle(5542, True)
        self.throttle.setIsForward(True)
        self.throttle.setF0(True)
        self.throttle.setSpeedSetting(0.35)     
        print("Now waiting to set west SW sensor on")
        self.waitSensorActive([self.westSWSensor])
        print("SW west is active - lowering speed to 15%")
        self.throttle.setSpeedSetting(0.25)
        print("Waiting for NW west to go inactive and will then stop")
        self.waitSensorInactive([self.westNWSensor])
        self.throttle.setSpeedSetting(0.0)
        self.waitMsec(2000)

        print("Now set reverse and open the second track")
        self.throttle.setIsForward(False)  
        self.openNWTrack2()
        print("Reverse speed at 25%")
        self.throttle.setSpeedSetting(0.25)
        print("We SW sensor active")
        self.waitSensorInactive([self.westSWSensor])
        self.throttle.setSpeedSetting(0.20)
        print("Sensor inactive - will drive for 28 seconds at 10%")
        self.waitMsec(17000)
        print("Throttle speed zero")
        self.throttle.setSpeedSetting(0)
        self.throttle.setF0(False)
        self.closeNWStaging()
        return False
        
# Create object and launch
a = StartTrainWithIntermediateActions()
a.start()
        