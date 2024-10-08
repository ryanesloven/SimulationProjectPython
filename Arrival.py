import random as rand
class Arrival:
    def forecast(self, time):
        if(time - self.lastTime > rand.randrange(900)): ##makes at least one train arrive every 15 minutes
            index = rand.randrange(len(self.Inbound.Tracks))
            delay = self.Inbound.addTrain(index)
            self.lastTime = time
            return delay*10 ##increases internal timer by the number of trains classifeid multiplied by the operation time
        else:
            return 0
    def __init__(self, In, Track, SimTime):
        self.lastTime = 0
        self.Inbound = In
        self.Tracker = Track
        self.MaxTime = SimTime