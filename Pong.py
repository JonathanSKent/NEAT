"""
Implements single-player endurance Pong
"""

import random

start = {
        'x':0.5,
        'y':0.5,
        'vx':0.03,
        'vy':0.01,
        'py':0.4,
        'ph':0.2
        }

class game:
    def __init__(self):
        self.ballX = start['x']
        self.ballY = start['y']
        self.ballVX = start['vx']
        self.ballVY = start['vy']
        self.paddleY = start['py']
        self.paddleH = start['ph']
        self.gamesLeft = 4
        self.bounces = 0
        
    def updateBall(self):
        if self.ballY + self.ballVY > 1:
            self.ballY = 2 - (self.ballY + self.ballVY)
            self.ballVY *= -1
        elif self.ballY + self.ballVY < 0:
            self.ballY = - (self.ballY + self.ballVY)
            self.ballVY *= -1
        else:
            self.ballY += self.ballVY
        if self.ballX + self.ballVX > 1:
            if self.paddleY < self.ballY < self.paddleY + self.paddleH:
                self.ballX = 2 - (self.ballX + self.ballVX)
                self.ballVX *= -1
                self.ballVX += (random.random() - 0.5) * 0.03
                self.ballVY += (random.random() - 0.5) * 0.06
                self.bounces += 1
            else:
                self.gamesLeft -= 1
                self.ballX = start['x']
                self.ballY = start['y']
                self.ballVX = start['vx']
                self.ballVY = start['vy']
                self.paddleY = start['py']
                self.paddleH = start['ph']
        elif self.ballX + self.ballVX < 0:
            self.ballX = - (self.ballX + self.ballVX)
            self.ballVX *= -1
        else:
            self.ballX += self.ballVX
        if abs(self.ballVX) < 0.03:
            self.ballVX = 0.03 * self.ballVX/abs(self.ballVX)
            
    def updatePaddle(self, instructions):
        if instructions[0] > 0:
            if instructions[1] > 0:
                self.paddleY += 0.04
            else:
                self.paddleY -= 0.04
        if self.paddleY < 0:
            self.paddleY = 0
        elif self.paddleY + self.paddleH > 1:
            self.paddleY = 1 - self.paddleH
            
    def getState(self):
        return([self.ballX, self.ballY, self.ballVX, self.ballVY, self.paddleY])