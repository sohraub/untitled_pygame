import random
import copy
import math

from rendering import board_renderer
from game_elements.ability import ActiveAbility, Ability
from utility_functions import get_knockback


def heavy_strike_func(self, targets, skill_level):
    """Ability function which deals heavy damage to target and knocks them back one tile."""
    target = targets[0]
    console_text = ''
    # First determine the relative positions to find the knockback.
    new_x, new_y = get_knockback(self.x, self.y, target)
    # Now calculate the damage
    damage = int((1.5 + skill_level* 0.5) * (self.attributes['str'] - target.attributes['end'] + self.off_rating))
    crit_chance = max(self.attributes['dex'] + (self.attributes['wis'] - target.attributes['wis']), 0)
    if crit_chance > random.randint(0, 100):
        console_text += 'Critical hit! '
        damage = 2 * damage
    target.hp[0] = max(0, target.hp[0] - damage)
    console_text += f'You use Heavy Strike on the {target.display_name}, dealing {damage} damage and knocking them back.'

    ability_outcomes = {
        'console_text': [console_text],
        'movements': [
            {
                'subject': target,
                'new_position': (new_x, new_y)
            }
        ]
    }
    return ability_outcomes

heavy_strike = ActiveAbility(name='Heavy Strike', mp_cost=2,
                             description=f'Strike an enemy with all your might, dealing massive damage and knocking'
                                         f' them back', active=True,
                             targeting_function=board_renderer.highlight_adjacent_tiles,
                             function=heavy_strike_func, level=1, cooldown=5)


def trolls_blood_func(self, skill_level, **kwargs):
    """Ability function which adds a health regen buff to self."""
    from element_lists.status_list import health_regen
    trolls_blood_regen = copy.copy(health_regen)
    trolls_blood_regen.params = {'value': skill_level * int(self.attributes['wis'] / 3)}
    self.apply_status(trolls_blood_regen)
    return {
        'console_text': ["You cast Troll's Blood on yourself."]
    }

trolls_blood = ActiveAbility(name="Troll's Blood", mp_cost=3,
                             description=f'Cast a spell on yourself to gain some passive health regeneration. Healing '
                                         f'amount scales with WIS.',
                             active=True, targeting_function=board_renderer.highlight_self,
                             function=trolls_blood_func, level=1, cooldown=15)


def leap_slam_func(self, targets, skill_level):
    """Ability function which transports the player to a tile, and damages and knocks back any adjacent enemies."""
    console_text = 'You use Leap Slam'
    self_new_x, self_new_y = targets.pop(-1)
    ability_outcomes = {
        'movements': [{
            'subject': self,
            # Leap slam is an ability with self.save_target = True, so the coords of the selected tile are appended
            # to the end of the list of targets.
            'new_position': (self_new_x, self_new_y)
        }]
    }
    damage = int(0.5 * (1 + skill_level) + 0.5 * self.attributes['str'])
    for target in targets:
        target.hp[0] = max(0, target.hp[0] - damage)
        ability_outcomes['movements'].append({
            'subject': target,
            'new_position': get_knockback(self_new_x, self_new_y, target)
        })
    if len(targets) == 0:
        console_text += '.'
    else:
        console_text += f', hitting {len(targets)} target{"s" if len(targets) > 1 else ""} and knocking ' \
                        f'{"them" if len(targets) > 1 else "it"} back.'
    ability_outcomes['console_text'] = [console_text]
    return ability_outcomes

leap_slam = ActiveAbility(name='Leap Slam', mp_cost=4,
                          description='Leap towards a targeted space, damaging and knocking back all adjacent enemies',
                          active=True, targeting_function=board_renderer.highlight_radius_with_splash_target,
                          targeting_function_params={'radius': 4}, function=leap_slam_func, level=0, cooldown=10,
                          save_target=True, multi_target=[(1, 0), (0, 1), (-1, 0), (0, -1)])


SKILL_TREE = {
    "active_1": [
        {
            'name': 'Heavy Strike',
            'ability': heavy_strike,
            'level_prereq': 1,
        },
        {
            'name': "Troll's Blood",
            'ability': trolls_blood,
            'level_prereq': 1,
        }
    ],
    "passive_1": [
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 2,
        },
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 2,
        }
    ],
    "active_2":[
        {
            'name': 'Leap Slam',
            'ability': leap_slam,
            'level_prereq': 4,
            'disabled': False

        },
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 4,
            'disabled': False
        },
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 4,
            'disabled': False
        }
    ],
    "passive_2": [
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 5,
        },
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 5,
        }
    ],
    "active_3": [
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 7,
            'disabled': False
        },
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 7,
            'disabled': False
        },
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 7,
            'disabled': False
        }
    ],
    "passive_3": [
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 8,
        },
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 8,
        }
    ],
    "active_4": [
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 10,
            'disabled': False
        },
        {
            'name': '',
            'ability': Ability(),
            'level_prereq': 10,
            'disabled': False
        }
    ]
}


warrior_config = {
    'starting_attributes': {
        'str': 6,
        'dex': 4,
        'int': 3,
        'end': 7,
        'vit': 7,
        'wis': 3
    },
    'skill_tree': SKILL_TREE
}
