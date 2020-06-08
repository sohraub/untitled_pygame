from element_lists.item_list import generate_random_item


class Chest:
    def __init__(self, level=1, type='both', item=None, opened=False):
        """
        Chest objects are used to store items on the board.
        :param level: The level used to determine the list the item will be randomly pulled from.
        :param type: The type of item this chest can contain, i.e. 'consumable', 'equipment', or 'both'
        :param item: The Item object contained inside the chest.
        :param opened: A flag to determine whether or not this chest has already been opened.
        """
        self.item = item if item is not None else generate_random_item(level, type)
        self.opened = opened

def generate_chest(level, type='both'):
    """
    Returns a Chest object of the given tier.
    :param tier: Int representing the tier of item in the chest.
    :param type: The type of item to be in the chest.
    :return: A Chest object.
    """
    return Chest(level=level, type=type)