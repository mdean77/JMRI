# StartTrain.py created by Mike Dean May 2021
# Hoping to set up automation for train club meeting later this week
#

import jarray
import jmri
global trainDone
global TrainNW8997
TrainNW8997 = jmri.util.FileUtil.getExternalFilename("scripts:MikeStartNW8997.py") 

class ExecuteTrains(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        trainDone = memories.provideMemory("Train Done").getValue()
        print(trainDone)    
        return
        
    def handle(self):
        execfile(TrainNW8997)
        trainDone = memories.provideMemory("Train Done").getValue()
        while trainDone != "Yes":
            self.waitMsec(10000)
            trainDone = memories.provideMemory("Train Done").getValue()
        print("Escaped from the loop")
        print(trainDone)
        trainDone = memories.provideMemory("Train Done").setValue("No")
        execfile(TrainNW8997)
        return False

a = ExecuteTrains()

a.start()
