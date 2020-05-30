import os


"""
A very simple script to read boards drawn in Excel and saved as csv files.
Reads the csv and prints it out as a list, which can then be easily copied and saved in element_lists/board_templates.py
"""


if __name__ == '__main__':

    with open('board_creator.csv', 'r') as f:
        board = [x.strip().replace(',', '') for x in f.readlines()]

    for i, line in enumerate(board):
        if i == 0:
            print(f"['{line}',")
        elif i == len(board) - 1:
            print(f" '{line}']")
        else:
            print(f" '{line}',")
