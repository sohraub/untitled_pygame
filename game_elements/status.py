
class Status:
    def __init__(self, name, type, duration, end_of_turn_effect=None, attribute_effects=None):
        """
        Statuses can be inflicted on Characters. They will last 'duration' number of turns and can be either a
        buff or a debuff, never both.
        :param name: String representing the name of the status
        :param type: 'buff' or 'debuff'
        :param duration: Int, number of turns the status will last
        :param turns_left: Int, number of turns left in the duration. Initially set to the value of duration
        :param end_of_turn_effect: Either a function to apply at the end of each turn, or None
        :param attribute_effects: Either a dict with all the changes applied to the character's stats for the duration,
                                  or None
        """
        self.name = name
        self.type = type
        self.duration = duration
        self.turns_left = duration
        self.end_of_turn_effect = end_of_turn_effect
        self.attribute_effects = attribute_effects


