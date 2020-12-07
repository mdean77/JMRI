# Adapted script showing how to initialize
# turnouts to a given state (THROWN or CLOSED)
#
# J. Michael Dean, December 2020

import jmri

for x in turnouts.getSystemNameList().toArray() :
   turnouts.provideTurnout(x).setState(THROWN)


