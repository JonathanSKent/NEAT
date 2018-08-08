"""
Implements generations for NEAT.

A generation is made up of a bunch of genomes. Each generation has its genomes evaluated,
and then produces the next generation based on that.
"""

import Genome
import Fitness
import Settings

import copy
import random
import math

class generation:
    #This generates a fresh, new generation networks. In the first generation, they each start with one random connection
    def __init__(self, inputCount, outputCount, population, activationFunction, innovation = 0):
        self.genomes = [Genome.genome(inputCount, outputCount, "SPEC0", activationFunction) for q in range(population)] #The list of genomes in the generation
        self.holotypes = [copy.deepcopy(self.genomes[0])] #This keeps track of the holotypes, against which species are defined
        self.IC = inputCount #The number of inputs the fitness function gives each network
        self.OC = outputCount #The number of outputs the fitness function expects from each network
        self.AF = activationFunction #The activation function the non-sensor, non-output nodes use
        self.IN = innovation #Tracks the innovation number between and within generations
        self.fitnessSum = 0 #The current diluted softmax sum of the fitnesses of the different genomes
        self.parentsA = [] #The orderded list of fathers* to be used to create the next generation
        self.parentsB = [] #The orderded list of mothers*
                           #*The genomes are asexual, and breed father-i with mother-i
        self.children = [] #OUR FUTURE. Well, the NEAT algorithm's future
        self.counts = [] #The population of each active species
        self.PO = population #The population of the entire generation
        
        #If this is the first generation, gives each genome a random connection, tracking the global innocation number with them
        if innovation == 0:
            for x in self.genomes:
                x.newRandomConnection(self.IN)
                self.IN += 1
            
    #Goes through the entire generation, figures out which holotype they're closest to, and assigns them the species of the
    #holotype. If they're too far away from any holotypes, they become the holotype of a new species
    def assignSpecies(self, threshold = Settings.speciationThreshold):
        for A in self.genomes:
            dists = [compatibilityDistance(A, B) for B in self.holotypes]
            if min(dists) > threshold:
                A.SP = "SPEC" + str(len(self.holotypes))
                self.holotypes.append(copy.deepcopy(A))
            else:
                for i in range(len(dists)):
                    if dists[i] == min(dists):
                        A.SP = "SPEC" + str(i)
                    
    #Counts up the population of every species in the current generation
    def countSpecies(self):
        self.counts = [sum([x.SP == h.SP for x in self.genomes]) for h in self.holotypes]
                  
    #Goes through every member of the generation, runs the fitness function against them, assigns the appropriate
    #species population based handicap, and keeps track of the diluted softmax fitness sum, which will be used to
    #assign baby-havin' responsibilities
    def assignFitnesses(self, window):
        for x in self.genomes:
            x.prepareEvaluation()
            x.FI = Fitness.fitness(x, window) / self.counts[int(x.SP[4:])]
            self.fitnessSum += math.e ** (Settings.softmaxDilution * x.FI)
    
    #After having assigned the fitnesses of the genomes in a generation, creates the ordered lists of parents
    #that will be used to generate the children that will go on to appear in the next generation. For each
    #genome, it assigns it a number of children to have based on the diluted softmax of its fitness. Then, it creates
    #a list of parents, in which a genome will appear as many times as kids it should have. This list is grouped based
    #on species, and then copied to the list of fathers. Then, each species grouping is shuffled, and assigned to the list
    #of mothers. This ensures that breeding will only occur within species, as father-i and mother-i will come from
    #the same intra-specific group. Sometimes, a genome will breed with itself, which just creates a copy of itself.
    #This function also leaves some slack in order to copy over the champions of the previous generation
    def assignParents(self, pool = Settings.championPoolSize):
        activeSpecies = []
        groupedParents = []
        numKids = [int(((math.e ** (Settings.softmaxDilution * x.FI))/self.fitnessSum) * (self.PO - pool)) for x in self.genomes]
        for q in range(self.PO - sum(numKids) - pool):
            numKids[random.choice(range(len(numKids)))] += 1
        parents = sum([numKids[x] * [x] for x in range(len(numKids))], [])
        for x in parents:
            if not(self.genomes[x].SP in activeSpecies):
                activeSpecies.append(self.genomes[x].SP)
        for y in activeSpecies:
            groupedParents.append([])
            for z in parents:
                if self.genomes[z].SP == y:
                    groupedParents[-1].append(z)
        self.parentsA = sum(groupedParents, [])
        for l in groupedParents:
            random.shuffle(l)
        self.parentsB = sum(groupedParents, [])
            
    #Zipper-breeds the two lists of parents from assignParents(), mutates them, and then adds in the champions from this generation
    #so that random mutation doesn't accidentally snuff out greatness
    def generateChildren(self, pool = Settings.championPoolSize):
        self.children = [breed(self.genomes[self.parentsA[x]], self.genomes[self.parentsB[x]]) for x in range(self.PO - pool)]
        for x in self.children:
            if random.random() < Settings.weightMutationProbability:
                x.mutateConnections()
            if random.random() < Settings.newNodeMutationProbability:
                x.newRandomNode(self.IN)
                self.IN += 2
            if random.random() < Settings.newConnectionMutationProbability:
                x.newRandomConnection(self.IN)
                self.IN += 1
        champions = []
        for c in self.genomes:
            if c.FI == max([k.FI * (not(k.champion)) for k in self.genomes]) and (len(champions) < pool):
                champions.append(copy.deepcopy(c))
                c.champion = True
        self.children += champions
       
#For two genomes, returns how distantly they are related, for purposes of speciation and breeding
def compatibilityDistance(A, B, c = Settings.compatibilityDistanceMultipliers):
    innovationNumbersA = [x.I for x in A.connectionGenes]
    innovationNumbersB = [x.I for x in B.connectionGenes]
    d = sum([not(x in innovationNumbersA) for x in innovationNumbersB]) + sum([not(x in innovationNumbersB) for x in innovationNumbersA])
    w = 0
    e = 0
    for j in A.connectionGenes:
        for k in B.connectionGenes:
            if j.I == k.I:
                w += abs(j.W - k.W)
                e += 1
    d /= 1 + (Settings.geneSizeNormalizationFactor * (max([len(innovationNumbersA), len(innovationNumbersB)])))
    if e:
        w /= e
    return((c[0] * d) + (c[1] * w))
    
#Given two genomes, produces a baby. Connection genes in the parents that share a historical origin flip a coin to determine
#which copy goes into the baby, and all genes that don't share an origin with one from the other parent automatically go into the baby.
#Genes that were not expressed in a parent have a chance to be expressed in the child
def breed(parentA, parentB):
    invNums = []
    newConnGenes = []
    for x in (parentA.connectionGenes + parentB.connectionGenes):
        if not(x.I in invNums):
            invNums.append(x.I)
            newConnGenes.append(copy.deepcopy(x))
            newConnGenes[-1].E = newConnGenes[-1].E or (random.random() < Settings.geneEnableProbability)
        else:
            for y in newConnGenes:
                if y.I == x.I:
                    y.W = random.choice([y.W, x.W])
        if len(parentA.nodeGenes) >= len(parentB.nodeGenes):
            newNodeGenes = copy.deepcopy(parentA.nodeGenes)
        else:
            newNodeGenes = copy.deepcopy(parentB.nodeGenes)    
    newGenome = Genome.genome(parentA.SC, parentA.OC, '', parentA.AF)
    newGenome.nodeGenes = newNodeGenes
    newGenome.connectionGenes = newConnGenes
    return(newGenome)
    