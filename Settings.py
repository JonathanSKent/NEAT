"""
Some settings
"""

leakFactor = 100 #The factor by which X is divided if X < 0 for Leaky ReLU
ELUMultiplier = 1 #The multiplier for ELU
sigmoidMultiplier = 1 #The multiplier for sigmoid

perturbationMagnitude = 0.2 #The maximimum size of a weight perturbation mutation
newValueMagnitude = 1 #The maximum size of a fresh weight mutation
perturbationGenerationThreshold = 0.9 #The probability that a weight mutation will perturb the value, rather than assigning a new one

nodeSizeRatio = 0.025 #Radius of a node relative to the size of the image in which the node is drawn
connectionSizeRatio = 0.01 #Width-per-unit-weight of a connection relative to the size of the image in which the node is drawn

defaultTimeStep = 0.001 #How long each frame of a fitness function animation is on screen

speciationThreshold = 3 #How far apart a genome has to be from every holotype before it's a new species
softmaxDilution = 0.3 #The multiplier applied to softmax to dilute it, to stop high-tier species from crushing nascent structures
championPoolSize = 3 #How many champions per generation are preserved
weightMutationProbability = 0.8 #Probability that a genome will have its weights mutates
newNodeMutationProbability = 0.03 #Probability that a genome will grow a new node
newConnectionMutationProbability = 0.05 #Probability that a genome will grow a new connection
compatibilityDistanceMultipliers = [1, 0.4] #Multipliers for the genetic distance function
geneSizeNormalizationFactor = 0.1 #Linear multiplier to account for species with more genes being harder to relate
geneEnableProbability = 0.25 #Probability that a previously disabled gene will become enabled

IOBufferSpace = 0.1 #Space between the edge of the image and the input and output nodes when drawing