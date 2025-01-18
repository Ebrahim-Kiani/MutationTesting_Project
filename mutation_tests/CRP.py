import ast
import astor
import random
from copy import deepcopy


class CRPMutator():
    """
    A class to perform Constant Replacement (CRP) mutation on a given AST.
    """
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleCRPMutator(ast.NodeTransformer):
        """
        A class to perform a single Constant Replacement (CRP) mutation.
        """
        def __init__(self, target_index, start, end):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1
            self.start = start
            self.end = end

        def visit_Constant(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                # Replace the constant with the new value
                return ast.Constant(value=random.randint(self.start, self.end))
            return node

    def find_constants(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.constants = []

            def visit_Constant(self, node):
                self.constants.append(node)
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.constants

    def generate_mutated_codes(self, start, end):
        self.mutated_codes = []  
        constants = self.find_constants()

        random_indices = list(range(len(constants)))
        random.shuffle(random_indices)  

        n = min(self.n, len(constants))  
        # Generate mutated versions
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)  

            # Mutate the target constant
            mutator = self.SingleCRPMutator(target_index=i, start=start, end=end)
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
    print(64*'-')


def test_CRP():
    # Example usage of CRP Mutator
    code = """
def check_value(x):
    x = 12
    y = 13
    if x > 5:
        return True
    elif x < 3 and x > 0:
        return False
    else:
        return x == 4
"""

    tree = ast.parse(code)
    mutator = CRPMutator(tree, n=2)
    mutated_codes = mutator.generate_mutated_codes(1, 100)
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_CRP()
