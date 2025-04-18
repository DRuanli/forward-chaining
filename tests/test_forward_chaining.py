"""
Unit tests for the forward_chaining module.
"""

import unittest
from src.knowledge_base import KnowledgeBase
from src.clause import Clause
from src.forward_chaining import forward_chaining, forward_chaining_with_trace


class TestForwardChaining(unittest.TestCase):
    """Test cases for the forward chaining algorithm."""

    def setUp(self):
        """Set up a knowledge base with test clauses."""
        # Create a simple knowledge base for testing
        self.kb = KnowledgeBase()

        # Add clauses: a, a → b, a ∧ b → c, b → d
        self.kb.add_clause(Clause([], 'a'))  # a is a fact
        self.kb.add_clause(Clause(['a'], 'b'))  # a → b
        self.kb.add_clause(Clause(['a', 'b'], 'c'))  # a ∧ b → c
        self.kb.add_clause(Clause(['b'], 'd'))  # b → d

    def test_forward_chaining_entailed(self):
        """Test forward chaining with entailed queries."""
        # Test various queries that should be entailed
        result_a, order_a = forward_chaining(self.kb, 'a')
        result_b, order_b = forward_chaining(self.kb, 'b')
        result_c, order_c = forward_chaining(self.kb, 'c')
        result_d, order_d = forward_chaining(self.kb, 'd')

        # Assertions for entailment
        self.assertTrue(result_a)
        self.assertTrue(result_b)
        self.assertTrue(result_c)
        self.assertTrue(result_d)

        # Check correct inference order for 'c'
        self.assertEqual(order_c, ['a', 'b', 'c'])

        # Check correct inference order for 'd'
        self.assertEqual(order_d, ['a', 'b', 'd'])

    def test_forward_chaining_not_entailed(self):
        """Test forward chaining with non-entailed queries."""
        # Test a query that should not be entailed
        result, order = forward_chaining(self.kb, 'e')

        self.assertFalse(result)
        self.assertEqual(set(order), {'a', 'b', 'c', 'd'})  # All inferred symbols

    def test_cyclic_knowledge_base(self):
        """Test forward chaining with a cyclic knowledge base."""
        # Create a knowledge base with cycles
        kb = KnowledgeBase()
        kb.add_clause(Clause([], 'a'))  # a is a fact
        kb.add_clause(Clause(['a'], 'b'))  # a → b
        kb.add_clause(Clause(['b'], 'c'))  # b → c
        kb.add_clause(Clause(['c'], 'a'))  # c → a (cycle)

        # Should still terminate correctly
        result, order = forward_chaining(kb, 'd')

        self.assertFalse(result)
        self.assertEqual(set(order), {'a', 'b', 'c'})  # All symbols in the cycle

    def test_empty_knowledge_base(self):
        """Test forward chaining with an empty knowledge base."""
        kb = KnowledgeBase()
        result, order = forward_chaining(kb, 'a')

        self.assertFalse(result)
        self.assertEqual(order, [])

    def test_disconnected_knowledge_base(self):
        """Test forward chaining with a disconnected knowledge base."""
        kb = KnowledgeBase()
        kb.add_clause(Clause([], 'a'))  # a is a fact
        kb.add_clause(Clause([], 'b'))  # b is a fact
        kb.add_clause(Clause(['a'], 'c'))  # a → c
        kb.add_clause(Clause(['b'], 'd'))  # b → d

        # Should infer both branches
        result, order = forward_chaining(kb, 'd')

        self.assertTrue(result)
        self.assertIn('a', order)
        self.assertIn('b', order)
        self.assertIn('c', order)
        self.assertIn('d', order)

    def test_forward_chaining_with_trace(self):
        """Test the detailed tracing version of forward chaining."""
        result, path, trace = forward_chaining_with_trace(self.kb, 'c')

        # Check result and path
        self.assertTrue(result)
        self.assertEqual(path, ['a', 'b', 'c'])

        # Check trace structure
        self.assertIsInstance(trace, list)
        self.assertGreater(len(trace), 0)

        # First step should be initialization
        self.assertEqual(trace[0]['action'], 'Initialize')

        # Last step should be finding the query
        self.assertEqual(trace[-1]['action'], 'Found query: c')
        self.assertEqual(trace[-1]['result'], 'ENTAILED')


if __name__ == '__main__':
    unittest.main()