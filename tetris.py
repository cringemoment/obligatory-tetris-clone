from random import choice
import keyboard
from copy import deepcopy

controls = {
"left" : "move_left",
"right" : "move_right",
"w" : "reset",
"up" : "clockwise_rotate",
"s" : "counterlockwise_rotate",
"d" : "full_rotate",
"x" : "harddrop",
"down" : "softdrop",
"z": "hold"
}

srskicktable = {
"J" : {
    0 : [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    1 : [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    2 : [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    3 : [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
},
"L" : {
    0 : [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    1 : [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    2 : [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    3 : [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
},
"S" : {
    0 : [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    1 : [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    2 : [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    3 : [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
},
"T" : {
    0 : [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    1 : [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    2 : [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    3 : [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
},
"Z" : {
    0 : [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    1 : [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    2 : [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
    3 : [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]
},
"I" : {
    0 : [[0, 0], [-1, 0], [2, 0], [-1, 0], [2, 0]],
    1 : [[-1, 0], [0, 0], [0, 0], [0, 1], [0, -2]],
    2 : [[-1, 1], [1, 1], [-2, 1], [1, 0], [-2, 0]],
    3 : [[0, 1], [0, 1], [0, 1], [0, -1], [0, 2]]
},
"O" : {
    0 : [[0, 0]],
    1 : [[0, -1]],
    2 : [[-1, -1]],
    3 : [[-1, 0]]
}
}

boardlength = 10
boardheight = 8
defaultboardcharacter = ","
board = [[defaultboardcharacter for idea in range(boardlength)] for i in range(boardheight)]
#board[6][2] = "J"
#board[7][4] = "J"
nopieceboard = deepcopy(board)

#Define color codesz
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
ORANGE = '\033[38;2;255;165;0m'

# Define the pieces dictionary with color codes as keys
pieces = {
    'I': {
        'shape': [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'color': CYAN
    },
    'J': {
        'shape': [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        'color': BLUE
    },
    'L': {
        'shape': [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ],
        'color': ORANGE
    },
    'O': {
        'shape': [
            [1, 1],
            [1, 1]
        ],
        'color': YELLOW
    },
    'S': {
        'shape': [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ],
        'color': GREEN
    },
    'T': {
        'shape': [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        'color': MAGENTA
    },
    'Z': {
        'shape': [
            [0, 0, 0],
            [1, 1, 0],
            [0, 1, 1]
        ],
        'color': RED
    },
    defaultboardcharacter : {
        'color': RESET
    }
}

def rotate(matrix):
    transposed = list(zip(*matrix))
    rotated = [list(row[::-1]) for row in transposed]
    return rotated

def placeable(piece, rotation, column, row):
    currentpieceboard = deepcopy(pieces[piece]["shape"])

    for i in range(rotation):
        currentpieceboard = rotate(currentpieceboard)

    for piecerowindex, piecerow in enumerate(currentpieceboard):
        for piececolumnindex, piecevalue in enumerate(piecerow):
            if(piecevalue == 1):
                if(column + piececolumnindex < 0 or row + piecerowindex < 0):
                    return False
                if(row + piecerowindex >= boardheight):
                    return False
                if(column + piececolumnindex >= boardlength):
                    return False
                if(nopieceboard[row + piecerowindex][column + piececolumnindex] != defaultboardcharacter):
                    return False
    return True

def putpiece(piece, rotation, column, row, board = board):
    if(placeable(piece, rotation, column, row)):
        currentpieceboard = pieces[piece]["shape"].copy()

        for i in range(rotation):
            currentpieceboard = rotate(currentpieceboard)

        for piecerowindex, piecerow in enumerate(currentpieceboard):
            for piececolumnindex, piecevalue in enumerate(piecerow):
                if(piecevalue == 1):
                    board[row + piecerowindex][column + piececolumnindex] = piece

def get_filled_rows(board):
    filled_rows = []
    for row in board:
        if all(square != defaultboardcharacter for square in row):
            filled_rows.append(board.index(row))
    return filled_rows

def clear_filled_rows(board):
    filled_rows = get_filled_rows(board)
    for row in filled_rows:
        del board[row]
        board.insert(0, [defaultboardcharacter for _ in range(boardlength)])


def printboard():
    global board
    print(f"Hold: {holdpiece}|Queue: {''.join(queue)}")
    putpiece(currentpiece, currentpiecerotation, currentpiecex, currentpiecey, board)
    print("----------------------")
    for row in board:
        print("|", end = "")
        for square in row:
            print(pieces[square]["color"] + square, end = " ")
        print("|")
    print("----------------------")
    clear_filled_rows(nopieceboard)
    board = deepcopy(nopieceboard)
    if(len(queue) < 5):
        queue.append(piecepick())

ogbag = [char for char in "IOSZJLT"]
bag = deepcopy(ogbag)

def piecepick():
    global bag
    piecepicked = choice(bag)
    bag.remove(piecepicked)
    if(len(bag) == 0):
        bag = deepcopy(ogbag)
    return piecepicked

currentpiece = piecepick()
#currentpiece = "S"
queue = [piecepick() for i in range(5)]

holdpiece = ""
currentpiecerotation = 0
currentpiecex = 3
currentpiecey = 0

printboard()

def reset():
    raise SystemExit(0)

def kicksubtract(kicktable1, kicktable2):
    subtractedkicktable = []
    for kick1, kick2 in zip(kicktable1, kicktable2):
        subtractedkicktable.append([kick1[0] - kick2[0], kick1[1] - kick2[1]])
    return subtractedkicktable

def rotatepiece(rotation):
    global currentpiecerotation, currentpiecex, currentpiecey
    plsbreak = False
    kicks = kicksubtract(srskicktable[currentpiece][currentpiecerotation], srskicktable[currentpiece][(currentpiecerotation + rotation) % 4])
    print(kicks)
    for offset in kicks:
        if placeable(currentpiece, (currentpiecerotation + rotation) % 4, currentpiecex + offset[0], currentpiecey + (offset[1] * -1)):
            print(f"offset of {offset[0]}x and {(offset[1] * -1)}y works")
            currentpiecex += offset[0]
            currentpiecey += (offset[1] * -1)
            currentpiecerotation = (currentpiecerotation + rotation) % 4
            break

def clockwise_rotate():
    rotatepiece(1)

def counterlockwise_rotate():
    rotatepiece(-1)

def full_rotate():
    rotatepiece(2)

def move_left():
    global currentpiecerotation, currentpiecex
    if placeable(currentpiece, currentpiecerotation, currentpiecex - 1, currentpiecey):
        currentpiecex -= 1

def move_right():
    global currentpiecerotation, currentpiecex
    if placeable(currentpiece, currentpiecerotation, currentpiecex + 1, currentpiecey):
        currentpiecex += 1

def harddrop():
    global currentpiece, currentpiecerotation, currentpiecex, currentpiecey
    while placeable(currentpiece, currentpiecerotation, currentpiecex, currentpiecey):
        currentpiecey += 1
    currentpiecey -= 1
    putpiece(currentpiece, currentpiecerotation, currentpiecex, currentpiecey, nopieceboard)
    currentpiece = queue[0]
    queue.pop(0)
    currentpiecerotation = 0
    currentpiecex = 3
    currentpiecey = 0
    board = deepcopy(nopieceboard)
    printboard()

def softdrop():
    global currentpiecey
    while placeable(currentpiece, currentpiecerotation, currentpiecex, currentpiecey):
        currentpiecey += 1
    currentpiecey -= 1
    printboard()

def hold():
    global currentpiece, holdpiece, currentpiecerotation, currentpiecex, currentpiecey
    if(holdpiece == ""):
        holdpiece = currentpiece
        currentpiece = queue[0]
        queue.pop(0)
        queue.append(piecepick())
    else:
        holdpiece, currentpiece = currentpiece, holdpiece

    currentpiecerotation = 0
    currentpiecex = 3
    currentpiecey = 0

keyspressed = []
while True:
    for key in controls:
        if(keyboard.is_pressed(key)):
            if(key in keyspressed):
                pass
            else:
                exec(f"{controls[key]}()")
                keyspressed.append(key)
                printboard()
        else:
            try:
                keyspressed.remove(key)
            except ValueError:
                pass

import pygame
import os
import pyperclip

running = True

startx = 150
starty = 180
blocksx = 10
blocksy = 7
blocksize = 32
blockwidth = 2

pygame.init()
s = pygame.display.set_mode((blocksx * blocksize + 10 * blocksize, blocksy * blocksize + 18 * blocksize))
s.fill((20, 20, 20))

def grid(startx, starty, blocksx, blocksy, blocksize, blockwidth):
    for i in range(startx, startx + (blocksx * blocksize), blocksize):
        for j in range(starty, starty + (blocksy * blocksize), blocksize):
            rect = pygame.Rect(i, j, blocksize, blocksize)
            pygame.draw.rect(s, (255, 255, 255), rect, blockwidth)

cpx = 0
cpy = 0

def blockrenderer(x, y, color, smaller = False):
    global startx, starty, blocksize, blockwidth
    if(smaller):
        block = pygame.Rect(startx + (x * blocksize) + blocksize // 4, starty + (y * blocksize) + blocksize // 4, blocksize // 2, blocksize // 2)
    else:
        block = pygame.Rect(startx + (x * blocksize), starty + (y * blocksize), blocksize, blocksize)
    pygame.draw.rect(s, color, block, blocksize - 1)

piecesindex = {
    "I": (0, 255, 255),
    "Z": (255, 0, 0),
    "S": (0, 255, 0),
    "J": (0, 0, 255),
    "L": (255, 100, 0),
    "T": (255, 0, 255),
    "O": (255, 255, 0),
    "G": (156, 156 , 156),
    " ": (20, 20, 20)
}

pieces = "IZSJLTOG "

rotation = 0

currentx = 0

piece = 0

smaller = False

filledpieces = []

def drawallpieces():
    for i in filledpieces:
        blockrenderer(i[0], i[1], piecesindex[i[2]], i[3])

def createcolorsquares():
    for v, i in enumerate(piecesindex):
        blockrenderer(blocksx + 2, v, piecesindex[i])

    blockrenderer(blocksx + 2, len(pieces) + 2, (255, 255, 255), smaller)

    blockrenderer(blocksx + 2, len(pieces) + 4, (0, 0, 255))

    blockrenderer(blocksx + 2, len(pieces) + 6, (255, 0, 255))

board = [["  " for i in range(blocksx)] for i in range(blocksy)]

def makeboard():
    for i in filledpieces:
        board[i[1]][i[0]] = str(i[2]) + "1" if (i[3]) else str(i[2]) + "0"

seperateframe = Faxzlsse

while running:
    s.fill((30, 30, 30))
    makeboard()
    grid(startx, starty, blocksx, blocksy, blocksize, blockwidth)
    createcolorsquares()

    drawallpieces()

    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0]:
            pos = list(pygame.mouse.get_pos())
            pos[0] = (pos[0] - startx) // blocksize
            pos[1] = (pos[1] - starty) // blocksize

            if(pos[0] >= 0 and pos[0] < blocksx and pos[1] >= 0 and pos[1] < blocksy):
                filledpieces.append([pos[0], pos[1], pieces[piece], smaller])

            if(pos[0] == blocksx + 2 and pos[1] >= 0 and pos[1] < len(pieces)):
                piece = pos[1]

            if(pos[0] == blocksx + 2 and pos[1] >= 0 and pos[1] == len(pieces) + 2):
                smaller = not smaller

            if(pos[0] == blocksx + 2 and pos[1] >= 0 and pos[1] == len(pieces) + 4):
                outputcode()

            if(pos[0] == blocksx + 2 and pos[1] >= 0 and pos[1] == len(pieces) + 6):
                filledpieces = []
                board = [["  " for i in range(blocksx)] for i in range(blocksy)]

        if event.type == pygame.QUIT:
            running = False

    grid(startx, starty, blocksx, blocksy, blocksize, blockwidth)

    #rendering the screen; keep last
    pygame.display.update()
