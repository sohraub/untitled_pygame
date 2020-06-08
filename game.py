import pygame as pg
import random
from copy import copy
from time import sleep, time
from datetime import datetime


from utility_functions import manhattan_distance, tile_from_xy_coords, xy_coords_from_tile, find_best_step
from rendering import window_renderer, board_renderer
from game_elements.board import Board
from game_elements.player import Player
from element_lists.board_templates import get_board_list, starting_board, testing
from misc_panel import MiscPanel
from player_panel import PlayerPanel


# List containing all of the keys that currently have a function
FUNCTIONAL_KEYS = [pg.K_SPACE, pg.K_UP, pg.K_DOWN, pg.K_RIGHT, pg.K_d, pg.K_LEFT, pg.K_w, pg.K_s, pg.K_d, pg.K_a,
                   pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_t, pg.K_ESCAPE]

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
        self.board = board if board is not None else Board(board_template=starting_board)
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
        self.board.generate_adjacent_boards(self.player.level, self.player.experience)

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
            self.console.update(new_lines)
        else:
            self.player.x, self.player_y = old_x, old_y
            if self.board.template[new_y][new_x] == 'E':  # Moving to a tile which contains an enemy attacks the enemy
                self.console.update(self.handle_attacking_enemy((new_x, new_y)))
                # console_text.extend(self.handle_attacking_enemy((new_x, new_y)))
            elif self.board.template[new_y][new_x] == 'T':  # Moving to a tile which contains a chest opens the chest
                self.console.update(self.handle_opening_chest((new_x, new_y)))
                # console_text.extend(self.handle_opening_chest((new_x, new_y)))
            elif self.board.template[new_y][new_x] == 'D':  # Moving to a tile which is a door to the next board
                self.handle_board_transition(door_coordinates=(new_x, new_y))

    def handle_opening_chest(self, chest_pos):
        """Calls methods to set chest status to 'open' and add item to player inventory."""
        target_chest = self.board.chests[chest_pos]
        if target_chest.opened:
            self.console.update('This chest is empty. ')
            return
        # pick_up_item returns text for the console as well as a boolean signifying the success of picking up item
        console_text, success = self.player.pick_up_item(target_chest.item, from_chest=True)
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
        """
        When an enemy dies, the following things will happen:
            i. Enemy must be removed from the board
            ii. Focus window in the misc. panel must be reset
            iii. Player gains experience, and possibly levels up. These changes must be reflected in the rendering
                 of the player panel.
        """
        self.board.handle_enemy_death(enemy_pos=(enemy.x, enemy.y))
        self.misc_panel.focus_tile = None
        self.refresh_focus_window()
        player_leveled_up = self.player.gain_experience()
        # Player.gain_experience() evaluates to True if the Player has leveled up. If so, the call the
        # handle_player_level_up method in the player panel.
        if player_leveled_up:
            self.player_panel.level_up()
            self.console.update(f"{self.player.name} has reached level {self.player.level}.")
            # Apply player's passives that modify the board, in case any new ones were allocated.
            self.board.apply_player_passives(self.player.passive_abilities['board_mods'])
        self.player_panel.refresh_player_panel()

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
        for enemy in list(self.board.enemies.values()):
            distance_to_player = manhattan_distance((enemy.x, enemy.y), (self.player.x, self.player.y))
            if distance_to_player <= enemy.aggro_range:
                if not enemy.aggro:
                    self.console.update(f"{enemy.display_name} has noticed you.")
                enemy.aggro = True
            if distance_to_player <= enemy.attack_range:
                self.console.update(enemy.basic_attack(self.player))
            else:
                # Enemies can move onto either open tiles or traps.
                open_tiles = self.board.tile_mapping['O'] + self.board.tile_mapping['R']
                new_x, new_y = None, None
                if enemy.aggro:
                    new_x, new_y = find_best_step(start=(enemy.x, enemy.y), goal=(self.player.x, self.player.y),
                                                  open_tiles=open_tiles)

                elif random.randint(0, 100) > 50:
                    # If enemy is not aggro'd, give a 50% chance to move one tile in a random direction
                    adjacent_tiles = ([(enemy.x + i, enemy.y) for i in [-1, 1]] +
                                      [(enemy.x, enemy.y + i) for i in [-1, 1]])
                    new_x, new_y = random.choice([tile for tile in adjacent_tiles if tile in set(open_tiles)])
                if new_x is not None and self.board.tile_is_open(new_x, new_y):  # Check if a valid movement was found
                    self.console.update(self.board.move_character(enemy, new_x, new_y))
                    enemy.x = new_x
                    enemy.y = new_y
            self.console.update(enemy.apply_end_of_turn_status_effects())
            enemy.passive_mp_regen()

    def handle_item_use(self):
        """
        Calls necessary functions and methods to handle the player using an item. This will differ depending on if
        the item is a consumable or equipment.

        :returns: New lines to be displayed in the console
        """
        item_index = self.player_panel.get_tooltip_index(element='inventory')
        item = self.player.inventory[item_index]
        if item.is_consumable() and self.check_item_prerequisites(item):
            self.console.update(self.player.consume_item(item_index))
        elif item.is_equipment():
            self.console.update(self.player.equip_item(item_index))
        self.player_panel.handle_item_consumption()
        return True

    def check_item_prerequisites(self, item):
        """
        Some consumable items have prerequisite conditions before they can be used. Those are checked here.
        Return True if all prerequisites are met (of if there are None), and False otherwise.
        """
        if item.prerequisites_for_use is None:
            return True
        for prerequisite in item.prerequisites_for_use:
            if prerequisite == 'no_enemies_on_board' and len(self.board.enemies.keys()) > 0:
                self.console.update('Conditions to use this item are not met.')
                return False

        return True

    def get_targets(self, ability):
        """
        Given a targeting function from an ability or item, enter the targeting loop to find a target, and return
        the chosen target, if any.
        """
        targets = list()
        target_tile_coordinates = ability.targeting_function(self.board.template, self.player.x, self.player.y,
                                                             **ability.targeting_function_params)
        target_tile_rects = [pg.Rect(tile_from_xy_coords(coords[0], coords[1])) for coords in target_tile_coordinates]
        target_rect = self.enter_targeting_game_loop(valid_target_tiles=target_tile_rects)
        if target_rect is False:  # If no valid target was returned.
            return targets
        else:
            target_coords = [targeted_coord := xy_coords_from_tile(target_rect)]
            if ability.multi_target_function:
                if len(ability.multi_target_function) == 2:
                    # In this case multi_target_function was passed a a 2-tuple of (function, parameters_dict)
                    target_coords += ability.multi_target_function[0](targeted_coord[0], targeted_coord[1],
                                                                       player_x=self.player.x, player_y=self.player.y,
                                                                       **ability.multi_target_function[1])
                else:
                    target_coords += ability.multi_target_function(targeted_coord[0], targeted_coord[1],
                                                                   player_x=self.player.x, player_y=self.player.y)
            for target_coord in target_coords:
                if self.board.enemies.get(target_coord, None):
                    target = self.board.enemies[target_coord]
                    targets.append(target)
                elif self.board.player_coordinates == target_coord:
                    target = self.player
                    targets.append(target)
            if ability.save_target:
                targets.append(targeted_coord)
            return targets

    def handle_ability_use(self, ability_index=None):
        """
        Calls necessary functions and methods to handle the player using an ability. Generally goes something like:
            i.   Get ability index from player panel
            ii.  Run ability targeting method
            iii. Use ability on selected target, if target is valid
            iv.  If target was moved as part of the ability, update positions on board accordingly
            v.   End player turn
        :param ability_index: If this is None, then it means ability was used by clicking on the player panel, so we get
                              the index from there. If it's not None, then ability was used by pressing the
                              corresponding key, in which case the index is passed in by the handle_key_presses() method
        :return: New lines to be displayed in the console
        """
        if ability_index is None:
            ability_index = self.player_panel.get_tooltip_index(element='abilities')
        ability = self.player.active_abilities[ability_index]
        # Return False if the ability is still on cooldown or player doesn't have enough MP
        if ability.turns_left > 0:
            self.console.update('That ability is still on cooldown!')
            return False
        elif ability.mp_cost > self.player.mp[0]:
            self.console.update('Not enough MP to use that ability!')
            return False
        targets = self.get_targets(ability)
        self.load_game_board()  # Refresh game board to get rid of targeting render
        if targets:
            # Using abilities returns a dict containing all the of the outcomes of the ability, e.g. new console text,
            # any movements of the player or target(s), etc.
            ability_outcome = self.player.use_ability(ability, targets)
            if ability_outcome.get('console_text', None):
                self.console.update(ability_outcome['console_text'])
            # Check to see if target was moved by ability, adjust position in board accordingly.
            # If no movements were found, loop over an empty list, i.e. do nothing
            for movement in ability_outcome.get('movements', list()):
                # Each movement entry in the ability_outcome dict will look like
                #   { 'subject': The character object that's being moved
                #     'new_position': (new_x, new_y) }
                if movement['subject'].hp[0] == 0:  # Don't bother moving the character if they were killed
                    continue
                new_x, new_y = movement['new_position']
                # Target is only moved if the new space is open or a trap
                if self.board.tile_is_open(new_x, new_y):
                    self.console.update(self.board.move_character(character=movement['subject'], new_x=new_x,
                                                                  new_y=new_y))
                    self.load_game_board()
                    pg.display.update()
            for target in targets:
                if target is not None and target.hp[0] == 0:
                    self.handle_enemy_death(target)
            return True
        return False

    def handle_turn_end(self):
        """
        Calls all necessary functions at the end of a turn, to check the players status and update things
        accordingly.

        conditions_worsen() and check_fatigue() each return a boolean which determines whether any player info has
        changed, and thus needs re-drawing.
        """
        if self.player.conditions_worsen():
            self.player_panel.refresh_player_panel()

        if self.player.decrement_ability_cooldowns():
            self.player_panel.refresh_abilities()

        self.player.passive_mp_regen()

        if self.player.check_fatigue():
            self.player_panel.refresh_attributes()

        if self.misc_panel.focus_tile is not None:
            self.misc_panel.refresh_focus_window(self.misc_panel.focus_tile)

    def draw_window(self):
        """Calls functions to render board and both panels"""
        self.load_game_board()
        self.load_player_panel()
        self.load_misc_panel()

    def load_game_board(self):
        """Calls render of the game board, and applies any board-modifiers in the Players passive abilities, if any."""
        board_renderer.render_game_board(self.board.template)
        self.board.apply_player_passives(self.player.passive_abilities['board_mods'])

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
        """
        Calls appropriate function based on pressed key. Returns a boolean which determines whether an action was
        taken and thus the player turn should end.
        """
        if pressed_key == pg.K_SPACE:
            self.player.wait()
            return True
        # Check if input is for a basic movement, i.e. up, down, left, right
        elif pressed_key in self.player.movement_mapping.keys():
            self.console.update(self.handle_player_movement(pressed_key))
            return True
        elif pressed_key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5]:
            key_mapping = {
                pg.K_1: 0,  # Map to one number lower since abilities are saved internally in a 0-indexed list
                pg.K_2: 1,
                pg.K_3: 2,
                pg.K_4: 3,
                pg.K_5: 4
            }
            return self.handle_ability_use(ability_index=key_mapping[pressed_key])
        elif pressed_key == pg.K_t:
            self.player_panel.display_skill_tree()
        elif pressed_key == pg.K_ESCAPE:
            if self.player_panel.skill_tree_displaying:
                self.player_panel.skill_tree_displaying = False
                self.player_panel.refresh_player_panel()

    def handle_player_turn_over(self, console_text=None):
        """
        Method that's called when the player has performed a turn-ending action. Calls methods to progress enemy turns
        and re-render necessary parts of the screen that may have changed.
        """
        console_text = console_text if console_text is not None else list()
        if console_text:
            self.console.update(console_text)
        self.console.update(self.player.apply_end_of_turn_status_effects())
        self.load_game_board()
        sleep(0.2)  # Want a slight pause after the player movement has been rendered before the enemy actions happen
        self.start_enemy_turn()
        self.handle_turn_end()
        self.player_panel.refresh_player_panel()
        self.load_game_board()

    def handle_left_clicks(self):
        """
        Method to handle cases in the main game loop when the left mouse button has been clicked.
        """
        new_actions = list()
        mouse_pos = pg.mouse.get_pos()
        # If a tooltip focus window is active, means a player has clicked on something that might have
        # a function when clicked.
        action_taken = False
        if self.player_panel.skill_tree_displaying and self.player_panel.panel_rect.collidepoint(mouse_pos):
            # If the skill tree is active and the mouse is on the player panel, then we assume that the player is
            # trying to allocate skill points
            self.player_panel.handle_skill_point_allocation()

        if self.player_panel.attributes_rect.collidepoint(mouse_pos) and self.player_panel.level_up_points > 0:
            self.player_panel.handle_allocate_attribute_point()

        elif self.player_panel.tooltip_focus is not None:
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

    def handle_board_transition(self, door_coordinates):
        """Handles all the necessary updates when the Player steps on a door and transitions to the next board."""
        new_board = self.board.doors[door_coordinates]['board']
        self.player.x, self.player.y = self.board.doors[door_coordinates]['entry_position']
        self.board = new_board
        self.board.player_coordinates = (self.player.x, self.player.y)
        self.misc_panel.board = new_board
        self.board.generate_adjacent_boards(self.player.level, self.player.experience)
        self.load_game_board()

    def enter_targeting_game_loop(self, valid_target_tiles):
        """
        Alternative game loop that is triggered when player enters targeting mode, to use an ability or item that
        requires a target. If player clicks on a valid target, return that tile and apply the ability/item effect. If
        the player clicks anywhere else, or presses ESC, then exit targeting mode and return to neutral game state.
        """
        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for tile in valid_target_tiles:
                        if tile.collidepoint(pg.mouse.get_pos()):
                            return tile
                    return False

    def game_loop_iteration(self):
        """
        Main game loop, which iterates over player inputs and calls appropriate methods.

        Returns False if the game has been finished, and True otherwise.

        Also records the time each loop iteration takes, and if the time > 0 (i.e. there was an actual input), we write
        the execution time to a text file to log our performance as we add features.
        """
        for event in pg.event.get():
            start = time()
            if event.type == pg.QUIT:
                return False
            # List holding text to be displayed on the console after turn, if any.
            # Handling the cases when there is a mouseover on the player panel
            if self.player_panel.panel_rect.collidepoint(pg.mouse.get_pos()):
                self.player_panel.handle_panel_mouseover()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Check if the left mouse button has been pressed
                self.handle_left_clicks()
            if event.type == pg.KEYDOWN:  # If mouse hasn't been pressed, check for keystrokes
                keys = pg.key.get_pressed()
                if keys[pg.K_RSHIFT] or keys[pg.K_LSHIFT]:
                    if event.key == pg.K_ESCAPE:  # SHIFT + ESC exits the game
                        return False
                if event.key in FUNCTIONAL_KEYS:  # Check if pressed key has an assigned function
                    action_taken = self.handle_key_presses(event.key)
                    if action_taken:
                        self.handle_player_turn_over()
            end = time()
            execution_time = end - start
            if execution_time > 0:
                with open('time_logs.txt', 'a+') as f:
                    f.write(f'{datetime.now()}, {execution_time}\n')
        return True
