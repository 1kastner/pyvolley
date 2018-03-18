import random

from cocos.layer import Layer

from . import constants

__author__ = '1kastner'

class AIInterface(Layer):
    """
    This wraps the game as good as possible so that we do not worry about this 
    when creating the great AIs :)
    """
    def __init__(self, game):
        super(AIInterface, self).__init__()
        self.bot_1 = Bot(
            game.ball.body,
            Controller(
                lambda : game.on_key_press(game.config_player[0]['left'], None),
                lambda : game.on_key_press(game.config_player[0]['right'], None),
                lambda : game.on_key_press(game.config_player[0]['jump'], None),
                lambda : game.on_key_release(game.config_player[0]['left'], None),
                lambda : game.on_key_release(game.config_player[0]['right'], None),
                lambda : game.on_key_release(game.config_player[0]['jump'], None)                   
            )
        )
        self.bot_2 = Bot(
            game.ball.body,
            Controller(
                lambda : game.on_key_press(game.config_player[1]['left'], None),
                lambda : game.on_key_press(game.config_player[1]['right'], None),
                lambda : game.on_key_press(game.config_player[1]['jump'], None),
                lambda : game.on_key_release(game.config_player[1]['left'], None),
                lambda : game.on_key_release(game.config_player[1]['right'], None),
                lambda : game.on_key_release(game.config_player[1]['jump'], None)              
            )
        )
        self.game = game
        
        self.schedule_interval(self.update, 1./constants.FPS)

    def update(self, dt):
        pos_1 = self.game.players[0].body.position
        pos_2 = self.game.players[1].body.position
        self.bot_1.update(pos_1, pos_2)
        self.bot_2.update(pos_2, pos_1)


class Controller:
    """
    Stores the controller information for each bot and returns which action was performed
    """
    def __init__(self, left_start, right_start, jump_start, left_end, right_end, jump_end):
        self.left_start = lambda : left_start() or "left"
        self.right_start = lambda : right_start() or "right"
        self.jump_start = lambda : jump_start() or "jump"
        self.left_end = lambda : left_end() or "left"
        self.right_end = lambda : right_end() or "right"
        self.jump_end = lambda : jump_end() or "jump"


class Bot:
    """
    Here we can put the AI stuff. By now it is quite stupid because it only performs random action
    but by the provided knowledge it actually *could* do much smarter stuff. That is left for the next
    commit.
    """
    def __init__(self, ball, controller):
        self.ball = ball
        self.controller = controller
        self.key_pressed = {'left':False, 'right':False, 'jump':False}
        
    def update(self, pos_me, pos_other):
        print(self.ball.position)
        print(pos_me)
        print(pos_other)
        action = random.choice([
            self.controller.left_start if self.key_pressed['left'] else self.controller.left_end,
            self.controller.right_start if self.key_pressed['right'] else self.controller.right_end,
            self.controller.jump_start if self.key_pressed['jump'] else self.controller.jump_end,
        ])
        if random.random() < 0.1:
            action_name = action()
            self.key_pressed[action_name] = not self.key_pressed[action_name]
            print(action_name, self.key_pressed)
