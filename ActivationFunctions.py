"""
Implements the activation functions for nodes in NEAT.

What activation functions do is govern the behavior of nodes in a neural net.
A node, for a given set of inputs, puts their sum through an activation function,
and returns the result as the node's own level of activation, to be passed via connections
to further nodes.
"""

import Settings
import math

#ReLU, or Rectified Linear Unit. For an input X, if X > 0, it returns X, and 0 if X <= 0
def ReLU(i):
    return(max([0, sum(i)]))

#Leaky ReLU is basically ReLU, but instead of returning 0 for X < 0, returns X / c, for
#some constant c
def LeakyReLU(i, lf = Settings.leakFactor):
    return(max([sum(i)/lf, sum(i)]))

#ELU, or Exponential Linear Unit. Returns X if X > 0, but e^x - 1 if X < 0
def ELU(i, a = Settings.ELUMultiplier):
    return(((sum(i) > 0) * sum(i)) + ((sum(i) <= 0) * (math.e**sum(i)-1)))
    
#It's just inverse tangent. It's sigmoid * 2 - 1
def tanh(i):
    return(math.tanh(sum(i)))
    
#For a very low number, goes to 0. For a very large number, goes to 1. Sorta linear around 0
def sigmoid(i, c = Settings.sigmoidMultiplier):
    return(1/(1+(math.e**-sum(i))))

#Returns if the number is above or below 0
def binary(i):
    return(int(sum(i) > 0))
    
#Just returns the sum of inputs
def simp(i):
    return(sum(i))
    
#A dictionary, so that I can pass a string to the node-producing functions, rather than
#the activation functions themselves
f = {
     'ReLU':ReLU,
     'LeakyReLU':LeakyReLU,
     'ELU':ELU,
     'tanh':tanh,
     'sigmoid':sigmoid,
     'binary':binary,
     'simp':simp
     }