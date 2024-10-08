This repository contain code for a simulation that simulates the operations within a Railyard.

Introduction:

In North America roughly 100,000 freight cars are loaded, the average freight train carrying 65 cars with only 37 being loaded [1]. These trains travel at an average speed of 22.4 mph when considering terminal operations and delays [1]. This speed being so low compared to the faster speed of road-based shipping [2]. As such development of models to improve the efficiency of rail-based delivery and transportation is of great importance. 
Research done by [2] has determined that a great deal of waiting time for railcars occurs in shunting yards. As such research into optimizing shunting yards is the best avenue for which to increase the efficiency of rail-based delivery systems. 
This study focuses on the development of a simulation to allow for better understanding of the shunting yard and to allow for testing of new ideas and structures to increase efficiency. 

Initial Literature Review:
Identification of the components and overall structure of a shunting yard is needed to allow for the accurate construction of the simulation. Information about the structure was from work done by John H. Armstrong [1], with more simplified models of railyards being taken from numerous studies [2], [3], [4] which research solutions to optimize railyard operations.

The basic structure of railyard can be divided into three main sections, the receiving yard, the classification yard, and the departure yard [3]. The receiving yard takes inbound trains from the main line, the trains then wait to be sorted into classification tracks. The classification yard is where railcars are divided into classification tracks, each track corresponding to a destination or other factor that rails cars sorted onto that track have. The departure yard is sometimes combined with the classification yard, it is where classified ‘cuts’ (sections of railcars that have been sorted) are connected to an engine and rejoin the main track [3]. 
Several other minor sections are present, those being tracks towards other sub-yards which do the same operations as an individual railyard they are used to balance the load of incoming trains among several smaller yard, and repair yards where railcars are taken off the track to be repaired as needed [1]. The tracks to other sub-yards are typically arranged such that they block standard operations in the sub-yard until complete, should this ‘blocking’ occur at a bad time it can greatly decrease the efficiency of the railyard. While the time spent on ‘blocking’ operations is notable, it is not the main time sink in railyards [4]. 
The main time sink is the classification yard, it is regarded as a bottleneck [4] with research into making shunting yards more efficient being focused on making classification more efficient. Several factors make this difficult including the number of classification tracks available, the length of the classification tracks, blocking operations, incomplete-cuts, misclassified railcars, and maintenance being some of the major factors that need to be considered. 
Previous research has focused on algorithms to find solutions and best practices for classification. The issue of classifying trains can is called the “Train Makeup Problem” or “Train-to-Yard Assignment Problem”, the problem concerns how trains should cut from inbound tracks and pushed to classification tracks [2]. The focus is on maximizing the value of cars that are classified and minimizing the cost of costly blocking actions. Previous research approaches this problem by assigning a value to each railcar using some criteria such as due date [3], priority [2], and flow cost [4]. Each railcar in the inbound yard has a value associated with it, by choosing the railcars that get classified based on criteria the value of cars classified can be maximized.

The issue is that not just any railcar in the inbound yard can be classified. Railcars in the inbound yard are in a line, even if a railcar with an incredibly high value is present if it is behind several other railcars then it can’t be accessed. This complicates making the most optimal classification choices, as occasionally several un-optimal railcars must be classified before an optimal railcar can be classified. 
Several approaches have been made to deal with this issue, Otto and Pesch use a Heuristic Greedy algorithm that chooses the best local option [4]. Jaehn et al. use a Branch and Bound algorithm which suffers from high performance costs as the number of inbound and classification tracks increases [3]. Boysen et al. use a Dynamic Programming approach that uses recursion to find the ideal choice, like the method used by it suffers from long processing times [2]. Notable is that the usage of Beam Search (BS) had in the worst case a 31 second processing time several factors lower than other methods [3], as such usage of a BS algorithm for finding the optimal solution is something to be considered for on-site simulation.
Boysen et al. developed three basic approaches to classifying inbound, TMP-Split, TMP-Full, and TMP-Last railcars (TMP referring to “Train Makeup Problem”). 
•	TMP-Split: An approach that has only a specific section of railcars to be classified, with other railcars having to wait until the next section is chosen.
•	TMP-Full: An approach that only allows full trains to be classified, that the entire set of railcars from an inbound train are sorted together.
•	TMP-Last: An approach where only full trains are to be classified, with the exception of the last train which can be cut as needed to satisfy the constraints of the classification yard. 

