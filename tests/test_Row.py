
import unittest
from nonogram import Row, Cell, Infeasible

class TestRow(unittest.TestCase):
    def test_create(self):
        row = Row(1)
        self.assertTrue(row)
        self.assertEqual(row.length, 10)
        self.assertEqual(len(row), 10)
        self.assertEqual(row.possible, [])
        self.assertEqual(row.num, 1)
        self.assertEqual(row.name, "R1")
        self.assertEqual(str(row), "..........")
        cell = row[0]
        self.assertEqual(cell.value, Cell.Unknown)
    
    def test_create_size(self):
        row = Row(1, 4)
        self.assertTrue(row)
        self.assertEqual(row.length, 4)
        self.assertEqual(len(row), 4)
        self.assertEqual(row.possible, [])
        self.assertEqual(row.num, 1)
        cell = row[0]
        self.assertEqual(cell.value, Cell.Unknown)
        self.assertIs(cell.row, row)

    def test_buildrow(self):
        r = Row(1, ".Yx")
        self.assertEqual(len(r), 3)
        self.assertEqual(r[0].value, Cell.Unknown)
        self.assertEqual(r[1].value, Cell.Yes)
        self.assertEqual(r[2].value, Cell.No)

    def test_build_invalid(self):
        self.assertRaises(ValueError, Row, 1, "z")

    def test_constuct_invalid(self):
        self.assertRaises(AssertionError, Row, 0)
        self.assertRaises(AssertionError, Row, -1)
        self.assertRaises(AssertionError, Row, 11)
        self.assertRaises(TypeError, Row, "a")

class TestPossibles(unittest.TestCase):
    def setUp(self):
        self.r = Row(1, 5)

    def test_invalid_clue(self):
        self.assertRaises(ValueError, self.r.find_possible, [])
        self.assertRaises(ValueError, self.r.find_possible, ['x'])
        self.assertRaises(ValueError, self.r.find_possible, [0])
        self.assertRaises(ValueError, self.r.find_possible, [-1])
        self.assertRaises(ValueError, self.r.find_possible, [20])
        self.assertRaises(ValueError, self.r.find_possible, [2, 3]) # xeeds 6

    def test_5(self):
        self.r.find_possible([5])
        self.assertEqual(self.r.possible, ["YYYYY"])
        self.assertEqual(self.r.clue, [5])

    def test_4(self):
        self.r.find_possible([4])
        self.assertEqual(self.r.possible, ["YYYYx", "xYYYY"])

    def test_1(self):
        self.r.find_possible([1])
        self.assertEqual(self.r.possible, ["Yxxxx", "xYxxx", "xxYxx", "xxxYx", "xxxxY"])

    def test_22(self):
        self.r.find_possible([2,2])
        self.assertEqual(self.r.possible, ["YYxYY"])

    def test_21(self):
        self.r.find_possible([2,1])
        self.assertEqual(self.r.possible, ["YYxYx", "YYxxY", "xYYxY"])
   
    def test_11(self):
        self.r.find_possible([1,1])
        self.assertEqual(self.r.possible, ["YxYxx", "YxxYx", "YxxxY",
                    "xYxYx", "xYxxY", "xxYxY"])

class TestSolvers(unittest.TestCase):
    def test_apply(self):
        r = Row(1, 5)
        r.apply_solution("xYYYx")
        self.assertEqual(str(r), "xYYYx")
        self.assertEqual(r.possible, [])

    def test_apply_infeasible(self):
        r = Row(1,3)
        r.value[0].set_value(Cell.No)
        self.assertEqual(str(r), "x..")
        self.assertRaises(Infeasible, r.apply_solution, "YYY")

    def test_reduce_possibles(self):
        r = Row(1, 3)
        r.find_possible([1])
        self.assertEqual(r.possible, ["Yxx", "xYx", "xxY"])
        r.value[0].set_value(Cell.No)
        r.reduce_possibles()
        self.assertEqual(r.possible, ["xYx", "xxY"])
        

if __name__ == "__main__":
    unittest.main()
