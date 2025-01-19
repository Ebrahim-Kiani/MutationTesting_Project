import ast
import random
from copy import deepcopy
import astor


class SCDMutator:
    """
    A class to perform Single Conditional Deletion (SCD) mutation on a given AST.
    """

    def __init__(self, tree, n=None):
        """
        Initialize the mutator.

        Args:
            tree: The AST tree of the code.
            n: The maximum number of mutations to apply. If None or float('inf'), mutate all possible conditions.
        """
        self.tree = tree
        self.n = float('inf') if n is None else n
        self.mutated_codes = []

    class SingleSCDMutator(ast.NodeTransformer):
        """
        A class to perform single Conditional Deletion (SCD) mutation.
        """

        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_If(self, node):
            """
            Delete the condition from the target 'if' statement.
            """
            self.current_index += 1
            if self.current_index == self.target_index:
                # Remove the condition by replacing it with 'True'
                node.test = ast.Constant(value=True)
            return self.generic_visit(node)

    def find_conditionals(self):
        """
        Identify all conditional statements in the AST.
        """

        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.conditionals = []

            def visit_If(self, node):
                self.conditionals.append(('if', node.lineno))
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.conditionals

    def generate_mutated_codes(self):
        """
        Generate mutated versions of the code.
        """
        self.mutated_codes = []
        conditionals = self.find_conditionals()

        random_indices = list(range(len(conditionals)))
        random.shuffle(random_indices)

        n = min(self.n, len(conditionals))  # Limit n to the total number of conditionals
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target conditional statement
            mutator = self.SingleSCDMutator(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            try:
                mutated_code = astor.to_source(mutated_tree)
                self.mutated_codes.append(mutated_code)
            except:
                pass

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
    print('-' * 64)  # Corrected separator line


def test_SCD():
    """
    Example usage of SCD Mutator.
    """
    code = """
class Payment:
    def process_payment(self, order, amount):
        try:
            if amount >= order.calculate_total():
                order.pay()
                return True
            else:
                raise ValueError("Insufficient funds")
        except ValueError as e:
            print(f"Payment error: {e}")
            return False
"""

    tree = ast.parse(code)

    # Example 2: Mutate all conditions
    mutator = SCDMutator(tree, n=None)  # Or n=float('inf')
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_SCD()
