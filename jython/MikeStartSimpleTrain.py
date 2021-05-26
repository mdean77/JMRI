# StartTrain.py created by Mike Dean May 2021
# Hoping to set up automation for train club meeting later this week
#

import jarray
import jmri

class StartSimpleTrain(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        # Get relevant routes
        self.trackBypassNW = routes.getRoute("NW Bypass")
        self.closeNW = routes.getRoute("NW Staging Close")
        self.track6NW = routes.getRoute("NW Track 6")
        self.crossOver = routes.getRoute("Crossover")
        self.straightThru = routes.getRoute("Straight Through")
        
        #Get relevant turnouts
        self.to403 = turnouts.getTurnout("Staging NW Turnout 403")
        self.to407 = turnouts.getTurnout("Staging NW Turnout 407")
        self.to400 = turnouts.getTurnout("Staging NW Turnout 400")
        self.to201 = turnouts.getTurnout("East Turnout 201")
        self.to202 = turnouts.getTurnout("East Turnout 202")
        self.to203 = turnouts.getTurnout("East Turnout 203")
        self.to204 = turnouts.getTurnout("East Turnout 204")
        self.to205 = turnouts.getTurnout("East Turnout 205")
        self.to206 = turnouts.getTurnout("East Turnout 206")
        self.to207 = turnouts.getTurnout("East Turnout 207")
        self.to208 = turnouts.getTurnout("East Turnout 208")
        self.to209 = turnouts.getTurnout("East Turnout 209")
        self.to210 = turnouts.getTurnout("East Turnout 210")
        self.to211 = turnouts.getTurnout("East Turnout 211") 
              
        #Get relevant sensors
        self.westSWSensor = sensors.getSensor("West / SW")
        self.westNWSensor = sensors.getSensor("West / NW")
        self.mountainSensor = sensors.getSensor("Mountain")
        self.southSensor1 = sensors.getSensor("South Zone 1")
        self.southSensor2 = sensors.getSensor("South Zone 2")
        self.southSensor3 = sensors.getSensor("South Zone 3")
        self.southSensor4 = sensors.getSensor("South Zone 4")
        self.southSensor5 = sensors.getSensor("South Zone 5")
        self.southSensor6 = sensors.getSensor("South Zone 6")
        self.southSensor7 = sensors.getSensor("South Zone 7")
        self.eastSensor1 = sensors.getSensor("East Zone 1")
        self.eastSensor2 = sensors.getSensor("East Zone 2")
        self.eastSensor3 = sensors.getSensor("East Zone 3")
        self.eastSensor4 = sensors.getSensor("East Zone 4")
        self.eastSensor5 = sensors.getSensor("East Zone 5")
        self.eastSensor6 = sensors.getSensor("East Zone 6")
        self.eastSensor7 = sensors.getSensor("East Zone 7")
        self.eastSensor8 = sensors.getSensor("East Zone 8")
        self.eastSensor9 = sensors.getSensor("East Zone 9")
        self.eastSensor10 = sensors.getSensor("East Zone 10")
        self.eastSensor11 = sensors.getSensor("East Zone 11")
        self.eastSensor12 = sensors.getSensor("East Zone 12")
        self.eastSensor13 = sensors.getSensor("East Zone 13")
        self.northSensor1 = sensors.getSensor("North Zone 1")
        self.northSensor2 = sensors.getSensor("North Zone 2")
        self.northSensor3 = sensors.getSensor("North Zone 3")
        self.northSensor4 = sensors.getSensor("North Zone 4")
        self.northSensor5 = sensors.getSensor("North Zone 5")
        self.northSensor6 = sensors.getSensor("North Zone 6")
        self.northSensor7 = sensors.getSensor("North Zone 7")
        self.northSensor8 = sensors.getSensor("North Zone 8")
        self.northSensor9 = sensors.getSensor("North Zone 9")        
        return

    def LongHorn(self,duration, pause, times):
        cnt = times
        while cnt > 0:
            self.throttle.setF2(True)
            self.waitMsec(duration)
            self.throttle.setF2(False)
            self.waitMsec(pause)
            cnt = cnt - 1
        return

    def openTrack6(self):
        self.track6NW.setRoute()
        print("Track 6 should be open")
        return
            
    def openBypass(self):
        self.trackBypassNW.setRoute()
        self.to403.setState(CLOSED)
        self.to407.setState(CLOSED)
        self.to400.setState(THROWN)
        print("Bypass should be open")
        return
        
    def closeStaging(self):
        self.closeNW.setRoute()
        self.to403.setState(THROWN)
        self.to400.setState(THROWN)
        print("Staging should be closed")
        return

    def startUpRoutines(self):
        print("Executing startup routine")
        self.throttle = self.getThrottle(8997, True)
        self.throttle.setF0(True)
        self.throttle.setSpeedSetting(0.01)
        self.waitMsec(200)
        self.throttle.setSpeedSetting(0)
        self.throttle.setF9(True)
        self.waitMsec(30000)
        self.LongHorn(1500, 1200,3)
        self.waitMsec(1000)
        print("Leaving startup routine")
        return

    def handle(self):
        print("This program will start up engine 8997 on NW Staging Track 6,")
        print("and circle the layout one time.  It will then back the train into")
        print("NW Staging Track 6 via the NW Bypass track, shutdown the engine,")
        print("and then restore the mainline, eliminating power to staging.")
        print("==================================================================")
        #Open staging via track 6
        self.openTrack6()
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
        self.closeStaging()
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
        self.openBypass()
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
        self.closeStaging()
        return False	# to continue
	
# end of class definition

# create one of these
a = StartSimpleTrain()

# and start it running
a.start()

