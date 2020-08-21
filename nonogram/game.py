from .cell import Cell, Infeasible
from .row import Row, Col

class Game:
    def __init__(self, size=10):
        self.size = size
        self.rows = [ Row(r, size) for r in range(1, size+1) ]
        self.cols = [
            Col(c, [self.cellat(r, c) for r in range(1, self.size+1) ])
            for c in range(1, self.size+1)
        ]
        for r in self.rows:
            for c in r:
                c.game = self

        self.rowscols = self.rows + self.cols
        self.remaining = size * size

    def cellat(self, r, c):
        '''r,c in range 1..size, not usual 0-based!'''
        if r < 1 or r > self.size or c < 1 or c > self.size:
            raise IndexError("Cell indexes from 1 .. size")
        return self.rows[r-1].value[c-1]

    def __str__(self):
        s = 'Remaining: %d/%d\n' % (self.remaining, self.size * self.size)
        for r in self.rows:
            s += ("%-3s: " % r.name) + str(r) + "\n"
        return s

    @staticmethod
    def fromfile(f):
        '''Read agame from a file-like object f (or a file called f) and return a new Game() object
        format is:
            size (int()
            <size x> row clues (int, space separated)
            <size x> col clues
        '''
        if type(f) == str:
            f = open(f, "r")
        size = int(f.readline())
        g  = Game(size)
        nrowcells = ncolcells = 0
        for i in range(size):
            clue = [int(x) for x in f.readline().split()]
            nrowcells += sum(clue)
            g.rows[i].find_possible(clue)
        for i in range(size):
            clue = [int(x) for x in f.readline().split()]
            ncolcells += sum(clue)
            g.cols[i].find_possible(clue)
        
        # some minor consistency checks,
        # do the column clues match the row clues?
        if nrowcells != ncolcells:
            raise Infeasible("Row clues have %d cells but Col clues have %d cells" % (nrowcells, ncolcells))
        return g

    # The solution functions
    
    # if there is only 1 possible, then use it!
    # return the number of rows fixed
    def solve_only(self):
        n = 0
        for rc in self.rowscols:
            if len(rc.possible) == 1:
                rc.apply_solution()
                n += 1
        return n

    def reduce_possibles(self):
        n = 0
        for rc in self.rowscols:
            n += rc.reduce_possibles()
        print("reduced possibles by", n)
        return n

    def common_cells(self):
        '''
        See if we can fix any cells because all possibilities have the same value
        return the number of cells fixed
        '''
        n = 0
        for rc in self.rowscols:
            n += rc.common_cells()
        return n

    def solve(self):
        self.solve_only()
        while self.remaining > 0:
            while self.remaining > 0 and self.reduce_possibles() > 0:
                self.solve_only()
                print(self)
            if self.remaining > 0:
                n = self.common_cells()
                if n > 0:
                    print("Fixed", n, "cells")
                    print(self)
                    continue
            if self.remaining > 0:
                raise Infeasible("Out of ideas!")

 