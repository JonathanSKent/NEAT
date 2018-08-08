"""
Relates the NEAT implementation to the fitness functions.

Write this for yourself; the NEAT algorithm will attempt to maximize the output given
by the fitness function. Call genome.evaluate(inputs) on a list of inputs, and it will
return a list of outputs of the approriate length.
"""

import Draw
import Pong
import Settings

import graphics
import time

windowSize = [400, 400]

failBox = graphics.Rectangle(graphics.Point(300, 100), graphics.Point(400, 400))
failBox.setFill('red')
statBox = graphics.Rectangle(graphics.Point(100, 0), graphics.Point(400, 100))
statBox.setFill('green')

lines = [
        graphics.Line(graphics.Point(0, 100), graphics.Point(400, 100)),
        graphics.Line(graphics.Point(100, 0), graphics.Point(100, 100)),
        ]

#Takes a genome, and assigns it a fitness. Can be positive or negative
def fitness(genome, window, timeStep = Settings.defaultTimeStep):
    for x in [failBox, statBox] + lines:
        x.draw(window)
        
    game = Pong.game()
    while game.gamesLeft:
        networkSprites = Draw.genomeToObjects(genome, 100)
        ball = graphics.Circle(graphics.Point(300 * game.ballX, 100 + (300 * game.ballY)), 15)
        ball.setFill('blue')
        paddle = graphics.Rectangle(graphics.Point(300, 100 + (300 * game.paddleY)), graphics.Point(310, 100 + (300 * (game.paddleY + game.paddleH))))
        paddle.setFill('black')
        for q in networkSprites + [ball, paddle]:
            q.draw(window)
        time.sleep(timeStep)
        for q in networkSprites + [ball, paddle]:
            q.undraw()
        game.updatePaddle(genome.evaluate(game.getState()))
        game.updateBall()
        
    for x in [failBox, statBox] + lines:
        x.undraw()
    return(game.bounces)