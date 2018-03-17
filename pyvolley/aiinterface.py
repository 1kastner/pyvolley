import random

from cocos.layer import Layer

from . import constants

class AIInterface(Layer):
    def __init__(self, game):
        super(AIInterface, self).__init__()
        self.ball = game.ball.body
        self.player1 = game.players[0]
        self.player2 = game.players[1]
        self.input_key_press = game.on_key_press
        self.input_key_release = game.on_key_release
        self.player2config = game.config_player[1]
        self.schedule_interval(self.update, 1./constants.FPS)
        self.key_pressed = {'left': False, 'right': False, 'jump': False}
    
    def update(self, dt):
        #print("P1", self.player1.body.position)
        #print("P2", self.player2.body.position)
        #print("ball", self.ball.position)
        action = random.choice(['left', 'right', 'jump'])
        if random.random() < 0.1:
            if self.key_pressed[action]:
                print("start action", action)
                self.input_key_press(self.player2config[action], None)
            else:
                print("stop action", action)
                self.input_key_release(self.player2config[action], None)
            self.key_pressed[action] = not self.key_pressed[action]
