import pygame as pg

from utility_functions import manhattan_distance
from rendering import window_renderer, board_renderer
from game_elements.board import Board
from game_elements.player import Player
from misc_panel import MiscPanel
from player_panel import PlayerPanel


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
                # The handle_attacking_enemy function returns a text string to be displayed in the console
                console_text.append(self.handle_attacking_enemy((new_x, new_y)))
            if self.board.template[new_y][new_x] == 'T':  # Moving a tile which contains a chest opens the chest
                console_text.append(self.handle_opening_chest((new_x, new_y)))

        if console_text:
            self.console.update_console(console_text)

        return True


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
        battle_text = self.player.basic_attack(target_enemy)
        if target_enemy.hp[0] == 0:
            self.board.handle_enemy_death(enemy_pos)
            self.misc_panel.focus_tile = None
            self.refresh_focus_window()
        # Battle text is returned to be fed into the console.
        return battle_text


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
        for enemy in enemies:
            console_text = list()
            distance_to_player = manhattan_distance((enemy.x, enemy.y), (self.player.x, self.player.y))
            if distance_to_player <= enemy.attack_range:
                console_text.append(enemy.basic_attack(self.player, enemy_attack=True))
            elif distance_to_player <= enemy.aggro_range:
                new_position = enemy.move_towards_target((self.player.x, self.player.y), self.board.tile_mapping['O'])
                if new_position is not None:
                    self.board.update_enemy_position((enemy.x, enemy.y), new_position)
                    enemy.x = new_position[0]
                    enemy.y = new_position[1]
                    self.load_game_board()

            if console_text:
                self.console.update_console(console_text)


    def handle_turn_end(self):
        """Calls all necessary functions at the end of a turn"""
        # conditions_worsen() and check_fatigue() each return a boolean which determines whether any player info has
        # changed, and thus needs re-drawing
        if self.player.conditions_worsen():
            self.player_panel.refresh_hp_mp()
            self.player_panel.refresh_conditions()
            self.player_panel.refresh_attributes()
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
        # Check if input is for a basic movement, i.e. up, down, left, right
        elif pressed_key in self.player.movement_mapping.keys():
            self.move_player_on_board(pressed_key)

    def handle_player_turn_over(self):
        """
        Method that's called when the player has performed a turn-ending action. Calls methods to progress enemy turns
        and re-render necessary parts of the screen that may have changed.
        """
        self.start_enemy_turn()
        self.handle_turn_end()
        self.player_panel.refresh_hp_mp()
        self.load_game_board()

    def game_loop_iteration(self):
        """
        Main game loop, which iterates over player inputs and calls appropriate methods.

        Returns False if the game has been finished, and True otherwise.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            # Handling the cases when there is a mouseover on the player panel
            if self.player_panel.panel_rect.collidepoint(pg.mouse.get_pos()):
                self.player_panel.handle_panel_mouseover()
                # Checks if the player clicks an item in the inventory
                if pg.mouse.get_pressed()[0] and self.player_panel.item_window_active is not None:
                    if self.player_panel.item_window_active.collidepoint(pg.mouse.get_pos()):
                        item_index = self.player_panel.active_item_index
                        self.player.consume_item(item_index)
                        self.player_panel.handle_item_consumption()
                        self.handle_player_turn_over()
            if event.type == pg.KEYDOWN:
                self.handle_key_presses(event.key)
                self.handle_player_turn_over()

        return True
