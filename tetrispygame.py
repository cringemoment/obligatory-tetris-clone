from random import choice
import keyboard
import pygame
from copy import deepcopy
import time

das = 83
softdropdelay = 0

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
boardheight = 15
defaultboardcharacter = ","
board = [[defaultboardcharacter for idea in range(boardlength)] for i in range(boardheight)]
nopieceboard = deepcopy(board)
startx = 150
starty = 180
blocksize = 32
blockwidth = 2

pygame.init()
s = pygame.display.set_mode((boardlength * blocksize + 10 * blocksize + 100, boardheight * blocksize + 8 * blocksize))
s.fill((20, 20, 20))

#Define color codes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 100, 0)
RESET = (20, 20, 20)

# Define the pieces dictionary with color codes as keys
pieces = {
    'I': {
        'shape': [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
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
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ],
        'color': RED
    },
    defaultboardcharacter : {
        'shape' : [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ],
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

ogbag = [char for char in "IOSZJLT"]
bag = deepcopy(ogbag)

def piecepick():
    global bag
    piecepicked = choice(bag)
    bag.remove(piecepicked)
    if(len(bag) == 0):
        bag = deepcopy(ogbag)
    return piecepicked

holdpiece = ""
currentpiece = piecepick()
queue = [piecepick() for i in range(5)]
currentpiecerotation = 0
currentpiecex = 3
currentpiecey = 0

def reset():
    global holdpiece, currentpiece, queue, currentpiecerotation, currentpiecex, currentpiecey, nopieceboard, board
    holdpiece = ""
    currentpiece = piecepick()
    queue = [piecepick() for i in range(5)]
    currentpiecerotation = 0
    currentpiecex = 3
    currentpiecey = 0
    nopieceboard = [[defaultboardcharacter for idea in range(boardlength)] for i in range(boardheight)]
    board = deepcopy(nopieceboard)
    drawallpieces()
    drawinfopieces(-3, -3, defaultboardcharacter)
    for pieceindex, piece in enumerate(queue):
        drawinfopieces(-3 + pieceindex * 3, boardlength + 2, defaultboardcharacter)
    bag = deepcopy(ogbag)

def kicksubtract(kicktable1, kicktable2):
    subtractedkicktable = []
    for kick1, kick2 in zip(kicktable1, kicktable2):
        subtractedkicktable.append([kick1[0] - kick2[0], kick1[1] - kick2[1]])
    return subtractedkicktable

def rotatepiece(rotation):
    global currentpiecerotation, currentpiecex, currentpiecey
    plsbreak = False
    kicks = kicksubtract(srskicktable[currentpiece][currentpiecerotation], srskicktable[currentpiece][(currentpiecerotation + rotation) % 4])
    #print(kicks)
    for offset in kicks:
        if placeable(currentpiece, (currentpiecerotation + rotation) % 4, currentpiecex + offset[0], currentpiecey + (offset[1] * -1)):
            #print(f"offset of {offset[0]}x and {(offset[1] * -1)}y works")
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

def move(distance):
    global currentpiecerotation, currentpiecex
    if placeable(currentpiece, currentpiecerotation, currentpiecex + distance, currentpiecey):
        currentpiecex += distance

def move_left():
    move(-1)

def move_right():
    move(1)

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
    drawallpieces()
    drawqueue()

def softdrop():
    global currentpiecey
    while placeable(currentpiece, currentpiecerotation, currentpiecex, currentpiecey):
        currentpiecey += 1
    currentpiecey -= 1
    drawallpieces()

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
    drawinfopieces(-3, -3, defaultboardcharacter)
    drawinfopieces(-3, -3, holdpiece)

running = True

def grid(startx, starty, boardlength, boardheight, blocksize, blockwidth):
    for i in range(startx, startx + (boardlength * blocksize), blocksize):
        for j in range(starty, starty + (boardheight * blocksize), blocksize):
            rect = pygame.Rect(i, j, blocksize, blocksize)
            pygame.draw.rect(s, (255, 255, 255), rect, blockwidth)

def blockrenderer(x, y, color, smaller = False):
    global startx, starty, blocksize, blockwidth
    if(smaller):
        block = pygame.Rect(startx + (x * blocksize) + blocksize // 4, starty + (y * blocksize) + blocksize // 4, blocksize // 2, blocksize // 2)
    else:
        block = pygame.Rect(startx + (x * blocksize), starty + (y * blocksize), blocksize, blocksize)
    pygame.draw.rect(s, color, block, blocksize - 1)

def drawinfopieces(x, y, piece):
    currentpieceboard = pieces[piece]["shape"]

    for piecerowindex, piecerow in enumerate(currentpieceboard):
        for piececolumnindex, piecevalue in enumerate(piecerow):
            if(piecevalue == 1):
                blockrenderer(y + piececolumnindex, x + piecerowindex, pieces[piece]["color"])

def drawallpieces():
    global board
    putpiece(currentpiece, currentpiecerotation, currentpiecex, currentpiecey, board)
    for boardcolumnindex, boardcolumn in enumerate(board):
        for boardrowindex, boardvalue in enumerate(boardcolumn):
            blockrenderer(boardrowindex, boardcolumnindex, pieces[boardvalue]["color"])
    grid(startx, starty, boardlength, boardheight, blocksize, blockwidth)
    clear_filled_rows(nopieceboard)

    board = deepcopy(nopieceboard)
    if(len(queue) < 5):
        queue.append(piecepick())

    drawqueue()

def drawqueue():
    for pieceindex, piece in enumerate(queue):
        drawinfopieces(-3 + pieceindex * 3, boardlength + 2, defaultboardcharacter)
        drawinfopieces(-3 + pieceindex * 3, boardlength + 2 + (4 - len(pieces[piece]["shape"][0])), piece)

putpiece(currentpiece, currentpiecerotation, currentpiecex, currentpiecey)
drawallpieces()

dastimer = 0
softdroptimer = 0

dohold = {
"move_left" : {
    "timer" : "dastimer",
    "delay" : "das"
},
"move_right" : {
    "timer" : "dastimer",
    "delay" : "das"
},
"softdrop" : {
    "timer" : "softdroptimer",
    "delay" : "softdropdelay"
},
}

keyspressed = []

while running:
    for key in controls:
        if(keyboard.is_pressed(key)):
            drawallpieces()
            if(key in keyspressed):
                if(controls[key] in dohold):
                    if(eval(f"time.time() * 1000 > {dohold[controls[key]]['timer']} + {dohold[controls[key]]['delay']}")):
                        exec(f"{controls[key]}()")
            else:
                exec(f"{controls[key]}()")
                keyspressed.append(key)
                drawallpieces()
                if(controls[key] in dohold):
                    exec(f"{dohold[controls[key]]['timer']} = time.time() * 1000")
        else:
            try:
                keyspressed.remove(key)
            except ValueError:
                pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
