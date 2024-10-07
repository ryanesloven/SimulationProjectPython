import queue
class OutboundTrack:
        def __init__(self, ID):
            self.TrackNumber = 0
            self.available = 65
            self.TrackCapacity = 65
            self.TrackID = ID
            self.Cars = []

        """
        def addRailcars(self, Outbound):
            for i in range(len(Outbound.storedCars)):
                if (self.available > 0):
                    self.storedCars.append(Outbound.storedCars[i])
                    self.available =- 1
        """
        