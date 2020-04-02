import random

from rendering import board_renderer
from game_elements.ability import Ability


def heavy_strike_func(self, target, skill_level):
    """Ability function which deals heavy damage to target and knocks them back one tile."""
    console_text = ''
    # First determine the relative positions to find the knockback.
    if self.x != target.x:
        target.x = target.x + 1 if self.x < target.x else target.x - 1
    else:
        target.y = target.y + 1 if self.y < target.y else target.y + 1
    # Now calculate the damage
    damage = (1.5 + skill_level* 0.5) * (self.attributes['str'] - target.attributes['end'] + self.off_rating)
    if random.randint(0, 100) > 90:
        console_text += 'Critical hit! '
        damage = 2 * damage
    target.hp[0] = max(0, target.hp[0] - damage)
    console_text += f'You use Heavy Strike on the {target.display_name}, dealing {damage} damage and knocking them back.'
    return console_text


heavy_strike = Ability(name='Heavy Strike',
                       description=f'Strike an enemy with all your might, dealing massive damage and knocking them back',
                       active=True, targeting_function=board_renderer.highlight_adjacent_tiles,
                       function=heavy_strike_func, level=1, cooldown=5)

warrior_config = {
    'starting_attributes': {
        'str': 6,
        'dex': 4,
        'int': 3,
        'end': 7,
        'vit': 7,
        'wis': 3
    },
    'abilities': [heavy_strike ]
}