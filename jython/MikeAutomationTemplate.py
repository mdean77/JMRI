# This is an example script for a JMRI "Automat" in Python
#
# AbstractAutomaton is a JMRI asset.  Notice the spelling!
#
# This script will define an AbstractAutomaton subclass named Template.
# It will create an instance (named myTemplate).
# It does nothing (empty handle() procedure) and then exits.  
#
# But the instance still exists.  I can still use myTemplate.

import jmri

class Template(jmri.jmrit.automat.AbstractAutomaton) :
	def init(self):
		# do whatever you want to do ONCE in the init procedure
		# identify any new variables that you will want to access later
		return

	def handle(self):
		# do whatever you want to do in the script.  If you want it to run
		# only one time, then return False.  If you want this to repeat over
		# and over in a loop, then return True,
		return False	# to run only one time
	
# end of class definition

# create one of these
myTemplate = Template()

# and start it running
myTemplate.start()

