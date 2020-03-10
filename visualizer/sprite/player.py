'''
Create a 'Player' object that stores all of the necessary physics-y info
(and rendering crap). Also the animation state, eventually?
'''
import numpy as np

from .sprite import Sprite
from ursina.input_handler import held_keys

#TODO get crushed
class Player(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, z_index=4)

    def update(self, dt):
        self.process_input(dt)
        super().update(dt)

    def process_input(self,dt):
        """Key player keyboard (WASD) input, store in player.input."""
        self.input = dt * np.array([held_keys['d'] - held_keys['a'], held_keys['w'] - held_keys['s']])

    def update_position_velocity(self, dt):
        super().update_position_velocity(dt)
        self.velocity[0] += self.input[0] * self.horizontal_speed * dt # slow down due to friction

        if self.can_jump and self.input[1] > 0:
            self.jump()
        else:
            if self.input[1] > 0:
                self.input[1] = 0

    def jump(self):
        self.velocity[1] += self.jump_speed
        self.can_jump = False