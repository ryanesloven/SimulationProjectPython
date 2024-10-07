import random as rand
import Railcar
class Train:
    def __init__(self, TrackID, ID, length, TrackNum):
            self.length = length
            self.Cars = []
            self.Destinations = [0] * int(TrackNum)
            self.TotalPriority = 0
            for i in range(length):
                carDestination = rand.randrange(int(TrackNum))
                carPrio = rand.randrange(4)
                self.Destinations[carDestination] +=1
                self.TotalPriority = self.TotalPriority + carPrio
                temp = Railcar.Railcar(carDestination, carPrio, TrackID, ID)
                self.Cars.append(temp)
            self.TrainID = ID