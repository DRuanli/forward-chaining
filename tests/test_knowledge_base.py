"""
Unit tests for the KnowledgeBase class.
"""

import unittest
import os
import tempfile
from src.knowledge_base import KnowledgeBase
from src.clause import Clause


class TestKnowledgeBase(unittest.TestCase):
    """Test cases for the KnowledgeBase class."""

    def setUp(self):
        """Set up a knowledge base with some test clauses."""
        self.kb = KnowledgeBase()

        # Add some test clauses
        self.kb.add_clause(Clause([], 'a'))  # a is a fact
        self.kb.add_clause(Clause(['a'], 'b'))  # a → b
        self.kb.add_clause(Clause(['a', 'b'], 'c'))  # a ∧ b → c

    def test_add_clause(self):
        """Test adding clauses to the knowledge base."""
        self.assertEqual(len(self.kb.clauses), 3)

        # Test facts are correctly identified
        self.assertIn('a', self.kb.facts)
        self.assertNotIn('b', self.kb.facts)
        self.assertNotIn('c', self.kb.facts)

        # Test clauses are indexed by premise
        self.assertEqual(len(self.kb.get_clauses_with_premise('a')), 2)
        self.assertEqual(len(self.kb.get_clauses_with_premise('b')), 1)
        self.assertEqual(len(self.kb.get_clauses_with_premise('c')), 0)

    def test_get_facts(self):
        """Test retrieving facts from the knowledge base."""
        facts = self.kb.get_facts()
        self.assertEqual(facts, {'a'})

        # Add another fact
        self.kb.add_clause(Clause([], 'd'))
        facts = self.kb.get_facts()
        self.assertEqual(facts, {'a', 'd'})

    def test_get_clauses_with_premise(self):
        """Test retrieving clauses by premise."""
        # 'a' appears in the premise of two clauses
        a_clauses = self.kb.get_clauses_with_premise('a')
        self.assertEqual(len(a_clauses), 2)

        # 'b' appears in the premise of one clause
        b_clauses = self.kb.get_clauses_with_premise('b')
        self.assertEqual(len(b_clauses), 1)

        # 'c' doesn't appear in any premise
        c_clauses = self.kb.get_clauses_with_premise('c')
        self.assertEqual(len(c_clauses), 0)

        # Unknown symbol should return empty list
        z_clauses = self.kb.get_clauses_with_premise('z')
        self.assertEqual(len(z_clauses), 0)

    def test_load_from_file(self):
        """Test loading clauses from a file."""
        # Create a temporary file with test content
        temp_content = "a\n-a b\n-a -b c\n"
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write(temp_content)
            tmp_name = tmp.name

        try:
            new_kb = KnowledgeBase()
            new_kb.load_from_file(tmp_name)

            # Check that the right number of clauses were loaded
            self.assertEqual(len(new_kb.clauses), 3)

            # Check that facts were correctly identified
            self.assertEqual(new_kb.get_facts(), {'a'})

            # Check that premises were correctly indexed
            self.assertEqual(len(new_kb.get_clauses_with_premise('a')), 2)
            self.assertEqual(len(new_kb.get_clauses_with_premise('b')), 1)
        finally:
            # Clean up the temporary file
            os.unlink(tmp_name)

    def test_get_all_symbols(self):
        """Test retrieving all symbols in the knowledge base."""
        symbols = self.kb.get_all_symbols()
        self.assertEqual(symbols, {'a', 'b', 'c'})

        # Add a clause with a new symbol
        self.kb.add_clause(Clause(['d'], 'e'))
        symbols = self.kb.get_all_symbols()
        self.assertEqual(symbols, {'a', 'b', 'c', 'd', 'e'})

    def test_str_representation(self):
        """Test string representation of the knowledge base."""
        kb_str = str(self.kb)
        self.assertIn("a", kb_str)
        self.assertIn("(¬a) → b", kb_str)
        self.assertIn("(¬a ∧ ¬b) → c", kb_str)


if __name__ == '__main__':
    unittest.main()