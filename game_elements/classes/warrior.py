import random
from copy import copy

from rendering import board_renderer
from game_elements.ability import ActiveAbility, PassiveAbility
from utility_functions import get_knockback


def heavy_strike_func(self, targets, skill_level):
    """Ability function which deals heavy damage to target and knocks them back one tile."""
    target = targets[0]
    console_text = ''
    # First determine the relative positions to find the knockback.
    new_x, new_y = get_knockback(self.x, self.y, target)
    # Now calculate the damage
    damage = (1 + skill_level) * (self.attributes['str'] - target.attributes['end'] + self.off_rating)
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
                                         f' them back', active=True, level=1, cooldown=5,
                             targeting_function=board_renderer.highlight_adjacent_tiles, function=heavy_strike_func,
                             details={'Damage Multiplier': '1 + {skill_level}', 'Cooldown': '5', 'MP Cost': '2'})


def trolls_blood_func(self, skill_level, **kwargs):
    """Ability function which adds a health regen buff to self."""
    from element_lists.status_list import health_regen
    trolls_blood_regen = copy(health_regen)
    trolls_blood_regen.params = {'value': skill_level * self.attributes['wis'] - 2}
    self.apply_status(trolls_blood_regen)
    return {
        'console_text': ["You cast Troll's Blood on yourself."]
    }

trolls_blood = ActiveAbility(name="Troll's Blood", mp_cost=3, function=trolls_blood_func, level=1, cooldown=15,
                             description=f'Cast a spell on yourself to gain some passive health regeneration. Healing '
                                         f'amount scales with WIS.',
                             active=True, targeting_function=board_renderer.highlight_self,
                             details={'HP Regen Per Turn': '{skill_level} * {wis} - 2',
                                      'Buff Duration': '7', 'Cooldown': '15', 'MP Cost': '3'})


def leap_slam_func(self, targets, skill_level):
    """Ability function which transports the player to a tile, and damages and knocks back any adjacent enemies."""
    console_text = 'You use Leap Slam'
    # Leap slam is an ability with self.save_target = True, so the coords of the selected tile are appended
    # to the end of the list of targets, and are popped from the list here.
    self_new_x, self_new_y = targets.pop(-1)
    ability_outcomes = {
        'movements': [{
            'subject': self,
            'new_position': (self_new_x, self_new_y)
        }]
    }
    for target in targets:
        damage = skill_level * max(1, self.attributes['str'] - target.attributes['end'] + self.off_rating)
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
                          save_target=True, multi_target=[(1, 0), (0, 1), (-1, 0), (0, -1)],
                          level_up_dict={'target_radius': 1, 'mp_cost': 1},
                          details={'Damage Multiplier': '{skill_level}', 'Range': '3 + {skill_level}',
                                   'Cooldown': '10', 'MP Cost': '4'})


def chain_hook_func(self, targets, skill_level):
    """
    Ability function that accepts as target either an enemy or an open tile. If an enemy, pull that enemy to be adjacent
    to you. If an open tile, reposition player to that tile. The targets parameter is a list that can either have one or
    two elements, signifying the different cases.
        i. If targets only has one element, then the ability was used on an open space, and the element is the
           coordinate of that space.
        ii. If targets has two elements, then the ability was used on an enemy, and the list looks like:
                [Enemy(), (enemy.x, enemy.y)]
            so we set the sole target to the first element of the list.
    """
    ability_outcomes = {'movements': list(), 'console_text': list()}
    if len(targets) > 1:  # In this case the target is an enemy
        target = targets[0]
        if target.x != self.x:
            target_new_pos = (self.x + int((target.x - self.x)/abs(target.x - self.x)), target.y)
        else:
            target_new_pos = (self.x, self.y + int((target.y - self.y)/abs(target.y - self.y)))
        ability_outcomes['movements'].append({'subject': target, 'new_position': target_new_pos})
        ability_outcomes['console_text'].append(f'You use Chain Hook on the {target.display_name}, pulling it '
                                                f'towards you.')
    else:  # In this case the target is an open space
        ability_outcomes['movements'].append({'subject': self, 'new_position': targets[0]})
    targets.pop(-1)  # Pop the coordinate entry from the list of targets, so the Player use_ability() function doesn't
                     # try and check if it's an enemy.
    return ability_outcomes

chain_hook = ActiveAbility(name='Chain Hook', mp_cost=5,
                           description='Throw a grappling hook in a straight line at a target. If the target is an '
                                       'enemy, pulls them towards you. Otherwise, pulls you to the target.',
                           active=True, targeting_function=board_renderer.highlight_cross_pattern,
                           function=chain_hook_func, level=0, cooldown=7, save_target=True,
                           level_up_dict={'cooldown': 1, 'mp_cost': -1},
                           details={'Cooldown': '7 - {skill_level}', 'MP Cost': '5 - {skill_level}'})

from element_lists.passive_abilities import calculated_strikes, bloodthirsty, deadly_momentum, thick_skin, quiet_steps

SKILL_TREE = {
    "active_1": [
        {
            'ability': copy(heavy_strike),
            'level_prereq': 1,
        },
        {
            'ability': copy(trolls_blood),
            'level_prereq': 1,
        }
    ],
    "passive_1": [
        {
            'ability': copy(calculated_strikes),
            'level_prereq': 2
        },
        {
            'ability': copy(thick_skin),
            'level_prereq': 2,
        }
    ],
    "active_2":[
        {
            'ability': copy(leap_slam),
            'level_prereq': 4,
            'disabled': False,
        },
        {
            'ability': copy(chain_hook),
            'level_prereq': 4,
            'disabled': False
        },
        {
            'ability': ActiveAbility(),
            'level_prereq': 4,
            'disabled': False
        }
    ],
    "passive_2": [
        {
            'ability': copy(bloodthirsty),
            'level_prereq': 5,
        },
        {
            'ability': copy(deadly_momentum),
            'level_prereq': 5,
        }
    ],
    "active_3": [
        {
            'ability': ActiveAbility(),
            'level_prereq': 7,
            'disabled': False
        },
        {
            'ability': ActiveAbility(),
            'level_prereq': 7,
            'disabled': False
        },
        {
            'ability': ActiveAbility(),
            'level_prereq': 7,
            'disabled': False
        }
    ],
    "passive_3": [
        {
            'ability': PassiveAbility(),
            'level_prereq': 8,
        },
        {
            'ability': PassiveAbility(),
            'level_prereq': 8,
        }
    ],
    "active_4": [
        {
            'ability': ActiveAbility(),
            'level_prereq': 10,
            'disabled': False
        },
        {
            'ability': ActiveAbility(),
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
