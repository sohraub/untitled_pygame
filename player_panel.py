import pygame as pg

from rendering import player_panel_renderer

from skill_tree import SkillTreeController

class PlayerPanel:
    def __init__(self, player):
        """
        Object that governs the player panel which displays all of the players information including stats, attributes,
        condition, inventory, and skills. Also acts as a middle-man between the Game object and the panel-rendering
        module.
        :param player: the Player object being controlled by the user.
        :param level_up_points: Every time the player levels up, they get two points to spend on their attributes. If
                                this value is != 0, then the extra buttons to add points to attributes will be visible.

        In the init method of this class, functions in the player_panel_render module are called to draw the individual
        components, and all of these functions return the Rect object that encloses their subject areas. These Rects
        are saved as attributes for the PlayerPanel to detect and handle mouseovers. In addition to these, we also
        save as attributes the following:
        :player_dict: A dict containing all of the necessary info about the Player.
        :buff_rects: A list of the dimensions of each buff indicator.
        :debuff_rects: A list of the dimensions of each debuff indicator.
        :inventory_tiles: The dimensions of all of the inventory tiles which actually hold and item.
        :tooltip_focus: If a tooltip window is active, this will hold the Rect of the focus of the window. If there
                        is no tooltip windows active, this will be set to None.
        :active_item_index: The index of the currently displayed item in the player's inventory, also used when
                            to tell the Player object which item is being clicked on.
        """
        self.player = player
        self.level_up_points = 0
        self.player_dict = player.to_dict()
        self.panel_rect = player_panel_renderer.draw_player_panel(self.player_dict['name'])
        self.hp_mp_rect = player_panel_renderer.draw_hp_mp(self.player_dict['hp'], self.player_dict['mp'])
        self.status_rect, self.buff_rects, self.debuff_rects = player_panel_renderer.\
                                                                draw_status(self.player_dict['status']['buffs'],
                                                                            self.player_dict['status']['debuffs'])
        self.conditions_rect = player_panel_renderer.draw_conditions(self.player_dict['conditions'])
        self.attributes_rect = player_panel_renderer.draw_attributes(self.player_dict['attributes'],
                                                                     self.level_up_points)
        self.level_and_exp_rect = player_panel_renderer.draw_level_and_experience(self.player_dict['level'],
                                                                                  self.player_dict['profession'],
                                                                                  self.player_dict['experience'])
        self.inventory_tiles, self.inventory_rect = player_panel_renderer.draw_inventory(self.player_dict['inventory'])
        self.equipment_tiles, self.equipment_rect = player_panel_renderer.draw_equipment(self.player_dict['equipment'])
        self.ability_tiles, self.abilities_rect = player_panel_renderer.draw_active_abilities(self.player_dict['active_abilities'])
        self.tooltip_focus = None
        self.active_item_index = None
        self.skill_tree = SkillTreeController(self.player_dict['skill_tree'], self.player_dict['profession'],
                                              self.player_dict['level'], self.player_dict['attributes'],
                                              self.player_dict['active_abilities'],
                                              self.player_dict['passive_abilities'])
        self.skill_tree_displaying = False

    def refresh_player_panel(self):
        """Refresh every part of the player panel."""
        if self.skill_tree_displaying:
            return
        self.player_dict = self.player.to_dict()
        player_panel_renderer.draw_player_panel(self.player_dict['name'], refresh=True)
        self.refresh_hp_mp()
        self.refresh_statuses()
        self.refresh_attributes()
        self.refresh_conditions()
        self.refresh_equipment()
        self.refresh_inventory()
        self.refresh_abilities()
        self.refresh_level_and_exp()

    def refresh_hp_mp(self):
        """Method to refresh the displayed HP and MP values."""
        if self.skill_tree_displaying:
            return
        player_panel_renderer.draw_hp_mp(self.player_dict['hp'], self.player_dict['mp'], refresh=True)

    def refresh_statuses(self):
        """Method to refresh the players statuses."""
        if self.skill_tree_displaying:
            return
        _, self.buff_rects, self.debuff_rects = player_panel_renderer.draw_status(self.player_dict['status']['buffs'],
                                                                                  self.player_dict['status']['debuffs'],
                                                                                  refresh=True)

    def refresh_level_and_exp(self):
        """Method to refresh the displayed level and experience bar."""
        if self.skill_tree_displaying:
            return
        player_panel_renderer.draw_level_and_experience(self.player_dict['level'], self.player_dict['profession'],
                                                        self.player_dict['experience'], refresh=True)

    def refresh_attributes(self):
        """Method to refresh the displayed players attributes."""
        if self.skill_tree_displaying:
            return
        player_panel_renderer.draw_attributes(self.player_dict['attributes'], self.level_up_points, refresh=True)
        if self.level_up_points > 0:
            player_panel_renderer.draw_attribute_level_up_buttons(self.level_up_points)

    def refresh_conditions(self):
        """Method to refresh the displayed conditions."""
        if self.skill_tree_displaying:
            return
        player_panel_renderer.draw_conditions(self.player_dict['conditions'], refresh=True)

    def refresh_inventory(self):
        """
        Refresh the displayed inventory, as well as re-set self.inventory_tiles based on the occupied inventory slots.
        """
        if self.skill_tree_displaying:
            return
        self.inventory_tiles, _ = player_panel_renderer.draw_inventory(self.player_dict['inventory'], refresh=True)

    def refresh_abilities(self):
        """Refresh the displayed abilities."""
        if self.skill_tree_displaying:
            return
        self.ability_tiles, _ = player_panel_renderer.draw_active_abilities(self.player_dict['active_abilities'],
                                                                            refresh=True,
                                                                            skill_points=self.skill_tree.skill_points)

    def refresh_equipment(self):
        """Refresh the displayed inventory, as well as reset self.equipment_tiles base on occupied equipment slots."""
        if self.skill_tree_displaying:
            return
        self.equipment_tiles, _ = player_panel_renderer.draw_equipment(self.player_dict['equipment'], refresh=True)

    def handle_panel_mouseover(self):
        """
        Method to handle the player mousing over the player panel, to display specific information on what is being
        moused over.
        """
        if self.skill_tree_displaying:
            self.skill_tree.handle_skill_tree_mouseover(self.player_dict['skill_tree'])
            return False
        mouse_pos = pg.mouse.get_pos()
        # These conditions check if the mouse is on a panel element that can show a detail window, and that no detail
        # window is currently being displayed.
        if not self.tooltip_focus:
            if self.status_rect.collidepoint(mouse_pos):
                self.handle_status_mouseover()
            elif self.attributes_rect.collidepoint(mouse_pos):
                self.handle_attributes_mouseover()
            elif self.inventory_rect.collidepoint(mouse_pos):
                self.handle_inventory_mouseover()
            elif self.equipment_rect.collidepoint(mouse_pos):
                self.handle_equipment_mouseover()
            elif self.abilities_rect.collidepoint(mouse_pos):
                self.handle_abilities_mouseover()
            elif self.level_and_exp_rect.collidepoint(mouse_pos):
                self.handle_level_exp_mouseover()

            # Shelving tooltips for conditions for now, colour indication should be sufficient
            # if self.conditions_rect.collidepoint(mouse_pos) and not self.tooltip_focus:
            #     self.handle_conditions_mouseover()
        if self.tooltip_focus is not None and not self.tooltip_focus.collidepoint(mouse_pos):
            # This condition checks if an info tooltip is still displaying even if the mouse is no longer
            # on that item, and if so, refreshes the inventory to get rid of the item info
            self.refresh_player_panel()
            self.tooltip_focus = None
            self.active_item_index = None

    def handle_status_mouseover(self):
        """
        Handle cases when the mouse is over the statuses, to display tooltip info for buffs and debuffs.
        """
        if self.skill_tree_displaying:
            return
        mouse_pos = pg.mouse.get_pos()
        buff_index = None
        debuff_index = None
        buff_rect = None
        debuff_rect = None
        for i, buff_rect in enumerate(self.buff_rects):
            if buff_rect.collidepoint(mouse_pos):
                buff_index = i
                print(buff_index)
                break

        if buff_index is None:  # No need to check debuff collisions if we already know a buff has been collided with.
            for i, debuff_rect in enumerate(self.debuff_rects):
                if debuff_rect.collidepoint(mouse_pos):
                    debuff_index = i
                    break

        if buff_index is not None:
            self.tooltip_focus = buff_rect
            player_panel_renderer.draw_status_details(self.player_dict['status']['buffs'][buff_index])
        elif debuff_index is not None:
            self.tooltip_focus = debuff_rect
            player_panel_renderer.draw_status_details(self.player_dict['status']['debuffs'][debuff_index])

    def handle_attributes_mouseover(self):
        """
        The attributes section of the panel has no real functionality on mouseover for the time being, might eventually
        add tooltips explaining what each attribute is useful for.
        """
        pass

    def handle_allocate_attribute_point(self):
        """
        Called when the Game object registers a left click and the mouse is on the attribute rectangle. If player has
        attribute points to spend, allocates them accordingly.
        """
        level_up_buttons = player_panel_renderer.draw_attribute_level_up_buttons(self.level_up_points,
                                                                                 return_only=True)
        mouse_pos = pg.mouse.get_pos()
        index_attribute_mapping = {
            0: 'str',
            1: 'dex',
            2: 'int',
            3: 'end',
            4: 'vit',
            5: 'wis'
        }
        for i, button in enumerate(level_up_buttons):
            if button.collidepoint(mouse_pos):
                clicked_attribute = index_attribute_mapping[i]
                self.player.attributes[clicked_attribute] += 1
                self.level_up_points -= 1
                self.player.apply_attribute_changes()
                self.refresh_player_panel()
                return

    def handle_inventory_mouseover(self):
        """
        Method to specifically handle cases then the mouse is over the inventory, and display the appropriate item info.
        """
        if self.skill_tree_displaying:
            return
        item_index = None
        item_tile = None
        mouse_pos = pg.mouse.get_pos()
        for i, item_tile in enumerate(self.inventory_tiles):
            # This loop checks if the tile being moused over currently holds an actual item, and if so, returns index.
            if item_tile.collidepoint(mouse_pos) and len(self.player_dict['inventory']) >= i + 1:
                item_index = i
                break

        if item_index is not None:
            self.tooltip_focus = item_tile
            self.active_item_index = item_index
            player_panel_renderer.draw_item_details(self.player_dict['inventory'][item_index].to_dict(),
                                                    self.player_dict['attributes'],
                                                    self.player_dict['equipment'])

    def handle_equipment_mouseover(self):
        """
        Handle cases when the mouse is over equipment, and display appropriate tooltips. If an item is currently
        equipped in the slot being moused over, display that item's tooltip. Otherwise, display a tooltip showing the
        empty slot.
        """
        if self.skill_tree_displaying:
            return
        mouse_pos = pg.mouse.get_pos()
        slot_moused_over = ''
        for slot in self.equipment_tiles:
            if self.equipment_tiles[slot].collidepoint(mouse_pos):
                slot_moused_over = slot
                break

        if slot_moused_over:
            self.tooltip_focus = self.equipment_tiles[slot_moused_over]
            if self.player_dict['equipment'][slot_moused_over]:  # i.e. if there is an item equipped in the slot
                equipment_dict = self.player_dict['equipment'][slot_moused_over].to_dict()
            else:
                equipment_dict = None
            player_panel_renderer.draw_equipment_details(equipment_dict, slot_moused_over)

    def handle_abilities_mouseover(self):
        """
        Handle cases when mouse is over player abilities, listening for clicks on ability tiles and displaying tooltips.
        """
        if self.skill_tree_displaying:
            return
        mouse_pos = pg.mouse.get_pos()
        ability_index = None
        for index, tile in enumerate(self.ability_tiles):
            if tile.collidepoint(mouse_pos):
                ability_index = index
                break

        # Check to make sure there are actually abilities up to that index before trying to do anymore.
        if ability_index is not None and len(self.player_dict['active_abilities']) >= ability_index + 1:
            self.tooltip_focus = self.ability_tiles[ability_index]
            player_panel_renderer.draw_ability_details(self.player_dict['active_abilities'][ability_index],
                                                       self.player_dict['attributes'],
                                                       self.player_dict['mp'])

    def handle_conditions_mouseover(self):
        """
        Method to handle the case when the mouse is over the player's conditions, calling the rendering method to draw
        the detail window.
        """
        if self.skill_tree_displaying:
            return
        player_panel_renderer.draw_condition_details(self.player_dict['conditions'], self.conditions_rect)

    def handle_level_exp_mouseover(self):
        """Handles displaying tooltip when user mouses over their level or experience bar."""
        if self.skill_tree_displaying:
            return
        self.tooltip_focus = self.level_and_exp_rect
        player_panel_renderer.draw_exp_details(self.player_dict['experience'])

    def handle_item_consumption(self):
        """Method to reset the necessary attributes and refresh the inventory when an item is consumed."""
        self.tooltip_focus = None
        self.active_item_index = None
        self.refresh_inventory()
        self.refresh_equipment()

    def get_tooltip_index(self, element):
        """
        Used by the Game object to get the index of tiles which we clicked on, to be passed to the relevant Player
        methods.
        """
        if element == 'inventory':
            return self.inventory_tiles.index(self.tooltip_focus)
        elif element == 'abilities':
            return self.ability_tiles.index(self.tooltip_focus)

        raise Exception('Incompatible element passed into get_tooltip_index() method of player_panel.')

    def level_up(self):
        self.level_up_points += 2
        self.skill_tree.level += 1
        self.skill_tree.skill_points += 1

    def display_skill_tree(self):
        """
        Method that calls necessary rendering functions to display the player's skill tree in the player panel.
        """
        self.skill_tree_displaying = True
        self.skill_tree.render_skill_tree()

    def handle_skill_point_allocation(self):
        """
        Calls methods to handle skill point allocation in SkillTreeController, and updates the players abilities
        accordingly.
        """
        changes_made = self.skill_tree.allocate_skill_points()  # This function returns a boolean
        if changes_made:
            self.player.set_abilities_from_skill_tree()
