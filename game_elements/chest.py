from item_list import generate_random_item


class Chest:
    def __init__(self, tier=1, item=None, opened=False):
        """
        Chest objects are used to store items on the board.
        :param tier: The tier used to determine the list the item will be randomly pulled from.
        :param item: The Item object contained inside the chest.
        :param opened: A flag to determine whether or not this chest has already been opened.
        """
        self.item = item if item is not None else generate_random_item(tier)
        self.opened = opened
