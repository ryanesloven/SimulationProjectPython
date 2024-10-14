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

    

    def DynamicGreedyRailcar(self, choices, carsSorted, operationTime, start, invalid):
        index = -1
        max = -1
        for i in range(len(choices)):
            ##print(choices[i])
            if(i not in invalid and self.Outbound.Tracks[choices[i].Destination].available > 0 and choices[i].Priority > max):
                max = choices[i].Priority
                index = i
            else:
                invalid.append(i)
        if(max == -1):
            stop = time.perf_counter() / 1000
            duration = stop - start
            operationTime = 650 * self.sendOutbound()
            if(carsSorted>0):
                print("reached")
                self.Tracker.functionTime(duration)
                self.Tracker.operationTime(carsSorted)
            return operationTime
        else:
            self.Outbound.addRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
            self.Inbound.Tracks[index].removeRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
            if(len(self.Inbound.Tracks[index].storedTrains) > 0 and len(self.Inbound.Tracks[index].storedTrains[0].Cars) > 0):
                choices[index] = self.Inbound.Tracks[index].storedTrains[0].Cars[0]
            else:
                choices[index] = -1
                invalid.append(index)
            carsSorted = carsSorted + 1
            return self.DynamicGreedyRailcar(choices, carsSorted, operationTime, start, invalid) + 10
        

    def callDynamic(self):
        max = 0 ##used to compare priority values of railcars and trains.
        carsSorted = 0
        operationTime = 0
        self.policy = 1
        begin = time.perf_counter() / 1000

        if(self.policy==1):
            invalid = []
            choices = []
            breakChecker = 0
            for i in range(len(self.Inbound.Tracks)):
                if(len(self.Inbound.Tracks[i].storedTrains) == 0 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0):
                    invalid.append(i)
                    choices.append(-1)
                    breakChecker = breakChecker + 1
                else:
                    choices.append(self.Inbound.Tracks[i].storedTrains[0].Cars[0])
            if(breakChecker == len(self.Inbound.Tracks)):
                return 0
            else:
                temp = self.DynamicGreedyRailcar(choices, 0, 0, begin, invalid)
                if(temp > 0):  
                    print(temp)
                return temp

        elif(self.policy==2):
            pass
        elif(self.policy==3):
            pass

    def callGreedy(self):
        max = 0 ##used to compare priority values of railcars and trains.
        carsSorted = 0
        operationTime = 0
        self.policy = 3
        index = 0 ##used to prevent unnecessary looping for queue/vector operations.
        skip = []
        begin = time.perf_counter() / 1000
        if (self.policy == 1): ##TMP-Full
            max = -1
            index = -1
            invalid = []
            while(True):
                max = -1
                invalid = []
                for i in range(len(self.Inbound.Tracks)):
                    if(len(self.Inbound.Tracks[i].storedTrains) == 0 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0):
                        invalid.append(i)
                    if(i not in invalid and self.Inbound.Tracks[i].storedTrains[0].TotalPriority > max ):
                        max = self.Inbound.Tracks[i].storedTrains[0].TotalPriority
                        index = i
                if(len(invalid) == len(self.Inbound.Tracks)):
                    operationTime = operationTime + (self.sendOutbound() * 65)
                    break
                ##print(invalid)
                ##print(index)
                
                ##print(len(self.Inbound.Tracks[index].storedTrains))
                if(len(self.Inbound.Tracks[index].storedTrains) == 0):
                    break

                ##destination = self.Inbound.Tracks[index].storedTrains[0].Cars[0].Destination

                for i in range(len(self.Inbound.Tracks[index].storedTrains[0].Cars)):
                    destination = self.Inbound.Tracks[index].storedTrains[0].Cars[i].Destination
                    if (self.Outbound.Tracks[destination].available < 1):
                        invalid.append(index)
                if(index in invalid):
                    self.Outbound.addRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                    self.Inbound.Tracks[index].removeRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                    carsSorted = carsSorted + len(self.Inbound.Tracks[index].storedTrains[0].Cars)

            
        elif(self.policy == 2):
            max = -1
            index = -1
            invalid = []
            while(True):
                max = -1
                invalid = []
                for i in range(len(self.Inbound.Tracks)):
                    if(len(self.Inbound.Tracks[i].storedTrains) == 0 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0):
                        invalid.append(i)
                    if(i not in invalid and self.Inbound.Tracks[i].storedTrains[0].TotalPriority > max ):
                        max = self.Inbound.Tracks[i].storedTrains[0].TotalPriority
                        index = i
                if(len(invalid) == len(self.Inbound.Tracks)):
                    max = -1
                    index = -1
                    invalid = []
                    for i in range(len(self.Inbound.Tracks)):
                        if(len(self.Inbound.Tracks[i].storedTrains) == 0 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0):
                            invalid.append(i)
                        if (i not in invalid and self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority > max ):
                            max = self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority
                            index = i
                        ##print(invalid)
                        ##print(index)
                    for i in range(len(self.Inbound.Tracks[index].storedTrains[0].Cars)):
                        ##print(len(self.Inbound.Tracks[index].storedTrains))
                        if(len(self.Inbound.Tracks[index].storedTrains.Cars) == 0):
                            break
                        destination = self.Inbound.Tracks[index].storedTrains[0].Cars[0].Destination
                        if (self.Outbound.Tracks[destination].available < 1):
                            invalid.append(index)
                            ##operationTime = operationTime + (self.sendOutbound() * 65)
                        else:
                            self.Outbound.addRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                            self.Inbound.Tracks[index].removeRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                            carsSorted = carsSorted + 1
                    break
                    ##print(invalid)
                    ##print(index)
                    ##print(len(self.Inbound.Tracks[index].storedTrains))

                    ##destination = self.Inbound.Tracks[index].storedTrains[0].Cars[0].Destination

                for i in range(len(self.Inbound.Tracks[index].storedTrains[0].Cars)):
                    destination = self.Inbound.Tracks[index].storedTrains[0].Cars[i].Destination
                    if (self.Outbound.Tracks[destination].available < 1):
                        invalid.append(index)

                self.Outbound.addRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                self.Inbound.Tracks[index].removeRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                carsSorted = carsSorted + len(self.Inbound.Tracks[index].storedTrains[0].Cars)

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
                    if (i not in invalid and self.Outbound.Tracks[self.Inbound.Tracks[i].storedTrains[0].Cars[0].Destination].available > 0 and self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority > max ):
                        max = self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority
                        index = i
                ##print(invalid)
                ##print(index)
                
                ##print(len(self.Inbound.Tracks[index].storedTrains))
                if(len(invalid)==len(self.Inbound.Tracks)):
                    break
                if (index not in invalid and len(self.Inbound.Tracks[index].storedTrains) != 0 and len(self.Inbound.Tracks[index].storedTrains[0].Cars) != 0):
                    self.Outbound.addRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                    self.Inbound.Tracks[index].removeRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                    carsSorted = carsSorted + 1
                else:
                    break

        stop = time.perf_counter() / 1000
        duration = stop-begin
        if(carsSorted>0):
            self.Tracker.functionTime(duration)
            self.Tracker.operationTime(carsSorted)
        return (carsSorted+operationTime) * 10