import json
import random
import pygame as pg

from game_elements.classes.warrior import warrior_config
from game_elements.character import Character
from game_elements.element_config_values import INVENTORY_LIMIT


class Player(Character):
    def __init__(self, name='Sohraub', x=0, y=0, status=None, inventory=None, equipment=None, condition=None, level=1,
                 experience=None, profession="warrior", skill_tree=warrior_config['skill_tree']):
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
        :param skill_tree: The skill tree of the Player's chosen profession

        As well as the above, the following attributes are also set and used throughout the Player's methods:
        :fatigued: A flag used when the player has become too tired. While True, all of the players attributes are
                   lowered.
        :movement_mapping: A dict that maps keyboard inputs to the proper methods and parameters which will be called.
        :off_rating: An int which represents the player's total offensive rating after factoring equipment bonuses
        :def_rating: Similar to off_rating, but for defense.
        """
        profession_config = profession_string_map[profession]
        super().__init__(name, x, y, profession_config['starting_attributes'], status)
        self.inventory = inventory if inventory is not None else list()
        self.equipment = equipment if equipment is not None else {
            'head': None,
            'body': None,
            'weapon': None,
            'hands': None,
            'feet': None
        }
        self.profession = profession
        self.off_rating = 0
        self.def_rating = 0
        self.update_off_def_ratings()
        self.conditions = condition if condition is not None else {
            'tired': [20, 20, 0],
            'hungry': [20, 20, 0],
            'thirsty': [20, 20, 0]
        }
        self.active_abilities = list()
        self.passive_abilities = {
            'combat': dict(),
            'on_kill': dict(),
            'board_mods': dict()
        }
        self.skill_tree = skill_tree
        self.set_abilities_from_skill_tree()
        self.level = level
        self.experience = experience if experience is not None else [19, 20]
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
            # 'passive_abilities': [ability.to_dict() for ability in self.passive_abilities],
            'passive_abilities': {},
            'level': self.level,
            'profession': self.profession,
            'skill_tree': self.skill_tree,
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
        Each condition is stored as a list of three integers, in the format
            [current_level, max_level, counter],
        where current_level starts equal to max_level, counter is incremented after every player turn, and when
        counter reaches the threshold defined in the condition_threshold dict below, then current_level is decremented
        by 1. As current_level approaches 0, players start to suffer penalties.
        """
        render_necessary = False
        condition_thresholds = {
            'thirsty': 1 * self.attributes['end'],
            'hungry': 2 * self.attributes['end'],
            'tired': 3 * self.attributes['end']
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
        if condition == 'hungry':
            self.hp[0] = max(self.hp[0] - 1, 0)
        if condition == 'thirsty':
            self.mp[0] = max(self.mp[0] - 1, 0)
        if condition == 'tired' and self.fatigued == 0:
            self.fatigued = 1
            for attribute in self.attributes:
                self.attributes[attribute] -= 2
            self.apply_attribute_changes()

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
            self.apply_attribute_changes()
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
        """
        For when the player attacks an enemy. Calculates damage based on strength, whether or not there's a crit or a
        miss based on dex, and applies the damage, if any, to the target.
        """
        console_text = ['']
        base_damage = max(self.attributes['str'] - target.attributes['end'], 1) + self.off_rating
        base_accuracy = 70 + 5 * (self.attributes['dex'] - target.attributes['dex'])
        crit_chance = max(self.attributes['dex'] + (self.attributes['wis'] - target.attributes['wis']), 0)
        base_damage, crit_chance, base_accuracy = self.apply_offensive_combat_passives(base_damage, crit_chance,
                                                                                       base_accuracy)
        if random.randint(0, 100) <= crit_chance:
            base_damage = 2 * base_damage
            console_text[0] += 'Critical hit! '
        elif random.randint(0, 100) >= base_accuracy:
            base_damage = 0
            console_text[0] += 'Miss! '
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

    def use_ability(self, ability, targets):
        """
        Player uses an ability on the target. If target is None, then the ability misses.
        """
        if targets is not None:
            ability_outcome = ability.function(self=self, targets=targets, skill_level=ability.level)
            ability.turns_left = ability.cooldown
            self.mp[0] = max(0, self.mp[0] - ability.mp_cost)
            for target in targets:
                if target.hp[0] == 0:
                    from game_elements.enemy import death_phrases
                    ability_outcome['console_text'].append(random.choice(death_phrases))
        else:
            ability_outcome = {
                'console_text': [f'You used {ability.name}, but there was no target!']
            }
        return ability_outcome

    def gain_experience(self, enemy_hp):
        """Called when an enemy is killed, the player gains experience based on the killed enemy's max HP"""
        exp_gained = int(0.5 * enemy_hp[1])
        if self.experience[0] + exp_gained >= self.experience[1]:
            # This is where the player levels up
            self.level_up(exp_gained)
            return True
        else:
            self.experience[0] += exp_gained
            return False

    def level_up(self, exp_gained):
        """
        Increases the player level, and also sets new experience level based on the overflow of the previous level's
        experience bar.
        """
        exp_overflow = exp_gained - (self.experience[1] - self.experience[0])
        self.level += 1
        self.hp[0] = self.hp[1]
        self.mp[0] = self.mp[1]
        self.experience[1] = level_to_max_exp_map.get(self.level, 100000)
        if exp_overflow > self.experience[1]:  # Handles the case when a player can gain multiple levels from one kill.
            self.level_up(exp_overflow)
            return
        self.experience[0] = exp_overflow

    def decrement_ability_cooldowns(self):
        """
        Decrements the # of turns left for each ability that is on cooldown.
        :return: Boolean flag will be true if any ability is on cooldown and had its turns left decremented, so that
                 player_panel renderer knows to refresh the ability tooltips.
        """
        refresh_necessary = False
        for ability in self.active_abilities:
            if ability.turns_left > 0:
                ability.turns_left -= 1
                refresh_necessary = True

        return refresh_necessary

    def set_abilities_from_skill_tree(self):
        """Sets the players passive and active abilities based off the values in the skill tree dict."""
        self.active_abilities = list()
        for tree_level in self.skill_tree:
            for ability_entry in self.skill_tree[tree_level]:
                ability = ability_entry['ability']
                if ability.level > 0:
                    if ability.active:  # Active and passive abilities are set differently
                        self.active_abilities.append(ability)
                    else:
                        # For passives, if the specific mod already has an entry in the passives dict, then we just
                        # add the ability's value to the existing value. Otherwise, we initialize the entry with the
                        # ability's value.
                        if self.passive_abilities[ability.mod_group].get(ability.specific_mod, False):
                            self.passive_abilities[ability.mod_group][ability.specific_mod] += ability.value
                        else:
                            self.passive_abilities[ability.mod_group][ability.specific_mod] = ability.value

    def apply_offensive_combat_passives(self, base_damage, base_crit, base_accuracy):
        """
        In the course of the basic_attack() function, applies any offensive bonuses/penalties to combat from the
        player's passive abilities, if any.
        """
        combat_passives = self.passive_abilities['combat']
        base_damage += combat_passives.get('base_dmg', 0)
        base_crit += combat_passives.get('crit_rate', 0)
        base_accuracy += combat_passives.get('base_acc', 0)
        return base_damage, base_crit, base_accuracy

    def apply_attribute_changes(self):
        """
        Function to be called every time the player's attributes change, so as to update the rest of the player's
        stats accordingly.
        """
        # Only max values for HP and MP are updated
        self.hp = [self.hp[0], self.attributes['vit'] * 2]
        self.mp = [self.mp[0], self.attributes['wis'] * 2, self.mp[2]]


level_to_max_exp_map = {
    1: 20,  # Todo: This definitely need some finetuning
    2: 40,
    3: 60,
    4: 80,
    5: 100,
    6: 800,
    7: 1000,
    8: 1300,
    9: 1500,
    10: 2000,
    11: 2500,
    12: 3000,
    13: 4000,
    14: 5000,
    15: 6000,
    16: 7000,
    17: 8000,
    18: 9000,
    19: 10000
}

profession_string_map = {
    "warrior": warrior_config
}
