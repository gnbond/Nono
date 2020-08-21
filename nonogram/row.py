# Represent a row or a column
# Each row contains N Cell objects, plus a list of strings
# for potential solutions to that row

from .cell import Cell, Infeasible

class RowColBase:
    def __init__(self, num, cells):
        self.num = num
        self.value = cells
        self.length = len(cells)

        assert 0 < self.num <= self.length

        self.possible = []
        self.clue = []

    def __len__(self):
        return self.length

    def __getitem__(self, n):
        return self.value[n]
       
    def find_possible(self, clue):
        '''
        Set self.possible to a list of strings with all the possible
        solutions to this row based on the clue.
        Clue is a sequence of integers, e.g. (1, 2)
        For a length=5 row, this result is something like
            [ "YxYYx", "YxxYY", "xYxYY" ]
            all strings have the same length
        Trick is to do this recursively
        '''
        if not clue:
            raise ValueError("Clue for " + self.name + " must have at least 1 entry")
        try:
            clue = [int(x) for x in clue]
        except (TypeError, ValueError):
            raise ValueError("Clue must be sequence of integers")
        for x in clue:
            if x <= 0 or x > self.length:
                raise ValueError("Clue must be > 0 and less than or equal to row size")
        if sum(clue) + len(clue) > self.length + 1:
            raise ValueError("Size of clue exceeds size of row")
    
        self.clue = clue
        self.possible = self._find_possible(clue, self.length)

    @staticmethod
    def _find_possible(clue, length):
        ''' in this recurive routine, we know clue is integers,
        > 0, <= len and the total clue is <= length
        '''

        #if not len(clue): return ["x" * length]
        #if length == 0: return ['']
        #if length < 0 or sum(clue) + len(clue) - 1 > length: return []

        first = clue[0]
        restclue = clue[1:]
        prefix = "Y" * first

        # Handle the simple cases
        if first == length:
            return [prefix]
        if first == length - 1:
            return [ prefix + "x", "x" + prefix ]

        ret = []
        if restclue:
            # not so simple, so recurse
            nclue = sum(restclue) + len(restclue) - 1 # how many required for remaining clue!
            for i in range(length - first - nclue):
                initial = "x" * i + prefix + "x" 
                ret.extend([ initial + x 
                                for x in Row._find_possible(restclue, length - first - i - 1)])
        else:
            # no remaining clue, so all variants of x Y x
            for i in range(length - first + 1):
                ret.append("x" * i + prefix + "x" * (length - first - i))

        # Just checking!
        for x in ret:
            assert len(x) == length
        return ret

    @property
    def name(self):
        raise RuntimeError("unimplemented")
    
    def __str__(self):
        return "".join([c.value for c in self.value]) 
        
    def apply_solution(self, s = None):
        '''
        Apply the solution s, marking cells as Yes or No as appropriate
        If this contradicts existing cell values, raise Infeasible
        If s is not given, use possibles[0]
        set possibles to None to indicate this row is done
        '''
        if s is None:
            s = self.possible.pop(0)
        print("Applying solution", s, "to", self.name)
        for i in range(self.length):
            self.value[i].set_value(s[i])
        self.possible = []

    def reduce_possibles(self):
        '''
        Given that some cells might have been fixed, see if that reduces
        the number of possibles.
        Return the number of possibiles removed
        '''
        olen = len(self.possible)
        if not olen:
            return 0 # already solved this row
        p = self.possible
        for i in range(self.length):
            if self.value[i].value == Cell.No:
                p = [ x for x in p if x[i] == 'x' ]
            elif self.value[i].value == Cell.Yes:
                p = [ x for x in p if x[i] == 'Y' ]
        if not p:
            raise Infeasible("No feasible solutions left for " + self.name)
        self.possible = p
        return olen - len(self.possible)

    def common_cells(self):
        '''
        Find the currently-unknown cells that are fixed to the same
        value by all the current possibilities
        return the number of cells updated
        '''
        n = 0
        for i in range(self.length):
            c = self.value[i]
            if c.value != Cell.Unknown:
                continue
            has_no = has_yes = False
            for p in self.possible:
                has_no = has_no or p[i] == Cell.No
                has_yes = has_yes or p[i] == Cell.Yes
            if not has_no:
                print(self.name, "Setting", c.name, "to YES common to all", len(self.possible), "possible solutions")
                c.set_value(Cell.Yes)
                n += 1
            elif not has_yes:
                print(self.name, "Setting", c.name, "to NO common to all", len(self.possible), "possible solutions")
                c.set_value(Cell.No)
                n += 1
        return n

class Row(RowColBase):
    def __init__(self, num, arg = 10):
        ''' num is the row number, 1..lenth
        arg is either an int length (row is filled with Unknown Cells)
        or a string which is converted to Cells '''
        try:
            arg = int(arg)
            cells = tuple([Cell() for x in range(arg)])
        except ValueError:
            # Assume a string of cell values
            cells = tuple([Cell(x) for x in arg])
        
        super().__init__(num, cells)

        for c in self.value:
            c.row = self

    @property
    def name(self):
        return "R%d" % self.num       

class Col(RowColBase):
    def __init__(self, num, cells):
        super().__init__(num, cells)

        for c in self.value:
            c.col = self

    @property
    def name(self):
        return "C%d" % self.num
 