import random
import copy

from rendering import board_renderer
from game_elements.ability import Ability


def heavy_strike_func(self, target, skill_level):
    """Ability function which deals heavy damage to target and knocks them back one tile."""
    console_text = ''
    # First determine the relative positions to find the knockback.
    if self.x != target.x:
        new_x = target.x + 1 if self.x < target.x else target.x - 1
        new_y = target.y
    else:
        new_y = target.y + 1 if self.y < target.y else target.y - 1
        new_x = target.x
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


def trolls_blood_func(self, skill_level, **kwargs):
    from element_lists.status_list import health_regen
    trolls_blood_regen = copy.copy(health_regen)
    trolls_blood_regen.params = {'value': skill_level}
    self.apply_status(trolls_blood_regen)
    return {
        'console_text': ["You cast Troll's Blood on yourself."]
    }


heavy_strike = Ability(name='Heavy Strike',
                       description=f'Strike an enemy with all your might, dealing massive damage and knocking them back',
                       active=True, targeting_function=board_renderer.highlight_adjacent_tiles,
                       targetable_tile_types=['E'],
                       function=heavy_strike_func, level=1, cooldown=5)

trolls_blood = Ability(name="Troll's Blood",
                       description=f'Cast a spell on yourself to gain some passive health regeneration.',
                       active=True, targeting_function=board_renderer.highlight_self, targetable_tile_types=['P'],
                       function=trolls_blood_func, level=1, cooldown=15)

warrior_config = {
    'starting_attributes': {
        'str': 6,
        'dex': 4,
        'int': 3,
        'end': 7,
        'vit': 7,
        'wis': 3
    },
    'active_abilities': [copy.copy(x) for x in [heavy_strike, trolls_blood]],
    'passive_abilities': [],
}