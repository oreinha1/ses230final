"""
  handles storage of information of the current state of the game
"""
class gamestate():
    def __init__(self):
        self.board = [ # maybe switch to an array
            ["bRook", "bHorse", "bBishop", "bQueen", "bKing", "bBishop", "bHorse", "bRook"],
            ["bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn"],
            ["__", "__", "__", "__", "__", "__", "__", "__" ],
            ["__", "__", "__", "__", "__", "__", "__", "__" ],
            ["__", "__", "__", "__", "__", "__", "__", "__" ],
            ["__", "__", "__", "__", "__", "__", "__", "__" ],
            ["wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn" ],
            ["wRook", "wHorse", "wBishop", "wQueen", "wKing", "wBishop", "wHorse", "wRook"]]
        self.whiteMove = True # white moves first
        self.moveLog = []
        self.moveMapping = {'P': self.pawnmovement, 'R': self.rookmovement, 'H': self.horsemovement,
                            'B': self.bishopmovement, 'Q': self.queenmovement, 'K': self.kingmovement}
        self.whiteKing = (7,4)
        self.blackKing = (0,4) # king location is important
        self.CheckMate = False
        self.StaleMate = False
    def doMove(self, move): # this doesn't work for special moves eg. castling
        self.board[move.startingRow][move.startingColumn] = "__"
        self.board[move.endingRow][move.endingColumn] = move.justmoved
        self.moveLog.append(move)
        self.whiteMove = not self.whiteMove
        if move.justmoved == 'wKing':
            self.whiteKing = (move.endingRow, move.endingColumn)
        if move.justmoved == 'bKing':
            self.blackKing = (move.endingRow, move.endingColumn)
    def undo(self):
        if len(self.moveLog) != 0: #can't undo when no move
            move = self.moveLog.pop()
            self.board[move.startingRow][move.startingColumn]=move.justmoved
            self.board[move.endingRow][move.endingColumn]=move.piecetaken
            self.whiteMove = not self.whiteMove #method to switch turns
            if move.justmoved == 'wKing':
                self.whiteKing = (move.startingRow, move.startingColumn)
            if move.justmoved == 'bKing':
                self.blackKing = (move.startingRow, move.startingColumn)
    def LegitMoves(self):
        moves = self.AllMoves()
        for k in range(len(moves)-1,-1,-1): # go backwards incase items repeat!
            self.doMove(moves[k])
            self.whiteMove = not self.whiteMove # the way inCheck works, it switches the turns, so it must be changed before called.
            if self.inCheck():
                moves.remove(moves[k])
            self.whiteMove = not self.whiteMove
            self.undo()
        if len(moves)==0: #zero left over moves means either a stalemate or a checkmate.
            if self.inCheck():
                self.CheckMate = True
            else:
                self.StaleMate = True
        else:
            self.CheckMate = False
            self.StaleMate = False
        return moves
    def inCheck(self):
        if self.whiteMove:
            return self.sqAttacked(self.whiteKing[0],self.whiteKing[1])
        else:
            return self.sqAttacked((self.blackKing[0]),self.blackKing[1])
    def sqAttacked(self,i,j):
        self.whiteMove = not self.whiteMove #basically checking from opponents pov
        enemyMoves = self.AllMoves()
        self.whiteMove = not self.whiteMove
        for move in enemyMoves:
            if move.endingRow == i and move.endingColumn == j:
                return True
        return False
    def AllMoves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                turn = self.board[i][j][0]
                if (turn == 'w' and self.whiteMove) or (turn == 'b' and not self.whiteMove):
                    piece = self.board[i][j][1]
                    self.moveMapping[piece](i,j,moves)
        return moves
    def pawnmovement(self, i, j, moves):
        if self.whiteMove:
            if self.board[i-1][j] == "__":
                moves.append(Move((i, j), (i-1, j), self.board))
                if i == 6 and self.board[i-2][j] == "__":
                    moves.append(Move((i, j), (i-2, j), self.board))
            if j-1 >= 0:
                if self.board[i-1][j-1][0] == 'b': # determines if there is an enemy piece in range
                    moves.append(Move((i, j), (i-1, j-1), self.board)) # forward and left
            if j+1 <= 7:
                if self.board[i-1][j+1][0] == 'b':
                    moves.append(Move((i, j), (i-1, j+1), self.board)) # forward and right
        else: # black movement
            if self.board[i+1][j] == "__":
                moves.append(Move((i,j),(i+1,j),self.board))
                if i == 1 and self.board[i+2][j]=="__":
                    moves.append(Move((i,j),(i+2,j),self.board))
            if j - 1 >=0:
                if self.board[i+1][j-1][0] == 'w':
                    moves.append(Move((i,j),(i+1,j-1),self.board)) #forward and left
            if j + 1 <= 7:
                if self.board[i+1][j+1][0] == 'w':
                    moves.append(Move((i,j),(i+1,j+1),self.board))
    def rookmovement(self, i, j, moves):
        vectors = ((-1,0),(0,-1),(1,0),(0,1))
        enemy = 'b' if self.whiteMove else 'w'
        for v in vectors:
            for k in range(1, 8):
                endingRow = i +v[0]*k
                endingColumn = j + v[1]*k
                if 0 <= endingRow < 8 and 0 <= endingColumn <8:
                    lastPiece = self.board[endingRow][endingColumn]
                    if lastPiece == "__":
                        moves.append(Move((i, j), (endingRow, endingColumn), self.board))
                    elif lastPiece[0] == enemy:
                        moves.append(Move((i, j), (endingRow, endingColumn), self.board))
                        break
                    else: #when its your own piece
                        break
                else: #when not on board
                    break
    def horsemovement(self, i, j, moves):
        hops = ((-2, -1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        friend = 'w' if self.whiteMove else 'b'
        for h in hops:
            endingRow = i + h[0]
            endingColumn = j + h[1]
            if 0 <= endingRow <8 and 0 <= endingColumn <8:
                lastPiece = self.board[endingRow][endingColumn]
                if lastPiece[0] != friend:
                    moves.append(Move((i, j), (endingRow, endingColumn), self.board))
    def bishopmovement(self, i, j, moves):
        vectors = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemy = 'b' if self.whiteMove else 'w'
        for v in vectors:
            for k in range(1, 8):
                endingRow = i +v[0]*k
                endingColumn = j + v[1]*k
                if 0 <= endingRow < 8 and 0 <= endingColumn <8:
                    lastPiece = self.board[endingRow][endingColumn]
                    if lastPiece == "__":
                        moves.append(Move((i, j), (endingRow, endingColumn), self.board))
                    elif lastPiece[0] == enemy:
                        moves.append(Move((i, j), (endingRow, endingColumn), self.board))
                        break
                    else: #when its your own piece
                        break
                else: #when not on board
                    break
    def queenmovement(self, i, j, moves):
        self.rookmovement(i,j,moves)
        self.bishopmovement(i,j,moves)

    def kingmovement(self, i, j, moves):
        movements = ((-1, -1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        friend = 'w' if self.whiteMove else 'b'
        for m in range(8):
            endingRow = i + movements[m][0]
            endingColumn = j + movements[m][1]
            if 0 <= endingRow <8 and 0 <= endingColumn <8:
                lastPiece = self.board[endingRow][endingColumn]
                if lastPiece[0] != friend:
                    moves.append(Move((i, j), (endingRow, endingColumn), self.board))
class Move():
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {d: p for p, d in ranksToRows.items()}
    filesToColumns = {"a":0, "b":1, "c":2, "d":3,
                      "e":4,"f":5, "g":6, "h":7}
    colsToFiles = {d: p for p, d in filesToColumns.items()}
    def __init__(self, start_square, end_square,board):
        self.startingRow=start_square[0]
        self.startingColumn=start_square[1]
        self.endingRow=end_square[0]
        self.endingColumn=end_square[1]
        self.justmoved = board[self.startingRow][self.startingColumn]
        self.piecetaken = board[self.endingRow][self.endingColumn]
        # self.moveName gives a unique numerical value for the completed move which shows it's movement. This is a huge shortcut for coding legal moves.
        self.moveName = self.startingRow * 1000 + self.startingColumn*100 + self.endingRow*10 + self.endingColumn
        print(self.moveName)
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveName == other.moveName
        return False
    def ChessGrid(self):
        return self.findRankFile(self.startingRow, self.startingColumn) + self.findRankFile(self.endingRow, self.endingColumn)

    def findRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
