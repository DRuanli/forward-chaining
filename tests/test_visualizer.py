"""
Unit tests for the visualizer module.
"""

import unittest
import os
import tempfile
from src.knowledge_base import KnowledgeBase
from src.clause import Clause
from src.visualizer import create_knowledge_graph, highlight_inference_path, save_graph_to_file


class TestVisualizer(unittest.TestCase):
    """Test cases for the visualization functionality."""

    def setUp(self):
        """Set up a knowledge base with test clauses."""
        # Create a simple knowledge base for testing
        self.kb = KnowledgeBase()

        # Add clauses: a, a → b, a ∧ b → c
        self.kb.add_clause(Clause([], 'a'))  # a is a fact
        self.kb.add_clause(Clause(['a'], 'b'))  # a → b
        self.kb.add_clause(Clause(['a', 'b'], 'c'))  # a ∧ b → c

        # Create a simple inference path
        self.inference_path = ['a', 'b', 'c']

    def test_create_knowledge_graph(self):
        """Test creating a knowledge graph without inference path."""
        graph = create_knowledge_graph(self.kb)

        # Basic checks that the graph was created correctly
        self.assertIsNotNone(graph)
        self.assertEqual(graph.format, 'png')

        # The graph body should contain node and edge definitions
        body_str = '\n'.join(graph.body)

        # Check that all symbols are in the graph
        self.assertIn('a [', body_str)
        self.assertIn('b [', body_str)
        self.assertIn('c [', body_str)

        # Check for edges (connections between nodes)
        self.assertIn(' -> ', body_str)

    def test_create_knowledge_graph_with_inference(self):
        """Test creating a knowledge graph with an inference path."""
        graph = create_knowledge_graph(self.kb, self.inference_path)

        # The graph should have highlighted nodes for the inference path
        body_str = '\n'.join(graph.body)

        # Check that nodes in the inference path have special attributes
        self.assertIn('a [', body_str)
        self.assertIn('fillcolor="#', body_str)  # Colored nodes

    def test_highlight_inference_path(self):
        """Test highlighting an inference path in an existing graph."""
        original_graph = create_knowledge_graph(self.kb)
        highlighted_graph = highlight_inference_path(original_graph, self.inference_path)

        # Check that the original graph is unchanged
        original_body = '\n'.join(original_graph.body)

        # Check that the highlighted graph has colored nodes
        highlighted_body = '\n'.join(highlighted_graph.body)

        # The highlighted graph should differ from the original
        self.assertNotEqual(original_body, highlighted_body)
        self.assertIn('fillcolor="#', highlighted_body)

    def test_save_graph_to_file(self):
        """Test saving a graph to a file."""
        graph = create_knowledge_graph(self.kb)

        # Create a temporary directory for the output
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, 'test_graph')

            # Save the graph
            result_path = save_graph_to_file(graph, output_path, view=False)

            # Check that the file was created
            self.assertTrue(os.path.exists(f"{output_path}.png"))
            self.assertEqual(result_path, f"{output_path}.png")


if __name__ == '__main__':
    unittest.main()