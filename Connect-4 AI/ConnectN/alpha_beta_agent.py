import math
import agent
import board

###########################
# Alpha-Beta Search Agent #
###########################

# Craig

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    # PARAM [float]   defense:  the defense multiplier
    def __init__(self, name, max_depth, defense, middle):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.defense = defense
        self.middle = middle


    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        inittable = self.initheuristic(brd)
        v = self.maxvalue(brd, 0, -math.inf, math.inf, inittable)
        return v[1]

    # Will check if a leaf node has been reached based on the given maximum depth
    def terminal_test(self, brd, depth):
        win = brd.get_outcome()
        if win == brd.player:
            return 1
        elif win != brd.player and win != 0:
            return -1
        if depth >= self.max_depth:
            return True
        return False

    # returns the total utility of the board
    def getUtility(self, brd, inittable):
        utility = 0
        r = 0
        c = 0
        while r < brd.h:
            while c < brd.w:
                utility += self.calcLine(brd, r, c, inittable)
                c += 1
            r += 1
        return utility

    def initheuristic(self, brd):
        i = 0
        j = 0
        evenWidth = 0
        mult = 0
        initTable = brd.h*[brd.w*[0]]

        if self.middle == 0:
            return initTable
        else:
            mult = self.middle

        if brd.w % 2 == 0:
            evenWidth = True
        else:
            evenWidth = False

        while i < brd.h:
            while j < brd.w/2:
                if evenWidth:
                    mid = int(brd.w/2)
                    minleft = mid-1
                    startNum = minleft

                    initTable[i][minleft-j] = (startNum - j + i) * mult
                    initTable[i][mid+j] = (startNum - j + i) * mult
                else:
                    mid = int(brd.w/2)
                    minleft = int(mid)
                    startNum = minleft

                    initTable[i][minleft-j] = (startNum - j + i) * mult
                    initTable[i][mid+j] = (startNum - j + i) * mult
                j += 1
            i += 1
        return initTable

    # calls calc spot in every direction looking for threats
    def calcLine(self, brd, r, c, inittable):
        utility = 0
        utility += self.isThreat(brd, self.defense, r, c, 1, 0, inittable)
        utility += self.isThreat(brd, self.defense, r, c, 0, 1, inittable)
        utility += self.isThreat(brd, self.defense, r, c, 1, 1, inittable)
        utility += self.isThreat(brd, self.defense, r, c, 1, -1, inittable)
        return utility

    # this function weights the points to add for each number of pieces in a row
    def weight(self, num, zeroValue, brd):
        if zeroValue < 1:
            zeroValue = 1
        one = 1 * zeroValue
        two = 20 * zeroValue
        three = 100 * zeroValue
        four = 200000 * zeroValue


        if num == 1:
            return one
        if num == 2:
            return two
        if num == 3:
            return three
        if num == 4:
            return four
        if brd.n >4 and num > 4:
            h = 4
            while h < num:
                return four * h
        else:
            return 0

    def isThreat(self, brd, defense, r, c, dx, dy, inittable):
        line = []
        iteration = 0
        x = 0
        row = r
        column = c
        playerOne = 0
        playerTwo = 0
        zeros = 0
        zeroValue = 0
        threats = 0
        score = 0

        # iterates through the next n cells
        while iteration < brd.n:
            # test is it is out of bounds
            if row >= brd.h or row < 0 or column >= brd.w or column < 0:
                break

            # create an array containing the n cells that are being examined
            line.append(brd.board[row][column])

            if brd.board[row][column] == 0:
                zeroValue += inittable[row][column]
            iteration += 1
            row += dy
            column += dx

        # loop through the array
        while x < len(line):
            # if a friendly piece
            if line[x] == 1:
                playerOne += 1
            # if an enemy piece
            if line[x] == 2:
                playerTwo += 1
            if line[x] == 0:
                zeros += 1
            x+=1

        # if only friendly pieces are present in the line
        if playerOne != 0 and playerTwo == 0:
            if brd.player == 1:
                # if player two is the current player then add to the score
                score += self.weight(playerOne, zeroValue, brd)
            elif brd.player == 2:
                # if player two is the other player then add to the threats
                threats += self.weight(playerOne, zeroValue, brd)

        # if only enemy pieces are present in the line
        if playerTwo != 0 and playerOne == 0:
            if brd.player == 2:
                # if player two is the current player then add to the score
                score += self.weight(playerTwo, zeroValue, brd)
            elif brd.player == 1:
                # if player two is the other player then add to the threats
                threats += self.weight(playerTwo, zeroValue, brd)

        # return the final board score
        return score - (threats * defense)

    # something is wrong with the pruning, scoring works fine
    # Max function returns the utility value for the maximizing player
    def maxvalue(self, brd, depth, alpha, beta, inittable):
        v = (-math.inf, -1)
        num = 0
        test = self.terminal_test(brd, depth)
        if test == True:
            return self.getUtility(brd, inittable), -1
        for s, a in self.get_successors(brd):
            b = self.minvalue(s, depth + 1, alpha, beta, inittable)
            num+=1
            if b >= v[0]:
                v = (b, a)
            alpha = max(alpha, v[0])
            if v[0] >= beta:
                return v
        return v

    # Min function returns the utility value for the minimizing player
    def minvalue(self, brd, depth, alpha, beta, inittable):
        v = math.inf
        num = 0
        test = self.terminal_test(brd, depth)
        if test == True:
            return self.getUtility(brd, inittable)
        for s, a in self.get_successors(brd):
            b = self.maxvalue(s, depth + 1, alpha, beta, inittable)
            num += 1
            v = min(v, b[0])
            beta = min(beta, v)
            if v <= alpha:
                return v
        return v



    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            #nb.player = 1
            # Add board to list of successors
            succ.append((nb,col))
        return succ


THE_AGENT = AlphaBetaAgent("MorrisonAndrew", 2, .77, 1)


