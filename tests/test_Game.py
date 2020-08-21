from nonogram import Game, Cell
import unittest

class TestGame(unittest.TestCase):
    def test_create(self):
        g = Game(5)
        self.assertEqual(g.size, 5)
        self.assertEqual(len(g.rows), 5)
        self.assertEqual(len(g.cols), 5)
        self.assertEqual(len(g.rowscols), 10)
    
    def test_cellat(self):
        g = Game(5)
        c = g.cellat(1,1)
        self.assertEqual(c.value, Cell.Unknown)
        self.assertIs(c.row, g.rows[0])
        self.assertIs(c.col, g.cols[0])

        c = g.cellat(5,5)
        self.assertEqual(c.value, Cell.Unknown)
        self.assertIs(c.row, g.rows[4])
        self.assertIs(c.col, g.cols[4])

    def test_cellat_invalid(self):
        g = Game(5)
        self.assertRaises(IndexError, g.cellat, 0, 1)
        self.assertRaises(IndexError, g.cellat, 1, 0)
        self.assertRaises(IndexError, g.cellat, 1, 11)
        self.assertRaises(IndexError, g.cellat, 11, 1)

if __name__ == "__main__":
    unittest.main()