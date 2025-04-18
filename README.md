# Forward Chaining for Propositional Logic

A comprehensive implementation of the Forward Chaining algorithm for propositional logic with graph visualization capabilities. This project is developed for the Introduction to Artificial Intelligence course at Ton Duc Thang University.

## Features

- Parse and represent definite clauses from text files
- Implement the Forward Chaining algorithm for inference
- Visualize the knowledge base as a directed graph using Graphviz
- Check whether a given query symbol is entailed by the knowledge base
- Provide detailed execution traces for debugging and understanding

## Requirements

- Python 3.6 or higher
- Graphviz (for visualization)
- Python packages:
  - graphviz
  - pytest (for running tests)

## Installation

1. Ensure you have Python 3.6+ installed
2. Install Graphviz system package:
   - For Ubuntu/Debian: `sudo apt-get install graphviz`
   - For macOS: `brew install graphviz`
   - For Windows: Download and install from the [Graphviz website](https://graphviz.org/download/)
3. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/forward-chaining.git
   cd forward-chaining
   ```
4. Install Python dependencies:
   ```bash
   pip install graphviz pytest
   ```

## Usage

### Basic Usage

Run the program with a knowledge base file and a query:

```bash
python -m src.main --data data/data.txt --query c
```

This will:
1. Load the knowledge base from `data/data.txt`
2. Check if the symbol `c` is entailed by the knowledge base
3. Generate a visualization of the knowledge base in `knowledge_graph.png`

### Command Line Arguments

- `--data`: Path to the knowledge base file (default: `data/data.txt`)
- `--query`: Symbol to check entailment for (required)
- `--output`: Output filename for the visualization, without extension (default: `knowledge_graph`)
- `--verbose`: Show detailed execution trace
- `--view`: Open the visualization after generating it
- `--trace-file`: Save execution trace to a specified JSON file

### Input File Format

The knowledge base file should contain one clause per line in the format:
- `-a -b c` (meaning "if not a and not b, then c")
- `a` (meaning "a is true" - a fact)

Negative literals (negated variables) start with a hyphen `-`, and positive literals (conclusions) don't have a prefix.

## Implementation Details

### Components

1. **Clause Class** (`src/clause.py`)
   - Represents a definite clause in propositional logic
   - Stores the premise literals, conclusion literal, and known count
   - Provides methods for parsing clauses from string format

2. **Knowledge Base** (`src/knowledge_base.py`)
   - Stores and manages a collection of clauses
   - Provides methods for querying and accessing clauses
   - Indexes clauses by premises for efficient lookup

3. **Forward Chaining Algorithm** (`src/forward_chaining.py`)
   - Implements the PL-FC-ENTAILS? algorithm as specified
   - Determines if a query symbol is entailed by the knowledge base
   - Provides a version with detailed execution tracing

4. **Visualization Utilities** (`src/visualizer.py`)
   - Creates directed graph visualizations of the knowledge base
   - Highlights inference paths for better understanding
   - Saves graphs to files in various formats

5. **Command Line Interface** (`src/main.py`)
   - Provides a user-friendly interface to the program
   - Handles command-line arguments and file I/O
   - Orchestrates the overall execution flow

### Algorithm Details

The Forward Chaining algorithm works as follows:
1. Initialize count table for each clause (number of premises)
2. Initialize inferred status for all symbols (initially false)
3. Initialize agenda with known facts
4. Process symbols from the agenda:
   - Mark the symbol as inferred
   - Update count for clauses containing the symbol in their premise
   - When all premises of a clause are known, add its conclusion to the agenda
5. Continue until either the query is proven or no more inferences can be made

## Running Tests

The project includes comprehensive unit tests for all components:

```bash
# Run all tests
pytest

# Run tests for a specific module
pytest tests/test_clause.py

# Run tests with verbose output
pytest -v
```

## Creating a New Knowledge Base

To create a new knowledge base, follow these steps:
1. Create a text file with one clause per line
2. Use the following format:
   - For facts: `a`
   - For implications: `-a -b c` (meaning if not a and not b, then c)
3. Save the file with a `.txt` extension
4. Run the program with your new file:
   ```bash
   python -m src.main --data path/to/your/file.txt --query your_query
   ```

## License

[MIT License](LICENSE)

## Author

[Your Name]

## Acknowledgments

- This project was developed for the Introduction to Artificial Intelligence course at Ton Duc Thang University
- Thanks to the instructor for providing the project requirements and guidance# forward-chaining
