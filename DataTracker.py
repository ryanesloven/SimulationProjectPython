class DataTracker:

    def __init__(self):
        self.FunctionDataStorage = "FunctionDataStore.txt"
        self.OperationDataStorage = "OperationDataStore.txt"
        self.Function = open(self.FunctionDataStorage, "a")
        self.Operation = open(self.OperationDataStorage, "a")

    def operationTime(self,carsProcessed):
        self.Operation.write("Cars Processed: "+ str(carsProcessed) +"\n")
    def functionTime(self,duration):
        self.Function.write("Classification Time: "+str(duration)+" milliseconds\n")