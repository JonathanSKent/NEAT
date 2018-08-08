"""
Implements node functionality for NEAT.
"""

from ActivationFunctions import f

class node:
    def __init__(self, nodeName, activationFunction, priority, location = [0, 0]):
        self.name = nodeName #The name of the node
        self.af = f[activationFunction] #The function that the node uses to generate its output
        self.p = priority #The priority that determines in what order nodes fire. 0 = fires first, 1 = fires last
        self.loc = location #The in-picture location of the node
            
    inputs = [] #The list of inputs that the node currently takes
    
    #Outputs what the node should output, by applying the activation function to the list of inputs
    def output(self):
        return(self.af(self.inputs))