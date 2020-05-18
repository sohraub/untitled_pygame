"""
Module that will contains all the templates from which boards are loaded. These templates will then be organized into
lists that will be randomly chosen from on the creation of a new Board object.
"""

#### TEMPLATES ####
x = ['XXXXXXXXXXXXXXX',
     'XXXXXXXXXXXXXXX',
     'XXXXXXXXXXXXDXX',
     'XOOEOTOOOOOOOOX',
     'XOOOOOOOOOEOOOX',
     'XOOOOOEOOOOOOOX',
     'XXXXXXOOOXXXXXX',
     'XXXXXXOOOXXXXXX',
     'XXXXXXOORXXXXXX',
     'XXXXOOOOOOTXXXX',
     'XXXXOOOPOOOXXXX',
     'XXXXXXXDXXXXXXX',
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
     'XOOOOXXXXXOOOOX',
     'XOOOOXXXXXOOOOX',
     'XOOOOXXXXXOOOOX',
     'XOOOOXXXXXOOOOX',
     'XOOOROOOOOROOOX',
     'XTOOOOOOOOOOOTX',
     'XOOOOOOOPOOOOOX',
     'XXXXXXXXDXXXXXX']

testing = ['XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XTTTTTTTTTTTTTX',
           'XOOOOOOOOOOOOOX',
           'XXXXXXXOXXXXXXX',
           'XXXXXXXPXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX',
           'XXXXXXXXXXXXXXX']


TEMPLATE_LIST_MAP = {
    1: [x, y],
    # 1: [testing]
}

def get_board_list(tier):
    """Function which returns a list of every board template for a given tier."""
    return TEMPLATE_LIST_MAP[tier]