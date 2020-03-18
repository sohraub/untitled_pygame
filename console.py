from rendering import console_renderer


class Console:
    def __init__(self):
        """
        Class for the console that will display text based on what is happening in the game.

        The following attributes are set and used by methods outside of init:
        :lines: A list of strings which will be displayed in the console.
        """
        self.lines = ['' for _ in range(5)]

    def update_console(self, new_lines):
        """
        A method to update the console with new lines. Console only displays 5 lines at a time, so adding a new
        line pops the oldest one in the list.
        """
        for new_line in new_lines:
            self.lines.pop(0)
            self.lines.append(new_line)
        self.refresh_console()

    def refresh_console(self):
        """Method to call the console renderer with the new lines."""
        console_renderer.render_console(self.lines)

