
import search
import random

# Module Classes

class SixteenPuzzleState:
    """
    The Sixteen Puzzle is a 4x4 grid with numbers from 0 to 15, where 0 represents the blank space.
    The goal state has the blank space in the bottom right corner.
    """

    def __init__(self, numbers):
        """
        Constructs a new sixteen puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 15 representing an instance of the sixteen puzzle.
        0 represents the blank space.
        """
        self.cells = []
        numbers = numbers[:]  # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range(4):
            self.cells.append([])
            for col in range(4):
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal(self):
        """
        Checks to see if the puzzle is in its goal state.

        The goal state has the blank space in the bottom right corner and numbers in ascending order.
        """
        current = 1
        for row in range(4):
            for col in range(4):
                if row == 3 and col == 3:
                    if self.cells[row][col] != 0:
                        return False
                else:
                    if self.cells[row][col] != current:
                        return False
                    current += 1
        return True

    def legalMoves(self):
        """
        Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left, or right.
        These are encoded as 'up', 'down', 'left', and 'right' respectively.
        """
        moves = []
        row, col = self.blankLocation
        if row != 0:
            moves.append('up')
        if row != 3:
            moves.append('down')
        if col != 0:
            moves.append('left')
        if col != 3:
            moves.append('right')
        return moves

    def result(self, move):
        """
        Returns a new sixteenPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception.
        """
        row, col = self.blankLocation
        if move == 'up':
            newrow = row - 1
            newcol = col
        elif move == 'down':
            newrow = row + 1
            newcol = col
        elif move == 'left':
            newrow = row
            newcol = col - 1
        elif move == 'right':
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current sixteenPuzzle
        newPuzzle = SixteenPuzzleState([0] * 16)
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
        Overloads '==' such that two sixteenPuzzles with the same configuration
        are equal.
        """
        for row in range(4):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
        Returns a display string for the puzzle
        """
        lines = []
        horizontalLine = ('-' * (17))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

class SixteenPuzzleSearchProblem(search.SearchProblem):
    """
    Implementation of a SearchProblem for the Sixteen Puzzle domain

    Each state is represented by an instance of a sixteenPuzzle.
    """
    def __init__(self, puzzle):
        "Creates a new SixteenPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        """
        Returns list of (successor, action, stepCost) pairs where
        each successor is either left, right, up, or down
        from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions. The sequence must
        be composed of legal moves
        """
        return len(actions)

SIXTEEN_PUZZLE_DATA = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 11, 12, 13, 14, 15]
]

def loadSixteenPuzzle(puzzleNumber):
    """
    puzzleNumber: The number of the sixteen puzzle to load.

    Returns a sixteen puzzle object generated from one of the
    provided puzzles in SIXTEEN_PUZZLE_DATA.

    puzzleNumber can range from 0 to 5.
    """
    return SixteenPuzzleState(SIXTEEN_PUZZLE_DATA[puzzleNumber])

def createRandomSixteenPuzzle(moves=100):
    """
    moves: number of random moves to apply

    Creates a random sixteen puzzle by applying
    a series of 'moves' random moves to a solved
    puzzle.
    """
    puzzle = SixteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

if __name__ == '__main__':
    puzzle = createRandomSixteenPuzzle(25)
    print('A random puzzle:')
    print(puzzle)

    problem = SixteenPuzzleSearchProblem(puzzle)
    path = search.uniformCostSearch(problem)
    print('A* found a path of %d moves: %s' % (len(path), str(path)))
    curr = puzzle
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i > 1], a))
        print(curr)

        input("Press return for the next state...")  # wait for key stroke
        i += 1
        