"""
Module that will contains all the templates from which boards are loaded. These templates will then be organized into
lists that will be randomly chosen from on the creation of a new Board object.
"""

#### TEMPLATES ####
starting_board = ['XXXXXXXXXXXXXXX',
                  'XXXXXXXXXXXXXXX',
                  'XXXXXXXXXXXXDXX',
                  'DOOEOTOOOOOOOOX',
                  'XOOOOOOOOOEOOOD',
                  'XOOOOOEOOOOOOOX',
                  'XXXXXXOOOXXXXXX',
                  'XXXXXXOOOXXXXXX',
                  'XXXXXXOORXXXXXX',
                  'XXXXOOOOOOTXXXX',
                  'XXXXOOOPOOOXXXX',
                  'XXXXXXXXXXXXXXX',
                  'XXXXXXXXXXXXXXX',
                  'XXXXXXXXXXXXXXX',
                  'XXXXXXXXXXXXXXX']

y = ['XXDXXXXXXXXXDXX',
     'XOOOOXXXXXOOOOX',
     'XOOEOXXXXXOEOOX',
     'XOOOOXXXXXOOOOX',
     'XOOOOXXXXXOOOOX',
     'XOOOOXXXXXOOOOX',
     'XOOOOXXXXXOOOOX',
     'XOOOOXXXXXOOOOD',
     'XOOOOXXXXXOOOOX',
     'XOOOOXXXXXOOOOX',
     'XOOOOXXXXXOOOOX',
     'XOOOROOOOOROOOX',
     'XTOOOOOOOOOOOTX',
     'XOOOOOOOOOOOOOX',
     'XXXXXXXXDXXXXXX']

z = ['XXXXXXXXXXXXXDX',
     'XXXXTOOOOOOOOOX',
     'XXXXOOOOEOOOOOX',
     'XXXXTOOOOOOOOOX',
     'XXXXXXXOOOROEOX',
     'XXTXXXXOEOOOOOX',
     'XXEXXXXOOOOOOOX',
     'XXOXXXXOOROOOOX',
     'XXRXXXXOOOOOOXX',
     'XXOOOOOOOOOOOXX',
     'XXXXXXXXOOOOOXX',
     'XXXXXXXXOOOOOXX',
     'XXXXXXXXXOOOOXX',
     'XXXXXXXXXXOOOXX',
     'XXXXXXXXXXXDXXX']

a = ['XXXXXXXXXXXXXXX',
     'XXXXTOOOOOOOOTX',
     'XXXXROOOOEOOOOX',
     'XXXXOOOOOOOOOOX',
     'XXXXOEOOOROOOOX',
     'XXXXOOOOOOOOOOD',
     'XOOOOOOOOOOEOOX',
     'XOOOOOOOOOOOOOX',
     'XOOOROOOXXXXXXX',
     'XOOOOOOOXXXXXXX',
     'DOOOOOOOXXXXXXX',
     'XOOXXXXXXXXXXXX',
     'XOOXXXXXXXXXXXX',
     'XOEXXXXXXXXXXXX',
     'XXXXXXXXXXXXXXX']


testing = ['XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXDXXXXXX',
           'XXXXXXXDEXXXXXX',
           'XXXXXXXXREDXXXX',
           'XXXXXXXXPXXXXXX',
           'XXXXXXXXDXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX']


TEMPLATE_LIST_MAP = {
    0: [starting_board],
    1: [y, z, a],
    # 1: [testing]
}

def get_board_list(tier):
    """Function which returns a list of every board template for a given tier."""
    return TEMPLATE_LIST_MAP[tier]