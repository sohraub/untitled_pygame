from rendering import player_panel_renderer

class PlayerPanel:
    def __init__(self, player):
        self.player = player
        self.player_dict = player.to_dict()
        player_panel_renderer.render_player_panel(self.player_dict)

    def refresh_hp_mp(self):
        player_panel_renderer.draw_hp_mp(self.player_dict['hp'], self.player_dict['mp'], refresh=True)

    def refresh_level_and_exp(self):
        player_panel_renderer.draw_level_and_experience(self.player_dict['level'], self.player_dict['type'],
                                                        self.player_dict['experience'], refresh=True)

    def refresh_attributes(self):
        player_panel_renderer.draw_attributes(self.player_dict['attributes'], refresh=True)

    def refresh_conditions(self):
        player_panel_renderer.draw_conditions(self.player_dict['conditions'], refresh=True)

