import OutboundTrack
class OutboundYard:
    def __init__(self, TrackNumber):
        self.NumberTracks = TrackNumber
        self.Tracks = []
        for i in range(int(self.NumberTracks)):
            TrackId = i+1
            self.Tracks.append(OutboundTrack.OutboundTrack(TrackId))
            ##print(len(self.Tracks[i].Cars))
            

    def addTrain(self, Outbound):
        for i in range(len(Outbound.Cars)):
            ##self.Tracks[Outbound.Cars[i].Destination].storedCars.append(Outbound.Cars[i])
            self.Tracks[Outbound.Cars[i].Destination].available = self.Tracks[Outbound.Cars[i].Destination].available - 1
    
    def addRailcar(self, Outbound):
        ##print(len(self.Tracks[Outbound.Destination].Cars))
        ##self.Tracks[Outbound.Destination].available = self.Tracks[Outbound.Destination].available - 1
        self.Tracks[Outbound.Destination].available = self.Tracks[Outbound.Destination].available - 1
        ##print(self.Tracks[Outbound.Destination].available)
