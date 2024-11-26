import InboundYard
import OutboundYard
import DataTracker
import Simulation
import Arrival
import time
import numpy as np
import matplotlib.pyplot as plt
class Driver:
    ##std::vector<Railcar> 
    def getSettings(self):
        while (True):  
            print("Enter the number of tracks the inbound yard will have (integer).")
            self.inboundTrackNum = int(input())
            if isinstance(self.inboundTrackNum, int):
                break
        while(True):
            print("Enter the number of tracks the outbound yard will have (integer).")
            self.outboundTrackNum = int(input())
            if isinstance(self.outboundTrackNum, int):
                break
        while(True):
            print("What policy will be used for this run of the simulation?")
            print("Option 1: TMP-Full")
            print("Option 2: TMP-Last")
            print("Option 3: TMP-Split")
            print("Enter a number corresponding to desired policy (1, 2, or 3).")
            self.policy = int(input())
            if (self.policy==1 or self.policy==2 or self.policy==3):
                break
        while(True):
            print("What algorithm will be used for this run of the simulation?")
            print("Option 1: Greedy")
            print("Option 2: Dynamic Programming")
            print("Enter a number corresponding to desired algorithm (1 or 2).")
            self.algorithm = int(input())
            if (self.algorithm==1 or self.algorithm==2):
                break

    def start(self):
        Inbound = InboundYard.InboundYard(self.inboundTrackNum, self.outboundTrackNum) ##second value needed to allow Train to work properly
        Outbound = OutboundYard.OutboundYard(self.outboundTrackNum)
        Track = DataTracker.DataTracker()
        Sim = Simulation.Simulation(self.policy, self.algorithm, Inbound, Outbound, Track)
        Arrive = Arrival.Arrival(Inbound, Track, self.SimulationTimer)
                
        counter = 0
        lastTime = 0
        while (self.currentTime < self.SimulationTimer):
            if(int(self.algorithm) == 1):
                counter = Sim.callGreedy()
                self.currentTime = self.currentTime +  counter
                self.currentTime = self.currentTime + Arrive.forecast(self.currentTime)
                if(self.currentTime==lastTime):
                    self.currentTime = self.currentTime + 1
                lastTime = self.currentTime
            elif(int(self.algorithm) == 2):
                counter = Sim.callDynamic()
                self.currentTime = self.currentTime + counter
                self.currentTime = self.currentTime + Arrive.forecast(self.currentTime)
                if(self.currentTime==lastTime):
                    self.currentTime = self.currentTime + 1
                lastTime = self.currentTime
        ##prints out inbound yard after simulation
        self.performanceCars.append(int(Track.get_carFinal()))
        self.performanceTime.append(float(Track.get_timeFinal()))


    def __init__(self):
        self.inboundTrackNum = 1
        self.outboundTrackNum = 1
        self.policy = 1
        self.algorithm = 1
        self.SimulationTimer = 28800
        self.currentTime = 0
        self.performanceCars = []
        self.performanceTime = []

run = Driver()

run.getSettings()
for i in range(1000):
    run.start()
    run.currentTime = 0

averageTime = sum(run.performanceTime)/len(run.performanceTime)
averageCars = sum(run.performanceCars)/len(run.performanceCars)
print("Average Processing Time in Milliseconds: "+ str(averageTime))
print("Average number of cars classified: "+ str(averageCars))
