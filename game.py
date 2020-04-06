import pygame as pg
import random
from copy import copy
from time import sleep

from utility_functions import manhattan_distance, tile_from_xy_coords, xy_coords_from_tile
from rendering import window_renderer, board_renderer
from game_elements.board import Board
from game_elements.player import Player
from misc_panel import MiscPanel
from player_panel import PlayerPanel


# List containing all of the keys that currently have a function
FUNCTIONAL_KEYS = [pg.K_SPACE, pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_d, pg.K_LEFT, pg.K_w, pg.K_s, pg.K_d, pg.K_a]

class Game:
    def __init__(self, console, board=None, player=None, filename='untitled'):
        """
        Initializes the Game object with all the necessary objects to get started, loaded as attributes.

        :param console: Console object that handles battle text being rendered at the top of the screen
        :param board: Board object that stores object locations and renders the board
        :param player: Player object controlled by the user
        :param filename: The save file which the game is loaded from. TODO: implement this
        """
        self.console = console
        self.board = board if board is not None else Board()
        self.player = player if player is not None else Player()
        # Player coordinates are initialized from the board template
        self.player.x = self.board.player_coordinates[0]
        self.player.y = self.board.player_coordinates[1]
        self.filename = filename
        # These two panels are initialized at rendering time
        self.player_panel = None
        self.misc_panel = None
        # Boolean flag showing if player is targeting an ability/item use
        self.targeting_mode = False

    def handle_player_movement(self, input):
        """Given a basic movement input, moves the player character and updates its position on the board."""
        # console_text = list()
        old_x, old_y = self.player.x, self.player.y
        # The following function reads the user input and updates the Player x and y attributes, but only in the player
        # class. If it's found to not be a valid movement, gets reset below.
        new_x, new_y = self.player.perform_movement(input)
        # Checks if player is moving to an open tile or trap
        if self.board.tile_is_open(new_x, new_y):
            new_lines = self.board.move_character(character=self.player, new_x=new_x, new_y=new_y)
            print(new_lines)
            self.console.update(new_lines)
        else:
            self.player.x, self.player_y = old_x, old_y
            if self.board.template[new_y][new_x] == 'E':  # Moving to a tile which contains an enemy attacks the enemy
                self.console.update(self.handle_attacking_enemy((new_x, new_y)))
                # console_text.extend(self.handle_attacking_enemy((new_x, new_y)))
            elif self.board.template[new_y][new_x] == 'T':  # Moving to a tile which contains a chest opens the chest
                self.console.update(self.handle_opening_chest((new_x, new_y)))
                # console_text.extend(self.handle_opening_chest((new_x, new_y)))

    def handle_opening_chest(self, chest_pos):
        """Calls methods to set chest status to 'open' and add item to player inventory."""
        target_chest = self.board.chests[chest_pos]
        if target_chest.opened:
            self.console.update('This chest is empty. ')
            return
        # pick_up_item returns text for the console as well as a boolean signifying the success of picking up item
        console_text, success = self.player.pick_up_item(target_chest.item)
        if success:
            self.board.handle_chest_has_been_opened(chest_pos)
            self.player_panel.refresh_inventory()
            self.console.update(console_text)

    def handle_attacking_enemy(self, enemy_pos):
        """Calls methods to update focus window, for player to attack enemy, and if enemy.hp=0, handle enemy death."""
        self.refresh_focus_window(enemy_pos)
        target_enemy = self.board.enemies[enemy_pos]
        self.console.update(self.player.basic_attack(target_enemy))
        if target_enemy.hp[0] == 0:
            self.handle_enemy_death(target_enemy)
        # Battle text is returned to be fed into the console.

    def handle_enemy_death(self, enemy):
        self.board.handle_enemy_death((enemy.x, enemy.y))
        self.misc_panel.focus_tile = None
        self.refresh_focus_window()
        self.player.gain_experience(enemy.hp)
        self.player_panel.refresh_level_and_exp()

    def start_enemy_turn(self):
        """
        Loops through list of enemies, having them act if necessary.

        Current behaviour for each enemy:
        if player is within attack range:
            attack player
        elif player is within aggro range:
            move towards player
        else
            wait
        """
        enemies = list()
        for enemy_coord in self.board.enemies:
            # Load all Enemy objects currently on the board into a list to iterate over
            enemies.append(self.board.enemies[enemy_coord])
        console_text = list()
        for enemy in enemies:
            distance_to_player = manhattan_distance((enemy.x, enemy.y), (self.player.x, self.player.y))
            if distance_to_player <= enemy.attack_range:
                self.console.update(enemy.basic_attack(self.player))
            elif distance_to_player <= enemy.aggro_range:
                # Enemies can move onto either open tiles or traps.
                open_tiles = self.board.tile_mapping['O'] + self.board.tile_mapping['R']
                new_x, new_y = enemy.move_towards_target((self.player.x, self.player.y), open_tiles)
                if new_x is not None:  # Check if a valid movement was found
                    self.console.update(self.board.move_character(enemy, new_x, new_y))
                    enemy.x = new_x
                    enemy.y = new_y
            self.console.update(enemy.apply_end_of_turn_status_effects())

    def handle_item_use(self):
        """
        Calls necessary functions and methods to handle the player using an item. This will differ depending on if
        the item is a consumable or equipment.

        :returns: New lines to be displayed in the console
        """
        item_index = self.player_panel.get_tooltip_index(element='inventory')
        item_dict = self.player.inventory[item_index].to_dict()
        if item_dict['type'] == 'consumable':
            self.console.update(self.player.consume_item(item_index))
        elif item_dict['type'] == 'equipment':
            self.console.update(self.player.equip_item(item_index))
        self.player_panel.handle_item_consumption()
        return True

    def get_targets(self, targeting_function):
        """
        Given a targeting function from an ability or item, enter the targeting loop to find a target, and return
        the chosen target, if any.
        """
        target_tile_coordinates = targeting_function(self.board.template, self.player.x, self.player.y)
        target_tile_rects = [pg.Rect(tile_from_xy_coords(coords[0], coords[1])) for coords in target_tile_coordinates]
        target_rect = self.enter_targeting_game_loop(valid_target_tiles=target_tile_rects)
        if target_rect is False:  # If no valid target was returned.
            return None
        else:
            target_coords = xy_coords_from_tile(target_rect)
            if self.board.enemies.get(target_coords, None):
                target = self.board.enemies[target_coords]
                self.refresh_focus_window(target_coords)
                return target
            return None

    def handle_ability_use(self):
        """
        Calls necessary functions and methods to handle the player using an ability. Generally goes something like:
            i.   Get ability index from player panel
            ii.  Run ability targeting method
            iii. Use ability on selected target, if target is valid
            iv.  If target was moved as part of the ability, update positions on board accordingly
            v.   End player turn
        :return: New lines to be displayed in the console
        """
        ability_index = self.player_panel.get_tooltip_index(element='abilities')
        ability = self.player.active_abilities[ability_index]
        if ability.turns_left > 0:
            # This ability is still on cooldown, so do nothing
            return False
        target = self.get_targets(ability.targeting_function)
        if target is not None:
            # Using abilities returns a dict containing all the of the outcomes of the ability, e.g. new console text,
            # any movements of the player or target(s), etc.
            ability_outcome = self.player.use_ability(ability, target)
            if ability_outcome.get('console_text', None):
                self.console.update(ability_outcome['console_text'])
            # Check to see if target was moved by ability, adjust position in board accordingly.
            # If no movements were found, loop over an empty list, i.e. do nothing
            for movement in ability_outcome.get('movements', list()):
                # Each movement entry in the ability_outcome dict will look like
                # { 'subject': The character object that's being moved
                #   'new_position': (new_x, new_y) }
                # Only bother moving the subject of the movement if they weren't outright killed by the ability
                if movement['subject'].hp[0] == 0:
                    continue
                new_x, new_y = movement['new_position']
                # Target is only moved if the new space is open or a trap
                if self.board.template[new_y][new_x] in {'O', 'R'}:
                    self.console.update(self.board.move_character(character=movement['subject'], new_x=new_x,
                                                                  new_y=new_y))
                    self.load_game_board()
                    pg.display.update()
                    sleep(0.3)

            if target is not None and target.hp[0] == 0:
                self.handle_enemy_death(target)
            return True
        self.load_game_board()  # Refresh board to get rid of targeting mode render
        return False

    def handle_turn_end(self):
        """
        Calls all necessary functions at the end of a turn, to check the players status and update things
        accordingly.

        conditions_worsen() and check_fatigue() each return a boolean which determines whether any player info has
        changed, and thus needs re-drawing.
        """
        if self.player.conditions_worsen():
            self.player_panel.refresh_hp_mp()
            self.player_panel.refresh_conditions()
            self.player_panel.refresh_attributes()

        if self.player.decrement_ability_cooldowns():
            self.player_panel.refresh_abilities()

        if self.player.check_fatigue():
            self.player_panel.refresh_attributes()

    def draw_window(self):
        """Calls functions to render board and both panels"""
        self.load_game_board()
        self.load_player_panel()
        self.load_misc_panel()

    def load_game_board(self):
        """Calls initial render of the game board"""
        board_renderer.render_game_board(self.board.template)

    def load_player_panel(self):
        """Initiates player_panel"""
        self.player_panel = PlayerPanel(self.player)

    def load_misc_panel(self):
        """Initiates misc_panel"""
        self.misc_panel = MiscPanel(self.board)

    def refresh_focus_window(self, focus_tile=None):
        """Calls misc_panel method to re-render focus window"""
        self.misc_panel.refresh_focus_window(focus_tile)

    def handle_key_presses(self, pressed_key):
        """Calls appropriate function based on pressed key."""
        if pressed_key == pg.K_SPACE:
            self.player.wait()
            # Not printing anything to console in this case, so just return empty list.
            return []
        # Check if input is for a basic movement, i.e. up, down, left, right
        elif pressed_key in self.player.movement_mapping.keys():
            self.console.update(self.handle_player_movement(pressed_key))

    def handle_player_turn_over(self, console_text=None):
        """
        Method that's called when the player has performed a turn-ending action. Calls methods to progress enemy turns
        and re-render necessary parts of the screen that may have changed.
        """
        console_text = console_text if console_text is not None else list()
        if console_text:
            self.console.update(console_text)
        self.console.update(self.player.apply_end_of_turn_status_effects())
        self.start_enemy_turn()
        self.handle_turn_end()
        self.player_panel.refresh_player_panel()
        self.load_game_board()

    def handle_left_clicks(self):
        """
        Method to handle cases in the main game loop when the left mouse button has been clicked.
        :return console_text: New lines for the console.
        """
        new_actions = list()
        mouse_pos = pg.mouse.get_pos()
        # If a tooltip focus window is active, means a player has clicked on something that might have
        # a function when clicked.
        action_taken = False
        if self.player_panel.tooltip_focus is not None:
            # If the user has clicked on the inventory with the tooltip window active, we check if the mouse
            # is on the inventory, implying that an item was clicked.
            if self.player_panel.inventory_rect.collidepoint(mouse_pos):
                action_taken = self.handle_item_use()
            # Do the same thing to check if an ability has been clicked.
            elif self.player_panel.abilities_rect.collidepoint(mouse_pos):
                action_taken = self.handle_ability_use()
        if action_taken:
            self.handle_player_turn_over(console_text=new_actions)
        return

    def enter_targeting_game_loop(self, valid_target_tiles):
        """
        Alternative game loop that is triggered when player enters targeting mode, to use an ability or item that
        requires a target. If player clicks on a valid target, return that tile and apply the ability/item effect. If
        the player clicks anywhere else, then exit targeting mode and return to neutral game state.
        """
        while True:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    for tile in valid_target_tiles:
                        if tile.collidepoint(pg.mouse.get_pos()):
                            return tile
                    return False

    def game_loop_iteration(self):
        """
        Main game loop, which iterates over player inputs and calls appropriate methods.

        Returns False if the game has been finished, and True otherwise.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            # List holding text to be displayed on the console after turn, if any.
            # Handling the cases when there is a mouseover on the player panel
            if self.player_panel.panel_rect.collidepoint(pg.mouse.get_pos()):
                self.player_panel.handle_panel_mouseover()
            if pg.mouse.get_pressed()[0]:  # Check if the left mouse button has been pressed
                self.handle_left_clicks()
            if event.type == pg.KEYDOWN:  # If mouse hasn't been pressed, check for keystrokes
                if event.key == pg.K_ESCAPE:  # ESC exits the game
                    return False
                if event.key in FUNCTIONAL_KEYS:  # Check if pressed key has an assigned function
                    self.console.update(self.handle_key_presses(event.key))
                    self.handle_player_turn_over()

        return True
