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
        self.Sorted = 0

    def sendOutbound(self):
        ##clears out queue if it reaches its size limit
        tracksClear = 0
        for i in range(len(self.Outbound.Tracks)):
            if (self.Outbound.Tracks[i].available <= 0):
                self.Outbound.Tracks[i].available = 65
                tracksClear = tracksClear + 1
        return tracksClear

    def DynamicGreedyCombinationLast(self, choice):
        carsClassified = 0
        for i in range(self.Inbound.Tracks[choice].storedTrains[0].length):
            if(len(self.Inbound.Tracks[choice].storedTrains) < 1 or i >= len(self.Inbound.Tracks[choice].storedTrains[0].Cars)):
                break
            temp = self.Inbound.Tracks[choice].storedTrains[0].Cars[i].Destination
            if (self.Outbound.Tracks[temp].available > 0):
                self.Outbound.addRailcar(self.Inbound.Tracks[choice].storedTrains[0].Cars[0])
                self.Inbound.removeRailcar(self.Inbound.Tracks[choice].storedTrains[0].Cars[0], choice)
                carsClassified = carsClassified + 1
            else:
                break
        return carsClassified
    
    def DynamicGreedyCombination(self, choices, carsSorted, operationTime, start, invalid, availability):
        index = -1
        max = -1
        if(len(invalid)==len(choices)): ##base case
            choice = -1
            for i in range(len(choices)):
                if (choices[i] != -1 and choices[i].Cars[0].Priority > max):
                    max = choices[i].Cars[0].Priority
                    choice = i
            if (choice != -1):
                carsSorted += self.DynamicGreedyCombinationLast(choice)
            stop = time.perf_counter() *1000
            duration = stop - start
            operationTime = 650 * self.sendOutbound()
            if(carsSorted>0):
                self.Tracker.functionTime(duration)
                self.Tracker.operationTime(carsSorted)
            return operationTime
        
        for trackIndex in range(len(self.Outbound.Tracks)):##stores availability status for computation of valid trains to be classified
            availability[trackIndex] = self.Outbound.Tracks[trackIndex].available

        ##checks validity of classification options and finds the highest priority to be classified
        for i in range(len(choices)):
            if(choices[i] == -1):
                continue
            for carIndex in range(choices[i].length): ##checks for availability
                if(carIndex >= len(choices[i].Cars)):
                    break
                destination = choices[i].Cars[carIndex].Destination
                availability[destination] = availability[destination] - 1
                if (availability[destination] < 0): ##determines if outbound yard can hold the train or not.
                    invalid.append(index) 

            if(choices[i] != -1 and i not in invalid and choices[i].TotalPriority > max):
                max = choices[i].TotalPriority
                index = i

        if(max == -1):
            choice = -1
            for i in range(len(choices)):
                if (choices[i] != -1 and choices[i].Cars[0].Priority > max):
                    max = choices[i].Cars[0].Priority
                    choice = i
            if (choice != -1):
                carsSorted += self.DynamicGreedyCombinationLast(choice)
            stop = time.perf_counter() *1000
            duration = stop - start
            operationTime = 650 * self.sendOutbound()
            if(carsSorted>0):
                self.Tracker.functionTime(duration)
                self.Tracker.operationTime(carsSorted)
            return operationTime
        else:
            trainlength = len(self.Inbound.Tracks[index].storedTrains[0].Cars)
            self.Outbound.addTrain(self.Inbound.Tracks[index].storedTrains[0])
            self.Inbound.Tracks[index].removeTrain(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
            if(len(self.Inbound.Tracks[index].storedTrains) > 0 and len(self.Inbound.Tracks[index].storedTrains[0].Cars) > 0):
                choices[index] = self.Inbound.Tracks[index].storedTrains[0]
            else:
                choices[index] = -1
                invalid.append(index)
            carsSorted = carsSorted + trainlength
            return self.DynamicGreedyCombination(choices, carsSorted, operationTime, start, invalid, availability) + (10*trainlength)
        
    def DynamicGreedyRailcar(self, choices, carsSorted, operationTime, start, invalid):
        index = -1
        max = -1
        if(len(invalid)==len(choices)):
            stop = time.perf_counter() *1000
            duration = stop - start
            operationTime = 650 * self.sendOutbound()
            if(carsSorted>0):
                self.Tracker.functionTime(duration)
                self.Tracker.operationTime(carsSorted)
            return operationTime

        for i in range(len(choices)):
            if(choices[i] == -1):
                invalid.append(i)
            if(i not in invalid and self.Outbound.Tracks[choices[i].Destination].available > 0 and choices[i].Priority > max):
                max = choices[i].Priority
                index = i
        if(max == -1):
            stop = time.perf_counter() *1000
            duration = stop - start
            operationTime = 650 * self.sendOutbound()
            if(carsSorted>0):
                self.Tracker.functionTime(duration)
                self.Tracker.operationTime(carsSorted)
            return operationTime
        else:
            self.Outbound.addRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
            self.Inbound.removeRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0], index)
            if(len(self.Inbound.Tracks[index].storedTrains) > 0 and len(self.Inbound.Tracks[index].storedTrains[0].Cars) > 0):
                choices[index] = self.Inbound.Tracks[index].storedTrains[0].Cars[0]
            else:
                choices[index] = -1
                invalid.append(index)
            carsSorted = carsSorted + 1
            return self.DynamicGreedyRailcar(choices, carsSorted, operationTime, start, invalid) + 10
    
    def DynamicGreedyTrain(self, choices, carsSorted, operationTime, start, invalid, availability):
        index = -1
        max = -1
        if(len(invalid)==len(choices)): ##base case
            stop = time.perf_counter() *1000
            duration = stop - start
            operationTime = 650 * self.sendOutbound()
            if(carsSorted>0):
                self.Tracker.functionTime(duration)
                self.Tracker.operationTime(carsSorted)
            return operationTime
        
        for trackIndex in range(len(self.Outbound.Tracks)):##stores availability status for computation of valid trains to be classified
            availability[trackIndex] = self.Outbound.Tracks[trackIndex].available

        ##checks validity of classification options and finds the highest priority to be classified
        for i in range(len(choices)):
            if(choices[i] == -1):
                continue
            for carIndex in range(choices[i].length): ##checks for availability
                if(carIndex >= len(choices[i].Cars)):
                    break
                destination = choices[i].Cars[carIndex].Destination
                availability[destination] = availability[destination] - 1
                if (availability[destination] < 0): ##determines if outbound yard can hold the train or not.
                    invalid.append(index) 

            if(choices[i] != -1 and i not in invalid and choices[i].TotalPriority > max):
                max = choices[i].TotalPriority
                index = i

        if(max == -1):
            stop = time.perf_counter() *1000
            duration = stop - start
            operationTime = 650 * self.sendOutbound()
            if(carsSorted>0):
                self.Tracker.functionTime(duration)
                self.Tracker.operationTime(carsSorted)
            return operationTime
        else:
            trainlength = len(self.Inbound.Tracks[index].storedTrains[0].Cars)
            self.Outbound.addTrain(self.Inbound.Tracks[index].storedTrains[0])
            self.Inbound.Tracks[index].removeTrain(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
            if(len(self.Inbound.Tracks[index].storedTrains) > 0 and len(self.Inbound.Tracks[index].storedTrains[0].Cars) > 0):
                choices[index] = self.Inbound.Tracks[index].storedTrains[0]
            else:
                choices[index] = -1
                invalid.append(index)
            carsSorted = carsSorted + trainlength
            return self.DynamicGreedyTrain(choices, carsSorted, operationTime, start, invalid, availability) + (10*trainlength)
        

    def callDynamic(self):
        begin = time.perf_counter() *1000 

        if(self.policy==1):
            invalid = []
            choices = []
            availability = [0] * len(self.Outbound.Tracks)
            breakChecker = 0
            for i in range(len(self.Inbound.Tracks)):
                if(len(self.Inbound.Tracks[i].storedTrains) == 0 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0):
                    invalid.append(i)
                    choices.append(-1)
                    breakChecker = breakChecker + 1
                else:
                    choices.append(self.Inbound.Tracks[i].storedTrains[0])
            if(breakChecker == len(self.Inbound.Tracks)):
                return 0
            else:
                temp = self.DynamicGreedyTrain(choices, 0, 0, begin, invalid, availability)
                self.Tracker.operationFinal()
                self.Tracker.functionFinal()
                return temp

        elif(self.policy==2):
            invalid = []
            choices = []
            availability = [0] * len(self.Outbound.Tracks)
            breakChecker = 0
            for i in range(len(self.Inbound.Tracks)):
                if(len(self.Inbound.Tracks[i].storedTrains) == 0 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0):
                    invalid.append(i)
                    choices.append(-1)
                    breakChecker = breakChecker + 1
                else:
                    choices.append(self.Inbound.Tracks[i].storedTrains[0])
            if(breakChecker == len(self.Inbound.Tracks)):
                return 0
            else:
                temp = self.DynamicGreedyCombination(choices, 0, 0, begin, invalid, availability)
                self.Tracker.operationFinal()
                self.Tracker.functionFinal()
                return temp
        elif(self.policy==3):
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
                self.Tracker.operationFinal()
                self.Tracker.functionFinal()
                return temp

    def callGreedy(self):
        max = 0 ##used to compare priority values of railcars and trains.
        carsSorted = 0
        operationTime = 0
        index = 0 ##used to prevent unnecessary looping for queue/vector operations.
        begin = time.perf_counter() *1000
        if (self.policy == 1): ##TMP-Full
            index = -1
            while(True):
                max = -1
                invalid = []
                availability = [0]*len(self.Outbound.Tracks)
                for i in range(len(self.Inbound.Tracks)):
                    if(len(self.Inbound.Tracks[i].storedTrains) == 0 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0):
                        invalid.append(i)
                    for trackIndex in range(len(self.Outbound.Tracks)):##stores availability status for computation of valid trains to be classified
                        availability[trackIndex] = self.Outbound.Tracks[trackIndex].available

                    if(len(self.Inbound.Tracks[i].storedTrains)>0):
                        for carIndex in range(len(self.Inbound.Tracks[i].storedTrains[0].Cars)): ##checks for availability
                            availability[self.Inbound.Tracks[i].storedTrains[0].Cars[carIndex].Destination] -= 1
                            if (availability[self.Inbound.Tracks[i].storedTrains[0].Cars[carIndex].Destination] < 0): ##determines if outbound yard can hold the train or not.
                                invalid.append(index) 

                    if (i not in invalid and self.Inbound.Tracks[i].storedTrains[0].TotalPriority > max ):
                        max = self.Inbound.Tracks[i].storedTrains[0].TotalPriority
                        index = i

                if(len(invalid)==len(self.Inbound.Tracks) or max == -1):
                    break
                else:
                    self.Outbound.addTrain(self.Inbound.Tracks[index].storedTrains[0])
                    carsSorted = carsSorted + self.Inbound.Tracks[index].storedTrains[0].length
                    self.Inbound.Tracks[index].removeTrain(self.Inbound.Tracks[index].storedTrains[0].Cars[0])

            
        elif(self.policy == 2):
            index = -1
            while(True):
                max = -1
                invalid = []
                availability = [0]*len(self.Outbound.Tracks)
                for i in range(len(self.Inbound.Tracks)):
                    if(len(self.Inbound.Tracks[i].storedTrains) == 0 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0):
                        invalid.append(i)
                    for trackIndex in range(len(self.Outbound.Tracks)):##stores availability status for computation of valid trains to be classified
                        availability[trackIndex] = self.Outbound.Tracks[trackIndex].available

                    if(len(self.Inbound.Tracks[i].storedTrains)>0):
                        for carIndex in range(len(self.Inbound.Tracks[i].storedTrains[0].Cars)): ##checks for availability
                            availability[self.Inbound.Tracks[i].storedTrains[0].Cars[carIndex].Destination] -= 1
                            if (availability[self.Inbound.Tracks[i].storedTrains[0].Cars[carIndex].Destination] < 0): ##determines if outbound yard can hold the train or not.
                                invalid.append(index) 

                    if (i not in invalid and self.Inbound.Tracks[i].storedTrains[0].TotalPriority > max ):
                        max = self.Inbound.Tracks[i].storedTrains[0].TotalPriority
                        index = i

                if(len(invalid)==len(self.Inbound.Tracks) or max == -1):
                    max = -1
                    invalid = []
                    for choices in range(len(self.Inbound.Tracks)):
                        if(len(self.Inbound.Tracks[choices].storedTrains) == 0 or len(self.Inbound.Tracks[choices].storedTrains[0].Cars) == 0 or self.Outbound.Tracks[self.Inbound.Tracks[choices].storedTrains[0].Cars[0].Destination].available < 1):
                            invalid.append(choices)
                        if (choices not in invalid and self.Inbound.Tracks[choices].storedTrains[0].Cars[0].Priority > max ):
                            max = self.Inbound.Tracks[choices].storedTrains[0].Cars[0].Priority
                            index = i
                    if(len(invalid)==len(self.Inbound.Tracks) or len(self.Inbound.Tracks[index].storedTrains)<1):
                        break
                    else:
                        for cars in range(len(self.Inbound.Tracks[index].storedTrains[0].Cars)):
                            if(self.Outbound.Tracks[self.Inbound.Tracks[index].storedTrains[0].Cars[0].Destination].available < 1):
                                self.Outbound.addRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                                self.Inbound.removeRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0], index)
                                carsSorted = carsSorted + 1
                            else:
                                break
                    break
                else:
                    trainLength = len(self.Inbound.Tracks[index].storedTrains[0].Cars)
                    self.Outbound.addTrain(self.Inbound.Tracks[index].storedTrains[0])
                    self.Inbound.Tracks[index].removeTrain(self.Inbound.Tracks[index].storedTrains[0])
                    carsSorted = carsSorted + 1*trainLength

        elif (self.policy == 3):
            index = -1
            while(True):
                max = -1
                invalid = []
                index = -1
                for i in range(len(self.Inbound.Tracks)):
                    if(len(self.Inbound.Tracks[i].storedTrains) < 1 or len(self.Inbound.Tracks[i].storedTrains[0].Cars) == 0 or self.Outbound.Tracks[self.Inbound.Tracks[i].storedTrains[0].Cars[0].Destination].available < 1):
                        invalid.append(i)
                    if (i not in invalid and self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority > max ):
                        max = self.Inbound.Tracks[i].storedTrains[0].Cars[0].Priority
                        index = i
                if(len(invalid)==len(self.Inbound.Tracks) or max == -1 or index == -1):
                    break
                else:
                    if(index in invalid):
                        break
                    else:
                        self.Outbound.addRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0])
                        self.Inbound.removeRailcar(self.Inbound.Tracks[index].storedTrains[0].Cars[0], index)
                        carsSorted = carsSorted + 1

        operationTime = 650*self.sendOutbound()
        stop = time.perf_counter() *1000 
        duration = stop-begin
        if(carsSorted>0):
            self.Tracker.functionTime(duration)
            self.Tracker.operationTime(carsSorted)
            self.Tracker.operationFinal()
            self.Tracker.functionFinal()
        return ((carsSorted * 10)+operationTime)