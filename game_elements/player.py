import json
import pygame as pg

from game_elements.character import Character


class Player(Character):
    def __init__(self, name, x=0, y=0, attributes=None, status=None, move_speed=1, in_combat=False,
                 inventory=None, equipment=None, condition=None):
        super().__init__(name, x, y, attributes, status, move_speed, in_combat)
        self.inventory = inventory if inventory is not None else dict()
        self.equipment = equipment if equipment is not None else {
            'head': None,
            'body': None,
            'weapon': None,
            'hands': None,
            'feet': None
        }
        self.condition = condition if condition is not None else {
            'HP':{
                'current': 10,
                'max': 10
            },
            'MP':{
                'current': 10,
                'max': 10
            },
            'tired':{
                'current': 10,
                'max': 10
            },
            'hungry': {
                'current': 10,
                'max': 10
            },
            'thirsty': {
                'current': 10,
                'max': 10
            }
        }
        # Here we create a mapping for all of the basic movements,
        # so that they can all be called from one function. The keys in
        # this dict are a tuple of (method, parameter), which are called
        # together in the perform_movement() method below. Good idea? Who
        # knows, but that's what we're trying for now
        self.movement_mapping = {
            pg.K_UP: (self.move_up, None),
            pg.K_w: (self.move_up, None),
            pg.K_DOWN: (self.move_up, -1),
            pg.K_s: (self.move_up, -1),
            pg.K_RIGHT: (self.move_right, None),
            pg.K_d: (self.move_right, None),
            pg.K_LEFT: (self.move_right, -1),
            pg.K_a: (self.move_right, -1)
        }

    def perform_movement(self, input):
        func = self.movement_mapping[input][0]
        param = self.movement_mapping[input][1]
        if param is None:
            func()
        else:
            func(param)
        return self.x, self.y

def load_player_from_json(filename):
    with open(filename, 'r') as f:
        character = json.load(f)
    return Player(
        name=character.get('name', 'TEST'),
        move_speed=character.get('move_speed', None),
        attributes=character.get('attributes', None),
        status=character.get('status', None),
        condition=character.get('condition', None),
        inventory=character.get('inventory', None),
        equipment=character.get('equipement', None)
    )
