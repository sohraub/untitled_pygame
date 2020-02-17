from rendering import console_renderer
"""
Class for the console that will display text based on what is happening in the game.
"""

class Console:
    def __init__(self):
        self.lines = ['' for _ in range(5)]

    def update_console(self, new_lines):
        for new_line in new_lines:
            self.lines.pop(0)
            self.lines.append(new_line)
        self.refresh_console()

    def refresh_console(self):
        console_renderer.render_console(self.lines)

