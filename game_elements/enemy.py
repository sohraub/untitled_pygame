from game_elements.character import Character
from utility_functions import manhattan_distance

death_phrases = ['It lets out one final, desperate breath before it ceases movement. ',
                 'You watch it slowly bleed out to death. ']

class Enemy(Character):
    def __init__(self, name, x=0, y=0, hp=None, mp=None, attributes=None, status=None, move_speed=1, in_combat=False,
                 attack_range=1, role='attacker', aggro_range=3, retreat_probability=0.3, flavour_text=None):
        super().__init__(name, x, y, hp, mp, attributes, status, move_speed, in_combat)
        self.aggro_range = aggro_range
        self.attack_range = attack_range
        self.retreat_probability = retreat_probability
        self.role = role
        self.flavour_text = flavour_text if flavour_text is not None else 'This is placeholder flavour text'

    def check_aggro(self, player):
        if manhattan_distance((self.x, self.y), (player.x, player.y)) <= self.aggro_range:
            self.in_combat = True
            player.in_combat = True
            return True
        return False

    def move_towards_target(self, point, open_tiles):
        # First check if it can close the x-distance, and then the y-distance
        if point[0] - self.x != 0:
            next_step_x = int((point[0] - self.x) / abs(point[0] - self.x))  # This will be either 1 or -1
            if (self.x + next_step_x, self.y) in set(open_tiles):
                return (self.x + next_step_x, self.y)
        if point[1] - self.y != 0:
            next_step_y = int((point[1] - self.y) / abs(point[1] - self.y))  # This will be either 1 or -1
            if (self.x, self.y + next_step_y) in set(open_tiles):
                return (self.x, self.y + next_step_y)
        # If no valid movement, return None
        return None




