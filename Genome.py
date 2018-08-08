"""
Implements genomes for NEAT.

Each genome is both a member of its generation, and a method by which to define a feed-forward neural network.
Genomes are made up of connection genes and node genes, and define a neural network made up of connections and nodes.
They take a list of numerical inputs, and return a list of numerical outputs when evaluated.
"""

import Nodes
import Connections
import Settings

import random
import copy
import numpy

class genome:
    def __init__(self, sensorCount, outputCount, species, activationFunction = 'ReLU'):
        #First SC genes are the senor nodes, e.g. 0-6 are Sensors
        #Next node is the bias, e.g. 7 is Bias
        #Final OC genes are the output nodes, e.g. 8-10 are Outputs 
        self.nodeGenes = [Nodes.node(str(x), 'simp', float(x > sensorCount)) for x in range(sensorCount + outputCount + 1)] #Sets up the sensor, bias, and output nodes, which output only the values given to them
        self.nodeGenes[sensorCount].inputs = [1] #This just takes care of the bias node, so that it outputs something
        
        #This just assigns the nodes a location in a picture, if you want to go draw them on the screen
        for i in range(sensorCount + 1):
            self.nodeGenes[i].loc = [Settings.IOBufferSpace, (1/(sensorCount + 1)) * (i + 0.5)]
        for o in range(outputCount):
            self.nodeGenes[sensorCount + 1 + o].loc = [1 - Settings.IOBufferSpace, (1/(outputCount)) * (o + 0.5)]
            
        self.connectionGenes = [] #The genome's connection genes
        self.SC = sensorCount #Number of sensors it should have
        self.OC = outputCount #Number of outputs it should have
        self.SP = species #What species the genome belongs to
        self.FI = 0 #The fitness of the genome
        self.AF = activationFunction #What activation function the intermediary nodes will be using
        self.nodeDict = {} #This is just a thing for when it comes time to evaluate the genome
        self.champion = False #Keeping track of which genomes are champions
        
    #Adds a new connection to the genome
    def addConnection(self, A, Z, weight, innovation):
        self.connectionGenes.append(Connections.connection(A, Z, weight, True, innovation))
        
    #Adds a new, random connection to the genome, making sure that the connection only goes in the feed-forward direction
    def newRandomConnection(self, innovation):
        nodeCount = len(self.nodeGenes)
        c = False
        A = random.choice(list(range(self.SC+1)) + list(range(self.SC + self.OC + 1, nodeCount)))
        while not(c):
            Z = random.choice(range(self.SC + 1, nodeCount))
            c = self.nodeGenes[Z].p > self.nodeGenes[A].p
        self.addConnection(A, Z, 2 * Settings.newValueMagnitude * (random.random() - 0.5), innovation)
        
    #Performs a weight mutation on each connection in the genome
    def mutateConnections(self):
        for x in self.connectionGenes:
            x.mutate()
        
    #Picks a random connection in the genome, splits it, and puts a new node in the middle. This node will be evaluated
    #between the nodes on either end of the original connection
    def newRandomNode(self, innovation):
        if len(self.connectionGenes) > 0:
            c = random.choice(range(len(self.connectionGenes)))
            priority = ((self.nodeGenes[int(self.connectionGenes[c].A)].p + self.nodeGenes[int(self.connectionGenes[c].Z)].p) / 2) + (random.random() / 10000)
            name = str(len(self.nodeGenes))
            location = list(((numpy.array(self.nodeGenes[int(self.connectionGenes[c].A)].loc) + numpy.array(self.nodeGenes[int(self.connectionGenes[c].Z)].loc)) / 2) + (numpy.array([random.random() - 0.5, random.random() - 0.5])/5))
            newNode = Nodes.node(name, self.AF, priority, location)
            self.nodeGenes.append(newNode)
            self.connectionGenes = self.connectionGenes + self.connectionGenes[c].split(newNode, innovation)
        else:
            print("Womp womp")
    
    #Preps the genome for having the evaluation run on it, by preparing the order in which nodes need to be evaluated
    #and which connections should be after evaluating a particular node
    def prepareEvaluation(self):
        self.nodeDict = {i.name:i.p for i in self.nodeGenes}
        self.connectionOrder = [[] for i in self.nodeGenes]
        for i in self.connectionGenes:
            self.connectionOrder[int(i.A)].append(i)
            
    #Takes a list of numerical inputs, and gives the genome's list of numerical ouputs.
    def evaluate(self, inp):
        #Cleans out each non-bias node's inputs
        for i in range(len(self.nodeGenes)):
            if i != self.SC:
                self.nodeGenes[i].inputs = []
        #Loads the numerical inputs into the sensor nodes
        for i in range(len(inp)):
            self.nodeGenes[i].inputs = [inp[i]]
        #Prepares the queue of nodes to fire
        dictCopy = copy.deepcopy(self.nodeDict)
        for j in range(len(self.nodeGenes)):
            currNode = min(dictCopy, key=dictCopy.get) #Picks the first node in the queue
            del dictCopy[currNode] #Deletes it from the queue
            for k in self.connectionOrder[int(currNode)]:
                k.inputValue = self.nodeGenes[int(currNode)].output() #Loads its output into each connection that comes from it
                self.nodeGenes[int(k.Z)].inputs.append(k.output()) #Loads the outputs of those connections into their destination nodes inputs
        return([l.output() for l in self.nodeGenes[self.SC + 1: self.SC + self.OC + 1]]) #Returns the outputs of the output nodes
                
            