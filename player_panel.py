from pygame import mouse, event, MOUSEMOTION
from rendering import player_panel_renderer

class PlayerPanel:
    def __init__(self, player):
        """
        Object that governs the player panel which displays all of the players information including stats, attributes,
        condition, inventory, and skills. Also acts as a middle-man between the Game object and the panel-rendering
        module.
        :param player: the Player object being controlled by the user.

        Throughout the methods of this class, the following attributes are also set:
        :player_dict: A dict containing all of the necessary info about the Player.
        :panel_rect: The dimensions of the player panel rectangle.
        :inventory_tiles: The dimensions of all of the inventory tiles which actually hold and item.
        :inventory_rect: The dimensions of the inventory rectangle.
        :item_window_active: A flag signifying whether or not the item display window is currently showing.
        :active_item_index: The index of the currently displayed item in the player's inventory.
        """
        self.player = player
        self.player_dict = player.to_dict()
        self.panel_rect, self.inventory_tiles, self.inventory_rect  = player_panel_renderer.render_player_panel(self.player_dict)
        self.item_window_active = None
        self.active_item_index = None

    def refresh_hp_mp(self):
        """Method to refresh the displayed HP and MP values."""
        player_panel_renderer.draw_hp_mp(self.player_dict['hp'], self.player_dict['mp'], refresh=True)

    def refresh_level_and_exp(self):
        """Method to refresh the displayed level and experience bar."""
        player_panel_renderer.draw_level_and_experience(self.player_dict['level'], self.player_dict['type'],
                                                        self.player_dict['experience'], refresh=True)

    def refresh_attributes(self):
        """Method to refresh the displayed players attributes."""
        player_panel_renderer.draw_attributes(self.player_dict['attributes'], refresh=True)

    def refresh_conditions(self):
        """Method to refresh the displayed conditions."""
        player_panel_renderer.draw_conditions(self.player_dict['conditions'], refresh=True)

    def refresh_inventory(self):
        """
        Method to refresh the displayed inventory, as well as re-set self.inventory_tiles based on the
        occupied inventory slots.
        """
        self.inventory_tiles, _ = player_panel_renderer.draw_inventory(self.player_dict['inventory'], refresh=True)

    def handle_panel_mouseover(self):
        """
        Method to handle the player mousing over the player panel, to display specific information on what is being
        moused over.
        """
        # This condition checks if the mouse is on the inventory and no item info is currently being displayed
        if self.inventory_rect.collidepoint(mouse.get_pos()) and not self.item_window_active:
            self.handle_inventory_mouseover()
        # This condition checks if an item info window is still displaying even if the mouse is no longer
        # on that item, and if so, refreshes the inventory to get rid of the item info
        if self.item_window_active is not None and \
                not self.item_window_active.collidepoint(mouse.get_pos()):
            self.refresh_inventory()
            self.item_window_active = None
            self.active_item_index = None

    def handle_inventory_mouseover(self):
        """
        Method to specifically handle cases then the mouse is over the inventory, and display the appropriate item info.
        """
        item_index = None
        item_tile = None
        for i, item_tile in enumerate(self.inventory_tiles):
            # This loop checks if the tile being moused over currently holds an actual item, and if so, returns index.
            if item_tile.collidepoint(mouse.get_pos()) and len(self.player_dict['inventory']) >= i + 1:
                item_index = i
                break

        if item_index is not None:
            self.item_window_active = item_tile
            self.active_item_index = item_index
            player_panel_renderer.draw_item_info(self.player_dict['inventory'][item_index].to_dict(), mouse.get_pos())

    def handle_item_consumption(self):
        """Method to reset the necessary attributes and refresh the inventory when an item is consumed."""
        self.item_window_active = None
        self.active_item_index = None
        self.refresh_inventory()