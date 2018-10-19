#!/usr/bin/python3
import unittest
from chemistry_research import chemistry

from pdb import set_trace


class TestChemistry(unittest.TestCase):

    def test_list_valid(self):
        to_test = ['Calcium, Ca', 'Fe', 'Potassium']
        expected = ['Ca', 'Fe', 'K']

        obj = chemistry.Chemistry(to_test)
        result = [ o.symbol for o in obj.elements]

        self.assertTrue(expected == result)


    def test_list_invalid(self):
        to_test = ['Ca', 'Fe', 'Invalid']

        try:
            chemistry.Chemistry(to_test)
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True, 'no exception for incorrect symbol')


    def test_all_permutations(self):
        to_test = ['Ca', 'Fe', 'K', 'Ba']
        expected = [('Ca', 'Fe'), ('Ca', 'K'), ('Ca', 'Ba'), ('Fe', 'K'),
                    ('Fe', 'Ba'), ('K', 'Ba'), ('Ca', 'Fe', 'K'),
                    ('Ca', 'Fe', 'Ba'), ('Ca', 'K', 'Ba'), ('Fe', 'K', 'Ba'),
                    ('Ca', 'Fe', 'K', 'Ba')]
        obj = chemistry.Chemistry(to_test)

        result = obj.all_permutations(to_test)
        self.assertTrue(result, expected)


if __name__ == '__main__':
    unittest.main()
