# Adapted script showing how to initialize
# turnouts to a given state (THROWN or CLOSED)
#
# J. Michael Dean, December 2020
#
# This script goes through all turnouts on my layout and closes them;  then
# it throws a subset to put the layout in a known state.
#
# I needed to put a delay when I was throwing turnouts - not sure why but otherwise
# I got erratic behavior.  This script is important so that JMRI knows the status of my
# turnouts;  if my operators (me) never manually touch a turnout, then the computer will
# always have an accurate picture of the state of the layout.

import jmri


class setStartup(jmri.jmrit.automat.AbstractAutomaton) :      
  def init(self):
    return
  def handle(self):
    for x in turnouts.getSystemNameList().toArray() :
       turnouts.provideTurnout(x).setState(CLOSED)
       #self.waitMsec(500)
    for x in ['NT400','NT403', 'NT303', 'NT202', 'NT102'] :
       turnouts.provideTurnout(x).setState(THROWN)
       #self.waitMsec(500)
    return False              # all done, don't repeat again

setStartup().start()          # create one of these, and start it running

