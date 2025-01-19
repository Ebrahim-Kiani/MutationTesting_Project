import ast
import astor
import random
from copy import deepcopy


class BCRMutator():
    """
    A class to perform Break Continue Replacement (BCR) mutation on a given AST.
    """
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleBCRMutator(ast.NodeTransformer):
        """
        A class to perform single Break Continue Replacement (BCR) mutation.
        """
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_Break(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                return ast.Continue()  # Replace 'break' with 'continue'
            return node

        def visit_Continue(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                return ast.Break()  # Replace 'continue' with 'break'
            return node

    def find_break_continue_statements(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.statements = []

            def visit_Break(self, node):
                self.statements.append(('break', node.lineno))
                self.generic_visit(node)

            def visit_Continue(self, node):
                self.statements.append(('continue', node.lineno))
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.statements

    def generate_mutated_codes(self):
        self.mutated_codes = []
        statements = self.find_break_continue_statements()

        random_indices = list(range(len(statements)))
        random.shuffle(random_indices)

        n = min(self.n, len(statements))
        # Generate mutated codes
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target statement
            mutator = self.SingleBCRMutator(target_index=i)
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


def test_BCR():
    # Example usage of BCR Mutator
    code = """
for i in range(10):
    if i == 5:
        break
    if i % 2 == 0:
        continue
        break
        break
    print(i)
"""

    tree = ast.parse(code)
    mutator = BCRMutator(tree, n=2)
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_BCR()
