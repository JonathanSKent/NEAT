"""
Implements connections for NEAT.

The purpose of a connection is to pass the activation level of one node to the input
of another node. The assembly of nodes and connections together forms a neural network.
Every connection has an associated weight, for which a high value represents a greater
effect of one neuron upon another, and low value, a lesser effect.
"""

import random
import Settings

class connection:
    def __init__(self, takesFrom, givesTo, weight, enabled, innovation):
        self.A = takesFrom #This represents which node in the network the connection takes its input from
        self.Z = givesTo #Which node it gives the output to
        self.W = weight #What it multiplies the output by, before handing it off to the destination node
        self.E = enabled #Whether or not a given connection is supposed to be expressed
        self.I = innovation #Tracks the mutation that this connection was created in, in the evolutionary
                            #record, allowing connections with the same ancestry to be matched up
        
    inputValue = 0 #A local variable, that tracks the activation of the takes-from node for output
    
    #Returns the output of the connection, which is equal to the weight times the input, but 0 if not enabled
    def output(self):
        return(self.inputValue * self.W * self.E)
        
    #When called by a particular connection, splits the connection into two new connections, to allow the insertion
    #of a new node into the structure of the network
    def split(self, newNode, innovation):
        connectionAlpha = connection(self.A, newNode.name, 1, True, innovation) #The new connection going from the old take-from
                                                                                #node to the new, intermediary node
        connectionBeta = connection(newNode.name, self.Z, self.W, True, innovation + 1) #The new connection going from the intermediary
                                                                                        #node to the destination node
        self.E = False #Stops the connection from being expressed, to allow the new node to do its work
        return([connectionAlpha, connectionBeta])
        
    #Mutates the weight of the connection, either with a small perturbation, or a completely new value
    def mutate(self, perturbationMagnitude = Settings.perturbationMagnitude, newValueMagnitude = Settings.newValueMagnitude, perturbationGenerationThreshold = Settings.perturbationGenerationThreshold):
        if random.random() < perturbationGenerationThreshold:
            self.W += 2 * perturbationMagnitude * (random.random() - 0.5)
        else:
            self.W = 2 * newValueMagnitude * (random.random() - 0.5)
