"""
Module for representing propositional logic clauses.

This module contains the Clause class which represents a definite clause
in propositional logic, with premises (negated literals) and a conclusion.
"""


class Clause:
    """
    A class representing a definite clause in propositional logic.

    A definite clause is a disjunction of literals with exactly one positive literal.
    In this implementation, we represent it as an implication where:
    - The premise is a conjunction of negative literals
    - The conclusion is a single positive literal

    For example, the clause "-a -b c" is interpreted as:
    "If NOT a AND NOT b, then c" or "¬a ∧ ¬b → c"
    """

    def __init__(self, premise_literals, conclusion_literal):
        """
        Initialize a clause with premise literals and a conclusion literal.

        Args:
            premise_literals (list of str): The list of literals in the premise (without negation)
            conclusion_literal (str): The conclusion literal (without negation)
        """
        self.premise_literals = premise_literals  # List of literals in the premise
        self.conclusion_literal = conclusion_literal  # The conclusion literal
        self.known_count = 0  # Number of known literals in the premise

    def __str__(self):
        """
        Return a string representation of the clause.

        Returns:
            str: A formatted string representing the clause
        """
        if not self.premise_literals:
            return f"{self.conclusion_literal}"

        premise_str = " ∧ ".join([f"¬{lit}" for lit in self.premise_literals])
        return f"({premise_str}) → {self.conclusion_literal}"

    def __repr__(self):
        """
        Return a string representation of the clause for debugging.

        Returns:
            str: A string representation of the clause object
        """
        return f"Clause(premise={self.premise_literals}, conclusion={self.conclusion_literal}, known_count={self.known_count})"

    def increment_known_count(self):
        """
        Increment the count of known literals in the premise.

        This is used by the forward chaining algorithm to track
        how many premises of a clause are known to be true.

        Returns:
            bool: True if all premise literals are now known, False otherwise
        """
        self.known_count += 1
        return self.known_count >= len(self.premise_literals)

    @property
    def is_fact(self):
        """
        Check if this clause is a fact (has no premises).

        A fact is a clause with no premises, e.g., just "a".

        Returns:
            bool: True if the clause is a fact, False otherwise
        """
        return len(self.premise_literals) == 0

    @classmethod
    def from_string(cls, clause_str):
        """
        Create a Clause object from a string representation.

        Args:
            clause_str (str): A string in the format "-a -b c" or "c" where -a and -b are
                              premise literals and c is the conclusion

        Returns:
            Clause: A new Clause object representing the given string

        Raises:
            ValueError: If the clause string does not contain a positive literal (conclusion)
        """
        literals = clause_str.strip().split()

        # Separate premises and conclusion
        premise_literals = []
        conclusion_literal = None

        for literal in literals:
            if literal.startswith('-'):
                # This is a negated literal (premise)
                premise_literals.append(literal[1:])  # Remove the negation for storage
            else:
                # This is a positive literal (conclusion)
                conclusion_literal = literal
                break

        # Validate that we have a conclusion
        if conclusion_literal is None and literals:
            # Special case: if there's just one literal and it's positive, it's a fact
            if len(literals) == 1 and not literals[0].startswith('-'):
                conclusion_literal = literals[0]
                premise_literals = []
            else:
                raise ValueError("Definite clause must have exactly one positive literal (conclusion)")

        return cls(premise_literals, conclusion_literal)