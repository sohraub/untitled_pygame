
class Status:
    def __init__(self, name, type, duration, description, end_of_turn_effect=None, attribute_effects=None,
                 params=None):
        """
        Statuses can be inflicted on Characters. They will last 'duration' number of turns and can be either a
        buff or a debuff, never both.
        :param name: String representing the name of the status
        :param type: 'buff' or 'debuff'
        :param duration: Int, number of turns the status will last
        :param description: A short description of the status, used for rendering.
        :param end_of_turn_effect: Either a function to apply at the end of each turn, or None
        :param attribute_effects: Either a dict with all the changes applied to the character's stats for the duration,
                                  or None
        :param params: If status has an end_of_turn_effect function, this will be a dict holding all the parameters.
                       Otherwise, it will be None.

        In addition to these, we also set:
        :turns_left: Int, number of turns left in the duration. Initially set to the value of duration
        """
        self.name = name
        self.type = type
        self.duration = duration
        self.turns_left = duration
        self.description = description
        self.end_of_turn_effect = end_of_turn_effect
        self.attribute_effects = attribute_effects
        self.params = params

    def __str__(self):
        return f'{self.name} - {self.turns_left} turns left'

    def __repr__(self):
        return f'{self.name} - {self.turns_left} turns left'

    def is_combat_status(self):
        """Simple function which returns True if self is a CombatStatus, and False otherwise."""
        return self.__class__.__name__ == 'CombatStatus'

    def to_dict(self):
        """Returns a dict representation of the status, for rendering purposes mostly."""
        return {
            'name': self.name,
            'type': self.type,
            'turns_left': self.turns_left,
            'description': self.description
        }


class CombatStatus(Status):
    def __init__(self, name, type, duration, description, combat_function, offensive=True):
        """
        Combat statuses are a sub-class of statuses which have their effects applied only in combat. These effects take
        the form of a function that will be applied on a dict which contains all of the individual data-point in an
        instance of combat (e.g. the attacker, the target, the damage dealt, crit rate, etc.) and apply their effects
        to the values.
        :param combat_function: The function that will be applied to the combat values dict as the effect of this status
        :param offensive: A boolean, True if this is an offensive status (i.e. applied when the player is attacking an
                          enemy) and False if it's a defensive status (i.e. applied when an enemy attacks the player).
        """
        super().__init__(name, type, duration, description)
        self.combat_function = combat_function
        self.offensive = offensive

