import ast
import random
from copy import deepcopy
import astor  # برای تبدیل AST به کد منبع


class AODMutator:
    """
    A class to perform Arithmetic Operator Deletion (AOD) mutation on a given AST.
    """

    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleAODMutator(ast.NodeTransformer):
        """
        A class to perform single Arithmetic Operator Deletion (AOD) mutation.
        """

        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_BinOp(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                # حذف عملگر و جایگزینی با یک طرف از عملگر
                return node.left if random.choice([True, False]) else node.right
            return self.generic_visit(node)

    def find_arithmetic_operators(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.operators = []

            def visit_BinOp(self, node):
                if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
                    self.operators.append(('arithmetic', node.lineno))
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.operators

    def generate_mutated_codes(self):
        self.mutated_codes = []
        operators = self.find_arithmetic_operators()

        random_indices = list(range(len(operators)))
        random.shuffle(random_indices)

        n = min(self.n, len(operators))
        # Generate mutated versions
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target arithmetic operator
            mutator = self.SingleAODMutator(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes


def print_codes(code, mutated_codes):
    print("Original Code:")
    print(code)

    for i, mutated_code in enumerate(mutated_codes):
        print(f"\nMutated Code {i + 1}:")
        print(mutated_code)
    print(64 * '-')


def test_AOD():
    # Example usage of AOD Mutator
    code = """
x = a + b
y = c * d
z = e / f - g
"""

    tree = ast.parse(code)
    mutator = AODMutator(tree, n=100)
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_AOD()
