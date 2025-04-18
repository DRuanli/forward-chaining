"""
Module for managing a knowledge base of propositional logic clauses.

This module contains the KnowledgeBase class which manages a collection
of definite clauses and provides operations for inference.
"""

from collections import defaultdict
from src.clause import Clause


class KnowledgeBase:
    """
    A class representing a knowledge base of definite clauses in propositional logic.

    The knowledge base stores clauses, indexes them for efficient access,
    and provides methods for querying and inference.
    """

    def __init__(self):
        """
        Initialize an empty knowledge base.
        """
        self.clauses = []  # List of all clauses
        self.clauses_by_premise = defaultdict(list)  # Map from symbols to clauses containing them in premise
        self.facts = set()  # Set of known facts (symbols)

    def add_clause(self, clause):
        """
        Add a clause to the knowledge base.

        Args:
            clause (Clause): The clause to add
        """
        self.clauses.append(clause)

        # If it's a fact, add it to our facts set
        if clause.is_fact:
            self.facts.add(clause.conclusion_literal)

        # Index the clause by its premise literals
        for literal in clause.premise_literals:
            self.clauses_by_premise[literal].append(clause)

    def load_from_file(self, filename):
        """
        Load clauses from a file.

        Args:
            filename (str): Path to the file containing clauses

        Returns:
            KnowledgeBase: self for method chaining

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If a line in the file isn't a valid clause
        """
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    clause = Clause.from_string(line)
                    self.add_clause(clause)
        return self

    def get_facts(self):
        """
        Get all facts in the knowledge base.

        Returns:
            set: Set of all facts (symbols known to be true)
        """
        return self.facts

    def get_clauses_with_premise(self, symbol):
        """
        Get all clauses that have the given symbol in their premise.

        Args:
            symbol (str): The symbol to search for in premises

        Returns:
            list: List of clauses containing the symbol in their premise
        """
        return self.clauses_by_premise.get(symbol, [])

    def get_all_symbols(self):
        """
        Get all unique symbols used in the knowledge base.

        Returns:
            set: Set of all symbols
        """
        symbols = set()

        # Add all conclusion literals
        for clause in self.clauses:
            symbols.add(clause.conclusion_literal)

            # Add all premise literals
            for literal in clause.premise_literals:
                symbols.add(literal)

        return symbols

    def __str__(self):
        """
        Return a string representation of the knowledge base.

        Returns:
            str: A formatted string listing all clauses in the knowledge base
        """
        return "\n".join(str(clause) for clause in self.clauses)