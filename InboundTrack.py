import queue
import random as rand
import Train
class InboundTrack:
    ##update this to accept trains instead of railcarls
    def addRailcars(self, Inbound):
        for i in range(len(Inbound.Cars)):
            self.storedCars.append(Inbound.Cars[i])

    def removeRailcar(self, Inbound):
            print(self.storedTrains[0].Cars[0].RailcarID)
            self.storedTrains[0].Cars.pop(0)
            if (len(self.storedTrains[0].Cars) == 0):
                self.storedTrains.pop(0)
    
    def removeTrain(self, Inbound):
            for i in range(len(self.storedTrains[0].Cars)): 
                del self.storedTrains[0].Cars[0]
            if (len(self.storedTrains[0].Cars) == 0):
                del self.storedTrains[0]

    def __init__(self, TrackID, OutboundTrackNumber, TrainID):
        self.TrackCapacity = 65
        self.storedTrains = []
        self.outboundTrackNum = OutboundTrackNumber
        self.TrackID = TrackID
        self.length = rand.randrange(10, 65)
        self.storedTrains.append(Train.Train(TrainID, self.TrackID, self.length, self.outboundTrackNum))