import os


"""
A very simple script to read boards drawn in Excel and saved as csv files.
Reads the csv and prints it out as a list, which can then be easily copied and saved in element_lists/board_templates.py
"""


if __name__ == '__main__':

    with open('board_creator.csv', 'r') as f:
        board = [x.strip().replace(',', '') for x in f.readlines()]

    for j in range(3):
        string = ' ' * 14
        if j == 0:
            string += "["
        else:
            string += ' '
        for i in range(5):
            string += f"'{board[i + 5*j]}', "
        if j == 2:
            string = string[:-2] + "]"
        print(string)
