from utility_functions import parse_description


class Ability:
    def __init__(self, name='', description='', active=False, level=0, details=None):
        """
        Abilities are used by the player to make their lives easier. This class serves as a base class for active
        abilities and passive abilities.
        :param name: String, the name of the ability.
        :parm description: String, describing the ability.
        :param active: Boolean, if true this skill is an active skill, else it is a passive skill.
        :param level: Int, the level of the skill which determines the numbers behind its effectiveness.
        :param details: Dict containing info for all the ability's values, for tooltip-display purposes.
        """
        self.name = name
        self.description = description
        self.active = active
        self.level = level
        self.details = details if details is not None else dict()

    def __str__(self):
        return f'Level {self.level} {self.name}'

    def __repr__(self):
        return f'Level {self.level} {self.name}'


class ActiveAbility(Ability):
    def __init__(self, name='', description='', active=True, details=None, targeting_function=None, function=None,
                 targeting_function_params=None, multi_target_function=None, save_target=False, level=0, mp_cost=1,
                 cooldown=0, level_up_dict=None):
        """
        Active abilities are abilities the player must actively use.
        :param targeting_function: A function called in the targeting phase, which will highlight on the board all the
                                   square that this ability can target, if the ability is active.
        :param targeting_function_params: A dict of parameters for the targeting function, if necessary. None otherwise
        :param function: A function that will apply the ability effect.
        :param multi_target_function: If ability can target multiple tiles, then this will be a function that gathers
                                      a list of every coordinate to be targeted.
        :param save_target: A boolean flag, set to True only for function which target a tile, but don't actually
                            affect a target on the tile but need those coordinates saved for other purposes.
        :param mp_cost: Int, the cost in mp points to use this ability once.
        :param cooldown: Int, the number of turns it takes for this ability to recharge.
        :param level_up_dict: Dict which contains the values that increases for an ability when it levels up, as well
                              as the values those attributes increase by.

        We also initialize the following attributes:
        :turns_left: Initialized to 0, this will hold the number of turns until the cooldown expires once an ability
                     is used.

        """
        super().__init__(name, description, active, level, details)
        self.targeting_function = targeting_function if self.active else None
        self.targeting_function_params = targeting_function_params if targeting_function_params is not None else dict()
        self.function = function
        self.multi_target_function = multi_target_function
        self.save_target = save_target
        self.cooldown = cooldown
        self.mp_cost = mp_cost
        self.level_up_dict = level_up_dict if level_up_dict is not None else dict()
        self.turns_left = 0

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'active': self.active,
            'level': self.level,
            'details': self.details,
            'cooldown': self.cooldown,
            'mp_cost': self.mp_cost,
            'turns_left': self.turns_left
        }

    def level_up(self):
        """Levels up an active ability by incrementing its attributes by the values found in its level_up_dict"""
        if self.level_up_dict.get('cooldown', False):
            self.cooldown = max(0, self.cooldown - self.level_up_dict['cooldown'])
        if self.level_up_dict.get('target_radius', False):
            self.targeting_function_params['radius'] += self.level_up_dict['target_radius']
        if self.level_up_dict.get('mp_cost', False):
            self.mp_cost = max(0, self.level_up_dict['mp_cost'] + self.mp_cost)



class PassiveAbility(Ability):
    def __init__(self, name='', description='', active=False, level=0, details=None, mod_group='combat',
                 specific_mod='', value=0):
        """
        Passive abilities are enabled as soon as they are allocated, and stay passively enabled forever (unless they
        somehow become de-allocated). Will be stored in the Player class as a dict of modifiers.
        :param mod_group: The high-level area where this ability's modifier will be applied.
        :param specific_mod: The specific value this ability will modify
        :param value: The magnitude of the modification.
        For example, assume the player allocated a passive skill that increased their crit rate by 5%. Then the Player's
        passive ability dict will look like:
        passive_abilities = {
            'combat': {
                'crit_rate': 5
            }
        }
        """
        super().__init__(name, description, active, level, details)
        self.mod_group = mod_group
        self.specific_mod = specific_mod
        self.value = value

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'active': self.active,
            'level': self.level,
            'details': self.details,
            'mod_group': self.mod_group,
            'specific_mod': self.specific_mod,
            'value': self.value
        }
