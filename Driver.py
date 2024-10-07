import InboundYard
import OutboundYard
import DataTracker
import Simulation
import Arrival
import time
class Driver:
    ##std::vector<Railcar> 
    
    def getSettings(self):
        print("Enter the number of tracks the inbound yard will have (integer).")
        self.inboundTrackNum = input()
        print("Enter the number of tracks the outbound yard will have (integer).")
        self.outboundTrackNum = input()
        print("What policy will be used for this run of the simulation?")
        print("Option 1: TMP-Full")
        print("Option 2: TMP-Last")
        print("Option 3: TMP-Split")
        print("Enter a number corresponding to desired policy (1, 2, or 3).")
        self.policy = input()
        print("What algorithm will be used for this run of the simulation?")
        print("Option 1: Dynamic Programming")
        print("Option 2: Greedy")
        print("Enter a number corresponding to desired algorithm (1 or 2).")
        self.algorithm = input()

    def start(self):
        Inbound = InboundYard.InboundYard(self.inboundTrackNum, self.outboundTrackNum) ##second value needed to allow Train to work properly
        Outbound = OutboundYard.OutboundYard(self.outboundTrackNum)
        Track = DataTracker.DataTracker()
        Sim = Simulation.Simulation(self.policy, self.algorithm, Inbound, Outbound, Track)
        Arrive = Arrival.Arrival(Inbound, Track, self.SimulationTimer)
        ##Code that setsup first trains. 
        for i in range(len(Inbound.Tracks)):
            print(str(i) + ": " + str(len(Inbound.Tracks[i].storedTrains)))
            for j in range(len(Inbound.Tracks[i].storedTrains)):
                print(str(i) +" " + str(j)+ ": " + str(len(Inbound.Tracks[i].storedTrains[j].Cars)))
        counter = 0
        while (self.currentTime < self.SimulationTimer):
            if(int(self.algorithm) == 1):
                counter = counter + Sim.callGreedy() / 10
                
                self.currentTime = self.currentTime +  counter*10
                ##print(self.currentTime)
                self.currentTime = self.currentTime + Arrive.forecast(self.currentTime)
                ##print(self.currentTime)
            elif(int(self.algorithm) == 2):
                ##currentTime =+ Sim.callDynamic()
                self.currentTime =+ Arrive.forecast(self.currentTime)
        print(counter)
        for i in range(len(Inbound.Tracks)):
            print(str(i) + ": " + str(len(Inbound.Tracks[i].storedTrains)))
            for j in range(len(Inbound.Tracks[i].storedTrains)):
                print(str(i) +" " + str(j)+ ": " + str(len(Inbound.Tracks[i].storedTrains[j].Cars)))
                ##print(str(i)+"TotalPrio: "+str(Inbound.Tracks[i].storedTrains[j].Cars[0].Priority))


    def __init__(self):
        self.inboundTrackNum = 1
        self.outboundTrackNum = 1
        self.policy = 1
        self.algorithm = 1
        self.SimulationTimer = 28800
        self.currentTime = 0

run = Driver()
run.getSettings()
run.start()