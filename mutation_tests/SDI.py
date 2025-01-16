import ast
import random
from copy import deepcopy
import astor


class SDIMutator:
    """
    A class to perform Statement Deletion Inside (SDI) mutation on a given AST.
    """

    def __init__(self, tree, n=None):
        """
        Initialize the mutator.

        :param tree: The AST of the code.
        :param n: The number of mutations to generate. If n is None or float('inf'), all possible mutations will be generated.
        """
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleSDIMutator(ast.NodeTransformer):
        """
        A class to perform single Statement Deletion Inside (SDI) mutation.
        """

        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_body(self, node_body):
            """
            Helper function to process and mutate body nodes.
            """
            self.current_index += 1
            if self.current_index == self.target_index:
                # Remove the statement at the target index
                return []
            return node_body

        def visit_FunctionDef(self, node):
            node.body = self.visit_body(node.body)
            return self.generic_visit(node)

        def visit_ClassDef(self, node):
            node.body = self.visit_body(node.body)
            return self.generic_visit(node)

        def visit_Module(self, node):
            node.body = self.visit_body(node.body)
            return self.generic_visit(node)

    def find_statements(self):
        """
        Find all statements in the AST.
        """
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.statements = []

            def visit_FunctionDef(self, node):
                self.statements.extend(node.body)
                self.generic_visit(node)

            def visit_ClassDef(self, node):
                self.statements.extend(node.body)
                self.generic_visit(node)

            def visit_Module(self, node):
                self.statements.extend(node.body)
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.statements

    def generate_mutated_codes(self):
        """
        Generate mutated versions of the code.
        """
        self.mutated_codes = []
        statements = self.find_statements()

        # Generate indices for all statements
        random_indices = list(range(len(statements)))
        random.shuffle(random_indices)

        # If n is infinite or None, consider all statements
        n = len(statements) if self.n is None or self.n == float('inf') else min(self.n, len(statements))

        # Generate mutated versions
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target statement
            mutator = self.SingleSDIMutator(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes


def print_codes(code, mutated_codes):
    """
    Print the original and mutated versions of the code.
    """
    print("Original Code:")
    print(code)

    for i, mutated_code in enumerate(mutated_codes):
        print(f"\nMutated Code {i + 1}:")
        print(mutated_code)
    print('-' * 64)


def test_SDI():
    """
    Example usage of SDIMutator.
    """
    code = """
class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

calc = Calculator()
result = calc.add(10, 20)
print(result)
"""

    tree = ast.parse(code)
    mutator = SDIMutator(tree, n=float('inf'))  # Use float('inf') for infinite mutations
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_SDI()

