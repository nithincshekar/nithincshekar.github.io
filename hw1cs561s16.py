import sys
from decimal import Decimal

MINIMUM_INT = Decimal("-inf")
MAXIMUM_INT = Decimal("inf")
GREEDY = 1
MINIMAX = 2
ALPHABETA = 3 

def TraverseLog(node,ab=False):
    i = node.pos[0]
    j = node.pos[1]
    dep = node.depth
    val = node.score
    s = ""
    if 0 == j:
        s = "A"+str(i+1)+","+str(dep)+","+str(val)
    elif 1 == j:
        s = "B"+str(i+1)+","+str(dep)+","+str(val)
    elif 2 == j:
        s = "C"+str(i+1)+","+str(dep)+","+str(val)
    elif 3 == j:
        s = "D"+str(i+1)+","+str(dep)+","+str(val)
    elif 4 == j:
        s = "E"+str(i+1)+","+str(dep)+","+str(val)
    else:
        s = "root"+","+str(dep)+","+str(val)
    if ab:
        s += ","+str(node.alpha)+","+str(node.beta)
    return s

def SwapPlayer(pPlayer):
    if 'O' == pPlayer:
        return 'X'
    else:
        return 'O'

class AIHW1(object):
    def __init__(self, prob_file):
        with open(prob_file) as f:
            lines = f.readlines()
            count = 0
            self.strategy = int(lines[0].strip())
            if self.strategy >= 4:
                self.firstPlayer = lines[1].strip()
                self.secondPlayer = lines[4].strip()
                self.firstPlayerAlgo = int(lines[2].strip())
                self.secondPlayerAlgo = int(lines[5].strip())
                self.firstPlayerCutOff = int(lines[3].strip())
                self.secondPlayerCutOff = int(lines[6].strip())
                count = 7

            if self.strategy <= 3:
                self.myPiece = lines[1].strip()
                self.oppPiece = SwapPlayer(self.myPiece)
                self.cutoff = int(lines[2].strip())
                count = 3

            self.costs = [[int(j) for j in lines[count + i].strip().split()]
                          for i in range(5)]
            count = count + 5

            self.state = [[j for j in lines[count + i].strip()]
                              for i in range(5)]

    def isTerminal(self, state,debug = False):
        bRes = True
        for i, j in self.Update():
            if state[i][j] == '*':
                return False
        return bRes

    def printState(self, state, fileName,debug = False):
        res = ""
        i = 0
        j = 0
        for row in state:
            for cell in row:
                res += str(cell)
            res += "\n"
        if fileName:
            with open(fileName, 'w') as w:
                w.write(res)
        return res

    def Calculate(self, state,player,debug = False):
        score = 0
        oppPlayer = SwapPlayer(player)
        for (i,j) in self.Update():
            if state[i][j] == oppPlayer:
                score = score - self.costs[i][j]
            elif state[i][j] == player:
                    score = score + self.costs[i][j]
        return score

    def Update(self,debug = False):
        res = []
        for i in range(5):
            for j in range(5):
                res.append((i, j))
        return res

    def PlaceableCells(self, state,debug = False):
        res = []
        for i in range(5):
           for j in range(5):
                if '*' == state[i][j]:
                    res.append((i, j))
        return res

    def Attack(self, state, row, col, playerPiece,debug = False):
        ReLog = []
        oppPiece = SwapPlayer(playerPiece)
        if state[row][col] == '*':
            self.state[row][col] = playerPiece
            ReLog.append((row, col, '*'))

            Negihbours = []
            Negihbours.append((row-1, col))
            Negihbours.append((row+1, col))
            Negihbours.append((row, col-1))
            Negihbours.append((row, col+1))
            raid = False
            oppCells = []
            for pos in Negihbours:
                if 0 <= pos[0]:
                    if pos[0] < 5:
                        if 0 <= pos[1]:
                           if pos[1] < 5:
                                if state[pos[0]][pos[1]] == oppPiece:
                                    oppCells.append((pos[0], pos[1]))
                                elif state[pos[0]][pos[1]] == playerPiece:
                                    raid = True
            if raid:
                for x, y in oppCells:
                    state[x][y] = playerPiece
                    ReLog.append((x, y, oppPiece))
        return ReLog


    def greedyBFS(self,player,debug = False):
        oppPiece = SwapPlayer(player)
        heuristic = [[None for j in range(5)] for i in range(5)]

        currentScore = self.Calculate(self.state,player)
        for i, j in self.Update():
            if self.state[i][j] == '*':  

                heuristic[i][j] = currentScore + self.costs[i][j]

                Neighbours = []
                Neighbours.append((i-1, j))
                Neighbours.append((i+1, j))
                Neighbours.append((i, j-1))
                Neighbours.append((i, j+1))
                raid = False

                oppLoss = 0
                for x, y in Neighbours:
                    if 0 <= x < 5 and 0 <= y < 5:
                        if self.state[x][y] == oppPiece:
                            oppLoss += self.costs[x][y]
                        elif self.state[x][y] == player:
                            raid = True
                if raid:
                    heuristic[i][j] += 2 * oppLoss
        maxVal = MINIMUM_INT
        pos = None

        for i, j in self.Update():
            if heuristic[i][j] != None and heuristic[i][j] > maxVal:
                maxVal = heuristic[i][j]
                pos = (i, j)
        if pos:
            return self.Attack(self.state, pos[0], pos[1], player)

    def miniMax(self,logfile,debug = False):
        if logfile:
            logfile.write("Node,Depth,Value")
        root = Box(MINIMUM_INT, (None, None), None)
        self.maximum(self.state, root,self.cutoff, self.myPiece, logfile)
        if root.nextMove:
            move = root.nextMove
            self.Attack(self.state, move.pos[0], move.pos[1], move.piece)

    def alphaBetaPruning(self,logfile,debug = False):
        if logfile:
            logfile.write("Node,Depth,Value,Alpha,Beta")
        root = Box(MINIMUM_INT, (None, None), None) 

        root.alpha = MINIMUM_INT                     
        root.beta = MAXIMUM_INT                      
        self.maximumAB(self.state, root,self.cutoff,logfile,self.myPiece)
        if root.nextMove:
            move = root.nextMove
            self.Attack(self.state, move.pos[0], move.pos[1], move.piece)

    def simulate(self,debug = False):
        count = 0
        with open("trace_state.txt", 'w') as out:
            while not self.isTerminal(self.state):
                if count % 2 != 0:
                    self.AlternatePlayer(self.secondPlayerAlgo, self.secondPlayer, self.firstPlayer, self.secondPlayerCutOff)
                elif count % 2 == 0:
                    self.AlternatePlayer(self.firstPlayerAlgo, self.firstPlayer, self.secondPlayer, self.firstPlayerCutOff)

                if count > 0:
                    out.write("\r\n")
                res = self.printState(self.state,None).strip()
                out.write(res)
                count = count + 1

    def AlternatePlayer(self, strategy, player, opponent, cutoff, logfile = None):
        if strategy == ALPHABETA:
            if logfile:
                logfile.write("Node,Depth,Value,Alpha,Beta")
            root = Box(MINIMUM_INT, (None, None), None) 

            root.alpha = MINIMUM_INT                     
            root.beta = MAXIMUM_INT                      
            self.maximumAB(self.state, root,cutoff,logfile,player)
            if root.nextMove:
                move = root.nextMove
                self.Attack(self.state, move.pos[0], move.pos[1], move.piece)
        elif strategy == MINIMAX:
            if logfile:
                logfile.write("Node,Depth,Value")
            root = Box(MINIMUM_INT, (None, None), None)
            self.maximum(self.state, root,cutoff, player, logfile)
            if root.nextMove:
                move = root.nextMove
                self.Attack(self.state, move.pos[0], move.pos[1], move.piece)
        elif strategy == GREEDY:
            self.greedyBFS(player)



    def nextMove(self, algorithm):

        if algorithm == MINIMAX:
            with open("traverse_log.txt", 'w') as logfile:
                self.miniMax(logfile)
        elif algorithm == GREEDY:
            self.greedyBFS(self.myPiece)
        elif algorithm == ALPHABETA:
            with open("traverse_log.txt", 'w') as logfile:
                self.alphaBetaPruning(logfile)
        else:
            self.simulate()

    def maximum(self, state, parent, pMaxDepth, pPlayer, pLogFile):
        cells = self.PlaceableCells(state)
        if parent.depth == pMaxDepth or not cells:
            parent.score = self.Calculate(state,pPlayer)
        else:
            if pLogFile:
                pLogFile.write("\n" + TraverseLog(parent))
            for x, (i, j) in enumerate(cells):
                undoMoves = self.Attack(state, i, j, pPlayer)    
                child = Box(MAXIMUM_INT, (i, j), pPlayer)
                parent.AddToBox(child)
                child.score = self.minimum(state, child,pMaxDepth,SwapPlayer(pPlayer), pLogFile)              
                if child.score > parent.score:
                    parent.score = child.score
                    parent.nextMove = child
                if x < len(cells) - 1: 
                    if pLogFile:
                        pLogFile.write("\n" + TraverseLog(parent))
                for a in undoMoves:
                    state[a[0]][a[1]] = a[2]
        if pLogFile:
            pLogFile.write("\n" + TraverseLog(parent))
        return parent.score

    def minimum(self, state, parent, pMaxDepth, pPlayer, pLogFile):
        cells = self.PlaceableCells(state)
        if parent.depth == pMaxDepth or not cells:
            parent.score = self.Calculate(state, SwapPlayer(pPlayer))
        else:
            if pLogFile:
                pLogFile.write("\n" + TraverseLog(parent))
            for x, (i, j) in enumerate(cells):
                undoMoves = self.Attack(state, i, j, pPlayer)     
                child = Box(MINIMUM_INT, (i, j), pPlayer)
                parent.AddToBox(child)
                self.maximum(state, child,pMaxDepth,SwapPlayer(pPlayer),pLogFile)                             
                if child.score < parent.score:
                    parent.score = child.score
                    parent.nextMove = child
                if x < len(cells) -1: 
                    if pLogFile:
                        pLogFile.write("\n" + TraverseLog(parent))
                for a in undoMoves:
                    state[a[0]][a[1]] = a[2]
        if pLogFile:
            pLogFile.write("\n" + TraverseLog(parent))
        return parent.score

    def maximumAB(self, state, parent,pMaxDepth,logfile,maxPlayer):
        cells = self.PlaceableCells(state)
        if parent.depth == pMaxDepth or not cells:
            parent.score = self.Calculate(state,maxPlayer)
        else:
            if logfile:
                logfile.write("\n" + TraverseLog(parent, True))
            for x, (i, j) in enumerate(cells):
                undoMoves = self.Attack(state, i, j, maxPlayer)    
                child = Box(MAXIMUM_INT, (i, j), maxPlayer)     

                child.alpha = parent.alpha                        
                child.beta = parent.beta
                parent.AddToBox(child)                          
                self.minimumAB(state, child,pMaxDepth,logfile,SwapPlayer(maxPlayer))              
                for a in undoMoves:
                    state[a[0]][a[1]] = a[2]

                if child.score > parent.score:
                    parent.score = child.score
                    parent.nextMove = child
                if child.score >= parent.beta: 
                    break
                if child.score > parent.alpha:
                    parent.alpha = child.score

                if x < len(cells) - 1:                                 
                    if logfile:
                        logfile.write("\n" + TraverseLog(parent, True))
        if logfile:
            logfile.write("\n" + TraverseLog(parent, True))
        return parent.score

    def minimumAB(self, state, parent,maxdepth,logfile,pPlayer):
        cells = self.PlaceableCells(state)
        if parent.depth == maxdepth or not cells:
            parent.score = self.Calculate(state,pPlayer)
        else:
            if logfile:
                logfile.write("\n" + TraverseLog(parent, True))
            for x, (i, j) in enumerate(cells):
                undoMoves = self.Attack(state, i, j, pPlayer)
                child = Box(MINIMUM_INT, (i, j), pPlayer)
                child.alpha = parent.alpha
                child.beta = parent.beta
                parent.AddToBox(child)
                self.maximumAB(state, child,maxdepth,logfile,SwapPlayer(pPlayer))                             
                for a in undoMoves:
                    state[a[0]][a[1]] = a[2]
                if child.score < parent.score:
                    parent.score = child.score
                    parent.nextMove = child
                if child.score <= parent.alpha:
                    break
                if child.score < parent.beta:
                    parent.beta = child.score

                if x < len(cells) -1: 
                    if logfile:
                        logfile.write("\n" + TraverseLog(parent, True))
        if logfile:
            logfile.write("\n" + TraverseLog(parent, True))
        return parent.score

class Box(object):

    def __init__(self, score, pos, piece, depth=0, parent=None):
        self.parent = parent
        self.children = None
        self.score = score
        self.pos = pos
        self.piece = piece
        self.depth = depth
        self.nextMove = None

    def AddToBox(self, node):
        node.parent = self
        node.depth = self.depth + 1
        if self.children == None:
            self.children = []
        self.children.append(node)

problem = AIHW1(sys.argv[2])
problem.nextMove(problem.strategy)
problem.printState(problem.state, "next_state.txt")