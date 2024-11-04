import random as rand
import InboundTrack
import Train
class InboundYard:
        def __init__(self, NumTracks, OutboundTrackNum):
            self.TrainIDIncrement = 1
            self.Tracks = []
            self.NumberTracks = NumTracks
            self.outboundTrackNum = OutboundTrackNum
            for i in range(int(self.NumberTracks)):
                TrackId = i+1
                self.Tracks.append(InboundTrack.InboundTrack(TrackId, OutboundTrackNum, self.TrainIDIncrement))
                self.TrainIDIncrement =+ 1


        def addTrain(self, index):
            TrackID = rand.randrange(len(self.Tracks))
            length = rand.randrange(10, 65)
            self.TrainIDIncrement =+ 1
            self.Tracks[index].storedTrains.append(Train.Train(TrackID, self.TrainIDIncrement, length, self.outboundTrackNum))
            return len(self.Tracks[index].storedTrains[-1].Cars)
        
        def removeRailcar(self, inbound, index):
            del self.Tracks[index].storedTrains[0].Cars[0]
            if(self.Tracks[index].storedTrains[0].Cars == []):
                del self.Tracks[index].storedTrains[0]

        def removeTrain(self, Inbound):
            self.Tracks[Inbound.TrackNumber].storedTrains.pop(0)
            for i in range(len(self.Tracks[Inbound.TrackNumber].Cars)):
                if(self.Tracks[Inbound.TrackNumber].Cars[i].TrainID == Inbound.TrainID):
                    self.Tracks[Inbound.TrackNumber].storedCars.pop(i)
                
            ##Tracks[inbound.TrackNumber].storedCars.erase(Tracks[inbound.TrackNumber].storedCars.begin());