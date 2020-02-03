from uuid import uuid4

from game_elements.enemy import Enemy


large_rat = Enemy(name='large_rat_'+str(uuid4()),
                  attributes={'str': 3, 'dex': 4, 'int': 1, 'end': 4, 'vit': 2, 'wis': 1})