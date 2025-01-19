import ast
import astor
import random
from copy import deepcopy


class ASRMutator:
    """
    A class to perform Assignment Operator Replacement (ASR) mutation on a given AST.
    """

    def __init__(self, tree, n):
        self.tree = tree
        self.n = float('inf') if n is None else n
        self.mutated_codes = []

    class SingleASRMutator(ast.NodeTransformer):
        """
        A class to perform single Assignment Operator Replacement (ASR) mutation.
        """

        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1
            self.operators = [ast.Add, ast.Sub, ast.Mult, ast.Div]

        def visit_Assign(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                # Replace the assignment with a random arithmetic operation
                new_operator = random.choice(self.operators)
                new_node = ast.BinOp(left=node.targets[0], op=new_operator(), right=node.value)
                node.value = new_node
            return self.generic_visit(node)

    def find_assignment_operators(self):
        """
        Find assignment operators in the AST.
        """
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.assignments = []

            def visit_Assign(self, node):
                self.assignments.append(('assignment', node.lineno))
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.assignments

    def generate_mutated_codes(self):
        """
        Generate mutated code by replacing assignment operators.
        """
        self.mutated_codes = []
        assignments = self.find_assignment_operators()

        random_indices = list(range(len(assignments)))
        random.shuffle(random_indices)

        n = min(self.n, len(assignments))
        # Generate mutated versions
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target assignment operator
            mutator = self.SingleASRMutator(target_index=i)
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
    print(64 * '-')


def test_ASR():
    # Example usage of ASR Mutator
    code = """
# Module: orders.py
x = 10
y = 5
z = x + y
u = x / y
"""

    tree = ast.parse(code)
    mutator = ASRMutator(tree, n=None)  # Or n=float('inf')
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_ASR()
