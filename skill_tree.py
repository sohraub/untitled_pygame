import pygame as pg
from rendering import skill_tree_renderer


"""
Module to store functions which have to do with the skill tree, e.g. calling rendering functions, handling events
for allocating skill points, etc.
"""

class SkillTreeController:
    def __init__(self, skill_tree, profession, level, active_abilities, passive_abilities):
        """
        Class that handles all things skill tree, from allocating new points to displaying mouse-over info. Is saved
        as an attribute to the PlayerPanel, so that the panel can act as an intermediary that reads any changes made
        to the skill tree and applies it to the Player. Thus this class has no writing access to the Player class.
        This class only head read access to Player attributes which are stored as dicts.
        :param skill_tree: The player's full skill tree dict.
        :param profession: The player's profession.
        :param level: The player's current level.
        :param active_abilities: List of the player's active abilities
        :param passive_abilities: List of the player's passive abilities

        In addition to the above, the following attributes are set at initialization:
        :skill_rect_map: A dict containing key-value pairs of each ability and their respective rects as follows:
                            (tree_level, index_in_level): Rect(),
                         where tree_level is the level the ability appears in the skill tree, and index_in_level is
                         the array index of the ability in that tree level.
        :skill_points: Initialized to 0, the player gains 1 point every level-up. These points are used to allocate new
                       skills or skill levels in the tree.
        :tooltip_focus: Analogous to the same-named attribute in the player panel, this is initialized to None and is
                        re-assigned whenever an ability in the skill tree is moused over to the rect of that ability,
                        and set back to None when it is no longer being moused over.
        """
        self.skill_tree = skill_tree
        self.profession = profession
        self.level = level
        self.active_abilities = active_abilities
        self.passive_abilities = passive_abilities
        self.skill_rect_map = dict()
        self.skill_points = 0
        self.tooltip_focus = None
        # self.initialize_skill_tree()

    def render_skill_tree(self):
        """Calls the function to render the skill tree."""
        self.skill_rect_map = skill_tree_renderer.draw_skill_tree(self.active_abilities, self.passive_abilities,
                                                                  self.skill_tree, self.profession, self.level,
                                                                  self.skill_points)

    def handle_skill_tree_mouseover(self, skill_tree):
        """Calls function to display skill info tooltips on mouse-over"""
        mouse_pos = pg.mouse.get_pos()
        if self.tooltip_focus is not None and not self.tooltip_focus.collidepoint(mouse_pos):
            self.render_skill_tree()
            self.tooltip_focus = None

        if self.tooltip_focus is None:
            for key, rect in self.skill_rect_map.items():
                if rect.collidepoint(mouse_pos):
                    # Todo: this condition is only while skill trees still have blank entries
                    if skill_tree[key[0]][key[1]]['ability'] != '':
                        skill_tree_renderer.draw_ability_details_in_skill_tree(skill_tree[key[0]][key[1]]['ability'])
                    self.tooltip_focus = rect

    def allocate_skill_points(self):
        """
        Allocates skill points to the skill being moused over, if any, and only if the player has skill points to
        spend and the skill is not already at max level.
        """
        if self.tooltip_focus is None or self.skill_points == 0:
            return False
        ability = None
        for (tree_level, index), value in self.skill_rect_map.items():
            if value == self.tooltip_focus:
                ability = self.skill_tree[tree_level][index]
                break
        if ability['skill_level'] < 3:
            # Also check that player meets the level requirement and the ability hasn't been disabled
            if self.level >= ability['level_prereq'] and not ability.get('disabled', False):
                ability['skill_level'] += 1
                self.skill_points -= 1
                self.render_skill_tree()
                return True
        return False
