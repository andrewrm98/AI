class ConnectFour:

    def __init__(self, board, w, h):
        """Class constructor"""
        # Board data
        self.board = board
        # Board width
        self.w = w
        # Board height
        self.h = h

    def isLineAt(self, x, y, dx, dy):
        """Return True if a line of identical tokens exists starting at (x,y)
           in direction (dx,dy)"""
        # Your code here
        win = 0  # win if this equals 4
        current = 0  # will keep track of whose score is being checked
        iteration = 0
        while (x < self.w and y < self.h) and y >= 0:  # while x is less than the width of the board, check for win condition
            if self.board[y][x] == 1 or self.board[y][x] == 2:
                if current != self.board[y][x]:
                    win = 0
                    current = self.board[y][x]
                win += 1
            else:
                win = 0  # if there is no one or two, resent win as it is an empty space
                current = 0
            x = x + dx
            y = y + dy
            iteration += 1
            if win == 4:
                return True
            if iteration == 4:
                break
        return False

    def isAnyLineAt(self, x, y):
        """Return True if a line of identical symbols exists starting at (x,y)
           in any direction"""
        return (self.isLineAt(x, y, 1, 0) or  # Horizontal
                self.isLineAt(x, y, 0, 1) or  # Vertical
                self.isLineAt(x, y, 1, 1) or  # Diagonal up
                self.isLineAt(x, y, 1, -1))  # Diagonal down

    def getOutcome(self):
        """Returns the winner of the game: 1 for Player 1, 2 for Player 2, and
           0 for no winner"""
        # Your code here, use isAnyLineAt()
        x = 0
        y = 0
        win = 0
        while x < self.w:
            while y < self.h:
                if self.isAnyLineAt(x, y) == True:
                    return self.board[y][x]
                    win = 1
                y += 1
            x += 1
            y = 0
        if win != 1:
            return 0

    def printOutcome(self):
        """Prints the winner of the game"""
        o = self.getOutcome()
        if o == 0:
            print("No winner")
        else:
            print("Player", o, " won")

