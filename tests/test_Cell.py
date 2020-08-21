import unittest
from nonogram import Cell, Infeasible

class Test_Cell(unittest.TestCase):
    def test_create(self):
        cell = Cell()
        self.assertTrue(cell)
        self.assertEqual(cell.value, Cell.Unknown)
    
    def test_init(self):
        c = Cell(Cell.Yes)
        self.assertEqual(c.value, Cell.Yes)
    
    def test_invalid(self):
        self.assertRaises(ValueError, Cell, 'z')

    def test_name(self):
        cell = Cell()
        class mockRow:
            def __init__(self):
                self.num = 1
        cell.row = cell.col = mockRow()
        self.assertEqual(cell.name, "R1C1")

    def test_setvalue(self):
        c = Cell()
        c.set_value(Cell.Yes)
        self.assertEqual(c.value, Cell.Yes)
        self.assertRaises(Infeasible, c.set_value, Cell.No)



if __name__ == "__main__":
    unittest.main()