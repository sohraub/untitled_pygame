from time import sleep
from rendering import console_renderer


class Console:
    def __init__(self):
        """
        Class for the console that will display text based on what is happening in the game.

        The following attributes are set and used by methods outside of init:
        :lines: A list of strings which will be displayed in the console.
        """
        self.lines = ['' for _ in range(5)]

    def refresh_console(self):
        """Method to call the console renderer with the new lines."""
        console_renderer.render_console(self.lines)

    def update(self, lines):
        """
        Accepts new lines, casting it to a single-item list if lines is just a string. Then adds new lines to console
        and refreshes it
        """
        if type(lines) == str:
            new_lines = [lines]
        else:
            new_lines = lines

        if new_lines:
            for new_line in new_lines:
                self.lines.pop(0)
                self.lines.append(new_line)
                self.refresh_console()
                sleep(0.25)
