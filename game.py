import pygame as pg

from utility_functions import manhattan_distance
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

    def move_player_on_board(self, input):
        """Given a basic movement input, moves the player character and updates its position on the board."""
        console_text = list()
        old_x = self.player.x
        old_y = self.player.y
        new_x, new_y = self.player.perform_movement(input)
        if self.board.template[new_y][new_x] == 'O':  # Checks if player is moving to an open tile
            self.board.player_coordinates = (new_x, new_y)
            self.board.rebuild_template()
        else:
            self.player.x = old_x
            self.player.y = old_y
            if self.board.template[new_y][new_x] == 'E':  # Moving to a tile which contains an enemy attacks the enemy
                # The handle_attacking_enemy function returns a list of strings to be displayed in the console
                console_text.extend(self.handle_attacking_enemy((new_x, new_y)))
            if self.board.template[new_y][new_x] == 'T':  # Moving a tile which contains a chest opens the chest
                # Opening a chest only returns a single string to display in the console
                console_text.append(self.handle_opening_chest((new_x, new_y)))

        return console_text

    def handle_opening_chest(self, chest_pos):
        """Calls methods to set chest status to 'open' and add item to player inventory."""
        target_chest = self.board.chests[chest_pos]
        if target_chest.opened:
            return 'This chest is empty. '
        # pick_up_item returns text for the console as well as a boolean signifying the success of picking up item
        console_text, success = self.player.pick_up_item(target_chest.item)
        if success:
            self.board.handle_chest_has_been_opened(chest_pos)
            self.player_panel.refresh_inventory()
        return console_text

    def handle_attacking_enemy(self, enemy_pos):
        """Calls methods to update focus window, for player to attack enemy, and if enemy.hp=0, handle enemy death."""
        self.refresh_focus_window(enemy_pos)
        target_enemy = self.board.enemies[enemy_pos]
        console_text = list()
        console_text.extend(self.player.basic_attack(target_enemy))
        if target_enemy.hp[0] == 0:
            self.board.handle_enemy_death(enemy_pos)
            self.misc_panel.focus_tile = None
            self.refresh_focus_window()
        # Battle text is returned to be fed into the console.
        return console_text

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
                console_text.extend(enemy.basic_attack(self.player, enemy_attack=True))
            elif distance_to_player <= enemy.aggro_range:
                new_position = enemy.move_towards_target((self.player.x, self.player.y), self.board.tile_mapping['O'])
                if new_position is not None:
                    self.board.update_enemy_position((enemy.x, enemy.y), new_position)
                    enemy.x = new_position[0]
                    enemy.y = new_position[1]
                    self.load_game_board()

        return console_text

    def handle_item_use(self):
        """
        Calls necessary functions and methods to handle the player using an item.

        :returns: New lines to be displayed in the console
        """
        console_text = list()
        item_index = self.player_panel.active_item_index
        console_text.append(self.player.consume_item(item_index))
        self.player_panel.handle_item_consumption()

        return console_text


    def handle_turn_end(self, console_text=None):
        """
        Calls all necessary functions at the end of a turn, to check the players status and update things
        accordingly.

        conditions_worsen() and check_fatigue() each return a boolean which determines whether any player info has
        changed, and thus needs re-drawing.
        """
        console_text = console_text if console_text is not None else list()
        if self.player.conditions_worsen():
            self.player_panel.refresh_hp_mp()
            self.player_panel.refresh_conditions()
            self.player_panel.refresh_attributes()

        if self.player.check_fatigue():
            self.player_panel.refresh_attributes()
        if console_text is not None:
            self.console.update_console(console_text)

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
            console_text = self.move_player_on_board(pressed_key)
            return console_text

    def handle_player_turn_over(self, console_text=None):
        """
        Method that's called when the player has performed a turn-ending action. Calls methods to progress enemy turns
        and re-render necessary parts of the screen that may have changed.
        """
        console_text = console_text if console_text is not None else list()
        console_text.extend(self.start_enemy_turn())
        self.handle_turn_end(console_text)
        self.player_panel.refresh_hp_mp()
        self.player_panel.refresh_conditions()
        self.load_game_board()

    def game_loop_iteration(self):
        """
        Main game loop, which iterates over player inputs and calls appropriate methods.

        Returns False if the game has been finished, and True otherwise.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            # List holding text to be displayed on the console after turn, if any.
            console_text = list()
            # Handling the cases when there is a mouseover on the player panel
            if self.player_panel.panel_rect.collidepoint(pg.mouse.get_pos()):
                self.player_panel.handle_panel_mouseover()
            if pg.mouse.get_pressed()[0]:  # Check if the left mouse button has been pressed
                mouse_pos = pg.mouse.get_pos()
                # If a tooltip focus window is active, means a player has clicked on something that might have
                # a function when clicked.
                if self.player_panel.tooltip_focus is not None:
                    # If the user has clicked on the inventory with the tooltip window active, they have clicked an item
                    if self.player_panel.inventory_rect.collidepoint(mouse_pos):
                        console_text.extend(self.handle_item_use())
                        self.handle_player_turn_over(console_text)
            if event.type == pg.KEYDOWN:  # If mouse hasn't been pressed, check for keystrokes
                if event.key == pg.K_ESCAPE:  # ESC exits the game
                    return False
                if event.key in FUNCTIONAL_KEYS:  # Check if pressed key has an assigned function
                    console_text.extend(self.handle_key_presses(event.key))
                    self.handle_player_turn_over(console_text)

        return True
