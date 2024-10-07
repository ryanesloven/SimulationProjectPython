import random as rand
class Railcar:
    RailcarID = 0
    def __init__(self, Dest, Prio, TrackNum, ID):
        self.status = True
        self.Destination = Dest
        self.Priority = Prio
        self.RepairMiles = rand.randrange(1150)
        self.TrainID = ID
        self.RailcarID = Railcar.RailcarID
        Railcar.RailcarID =+ 1
        self.TrackNumber = TrackNum