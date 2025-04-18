"""
Module implementing the Forward Chaining algorithm for propositional logic.

This module contains the implementation of the PL-FC-ENTAILS? algorithm
as described in the project specification.
"""

from collections import defaultdict, deque


def forward_chaining(kb, query):
    """
    Determine if a query symbol is entailed by the knowledge base using forward chaining.

    This is an implementation of the PL-FC-ENTAILS? algorithm from the project specification.

    Args:
        kb (KnowledgeBase): The knowledge base of definite clauses
        query (str): The query symbol

    Returns:
        tuple: (is_entailed, inference_path)
            - is_entailed (bool): True if the query is entailed, False otherwise
            - inference_path (list): The order of inferred symbols (for visualization)
    """
    # Initialize count table: count[c] is the number of symbols in c's premise
    count = {clause: len(clause.premise_literals) for clause in kb.clauses}

    # Initialize inferred table: inferred[s] is initially false for all symbols
    inferred = defaultdict(bool)

    # Initialize agenda: a queue of symbols, initially symbols known to be true in KB
    agenda = deque(kb.get_facts())

    # Track inference order for visualization and debugging
    inference_path = []

    # While agenda is not empty
    while agenda:
        p = agenda.popleft()

        # If p is the query, we're done
        if p == query:
            inference_path.append(p)  # Add the query to the inference path
            return True, inference_path

        # If p has not been inferred yet
        if not inferred[p]:
            # Mark p as inferred
            inferred[p] = True
            inference_path.append(p)

            # For each clause where p is in the premise
            for clause in kb.get_clauses_with_premise(p):
                # Decrement the count for this clause
                count[clause] -= 1

                # If all premises are now known (count = 0)
                if count[clause] == 0:
                    # Add the conclusion to the agenda
                    agenda.append(clause.conclusion_literal)

    # If we get here, the query is not entailed
    return False, inference_path


def forward_chaining_with_trace(kb, query):
    """
    Extended version of forward chaining that provides detailed tracing.

    Similar to forward_chaining(), but returns additional information
    for debugging and visualization.

    Args:
        kb (KnowledgeBase): The knowledge base of definite clauses
        query (str): The query symbol

    Returns:
        tuple: (is_entailed, inference_path, trace)
            - is_entailed (bool): True if the query is entailed, False otherwise
            - inference_path (list): The order of inferred symbols
            - trace (list): Detailed trace of algorithm steps
    """
    # Initialize count table: count[c] is the number of symbols in c's premise
    count = {clause: len(clause.premise_literals) for clause in kb.clauses}

    # Initialize inferred table: inferred[s] is initially false for all symbols
    inferred = defaultdict(bool)

    # Initialize agenda: a queue of symbols, initially symbols known to be true in KB
    agenda = deque(kb.get_facts())

    # Track inference order and algorithm trace
    inference_path = []
    trace = []

    # Initial state for trace
    trace.append({
        'step': 0,
        'action': 'Initialize',
        'agenda': list(agenda),
        'inferred': {k: v for k, v in inferred.items() if v},
        'count': {str(k): v for k, v in count.items()}
    })

    step = 1

    # While agenda is not empty
    while agenda:
        p = agenda.popleft()

        trace.append({
            'step': step,
            'action': f'Pop from agenda: {p}',
            'agenda': list(agenda),
            'current': p
        })
        step += 1

        # If p is the query, we're done
        if p == query:
            inference_path.append(p)
            trace.append({
                'step': step,
                'action': f'Found query: {p}',
                'result': 'ENTAILED'
            })
            return True, inference_path, trace

        # If p has not been inferred yet
        if not inferred[p]:
            # Mark p as inferred
            inferred[p] = True
            inference_path.append(p)

            trace.append({
                'step': step,
                'action': f'Infer: {p}',
                'inferred': {k: v for k, v in inferred.items() if v}
            })
            step += 1

            # For each clause where p is in the premise
            affected_clauses = kb.get_clauses_with_premise(p)
            for clause in affected_clauses:
                # Decrement the count for this clause
                old_count = count[clause]
                count[clause] -= 1
                new_count = count[clause]

                trace.append({
                    'step': step,
                    'action': f'Update count for {clause}',
                    'clause': str(clause),
                    'old_count': old_count,
                    'new_count': new_count
                })
                step += 1

                # If all premises are now known (count = 0)
                if new_count == 0:
                    # Add the conclusion to the agenda
                    conclusion = clause.conclusion_literal
                    agenda.append(conclusion)

                    trace.append({
                        'step': step,
                        'action': f'Add to agenda: {conclusion}',
                        'reason': f'All premises of {clause} are known',
                        'agenda': list(agenda)
                    })
                    step += 1

    # If we get here, the query is not entailed
    trace.append({
        'step': step,
        'action': 'Agenda empty',
        'result': 'NOT ENTAILED'
    })
    return False, inference_path, trace