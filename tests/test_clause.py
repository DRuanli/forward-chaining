"""
Unit tests for the Clause class.
"""

import unittest
from src.clause import Clause


class TestClause(unittest.TestCase):
    """Test cases for the Clause class."""

    def test_initialize_clause(self):
        """Test basic initialization of a clause."""
        clause = Clause(['a', 'b'], 'c')
        self.assertEqual(clause.premise_literals, ['a', 'b'])
        self.assertEqual(clause.conclusion_literal, 'c')
        self.assertEqual(clause.known_count, 0)

    def test_is_fact(self):
        """Test the is_fact property."""
        fact_clause = Clause([], 'a')
        non_fact_clause = Clause(['b'], 'a')
        self.assertTrue(fact_clause.is_fact)
        self.assertFalse(non_fact_clause.is_fact)

    def test_increment_known_count(self):
        """Test incrementing the known count of premises."""
        clause = Clause(['a', 'b', 'c'], 'd')
        self.assertFalse(clause.increment_known_count())  # 1/3
        self.assertFalse(clause.increment_known_count())  # 2/3
        self.assertTrue(clause.increment_known_count())  # 3/3

    def test_str_representation(self):
        """Test string representation of clauses."""
        clause1 = Clause(['a', 'b'], 'c')
        clause2 = Clause([], 'd')
        self.assertEqual(str(clause1), "(¬a ∧ ¬b) → c")
        self.assertEqual(str(clause2), "d")

    def test_from_string_fact(self):
        """Test parsing a fact from a string."""
        clause = Clause.from_string("a")
        self.assertEqual(clause.premise_literals, [])
        self.assertEqual(clause.conclusion_literal, "a")
        self.assertTrue(clause.is_fact)

    def test_from_string_simple_implication(self):
        """Test parsing a simple implication from a string."""
        clause = Clause.from_string("-a b")
        self.assertEqual(clause.premise_literals, ["a"])
        self.assertEqual(clause.conclusion_literal, "b")

    def test_from_string_complex_implication(self):
        """Test parsing a complex implication from a string."""
        clause = Clause.from_string("-a -b -c d")
        self.assertEqual(clause.premise_literals, ["a", "b", "c"])
        self.assertEqual(clause.conclusion_literal, "d")

    def test_from_string_invalid_no_conclusion(self):
        """Test parsing an invalid string (no conclusion)."""
        with self.assertRaises(ValueError):
            Clause.from_string("-a -b -c")

    def test_repr(self):
        """Test the repr representation."""
        clause = Clause(['a', 'b'], 'c')
        repr_str = repr(clause)
        self.assertIn("premise=['a', 'b']", repr_str)
        self.assertIn("conclusion=c", repr_str)
        self.assertIn("known_count=0", repr_str)


if __name__ == '__main__':
    unittest.main()