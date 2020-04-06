from utility_functions import parse_description


class Ability:
    def __init__(self, name, description, active, targeting_function, targetable_tile_types, function, level=0,
                 cooldown=0, prerequisites=None):
        """
        Abilities are used by the player to make their lives easier.
        :param name: String, the name of the ability.
        :parm description: String, describing the ability.
        :param active: Boolean, if true this skill is an active skill, else it is a passive skill.
        :param targeting_function: A function called in the targeting phase, which will highlight on the board all the
                                   square that this ability can target, if the ability is active.
        :param targetable_tile_types: A list of tile types that this ability can target.
        :param function: A function that will apply the ability effect.
        :param level: Int, the level of the skill which determines the numbers behind its effectiveness.
        :param cooldown: Int, the number of turns it takes for this ability to recharge.
        :param prerequisites: A list of abilities, which the player must have before they can use this ability.

        We also initialize the following attributes:
        :turns_left: Initialized to 0, this will hold the number of turns until the cooldown expires once an ability
                     is used.
        """
        self.name = name
        self.description = parse_description(description, char_limit=33)
        self.active = active
        self.targeting_function = targeting_function if self.active else None
        self.targetable_tile_types = targetable_tile_types if self.active else None
        self.function = function
        self.level = level
        self.cooldown = cooldown
        self.turns_left = 0
        self.prerequisites = prerequisites if prerequisites is not None else list()

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'active': self.active,
            'level': self.level,
            'cooldown': self.cooldown,
            'turns_left': self.turns_left
        }