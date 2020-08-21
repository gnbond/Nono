# Base Cell() class
# this represents the current state of a cell

class Infeasible(RuntimeError):
    pass

class Cell:
    Unknown = '.'
    Yes = 'Y'
    No = 'x'

    def __init__(self, v = None):
        if v:
            if v not in (Cell.Unknown, Cell.Yes, Cell.No):
                raise ValueError("Cell must be Y/x/.)")
        else:
            v = Cell.Unknown
        self.value = v
        # These three are set once the Cell is connected to the rows
        self.row = None
        self.col = None
        self.game = None
    
    @property
    def name(self):
        if not self.row or not self.col: # unit tests
            return "<anonymous>"
        return "R%dC%d" % (self.row.num, self.col.num)

    def set_value(self, v):
        if v == self.value:
            return
        if self.value != Cell.Unknown:
            raise Infeasible("Cell " + self.name + " is already " + self.value + ", cannot set to " + v)
        self.value = v
        if self.game: # unit tests have this as None
            self.game.remaining -= 1
