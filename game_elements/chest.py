from item_list import generate_random_item


class Chest:
    def __init__(self, tier=1, type='both', item=None, opened=False):
        """
        Chest objects are used to store items on the board.
        :param tier: The tier used to determine the list the item will be randomly pulled from.
        :param type: The type of item this chest can contain, i.e. 'consumable', 'equipment', or 'both'
        :param item: The Item object contained inside the chest.
        :param opened: A flag to determine whether or not this chest has already been opened.
        """
        self.item = item if item is not None else generate_random_item(tier, type)
        self.opened = opened
