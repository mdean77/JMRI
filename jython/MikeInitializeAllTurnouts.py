# Adapted script showing how to initialize
# turnouts to a given state (THROWN or CLOSED)
#
# J. Michael Dean, December 2020

import jmri


class setStartup(jmri.jmrit.automat.AbstractAutomaton) :      
  def init(self):
    return
  def handle(self):
    for x in turnouts.getSystemNameList().toArray() :
       turnouts.provideTurnout(x).setState(CLOSED)
    for x in ['NT400','NT403'] :
       turnouts.provideTurnout(x).setState(THROWN)
       self.waitMsec(50)
    return False              # all done, don't repeat again

setStartup().start()          # create one of these, and start it running

