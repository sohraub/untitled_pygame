

class Ability:
    def __init__(self, name, active, targeting_function, function, level=0, cooldown=0, prerequisites=None):
        """
        Abilities are used by the player to make their lives easier.
        :param name: String, the name of the ability.
        :param active: Boolean, if true this skill is an active skill, else it is a passive skill.
        :param targeting_function: A function called in the targeting phase, which will highlight on the board all the
                                   square that this ability can target, if the ability is active.
        :param function: A function that will apply the ability effect.
        :param level: Int, the level of the skill which determines the numbers behind its effectiveness.
        :param cooldown: Int, the number of turns it takes for this ability to recharge.
        :param prerequisites: A list of abilities, which the player must have before they can use this ability.
        """
        self.name = name
        self.active = active
        self.targeting_function = targeting_function if self.active else None
        self.function = function
        self.level = level
        self.cooldown = cooldown
        self.prerequisites = prerequisites if prerequisites is not None else list()

    def to_dict(self):
        return {
            'name': self.name,
            'active': self.active,
            'level': self.level,
            'cooldown': self.cooldown
        }