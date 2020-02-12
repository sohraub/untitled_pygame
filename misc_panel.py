from rendering import misc_panel_renderer


class MiscPanel:
    def __init__(self, board, focus_tile=None):
        self.board = board
        self.focus_tile = focus_tile
        misc_panel_renderer.render_misc_panel()


    def refresh_misc_panel(self):
        if self.focus_tile is not None:
            self.load_focus_window()


    def load_focus_window(self):
        # This mapping gives the appropriate function to load data, based on the type of tile which under focus
        focus_function_mapping = {
            'E': self.load_enemy_info
        }
        # Get the letter representation of the tile from the board template
        tile_type = self.board.template[self.focus_tile[1]][self.focus_tile[0]]
        focus_dict = focus_function_mapping[tile_type]()
        misc_panel_renderer.render_focus_window(focus_dict)


    def load_enemy_info(self):
        enemy = self.board.enemies[self.focus_tile]
        enemy_dict = {
            'type': 'enemy',
            'name': enemy.name,
            'hp': enemy.hp,
            'flavour_text': enemy.flavour_text
        }
        return enemy_dict
