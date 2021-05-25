# TootHorn.py
# Acquire a locomotive and toot the horn.

import jarray
import jmri
global TootHorn

class TootHorn(jmri.jmrit.automat.AbstractAutomaton):
    def init(self):
        global HornTooted
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

    def handle(self):
        print("Executing TootHorn handle")
        self.throttle = self.getThrottle(8997, True)
        self.throttle.setF9(True)
        self.waitMsec(30000)
        self.LongHorn(1200, 800,6)
        self.waitMsec(1000)
        self.HornTooted = "Done"
        print("Leaving TootHorn handle")
        return False
        
#TootHorn().start()