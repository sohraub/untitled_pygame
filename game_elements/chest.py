from item_list import generate_random_item


class Chest:
    def __init__(self, tier=1, item=None, opened=False):
        self.item = item if item is not None else generate_random_item(tier)
        self.opened = opened
