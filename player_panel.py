from rendering import player_panel_renderer

class PlayerPanel:
    def __init__(self, player):
        self.player = player
        self.player_dict = player.to_dict()
        player_panel_renderer.render_player_panel(self.player_dict)

    def refresh_hp_mp(self):
        player_panel_renderer.redraw_hp_mp(self.player_dict)

    def refresh_level_and_exp(self):
        player_panel_renderer.redraw_level_and_experience(self.player_dict)


