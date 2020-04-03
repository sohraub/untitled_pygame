import json
import random
import pygame as pg

from game_elements.classes.warrior import warrior_config
from game_elements.character import Character
from game_elements.element_config_values import INVENTORY_LIMIT


class Player(Character):
    def __init__(self, name='default', x=0, y=0, hp=None, mp=None, attributes=None, status=None, inventory=None,
                 equipment=None, condition=None, active_abilities=None, passive_abilities=None, level=1,
                 experience=None, profession="warrior"):
        """
        The Player object which will be the user's avatar as they navigate the world, an extension of the Character
        class. For explanations on the parameters used in the super() init, refer to the Character module.

        :param inventory: A list containing all of the Item objects in the players inventory.
        :param equipment: A dict showing the user's equipped items.
        :param condition: A dict storing the levels of the player's tiredness, hunger, and thirst. The info for each
                          condition is stored as a 3-tuple of ['current', 'max', 'counter'], where 'current' decrements
                          by one every time 'counter' reaches a certain threshold, based on the players attributes.
        :param active_abilities: A list of all of the player's Ability objects which are active.
        :param passive_abilities: A list of all of the player's Ability objects which are passive.
        :param level: The Player's level.
        :param experience: The Player's current experience progress, stored as ['current', 'max']
        :param profession: The Player's profession (i.e. the class, job, etc.).

        As well as the above, the following attributes are also set and used throughout the Player's methods:
        :fatigued: A flag used when the player has become too tired. While True, all of the players attributes are
                   lowered.
        :movement_mapping: A dict that maps keyboard inputs to the proper methods and parameters which will be called.
        :off_rating: An int which represents the player's total offensive rating after factoring equipment bonuses
        :def_rating: Similar to off_rating, but for defense.
        """
        super().__init__(name, x, y, hp, mp, attributes, status)
        self.inventory = inventory if inventory is not None else list()
        self.equipment = equipment if equipment is not None else {
            'head': None,
            'body': None,
            'weapon': None,
            'hands': None,
            'feet': None
        }
        self.off_rating = 0
        self.def_rating = 0
        self.update_off_def_ratings()
        self.conditions = condition if condition is not None else {
            'tired': [10, 10, 0],
            'hungry': [10, 10, 0],
            'thirsty': [10, 10, 0]
        }
        self.active_abilities = active_abilities if active_abilities is not None else list()
        self.passive_abilities = passive_abilities if passive_abilities is not None else list()
        self.level = level
        self.experience = experience if experience is not None else [0, 20]
        self.profession = profession
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
        """Method which returns a dict representation of the Player object."""
        return {
            'name': self.name,
            'hp': self.hp,
            'mp': self.mp,
            'attributes': self.attributes,
            'status': {
                'buffs': [buff.to_dict() for buff in self.status['buffs']],
                'debuffs': [debuff.to_dict() for debuff in self.status['debuffs']]
            },
            'inventory': self.inventory,
            'equipment': self.equipment,
            'conditions': self.conditions,
            'active_abilities': [ability.to_dict() for ability in self.active_abilities],
            'passive_abilities': [ability.to_dict() for ability in self.passive_abilities],
            'level': self.level,
            'profession': self.profession,
            'experience': self.experience
        }

    def perform_movement(self, input):
        """Method that calls the appropriate method from self.movement_mapping based on the keyboard input."""
        func = self.movement_mapping[input][0]
        param = self.movement_mapping[input][1]
        if param is None:
            new_x, new_y = func()
        else:
            new_x, new_y = func(param)
        return new_x, new_y

    def wait(self):
        """Method called when the Player is to wait a turn."""
        # TODO: Placeholder for now, might want to add extra functionality later
        pass

    def pick_up_item(self, item, from_chest=False):
        """Method to pick up items that the Player encounters on the board."""
        console_text = list()
        if len(self.inventory) == INVENTORY_LIMIT:
            console_text.append(f'Inventory is full. You cannot pick up {item.name}.')
            return console_text, False
        else:
            self.inventory.append(item)
            if from_chest:
                console_text.append(f'The chest creaks open, and you find {item.name}')
            else:
                console_text.append(f'You picked up {item.name}.')
            return console_text, True

    def conditions_worsen(self):
        """
        Method to be called at the end of every turn, which will increment the condition-worsening counter, and
        de-increment the current condition value if the counter reaches the threshold.
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
        """Method which applies the appropriate condition penalties when its thresholds are met."""
        if condition == 'thirsty' or condition == 'hungry':
            self.hp[0] = max(self.hp[0] - 1, 0)
        if condition == 'hungry':
            self.mp[0] = max(self.mp[0] - 1, 0)
        if condition == 'tired' and self.fatigued == 0:
            self.fatigued = 1
            for attribute in self.attributes:
                self.attributes[attribute] -= 2

    def check_fatigue(self):
        """
        Method which checks if the player is fatigued or not, and adjusts their stats accordingly.
        :return: render_necessary, a boolean signifying if attributes have been changed, and thus need to re-render.
        """
        render_necessary = False
        if self.conditions['tired'][0] >= 0.15*self.conditions['tired'][1] and self.fatigued == 1:
            self.fatigued = 0
            for attribute in self.attributes:
                self.attributes[attribute] += 2
            render_necessary = True
        return render_necessary

    def consume_item(self, index):
        """Method to consume the item located at 'index' in the player's inventory."""
        item = self.inventory.pop(index)
        for effect, parameter_dict in zip(item.effects, item.parameters):
            parameter_dict['target'] = self
            effect(**parameter_dict)
        console_text = f'You {item.verb} the {item.name}.'
        return console_text

    def equip_item(self, index):
        """Equips item at 'index', replacing it in the inventory with what was previously equipped, if any."""
        item = self.inventory[index]
        equip_slot = item.slot
        if self.equipment[equip_slot]:  # If the player already has an item equipped in this slot, swap them
            temp = self.equipment[equip_slot]
            self.equipment[equip_slot] = item
            self.inventory[index] = temp
        else:  # The player has nothing currently equipped at that slot
            self.equipment[equip_slot] = self.inventory.pop(index)
        console_text = f'You equip the {item.name}.'
        self.update_off_def_ratings()
        return console_text

    def basic_attack(self, target):
        console_text = ['']
        base_damage = max(self.attributes['str'] - target.attributes['end'], 1) + self.off_rating
        base_accuracy = 70 + 5 * (self.attributes['dex'] - target.attributes['dex'])
        crit_chance = max(self.attributes['dex'] + (self.attributes['wis'] - target.attributes['wis']), 0)
        if random.randint(0, 100) <= crit_chance:
            base_damage = 2 * base_damage
            console_text[0] += 'Critical hit! '
        elif random.randint(0, 100) >= base_accuracy:
            base_damage = 0
            console_text[0] += 'Miss! '
        # The join in the formatting below just replaces _ with spaces and gets rid of the uuid in enemy names.
        # e.g. large_rat_81d1db04-dfba-4680-a179-dba9d91cdc23 -> large rat
        console_text[0] += f"You dealt {base_damage} damage to {target.display_name}. "
        target.hp[0] = max(target.hp[0] - base_damage, 0)
        if target.hp[0] == 0:
            from game_elements.enemy import death_phrases
            console_text.append(random.choice(death_phrases))
        return console_text

    def update_off_def_ratings(self):
        """Sets the players offensive and defensive rating based on current equipment, if any."""
        if self.equipment.get('weapon', None):
            self.off_rating = self.equipment['weapon'].off_rating
        else:
            self.off_rating = 0
        self.def_rating = 0
        for slot in ['head', 'body', 'hands', 'feet']:
            if self.equipment.get(slot, None):
                self.def_rating += self.equipment[slot].def_rating

    def use_ability(self, ability, target):
        """
        Player uses an ability on the target. If target is None, then the ability misses.
        """
        console_text = list()
        if target is not None:
            console_text.append(ability.function(self=self, target=target, skill_level=ability.level))
            if target.hp[0] == 0:
                from game_elements.enemy import death_phrases
                console_text.append(random.choice(death_phrases))
        else:
            console_text.append([f'You used {ability.name}, but there was no target!'])
        return console_text

    def gain_experience(self, enemy_hp):
        """Called when an enemy is killed, the player gains experience based on the killed enemy's max HP"""
        exp_gained = int(0.5 * enemy_hp[1])
        if self.experience[0] + exp_gained >= self.experience[1]:
            # This is where the player levels up
            self.level_up(exp_gained)
        else:
            self.experience[0] += exp_gained

    def level_up(self, exp_gained):
        """
        Increases the player level, calls necessary rendering functions for increasing attributes and skill levels,
        and also sets new experience level based on the overflow of the previous level's experience bar.
        """
        exp_overflow = exp_gained - (self.experience[1] - self.experience[0])
        self.level += 1
        self.experience[1] = level_to_max_exp_map[self.level]
        if exp_overflow > self.experience[1]:  # Handles the case when a player can gain multiple levels from one kill.
            self.level_up(exp_overflow)
            return
        self.experience[0] = exp_overflow


def load_player_from_json(filename):
    """Function to initialize a Player object from a JSON file."""
    with open(filename, 'r') as f:
        character = json.load(f)

    profession = character.get('profession', 'warrior')
    attributes = None
    active_abilities = None
    passive_abilities = None
    if character.get('attributes', None) is None:
        attributes = profession_string_map[profession]['starting_attributes']
    if character.get('active_abilities', None) is None:
        active_abilities = profession_string_map[profession]['active_abilities']
    if character.get('passive_abilities', None) is None:
        passive_abilities = profession_string_map[profession]['passive_abilities']

    player = Player(
        name=character.get('name', 'TEST'),
        hp=character.get('hp', None),
        mp=character.get('mp', None),
        profession=profession,
        active_abilities=active_abilities,
        passive_abilities=passive_abilities,
        attributes=attributes,
        status=character.get('status', None),
        condition=character.get('condition', None),
        inventory=character.get('inventory', None),
        equipment=character.get('equipment', None),
        experience=character.get('experience', None)
    )

    return player


level_to_max_exp_map = {
    1: 20,
    2: 50,
    3: 100,
    4: 200,
    5: 500
}

profession_string_map = {
    "warrior": warrior_config
}
