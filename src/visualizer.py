"""
Module for visualizing knowledge bases as directed graphs.

This module provides functionality to create graphviz directed graphs
representing the knowledge base and inference paths.
"""

import graphviz


def create_knowledge_graph(kb, inference_path=None):
    """
    Create a visualization of the knowledge base as a directed graph.

    This function creates a Graphviz graph showing the relationships between
    literals in the knowledge base. If an inference path is provided,
    the nodes in the path are highlighted.

    Args:
        kb (KnowledgeBase): The knowledge base to visualize
        inference_path (list, optional): The order of inferred symbols from forward chaining

    Returns:
        graphviz.Digraph: A graphviz graph representing the knowledge base
    """
    # Create a new directed graph
    dot = graphviz.Digraph(comment='Knowledge Base', format='png')

    # Set graph attributes for better appearance
    dot.attr('graph', rankdir='BT', size='10,10', ratio='fill')
    dot.attr('node', shape='ellipse', style='filled', fillcolor='lightgray',
             fontname='Arial', fontsize='12')
    dot.attr('edge', fontname='Arial', fontsize='10')

    # Create a unique identifier for intermediate nodes
    node_id = 0

    # Add all literals as nodes first
    for symbol in kb.get_all_symbols():
        # If inference path is provided, color the nodes accordingly
        if inference_path and symbol in inference_path:
            # Get the position in the inference path
            pos = inference_path.index(symbol)
            # Use a color gradient for the inference path
            # The first nodes are darker green, later nodes lighter
            color_intensity = 100 - min(80, 80 * pos / len(inference_path))
            fillcolor = f'#00{int(color_intensity):02x}00'
            fontcolor = 'white'
            dot.node(symbol, symbol, fillcolor=fillcolor, fontcolor=fontcolor)
        else:
            dot.node(symbol, symbol)

    # Add edges for each clause
    for clause in kb.clauses:
        conclusion = clause.conclusion_literal

        # Handle facts (clauses with no premises)
        if clause.is_fact:
            # For facts, use a special "FACT" node as source
            fact_node = f"FACT_{node_id}"
            node_id += 1
            dot.node(fact_node, "FACT", shape='box', fillcolor='lightblue')
            dot.edge(fact_node, conclusion, label='given')

        # Handle clauses with premises
        elif len(clause.premise_literals) == 1:
            # Single premise: direct edge
            premise = clause.premise_literals[0]
            dot.edge(premise, conclusion, label='implies')
        else:
            # Multiple premises: create an AND node
            and_node = f"AND_{node_id}"
            node_id += 1
            dot.node(and_node, "AND", shape='diamond', fillcolor='lightyellow')

            # Connect each premise to the AND node
            for premise in clause.premise_literals:
                dot.edge(premise, and_node)

            # Connect the AND node to the conclusion
            dot.edge(and_node, conclusion)

    return dot


def highlight_inference_path(graph, inference_path):
    """
    Highlight the inference path in the graph.

    Args:
        graph (graphviz.Digraph): The graph to modify
        inference_path (list): The ordered list of inferred symbols

    Returns:
        graphviz.Digraph: The modified graph with highlighted path
    """
    # Create a copy to avoid modifying the original
    highlighted = graph.copy()

    # Highlight nodes in the inference path
    for i, symbol in enumerate(inference_path):
        # Use a color gradient
        color_intensity = 100 - min(80, 80 * i / len(inference_path))
        fillcolor = f'#00{int(color_intensity):02x}00'
        highlighted.node(symbol, symbol, style='filled', fillcolor=fillcolor, fontcolor='white')

    return highlighted


def save_graph_to_file(graph, filename, view=False):
    """
    Save the graph to a file.

    Args:
        graph (graphviz.Digraph): The graph to save
        filename (str): The filename (without extension)
        view (bool, optional): Whether to open the rendered graph

    Returns:
        str: The path to the saved file
    """
    return graph.render(filename, cleanup=True, view=view)