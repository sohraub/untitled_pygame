

class Trap:
    def __init__(self, x=0, y=0, type='spike', trigger_prob=0.9, trigger_avoid_coeff=1, def_rating_coeff=1):
        """
        Traps are objects that can be placed on boards, that will cause various affects once stepped on by either
        the player or an enemy.
        :param x: x-coordinate of the trap
        :param y: y-coordinate of the trap
        :param type: String representing the type of trap, e.g. spike trap, poison gas trap, etc.
        :param trigger_prob: Probability of the trap to trigger when stepped on.
        :param trigger_avoid_coeff: Coefficient for victim's dex attributed used to calculate the probability of the
                                    trap not triggering.
        :param def_rating_coeff: Coefficient for the victim's defensive rating, used to calculate final damage of
                                 certain traps (only relevant for Players, Enemies do not have a defensive rating).
        """
        self.x = x
        self.y = y
        self.type = type
        self.trigger_prob = trigger_prob
        self.trigger_avoid_coeff = trigger_avoid_coeff
        self.def_rating_coeff = def_rating_coeff
