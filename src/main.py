"""
Main module for the Forward Chaining application.

This module provides a command-line interface for loading knowledge bases,
running the forward chaining algorithm, and visualizing the results.
"""

import argparse
import os
import sys
import json
from src.knowledge_base import KnowledgeBase
from src.forward_chaining import forward_chaining, forward_chaining_with_trace
from src.visualizer import create_knowledge_graph, save_graph_to_file


def main():
    """
    Main function to run the forward chaining algorithm on a knowledge base.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Forward Chaining for Propositional Logic',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--data', type=str, default='data/data.txt',
                        help='Path to the data file containing clauses')
    parser.add_argument('--query', type=str, required=True,
                        help='Query symbol to check entailment')
    parser.add_argument('--output', type=str, default='knowledge_graph',
                        help='Output filename for graph visualization (without extension)')
    parser.add_argument('--verbose', action='store_true',
                        help='Show detailed execution trace')
    parser.add_argument('--view', action='store_true',
                        help='Open the visualization after generating it')
    parser.add_argument('--trace-file', type=str, default=None,
                        help='Save execution trace to a JSON file')

    args = parser.parse_args()

    # Check if the data file exists
    if not os.path.exists(args.data):
        print(f"Error: Data file '{args.data}' not found.")
        sys.exit(1)

    try:
        # Load the knowledge base
        print(f"Loading knowledge base from '{args.data}'...")
        kb = KnowledgeBase()
        kb.load_from_file(args.data)

        print(f"Knowledge base loaded successfully with {len(kb.clauses)} clauses.")
        if args.verbose:
            print("\nKnowledge base contents:")
            print(kb)
            print(f"\nInitial facts: {', '.join(kb.get_facts())}\n")

        # Run forward chaining
        print(f"\nRunning forward chaining to check if '{args.query}' is entailed...")

        if args.verbose or args.trace_file:
            is_entailed, inference_path, trace = forward_chaining_with_trace(kb, args.query)

            # Save trace to file if requested
            if args.trace_file:
                with open(args.trace_file, 'w') as f:
                    json.dump(trace, f, indent=2)
                print(f"Execution trace saved to '{args.trace_file}'")

            # Print detailed trace if verbose
            if args.verbose:
                print("\nExecution trace:")
                for step in trace:
                    print(f"Step {step['step']}: {step['action']}")
                    for k, v in step.items():
                        if k not in ['step', 'action']:
                            print(f"  {k}: {v}")
                    print()
        else:
            is_entailed, inference_path = forward_chaining(kb, args.query)

        # Print the result
        if is_entailed:
            print(f"\nResult: Query '{args.query}' IS entailed by the knowledge base.")
            print(f"Inference path: {' → '.join(inference_path)}")
        else:
            print(f"\nResult: Query '{args.query}' is NOT entailed by the knowledge base.")
            if inference_path:
                print(f"Symbols that could be inferred: {', '.join(inference_path)}")

        # Create and save the knowledge graph
        print(f"\nCreating knowledge graph visualization...")
        graph = create_knowledge_graph(kb, inference_path)

        output_path = save_graph_to_file(graph, args.output, view=args.view)
        print(f"Knowledge graph saved to '{output_path}'")

        print("\nDone!")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()