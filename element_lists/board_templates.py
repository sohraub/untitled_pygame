"""
Module that will contains all the templates from which boards are loaded. These templates will then be organized into
lists that will be randomly chosen from on the creation of a new Board object. The first board in a game will always
be starting_board below, and the subsequent ones are chosen randomly from the templates list.
"""

#### TEMPLATES ####
starting_board = ['XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXDXX', 'DOOEOTOOOOOOOOX', 'XOOOOOOOOOEOOOD',
                  'XOOOOOEOOOOOOOX', 'XXXXXXOOOXXXXXX', 'XXXXXXOOOXXXXXX', 'XXXXXXOORXXXXXX', 'XXXXOOOOOOTXXXX',
                  'XXXXOOOPOOOXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX']

templates = [ ['XXDXXXXXXXXXDXX', 'XOOOOXXXXXOOOOX', 'XOOEOXXXXXOEOOX', 'XOOOOXXXXXOOOOX', 'XOOOOXXXXXOOOOX',
               'XOOOOXXXXXOOOOX', 'XOOOOXXXXXOOOOX', 'XOOOOXXXXXOOOOD', 'XOOOOXXXXXOOOOX', 'XOOOOXXXXXOOOOX',
               'XOOOOXXXXXOOOOX', 'XOOOROOOOOROOOX', 'XTOOOOOOOOOOOTX', 'XOOOOOOOOOOOOOX', 'XXXXXXXXDXXXXXX'],
              ['XXXXXXXXXXXXXDX', 'XXXXTOOOOOOOOOX', 'XXXXOOOOEOOOOOX', 'XXXXTOOOOOOOOOX', 'XXXXXXXOOOROEOX',
               'XXTXXXXOEOOOOOX', 'XXEXXXXOOOOOOOX', 'XXOXXXXOOROOOOX', 'XXRXXXXOOOOOOXX', 'XXOOOOOOOOOOOXX',
               'XXXXXXXXOOOOOXX', 'XXXXXXXXOOOOOXX', 'XXXXXXXXXOOOOXX', 'XXXXXXXXXXOOOXX', 'XXXXXXXXXXXDXXX'],
              ['XXXXXXXXXXXXXXX', 'XXXXTOOOOOOOOTX', 'XXXXROOOOEOOOOX', 'XXXXOOOOOOOOOOX', 'XXXXOEOOOROOOOX',
               'XXXXOOOOOOOOOOD', 'XOOOOOOOOOOEOOX', 'XOOOOOOOOOOOOOX', 'XOOOROOOXXXXXXX', 'XOOOOOOOXXXXXXX',
               'DOOOOOOOXXXXXXX', 'XOOXXXXXXXXXXXX', 'XOOXXXXXXXXXXXX', 'XOEXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX'],
              ['XXXXXXXXXDXXXXX', 'XOOOOOOOOOXXXXX', 'XOOOOOOOOOXXXXX', 'XOOOOOOOOOXXXXX', 'XOOOOXXXXXXOOOX',
               'XOOOOXXORXXOOOD', 'XEOOEXXOTXXOOOX', 'XOOOOXXXXXXOOOX', 'XOOOOXXXXXXOEOX', 'XOOOOOOOOOOOOOX',
               'XOOOOOOOOEOOOOX', 'XOOOOOOOOOOOOOX', 'XROOOXXXXOOOOOX', 'XTOOOXXXXOOORTX', 'XXXXXXXXXXXXXXX'],
              ['XXXXXXXXXXXXXXX', 'XOOOOOOOOOOOETX', 'XOOOOOOROOOOOOX', 'DOOOOOOOOOEOOOX', 'XOOOOXXXXXOOOOX',
               'XOOOOXXXXXOOOOX', 'XOOOOXXOXXOOOOX', 'XOROOXXTXXOOROX', 'XOOOOXXOXXOOOOX', 'XOOOOXXXXXOOOOX',
               'XOOOOXXXXXOOOOX', 'XOOOEOOOOOOOOOX', 'XOOOOOROOOOOOOX', 'XTEOOOOOOOOOOOX', 'XXXXXXXXXXXDXXX'],
              ['XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX',
               'XXXXXXXXXXXXXXX', 'XXXXXTOTOTXXXXX', 'XXXXXOEEEOXXXXX', 'DOOOROOOOOXXXXX', 'XOOOOOOOOOXXXXX',
               'XOOOEOOOOOXXXXX', 'XXXXOROOOOXXXXX', 'XXXXOOOOOOXXXXX', 'XXXXOOOOOOXXXXX', 'XXXXXXXXDXXXXXX'],
              ['XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXDXXXXXXX', 'XXXXXOOOOOXXXXX',
               'XXXXXOOOOOXXXXX', 'XXXOOOEOOROOXXX', 'XXDOOOOTOOOODXX', 'XXXOOROOEOOOXXX', 'XXXXXOOOOOXXXXX',
               'XXXXXOOOOOXXXXX', 'XXXXXXXDXXXXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX'],
              ['XXXXXXXDXXXXXXX', 'XXXXXOOOOOXXXXX', 'XXXXXOOOOOXXXXX', 'XXXXXOOOOOXXXXX', 'XXXXXOOOOOXXXXX',
               'XXXXXOOORTXXXXX', 'XXXXXXOEOXXXXXX', 'XXXXXXXOXXXXXXX', 'XXXXXXXRXXXXXXX', 'XXXXXXOEOXXXXXX',
               'XXXXXTROOOXXXXX', 'XXXXXOOOOOXXXXX', 'XXXXXOOOOOXXXXX', 'XXXXXOOOOOXXXXX', 'XXXXXXXDXXXXXXX']
              ]


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


def get_board_list(tier):
    """Function which returns a list of every board non-starting template."""
    return templates