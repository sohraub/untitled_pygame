from pygame import mouse, Rect
from rendering import player_panel_renderer

class PlayerPanel:
    def __init__(self, player):
        self.player = player
        self.player_dict = player.to_dict()
        self.panel_rect = player_panel_renderer.render_player_panel(self.player_dict)
        self.inventory_tiles, self.inventory_rect = player_panel_renderer.draw_inventory(self.player_dict['inventory'])

    def refresh_hp_mp(self):
        player_panel_renderer.draw_hp_mp(self.player_dict['hp'], self.player_dict['mp'], refresh=True)

    def refresh_level_and_exp(self):
        player_panel_renderer.draw_level_and_experience(self.player_dict['level'], self.player_dict['type'],
                                                        self.player_dict['experience'], refresh=True)

    def refresh_attributes(self):
        player_panel_renderer.draw_attributes(self.player_dict['attributes'], refresh=True)

    def refresh_conditions(self):
        player_panel_renderer.draw_conditions(self.player_dict['conditions'], refresh=True)

    def refresh_inventory(self):
        self.inventory_tiles, _ = player_panel_renderer.draw_inventory(self.player_dict['inventory'], refresh=True)

    def handle_panel_mouseover(self):
        if self.inventory_rect.collidepoint(mouse.get_pos()):
            self.handle_inventory_mouseover()

    def handle_inventory_mouseover(self):
        for i, item_tile in enumerate(self.inventory_tiles):
            x = mouse.get_pos()
            if item_tile.collidepoint(mouse.get_pos()):
                try:
                    print(self.player_dict['inventory'][i].name)
                except:
                    print('no item here')
                break

