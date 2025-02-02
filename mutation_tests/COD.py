import ast
import astor
import random
from copy import deepcopy


class CODMutator():
    """
    A class to perform Conditional Operator Deletion (COD) mutation on a given AST.
    """
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleCODMutator(ast.NodeTransformer):
        """
        A class to perform single Conditional Operator Deletion (COD) mutation.
        """
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_Compare(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                return ast.Constant(value=random.choice([True, False]))  # Replace with a valid constant
            return node

    def find_conditional_operators(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.operators = []

            def visit_Compare(self, node):
                self.operators.append(('compare', node.lineno))
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.operators

    def generate_mutated_codes(self):
        self.mutated_codes = []
        operators = self.find_conditional_operators()

        random_indices = list(range(len(operators)))
        random.shuffle(random_indices)

        n = min(self.n, len(operators))
        # Generate mutated versions
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target conditional operator
            mutator = self.SingleCODMutator(target_index=i)
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
    print("Original Code:")
    print(code)

    for i, mutated_code in enumerate(mutated_codes):
        print(f"\nMutated Code {i + 1}:")
        print(mutated_code)
    print(64*'-')


def test_COD():
    # Example usage of COD Mutator
    code = """
if x == 5:
    print("x is 5")
elif x == 10:
    print("x is 10")
else:
    print("x is neither 5 nor 10")
"""

    tree = ast.parse(code)
    mutator = CODMutator(tree, n=2)
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_COD()
