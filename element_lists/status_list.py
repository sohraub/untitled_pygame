from math import ceil

from game_elements.status import Status, CombatStatus
from utility_functions import parse_description


"""
Module for storing the list of every status and the possible effects.
"""

#### EFFECTS ####

def lesser_poison_effect(target):
    """Target loses 10% of their max HP, rounded up."""
    damage = ceil(0.1 * target.hp[1])
    target.hp[0] = max(0, target.hp[0] - damage)
    if target.__class__.__name__ == 'Enemy':
        console_text = f'The {target.display_name} takes '
    else:
        console_text = f'You take '
    console_text += f'{damage} damage from being poisoned.'
    return console_text


def hp_regen_effect(target, value):
    """Target regains 'value' HP every turn."""
    target.hp[0] = min(target.hp[0] + value, target.hp[1])
    return ''  # No console output for regenerating health


def mp_regen_effect(target, value):
    """Target regains 'value' MP every turn."""
    target.mp[0] = min(target.mp[0] + value, target.mp[1])
    return ''


def reflect_damage(attacker, target, damage, **kwargs):
    """Any damage taken is reflected back to the attacker. If damage being dealt is 0, do nothing."""
    if damage == 0:
        return ''
    attacker.hp[0] = max(0, attacker.hp[0] - damage)
    # Add the damage value to target's hp to cancel out when it's subtracted later in the combat function
    target.hp[0] += damage
    attacker_name = attacker.display_name if attacker.is_enemy() else attacker.name
    target_name = target.display_name if target.is_enemy() else target.name
    console_text = f'{attacker_name} attempts to deal {damage} damage to {target_name}, but the damage is reflected.'
    return console_text


#### STATUSES ####

lesser_poison = Status(name='Lesser Poison', type='debuff', duration=5,
                       description=parse_description('Take a small amount of poison damage every turn.', char_limit=30),
                       end_of_turn_effect=lesser_poison_effect, params={})

hp_regen = Status(name='HP Regeneration', type='buff', duration=7,
                  description=parse_description('Heal a small amount of HP every turn.', char_limit=30),
                  end_of_turn_effect=hp_regen_effect, params={'value': 1})

mp_regen = Status(name='MP Regeneration', type='buff', duration=7,
                  description=parse_description('Regain a small amount of MP every turn.', char_limit=30),
                  end_of_turn_effect=mp_regen_effect, params={'value': 2})

increased_strength = Status(name='Increased Strength', type='buff', duration=5,
                            description=parse_description('Temporarily increase Strength'),
                            attribute_effects={'str': 2})

reflect_damage = CombatStatus(name='Reflect Damage', type='buff', duration=5,
                              description=parse_description('Reflects all damage taken back to the attacker',
                                                            char_limit=30),
                              offensive=False, combat_function=reflect_damage)

