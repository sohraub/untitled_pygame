import pygame as pg
from rendering import skill_tree_renderer


"""
Module to store functions which have to do with the skill tree, e.g. calling rendering functions, handling events
for allocating skill points, etc.
"""

class SkillTreeController:
    def __init__(self, skill_tree, profession, level, active_abilities, passive_abilities):
        self.skill_tree = skill_tree
        self.profession = profession
        self.level = level
        self.active_abilities = active_abilities
        self.passive_abilities = passive_abilities
        self.skill_rect_map = dict()
        self.level_up_points = 0

    def initialize_skill_tree(self, active_abilities, passive_abilities, skill_tree, profession, player_level):
        """Calls the function to render the skill tree."""
        self.skill_rect_map = skill_tree_renderer.draw_skill_tree(active_abilities, passive_abilities, skill_tree,
                                                                  profession, player_level)

    def handle_skill_tree_mouseover(self, skill_tree):
        mouse_pos = pg.mouse.get_pos()
        for key, rect in self.skill_rect_map.items():
            if rect.collidepoint(mouse_pos):
                # Todo: this condition is only while skill trees still have blank entries
                if skill_tree[key[0]][key[1]]['ability'] != '':
                    skill_tree_renderer.draw_ability_details_in_skill_tree(skill_tree[key[0]][key[1]]['ability'])

