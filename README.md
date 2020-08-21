# Nono
Solver for Nonogram puzzles.

If you are new to Nonogram puzzle, see the various iOS / Google apps, e.g. See for example [iOS](https://fnd.io/#/us/ios-universal-app/1452992954-nonogramcom-griddlers-game-by-easybrain) or [Android](https://play.google.com/store/apps/details?id=com.easybrain.nonogram) apps.

This solver is currently text-mode only.  Input is text file describing the puzzle, output is each of the steps (and some intermediate board positions) as the solver progresses:

    $ cat 3x3game 
    3
    1 1
    2
    2
    1 1
    2
    2
    $ ./run.py 3x3game 
    R1 [1, 1] , 1 possibles
    R2 [2] , 2 possibles
    R3 [2] , 2 possibles
    C1 [1, 1] , 1 possibles
    C2 [2] , 2 possibles
    C3 [2] , 2 possibles
    Applying solution YxY to R1
    Applying solution YxY to C1
    Remaining: 4/9
    R1 : YxY
    R2 : x..
    R3 : Y..

    reduced possibles by 4
    Applying solution xYY to R2
    Applying solution YYx to R3
    Applying solution xYY to C2
    Applying solution YYx to C3
    Remaining: 0/9
    R1 : YxY
    R2 : xYY
    R3 : YYx

    $

# Input format
input file is text, in 3 sections.  All lines are lists of integers, there is currently no comment syntax or any other formatting:
 - 1 line containing a single integer for the size of the puzzle grid (call it `n`, 3 in the above example).  Currently, only square grids are supported (3x3), but expanding to rectangular should not be hard.
 - `n` lines of row clues, 1 line per row. 
 - `n` lines of column clues, 1 line per column
 - There is currently no support for inputting already-solved pieces of the puzzle, solver assumes initial grid is empty.
 - Some minor sanity-checking is done on the clue lines, see `RowColBase.find_possible()`.

 # Solution algorithm

 I create solver programs for puzzles as a way of exploring the puzzles and thinking about how to solve them.  Alas, unlike Sudoku, Nonogram puzzles are very basic and a single, simple algorithm is sufficient to solve all puzzles I have encountered so far with no guessing or back-tracking.  This was something of a disappointment. 

 The basic algorithm is as follows:

  - Read the puzzle in
  - Set each cell in the grid to "unknown", represented by '.'
  - For each row & column in the grid, generate a set of possible solutions for that row, based only on the clue.  This is the most algorithmically interesting part of the problem, see `RowColBase._find_possible()` and the unit tests in `tests/test_Row.py`.
  - While the puzzle is not solved:
    - For any row or column with only 1 remaining possible solution, apply that and mark all the cells in that row as solved with a state of "Y" or "x" (`RowColbase.apply_solution()`)
    - For each row & column, check each possible solution and discard any possible solution that has been disqualified by any cell that has been solved (i.e. possible solution has 'Y' but cell has 'x', and vice-versa).  (`RowColBase.reduce_possibles()`)
    - For each row and column:
      - check each unsolved cell in that row.  If all remaining possible solutions for that row have the same value for that cell, set that cell as solved with that value.  (`RowColbase.common_cells()`)
  - If the puzzle is not solvable (probably because the input file is not correct), an `Infeasible` exception will be raised.

That's it.

# Implementation

The solver is implemented in python 3, but should easily be made to work on python2 if required (consider `print()` and `super()`).  

Actual solver is in the `nonogram` module.

Unit tests in the `tests/` directory are built using the standard `unittest` library, they can be run by 

  python3 -m unittest discover -s tests

Some sample puzzles are in the `puzzles/` directory.
