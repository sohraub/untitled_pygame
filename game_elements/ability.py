from utility_functions import parse_description


class Ability:
    def __init__(self, name, description, active, targeting_function, function, targeting_function_params=None,
                 multi_target=None, save_target=False, level=0, cooldown=0, prerequisites=None):
        """
        Abilities are used by the player to make their lives easier.
        :param name: String, the name of the ability.
        :parm description: String, describing the ability.
        :param active: Boolean, if true this skill is an active skill, else it is a passive skill.
        :param targeting_function: A function called in the targeting phase, which will highlight on the board all the
                                   square that this ability can target, if the ability is active.
        :param targeting_function_params: A dict of parameters for the targeting function, if necessary. None otherwise
        :param function: A function that will apply the ability effect.
        :param multi_target: If ability can target multiple tiles, then this will be a list of every targeted tile
                             relative to the target chosen through the targeting function. Otherwise None
        :param save_target: A boolean flag, set to True only for function which target a tile, but don't actually
                            affect a target on the tile but need those coordinates saved for other purposes.
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
        self.targeting_function_params = targeting_function_params if targeting_function_params is not None else dict()
        self.function = function
        self.multi_target = multi_target
        self.save_target = save_target
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
