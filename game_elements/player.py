import json
import copy
import pygame as pg

from game_elements.character import Character


class Player(Character):
    def __init__(self, name='default', x=0, y=0, hp=None, mp=None, attributes=None, status=None, move_speed=1,
                 in_combat=False, inventory=None, equipment=None, condition=None, level=1, experience=None,
                 type="adventurer"):
        super().__init__(name, x, y, hp, mp, attributes, status, move_speed, in_combat)
        self.inventory = inventory if inventory is not None else dict()
        self.equipment = equipment if equipment is not None else {
            'head': None,
            'body': None,
            'weapon': None,
            'hands': None,
            'feet': None
        }
        self.conditions = condition if condition is not None else {
            'tired': [10, 10, 0],
            'hungry': [10, 10, 0],
            'thirsty': [10, 10, 0]
        }
        self.level = level
        self.experience = experience if experience is not None else [0, 20]
        self.type = type
        self.fatigued = 0
        # Here we create a mapping for all of the basic movements, so that they can all be called from one function.
        # The keys in this dict are a tuple of (method, parameter), which are called together in the perform_movement()
        # method below. Good idea? Who knows, but that's what we're trying for now
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

    def to_dict(self):
        dict = {
            'name': self.name,
            'hp': self.hp,
            'mp': self.mp,
            'attributes': self.attributes,
            'status': self.status,
            'inventory': self.inventory,
            'equipment': self.equipment,
            'conditions': self.conditions,
            'level': self.level,
            'type': self.type,
            'experience': self.experience
        }
        return dict

    def perform_movement(self, input):
        func = self.movement_mapping[input][0]
        param = self.movement_mapping[input][1]
        if param is None:
            func()
        else:
            func(param)
        return self.x, self.y

    def wait(self):
        # Placeholder for now, might want to add extra functionality later
        pass

    def conditions_worsen(self):
        """
        Function to be called at the end of every turn, which will increment the condition-worsening counter, and
        de-increment the current condition value if the counter reaches the threshold.
        :return: n/a
        """
        render_necessary = False
        condition_thresholds = {
            'thirsty': 5 * self.attributes['end'],
            'hungry': 7 * self.attributes['end'],
            'tired': 9 * self.attributes['end']
        }
        for condition in self.conditions:
            self.conditions[condition][2] += 1
            if self.conditions[condition][2] >= condition_thresholds[condition]:
                self.conditions[condition][0] = max(self.conditions[condition][0] - 1, 0)
                self.conditions[condition][2] = 0
            if self.conditions[condition][0] < 0.15*self.conditions[condition][1]:
                self.apply_condition_penalty(condition)
                render_necessary = True
        return render_necessary


    def apply_condition_penalty(self, condition):
        if condition == 'thirsty' or condition == 'hungry':
            self.hp[0] = max(self.hp[0] - 1, 0)
        if condition == 'hungry':
            self.mp[0] = max(self.mp[0] - 1, 0)
        if condition == 'tired' and self.fatigued == 0:
            self.fatigued = 1
            for attribute in self.attributes:
                self.attributes[attribute] -= 2


    def check_fatigue(self):
        render_necessary = False
        if self.conditions['tired'][0] >= 0.15*self.conditions['tired'][1] and self.fatigued == 1:
            self.fatigued = 0
            for attribute in self.attributes:
                self.attributes[attribute] += 2
            render_necessary = True
        return render_necessary

def load_player_from_json(filename):
    with open(filename, 'r') as f:
        character = json.load(f)
    return Player(
        name=character.get('name', 'TEST'),
        hp=character.get('hp', None),
        mp=character.get('mp', None),
        move_speed=character.get('move_speed', None),
        attributes=character.get('attributes', None),
        status=character.get('status', None),
        condition=character.get('condition', None),
        inventory=character.get('inventory', None),
        equipment=character.get('equipment', None),
        experience=character.get('experience', None)
    )


