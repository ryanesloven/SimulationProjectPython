import time
import DataTracker
import InboundYard
import OutboundYard
import Train
import Railcar
import Arrival
import InboundTrack
import OutboundTrack

class Simulation:
    def __init__(self, Policy, Algorithm, inbound, outbound, Tracker):
        self.policy = Policy
        self.algorithm = Algorithm
        self.Inbound = inbound
        self.Outbound = outbound
        self.Tracker = Tracker

    def sendOutbound(self):
        ##clears out queue if it reaches its size limit
        tracksClear = 0
        for i in range(len(self.Outbound.Tracks)):
            if (len(self.Outbound.Tracks[i].Cars) == 65):
                self.Outbound.Tracks[i] = []
                tracksClear = tracksClear + 1
        return tracksClear

    def callGreedy(self):
        max = 0 ##used to compare priority values of railcars and trains.
        carsSorted = 0
        operationTime = 0
        self.policy = 3
        index = 0 ##used to prevent unnecessary looping for queue/vector operations.
        skip = []
        begin = time.perf_counter() / 1000
        if (self.policy == 1):
            ValidExists = True; ##used to indicate if the max is valid or not
            InvalidChoices = 0
            findSkipIndex = 0
            ##install checks for available space of tracks.
            
            #finds max priority of top value in queues.
            while (ValidExists):
                for i in range(len(self.Inbound.Tracks)):
                    ##ensures that the maximum, VALID railcar will be chosen
                    if(self.Inbound.Tracks[i].storedTrains[0].TotalPriority > max and i not in skip):
                        max = self.Inbound.Tracks[i].storedTrains[0].TotalPriority
                        index = i
                    if (i in skip): ##used to determine if no valid choices exist
                        InvalidChoices = InvalidChoices + 1
                    ##exits if no entire train can be classified validly.
                    if (InvalidChoices >= len(self.Inbound.Tracks)):
                        ##end sorting
                        ValidExists = False

                ##move railcar to outbound yard and remove from inbound yard, also updates local data
                for i in range(len(self.Inbound.Tracks[index].storedTrains[0].Cars)):
                    if(self.Outbound.Tracks[self.Inbound.Tracks[index].storedTrains[0].Cars[i].Destination].available - 1 < 1):
                        skip.push_back(index)
                
                ##checks that a valid option is chosen
                if(index in skip):
                    ##updates inbound and outbound yard with the train being removed and added respectively
                    self.Outbound.addTrain(self.Inbound.Tracks[index].storedTrains[0])
                    self.Inbound.removeRailcars(self.Inbound.Tracks[index].storedTrains[0])
                    carsSorted += self.Inbound.Tracks[index].storedTrains[0].Cars.size()
                    self.Tracker.operationtime(self.Inbound.Tracks[index].storedTrains[0].Cars.size())
            
        elif(self.policy == 2):
            max = 0
            index = 0
            ValidExists = True ##used to indicate if the max is valid or not
            InvalidChoices = 0
            ##install checks for available space of tracks.
            
            #finds max priority of top value in queues.
            while (ValidExists):
                for i in range(len(self.Inbound.Tracks)):
                    ##ensures that the maximum, VALID railcar will be chosen
                    if(self.Inbound.Tracks[i].storedTrains[0].TotalPriority > max and i not in skip):
                        max = self.Inbound.Tracks[i].storedTrains[0].TotalPriority
                        index = i
                    
                    if (i in skip): ##used to determine if no valid choices exist
                        InvalidChoices = InvalidChoices + 1
                    
                    if (InvalidChoices >= len(self.Inbound.Tracks)):
                        print("No Valid Choices")
                        max = 0
                        for i in range(len(self.Inbound.Tracks)):
                            ##ensures that the maximum, railcar will be chosen
                            if(self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority > max):
                                max = self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority
                                index = i
                        
                        for i in range(len(self.Inbound.Tracks[index].Cars)):
                            if(self.Outbound.Tracks[self.Inbound.Tracks[index].storedTrains[0].Cars[i].Destination].Available - 1 > -1):
                                self.Outbound.addRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[i])
                                self.Inbound.removeRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[i])
                                self.Tracker.operationtime(1)
                                carsSorted += 1
                            else:
                                ValidExists = False
                                return; ##gracefully exit after classification done to best of ability
            
                ##move railcar to outbound yard and remove from inbound yard, also updates local data
                for i in range(len(self.Inbound.Tracks[index].storedTrains[0].Cars)):
                    if(self.Outbound.Tracks[self.Inbound.Tracks[index].storedTrains[0].Cars[i].Destination].Available - 1 < 1):
                        skip.push_back(index)

                ##checks that a valid option is chosen
                if(index in skip):
                    ##updates inbound and outbound yard with the train being removed and added respectively
                    self.Outbound.addTrain(self.Inbound.Tracks[index].storedTrains[0])
                    self.Inbound.removeRailcars(self.Inbound.Tracks[index].storedTrains[0])
                    carsSorted += len(self.Inbound.Tracks[index].storedTrains.front.Cars)
                    self.Tracker.operationtime(len(self.Inbound.Tracks[index].storedTrains.front.Cars))
 
        elif (self.policy == 3):
            max = -1
            index = -1
            invalid = []
            while(True):
                max = -1
                invalid = []
                for i in range(len(self.Inbound.Tracks)):
                    if(len(self.Inbound.Tracks[i].storedTrains) == 0 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0):
                        invalid.append(i)
                    if (i not in invalid and self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority > max ):
                        max = self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority
                        index = i
                ##print(invalid)
                ##print(index)
                
                ##print(len(self.Inbound.Tracks[index].storedTrains))
                if(len(self.Inbound.Tracks[index].storedTrains) == 0):
                    break
                destination = self.Inbound.Tracks[index].storedTrains[0].Cars[0].Destination
                if (self.Outbound.Tracks[destination].available < 1):
                    invalid.append(index)
                    operationTime = operationTime + (self.sendOutbound() * 65)
                self.Outbound.addRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                self.Inbound.Tracks[index].removeRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                carsSorted = carsSorted + 1











            """
            max = -1
            index = 0
            ValidExists = True ##used to indicate if the max is valid or not

            ##install checks for available space of tracks.
            ##finds max priority of top value in queues.
            while (ValidExists):
                max = 0
                skip = []
                index = 0
                for i in range(len(self.Inbound.Tracks)):
                    ##ensures that the maximum, VALID railcar will be chosen
                    if(len(self.Inbound.Tracks[i].storedTrains)==0 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0):
                        skip.append(i)
                        break
                    if(self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority > max and i not in skip):
                        ##print(self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority)
                        max = self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority
                        index = i

                ##stops classifying if no railcars can be sorted validly
                if(len(skip) >= len(self.Inbound.Tracks)):
                    ValidExists = False
                    break
                if(len(self.Inbound.Tracks[i].storedTrains)==0):
                    break
                if(index in skip):
                    break
                ##checks if railcar can be placed in the outbound track.
                if(self.Outbound.Tracks[self.Inbound.Tracks[index].storedTrains[0].Cars[0].Destination].available - 1 < 1):
                    self.sendOutbound()
                else:
                    temp = self.Inbound.Tracks[index].storedTrains[0].Cars[0]
                    self.Outbound.addRailcar(temp)
                    self.Inbound.Tracks[index].removeRailcar(temp)
                    ##time.sleep(5)
                    ##print(carsSorted)
                    carsSorted = carsSorted + 1
        """

        stop = time.perf_counter() / 1000
        duration = stop-begin
        if(carsSorted>0):
            self.Tracker.functionTime(duration)
            self.Tracker.operationTime(carsSorted)
        return (carsSorted+operationTime) * 10