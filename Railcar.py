import random as rand
class Railcar:
    RailcarID = 0
    def __init__(self, Dest, Prio, TrackNum, ID):
        self.Destination = Dest
        self.Priority = Prio
        self.TrainID = ID
        self.RailcarID = Railcar.RailcarID
        Railcar.RailcarID = Railcar.RailcarID + 1
        self.TrackNumber = TrackNum