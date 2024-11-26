class DataTracker:

    def __init__(self):
        self.FunctionDataStorage = "FunctionDataStore.txt"
        self.OperationDataStorage = "OperationDataStore.txt"
        self.Function = open(self.FunctionDataStorage, "a")
        self.Operation = open(self.OperationDataStorage, "a")
        self.Operation.truncate(0)
        self.Function.truncate(0)
        self.TotalCars = 0
        self.TotalTime = 0

    def operationTime(self,carsProcessed):
        self.Operation.write("Cars Processed: "+ str(carsProcessed) +"\n")
        self.TotalCars = self.TotalCars + carsProcessed
    def functionTime(self,duration):
        self.Function.write("Classification Time: "+str(duration)+" Milliseconds\n")
        self.TotalTime = self.TotalTime + duration
    def operationFinal(self):
        self.Operation.write("Total Cars Processed: "+ str(self.TotalCars) +"\n")
    def functionFinal(self):
        self.Function.write("Total Classification Time: "+str(self.TotalTime)+" Milliseconds\n")
    def get_carFinal(self):
        return self.TotalCars
    def get_timeFinal(self):
        return self.TotalTime
