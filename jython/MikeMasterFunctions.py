# Mike MasterFunctions.py
# Definitions and functions used by each train controlled by ExecuteTrains


def getTableData(self):
# Get relevant routes
    self.crossOver = routes.getRoute("Crossover")
    self.straightThru = routes.getRoute("Straight Through")
    
# Get relevant internal sensors that set up routes
    self.trackBypassNW = sensors.provideSensor("NW Bypass Track")
    self.closeNW = sensors.provideSensor("NW Staging Close")
    self.closeSW = sensors.provideSensor("SW Staging Close")
    self.track3SW = sensors.provideSensor("SW Staging Track 3")
    self.track6NW = sensors.provideSensor("NW Staging Track 6")
    self.track2NW = sensors.provideSensor("NW Staging Track 2")
    
#Get relevant turnouts
    self.to403 = turnouts.getTurnout("Staging NW Turnout 403")
    self.to407 = turnouts.getTurnout("Staging NW Turnout 407")
    self.to400 = turnouts.getTurnout("Staging NW Turnout 400")
    self.to401 = turnouts.getTurnout("Staging NW Turnout 401")
    self.to402 = turnouts.getTurnout("Staging NW Turnout 402")
    self.to404 = turnouts.getTurnout("Staging NW Turnout 404")
    self.to405 = turnouts.getTurnout("Staging NW Turnout 405")
    self.to406 = turnouts.getTurnout("Staging NW Turnout 406")
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
    self.to500 = turnouts.getTurnout("Staging SW Turnout 500")
    self.to501 = turnouts.getTurnout("Staging SW Turnout 501")
    self.to502 = turnouts.getTurnout("Staging SW Turnout 502")
    self.to503 = turnouts.getTurnout("Staging SW Turnout 503")
    self.to504 = turnouts.getTurnout("Staging SW Turnout 504")
              
#Get NCE relevant sensors
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

def openNWTrack6(self):
    self.track6NW.setCommandedState(ACTIVE)
    self.track6NW.setCommandedState(INACTIVE)
    print("Track 6 should be open")
    return
def openNWTrack2(self):
    self.track2NW.setCommandedState(ACTIVE)
    self.track2NW.setCommandedState(INACTIVE)
    print("Track 2 should be open")
    return
    
def openNWBypass(self):
    self.trackBypassNW.setCommandedState(ACTIVE)
    self.trackBypassNW.setCommandedState(INACTIVE)
    #self.to403.setState(CLOSED)
    #self.to407.setState(CLOSED)
    #self.to400.setState(THROWN)
    print("Bypass should be open")
    return
    
def closeNWStaging(self):
    self.closeNW.setCommandedState(ACTIVE)
    self.closeNW.setCommandedState(INACTIVE)
    #self.to403.setState(THROWN)
    #self.to400.setState(THROWN)
    print("Staging should be closed")
    return

def openSWTrack3(self):
    self.track3SW.setCommandedState(ACTIVE)
    self.track3SW.setCommandedState(INACTIVE)
    print("Staging SW Track 3 should be open")
    return
    
def closeSWStaging(self):
    self.closeSW.setCommandedState(ACTIVE)
    self.closeSW.setCommandedState(INACTIVE)
    #self.to500.setState(CLOSED)
    print("Staging SW should be closed")
    return