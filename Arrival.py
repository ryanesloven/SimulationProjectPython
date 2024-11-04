import random as rand
class Arrival:
    def forecast(self, time):
        difference = time - self.lastTime 
        delay = 0
        while (True):
            difference = difference - 1800
            if(difference > 0):
                index = rand.randrange(len(self.Inbound.Tracks))
                delay = delay + self.Inbound.addTrain(index)
                self.lastTime = time
                self.Wins = self.Wins + 1
            else:
                break
        return delay

    def __init__(self, In, Track, SimTime):
        self.lastTime = 0
        self.Inbound = In
        self.Tracker = Track
        self.MaxTime = SimTime
        self.Wins = 0