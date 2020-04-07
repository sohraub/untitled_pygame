import random

from game_elements.character import Character
from utility_functions import manhattan_distance

# Phrases that are added to the console text when an enemy is killed. TODO: See if there is a better place for this
death_phrases = ['It lets out one final, desperate breath before it ceases movement. ',
                 'You watch it slowly bleed out to death. ']

class Enemy(Character):
    def __init__(self, name, x=0, y=0, hp=None, mp=None, attributes=None, status=None, attack_range=1, role='attacker',
                 aggro_range=3, retreat_probability=0.3, flavour_text=None, display_name=''):
        """
        Initializes the Enemy class, extended from Character. For explanations on parameters initialized through
        super(), refer to the Character module.
        :param attack_range: Denotes from how far an enemy can attack.
        :param role: A string which will determine the behaviour of the enemy AI. Not yet implemented.
        :param aggro_range: Denotes from how far an enemy will notice a player and start acting.
        :param retreat_probability: Probability of an enemy retreating when it is weak.
        :param flavour_text: Some flavour text that is displayed in the focus window.
        :param display_name: Enemy's name in a nicer format for display purposes.

        In addition to the above, the following attributes are also initialized for each Enemy:
        :aggro: Boolean which determines if the player has ever entered the the Enemy's aggro range. If ever set to
                True, will never go back to False even if the player moves away, under normal circumstances.
        """
        super().__init__(name, x, y, hp, mp, attributes, status)
        self.aggro_range = aggro_range
        self.aggro = False
        self.attack_range = attack_range
        self.retreat_probability = retreat_probability
        self.role = role
        self.flavour_text = flavour_text if flavour_text is not None else 'This is placeholder flavour text'
        self.display_name = display_name

    def check_aggro(self, player):
        """Method to check if the player is within the enemy's aggro range."""
        if manhattan_distance((self.x, self.y), (player.x, player.y)) <= self.aggro_range:
            self.in_combat = True
            player.in_combat = True
            return True
        return False

    def move_towards_target(self, target_coords, open_tiles):
        """Method to move the enemy towards a target coordinate."""
        # First check if it can close the x-distance, and then the y-distance
        if target_coords[0] != self.x:
            next_step_x = int((target_coords[0] - self.x) / abs(target_coords[0] - self.x))  # This will be either 1 or -1
            if (self.x + next_step_x, self.y) in set(open_tiles):
                return self.x + next_step_x, self.y
        if target_coords[1] != self.y:
            next_step_y = int((target_coords[1] - self.y) / abs(target_coords[1] - self.y))  # This will be either 1 or -1
            if (self.x, self.y + next_step_y) in set(open_tiles):
                return self.x, self.y + next_step_y
        # If no valid movement, return None
        return None, None

    def basic_attack(self, target):
        console_text = ['']
        # Enemies will always deal at least 1 damage, unless they miss
        base_damage = max(self.attributes['str'] - target.attributes['end'] - target.def_rating, 1)
        base_accuracy = 70 + 5 * (self.attributes['dex'] - target.attributes['dex'])
        crit_chance = self.attributes['dex'] + (self.attributes['wis'] - target.attributes['wis'])

        if random.randint(0, 100) <= crit_chance:
            base_damage = 2 * base_damage
            console_text[0] += 'Critical hit! '
        elif random.randint(0, 100) >= base_accuracy:
            base_damage = 0
            console_text[0] += 'Miss! '

        console_text[0] += f"The {self.display_name} attacks you for {base_damage} damage. "
        target.hp[0] = max(target.hp[0] - base_damage, 0)
        return console_text


def generate_new_enemy(x, y, tier):
    import copy
    from uuid import uuid4
    from element_lists import enemy_list
    tier_mapping = {
        1: enemy_list.tier_1
    }
    new_enemy = copy.deepcopy(random.choice(tier_mapping[tier]))
    new_enemy.name = new_enemy.name + '_{}'.format(str(uuid4()))
    new_enemy.x = x
    new_enemy.y = y
    return new_enemy


