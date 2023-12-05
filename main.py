"""
primary tasks like user input, game display/state, etc.
"""
import pygame as p
from Chess import engine, Robot
width = 512
height = 512
dimension = 8
square_size = height//dimension
images = {}

# initialize images
def image_load():
    drawings = ("bBishop", "bKing", "bHorse", "bPawn", "bQueen", "bRook", "wBishop", "wKing", "wHorse", "wPawn", "wQueen", "wRook")
    for piece in drawings:
        images[piece] = p.transform.scale(p.image.load("images/"+piece+".png"), (square_size, square_size))

"""
user input and graphical things below
"""

def central():
    p.init()
    screen = p.display.set_mode((width, height))
    # clock = p.time.Clock()
    screen.fill(p.Color("red"))
    gs = engine.gamestate()
    image_load()
    gameRunning = True
    chosen_square = ()
    legitMoves = gs.LegitMoves()
    moveCompleted = False
    clicks = []
    playerOne = False #if human, set true, if robot, set false
    playerTwo = False # ^^^^
    gameOver = False
    while gameRunning:
        realTurn = (gs.whiteMove and playerOne) or (not gs.whiteMove and playerTwo)
        for i in p.event.get():
            if i.type == p.QUIT:
                running = False
            elif i.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    loc = p.mouse.get_pos()
                    column = loc[0]//square_size
                    row = loc[1]//square_size # this uses the fact that all squares are the same size (effectively 8x8 coordinate plane)
                    if chosen_square == (row,column):
                        chosen_square = ()
                        clicks = []
                    else:
                        chosen_square = (row,column)
                        clicks.append(chosen_square)
                    if len(clicks) == 2:
                        move = engine.Move(clicks[0],clicks[1],gs.board)
                        print(move.ChessGrid())
                        if move in legitMoves:
                            gs.doMove(move)
                            moveCompleted = True
                            clicks = [] # resets clicks back to 0
                            chosen_square = ()
                    else: #if its invalid
                        clicks = [chosen_square]
            elif i.type == p.KEYDOWN:
                if i.key == p.K_u:
                    gs.undo()
                    moveCompleted = True
        if not realTurn:
            RobotMove = Robot.RandomMove(legitMoves)
            gs.doMove(RobotMove)
            moveCompleted = True
            p.time.delay(500)

        if moveCompleted:
            legitMoves = gs.LegitMoves()
            moveCompleted = False

        if gs.CheckMate:
            gameOver = True
            if gs.whiteMove:
                print("black wins!")
            else:
                print("white wins!")
        elif gs.StaleMate:
            gameOver = True
            print('stalemate!')
        CurrentGame(screen, gs)
        p.display.flip()

def CurrentGame(screen, gs):
    showBoard(screen)
    showPieces(screen, gs.board)

def showBoard(screen):
    colors = [p.Color("white"), p.Color("blue")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*square_size, r*square_size, square_size, square_size))
def showPieces(screen, board):
    for x in range(dimension):
        for y in range(dimension):
            piece = board[x][y]
            if piece != "__":
                screen.blit(images[piece], p.Rect((y)*square_size, (x)*square_size, square_size, square_size))

central()
