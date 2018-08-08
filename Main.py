"""
Runs NEAT.

Yep, it runs NEAT.
"""

import Generation
import Fitness

import copy
import graphics

def run(inputCount, outputCount, population, activationFunction, generationCount, windowSize = Fitness.windowSize):
    win = graphics.GraphWin("NEAT", width = windowSize[0], height = windowSize[1]) #The window that NEAT will draw the evaluation of each genome in
    currGeneration = Generation.generation(inputCount, outputCount, population, activationFunction) #Creates a first generation
    t = 0 #Keeps track of which generation we're on
    while t < generationCount:
        print("Beginning Generation " + str(t))
        currGeneration.assignSpecies() #Assigns a species to each member of the current generation
        currGeneration.countSpecies() #Counts up how many members are in each species
        activeSpecies = sum([x > 0 for x in currGeneration.counts])
        print("Active Species: " + str(activeSpecies)) #Prints how many species still have living members
        print("Extinct Species: " + str(len(currGeneration.counts) - activeSpecies)) #Prints how many species have lived and then gone extinct
        currGeneration.assignFitnesses(win) #Assigns each genome in the generation its fitness
        print("Max Fitness: " + str(max([x.FI * currGeneration.counts[int(x.SP[4:])] for x in currGeneration.genomes]))) #Prints the raw fitness of the best genome
        print("Average Fitness: " + str((sum([x.FI * currGeneration.counts[int(x.SP[4:])] for x in currGeneration.genomes])) / population)) #Prints the average raw fitness of the generation
        currGeneration.assignParents() #Creates the list of parents
        currGeneration.generateChildren() #Creates the genomes in the next generation
        nextGeneration = Generation.generation(inputCount, outputCount, population, activationFunction, currGeneration.IN) #Creates the next generation
        print("Current Innovation Number: " + str(currGeneration.IN)) #Prints the current innovation number
        nextGeneration.genomes = copy.deepcopy(currGeneration.children) #Loads the genomes into the new generation
        nextGeneration.holotypes = copy.deepcopy(currGeneration.holotypes) #Preserves the collection of holotypes
        currGeneration = copy.deepcopy(nextGeneration) #Loads the next generation
        del nextGeneration #Deletes the placeholder generation
        t += 1 #Moves the generation counter
        print(20 * "~*")
    win.close()