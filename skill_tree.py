from rendering import skill_tree_renderer


"""
Module to store functions which have to do with the skill tree, e.g. calling rendering functions, handling events
for allocating skill points, etc.
"""

def initialize_skill_tree(active_abilities, passive_abilities, skill_tree, profession, player_level):
    """Calls the function to render the skill tree."""
    skill_tree_renderer.draw_skill_tree(active_abilities, passive_abilities, skill_tree, profession, player_level)

