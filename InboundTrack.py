import queue
import random as rand
import Train
class InboundTrack:
    ##update this to accept trains instead of railcarls
    def addRailcars(self, Inbound):
        for i in range(len(Inbound.Cars)):
            self.storedCars.append(Inbound.Cars[i])

    def removeRailcar(self, Inbound):
            del self.storedTrains[0].Cars[0]
            if (len(self.storedTrains[0].Cars) == 0):
                 del self.storedTrains[0]

    def __init__(self, TrackID, OutboundTrackNumber, TrainID):
        self.TrackCapacity = 65
        self.storedTrains = []
        self.outboundTrackNum = OutboundTrackNumber
        self.TrackID = TrackID
        self.length = rand.randrange(65)
        self.storedTrains.append(Train.Train(TrainID, self.TrackID, self.length, self.outboundTrackNum))