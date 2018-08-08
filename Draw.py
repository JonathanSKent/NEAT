"""
Produces a set of objects to draw based on a genome
"""

import Settings

import graphics
import math

#Takes a genome, and renders it into a set of graphics.py shapes for drawing into a window
def genomeToObjects(genome, size):
    circles = []
    lines = []
    for x in genome.nodeGenes:
        newCircle = graphics.Circle(graphics.Point(x.loc[0] * size, x.loc[1] * size), size * Settings.nodeSizeRatio)
        newCircle.setFill(graphics.color_rgb(int(255/(1+(math.e**-x.output()))), int(255/(1+(math.e**-x.output()))), int(255/(1+(math.e**-x.output())))))
        circles.append(newCircle)
    for y in genome.connectionGenes:
        A = genome.nodeGenes[int(y.A)].loc
        Z = genome.nodeGenes[int(y.Z)].loc
        newLine = graphics.Line(graphics.Point(A[0] * size, A[1] * size), graphics.Point(Z[0] * size, Z[1] * size))
        if y.E:
            if y.W > 0:
                newLine.setFill('green')
            else:
                newLine.setFill('red')
        else:
            newLine.setFill('black')
        newLine.setWidth(abs(y.W) * (size * Settings.connectionSizeRatio))
        lines.append(newLine)
    return(lines + circles)
    
def draw(window, obj):
    for x in obj:
        x.draw(window)