This approach to identifying the general strategies for approaching classification is something that previous studies didn’t consider, more focus being on a TMP-Split policy with railcars being treated as individual units rather than as being associated with an inbound train. Boysen et al. limit their testing to a Dynamic Programming approach, while other studies limit themselves to what could be considered a TMP-Split policy using Greedy [4] and Bound Branch [3] approaches. This simulation and research aims to branch the gap in research of different programming paradigms and classification approaches. By using the classification approaches defined by Boysen et al. and combining them with programming paradigms used in other studies this study will allow for a better overview of how solutions to railyard inefficiency compare to one another. 
The goal of this simulation is to compare the performance of Dynamic Programming and Greedy algorithms for classifying railcars. Efforts to implement a Branch-and-Bound algorithm have proven infeasible due to time constraints. The current implementation functions for Greedy TMP-Split simulations with further functionalities to be developed.

Citations:

1.	J. H. Armstrong, The Railroad What It is, What It Does, 4th ed. Omaha, NE: Simmons-Boardman Books, Inc., 1998
2.	Boysen, N., Emde, S. & Fliedner, M. The basic train makeup problem in shunting yards. OR Spectrum 38, 207–233 (2016). https://doi.org/10.1007/s00291-015-0412-0
3.	Jaehn, F., Rieder, J. & Wiehl, A. Minimizing delays in a shunting yard. OR Spectrum 37, 407–429 (2015). https://doi.org/10.1007/s00291-015-0391-1
4.	Otto, A., Pesch, E. The train-to-yard assignment problem. OR Spectrum 41, 549–580 (2019). https://doi.org/10.1007/s00291-019-00547-y

 UML Diagram:![UMLDiagramUpdate](https://github.com/user-attachments/assets/7d02e8e8-73f0-4ebe-a325-a7e00e42c98d)

 
Overview:
The simulation is controlled from the Driver class, the class determines how the simulation is run within the start() method. The class also has the getSettings() method which is used to determine which policy and simulation will be used for classifying the railcars. 
The first class to be called in Start() is the Simulation class. The class will be passed Settings data which is used to determine which Policy and which Simulation type will be used for this iteration. 
The second class to be called in Start() is the DataTracker class. This class takes care of data recording during the simulation.
The third class to be called is the InboundYard class which receives data on inbound trains and railcars it will hold. The InboundYard class is concerned with Railcars which are their own class. It also works with the InboundTrackClass.
The fourth class to be called is the OutboudnYard class which receives data on outbound trains and railcars it will hold. The OutboundYard class is concerned with Railcars which are their own class. It also works with the OutboundTrackClass.
The fifth class to be called is the Simulation class which is used to access the algorithm and policy that will classify railcars.
The sixth class to be called is the Arrival class which is used to have trains enter the inbound yard at random intervals.
Driver Class:
This class is the controller for the entire simulation. It contains six and three functions.
Variables:
•	inboundTrackNum:
o	Data Type: Integer
o	Purpose: To indicate the number of tracks for the InboundYard
•	outboundTrackNum:
o	Data Type: Integer
o	Purpose: To indicate the number of tracks for the OutboundYard
•	Policy:
o	Data Type: Integer
o	Purpose: To indicate which policy is to be used for the simulation
•	Algorithm:
o	Data Type: Integer
o	Purpose: To indicate which algorithm will be used for the simulation
•	SimulationTimer:
o	Data Type: Integer
o	Purpose: To track the maximum time that can elapse for the simulation
•	currentTime:
o	Data Type: Integer
o	Purpose: To increment the timer towards the SimulationTimer
Functions:
•	GetSettings:
o	ReturnType: None
o	Purpose: To gain information on how the simulation will be run.
•	Start:
o	Return Type: None
o	Purpose: To run the simulation, it is in-charge of how the simulation progresses. 
DataTracker:
This class is responsible for tracking and recording data. It has four variables and two functions.
Variables:
•	FunctionDataStorage:
o	Data Type: String
o	Purpose: To hold the path to the document that holds data on functions performed in the simulation.
•	OperationDataStorage:
o	Data Type: String
o	Purpose: To hold the path to the document that holds data on operations performed in the simulation.
•	Function:
o	Data Type: ofstream
o	Purpose: To write to the function data storage.
•	Operation:
o	Data Type: ofstream
o	Purpose: To write to the operation data storage.
Functions:
•	functionTime:
o	Data Type: ofstream
o	Purpose: To write provided data to the function data storage.
•	operationTime:
o	Data Type: ofstream
o	Purpose: To write provided data to the operation data storage.
Simulation:
This class is responsible for storing and accessing the policy and algorithm that will be used for a run of the simulation. The function contains four variables and three functions.
Variables:
•	Policy:
o	Data Type: Integer
o	Purpose: To determine which policy is to be used for this run of the simulation.
•	Algorithm:
o	Data Type: Integer
o	Purpose: To indicate the algorithm used for simulation
•	Inbound:
o	Data Type: InboundYard Object
o	Purpose: To use InboundYard object for simulation
•	Outbound:
o	Data Type: OutboundYard Object
o	Purpose: To use OutboundYard object for simulation
•	Tracker:
o	Data Type: DataTracker Object
o	Purpose: To use the DataTracker object for data recording
Functions:
•	callGreedy:
o	Return Type: Integer
o	Purpose: Performs simulation using the Greedy algorithm.
•	callDynamic:
o	Return Type: Integer
o	Purpose: Performs simulation using Dynamic Programming algorithm.
•	sendOutbound:
o	Return Type: Integer
o	Purpose: Empties outbound tracks in the Outbound yard that are at capacity.
InboundTrack:
This class describes railcars on the inbound track. The class has four variables and three functions.
Variables:
•	TrackID: 
o	Data Type: Integer
o	Purpose: To identify the specific InboundTrack an object is.
•	TrackCapacity:
o	Data Type: Integer
o	Purpose: To indicate how full the track is, that is how many railcars it is currently holding.
•	Length:
o	Data Type: Integer
o	Purpose: To indicate the length of the first train in the track.
•	outboundTrackNum:
o	Data Type: Integer
o	Purpose: To indicate the number of tracks in the OutboundYard
Functions:
•	addRailcars:
o	Return Type: None
o	Purpose: To add a railcar to the Inbound Track
•	removeRailcar:
o	Return Type: None
o	Purpose: To remove a railcar from the Inbound Track
•	Initialize:
o	Return Type: None
o	Purpose: Intitializes InboundTrack object.
InboundYard:
This class represents the classification tracks within a railyard. It has four variables and five functions. 
Variables:
•	TrackNumber:
o	Data Type: Integer
o	Purpose: To identify the classification track
•	TrackStatus:
o	Data Type: Integer
o	Purpose: To indicate the number of railcars currently on the track.
•	TrackCapacity:
o	Data Type: Integer
o	Purpose: To indicate the maximum number of railcars the track can hold.
•	Destination:
o	Data Type: Stirng
o	Purpose: To identify the destination to which all railcars on the track are headed to. 
Functions:
•	GetTrackNumber:
o	Return Type: Integer
o	Purpose: To return the track number and identify the track.
•	GetTrackStatus:
o	Return Type: Integer
o	Purpose: To indicate how many railcars the track has on it.
•	UpdateStatus:
o	Return Type: None
o	Purpose: To change data regarding the number of railcars on the track.
•	GetDestination:
o	Return Type: String
o	Purpose: To indicate the destination of all railcars on the track.
•	RequestEngine:
o	Return Type: None
o	Purpose: To have all railcars on the track moved to their shared destination. Clears all railcars from the track.
Railcar:
This class is the blueprint for the railcar objects that are used throughout the simulation. The class has five variables and one function.
Variables:
•	Destination:
o	Data Type: Integer
o	Purpose: To identify the track that the railcar is wants to go to.
•	RailcarID:
o	Data Type: Integer
o	Purpose: A unique ID to identify the railcar.
•	TrainID:
o	Data Type: Integer
o	Purpose: To indicate what train the railcar is associated with.
•	TrackNumber:
o	Data Type: Integer
o	Purpose: To indicate what track the railcar is on. 
•	Priority: 
o	Data Type: Integer
o	Purpose: To indicate the value of the railcar being sorted compared to not being sorted.
Functions: 
•	Initialize:
o	Return Type: None
o	Purpose: Initialize a railcar object.
Train:
This class is the blueprint for the train objects that are used throughout the simulation. The class has five variables and one function.
Variables:
•	Destinations:
o	Data Type: Integer List
o	Purpose: To identify the track that the railcars wants to go to.
•	TrainID:
o	Data Type: Integer
o	Purpose: A unique ID to identify the train.
•	TotalPriority:
o	Data Type: Integer
o	Purpose: To indicate the total value of a train.
•	Length:
o	Data Type: Integer
o	Purpose: To indicate the length of the train. 
•	Cars: 
o	Data Type: Railcar List
o	Purpose: To hold railcars that are in the train.
Functions: 
•	Initialize:
o	Return Type: None
o	Purpose: Initialize a train object.
OutboundTrack:
This class is the blueprint for the OutboudnTrack objects that are used throughout the simulation. The class has five variables and one function.
Variables:
•	TrackNumber:
o	Data Type: Integer 
o	Purpose: To identify the track
•	Available:
o	Data Type: Integer
o	Purpose: To track the number of cars on each track.
•	TrackID:
o	Data Type: Integer
o	Purpose: To indicate each track.
•	Cars:
o	Data Type: Railcar List
o	Purpose: To store railcars on the track
•	TrackCapacity: 
o	Data Type: Integer
o	Purpose: To indicate the maximum amount of railcars a track can hold.
Functions: 
•	Initialize:
o	Return Type: None
o	Purpose: Initialize an OutboundTrack object.
OutboundYard:
This class is the blueprint for the OutboudnYard objects that are used throughout the simulation. The class has two variables and three function.
Variables:
•	NumberTracks:
o	Data Type: Integer 
o	Purpose: Used to indicate the number of tracks in the yard.
•	Tracks:
o	Data Type: OutboundTrack List
o	Purpose: Used to hold tracks associated with the yard.
Functions: 
•	Initialize:
o	Return Type: None
o	Purpose: Initialize an OutboundYard object.
•	addTrain:
o	Return Type: Integer
o	Purpose: Add train to tracks depending on destination.
•	AddRailcar:
o	Return Type: Integer
o	Purpose: Add railcar to track depending on destination.
Arrival:
This class is the blueprint for the Arrival objects that are used throughout the simulation. The class has four variables and two function.
Variables:
•	lastTime:
o	Data Type: Integer 
o	Purpose: To identify the last time that a train has arrived
•	Inbound:
o	Data Type: InboundYard Object
o	Purpose: To allow access to InboundYard to add train to.
•	MaxTime:
o	Data Type: Integer
o	Purpose: To indicate the maximum time the simulation can go for.
•	Tracker:
o	Data Type: DataTracker Object
o	Purpose: To access DataTracker functions for data recording.
Functions: 
•	Initialize:
o	Return Type: None
o	Purpose: Initialize an OutboundTrack object.
•	Forecast:
o	Return Type: Integer
o	Purpose: To randomly add a train to the inbound yard.




