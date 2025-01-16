import ast
import random
from copy import deepcopy
import astor


class AORMutator:
    """
    A class to perform Arithmetic Operator Replacement (AOR) mutation on a given AST.
    """

    def __init__(self, tree, n):
        self.tree = tree
        self.n = float('inf') if n is None else n
        self.mutated_codes = []

    class SingleAORMutator(ast.NodeTransformer):
        """
        A class to perform single Arithmetic Operator Replacement (AOR) mutation.
        """

        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1
            self.operators = [ast.Add, ast.Sub, ast.Mult, ast.Div]

        def visit_BinOp(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                # Replace the operator with a random different operator
                current_operator = type(node.op)
                possible_operators = [op for op in self.operators if op != current_operator]
                new_operator = random.choice(possible_operators)
                node.op = new_operator()
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
            mutator = self.SingleAORMutator(target_index=i)
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


def test_AOR():
    # Example usage of AOR Mutator
    code = """
# Module: orders.py
class Order:
    def __init__(self, customer):
        self.customer = customer
        self.items = []
        self.total = 0
        self.paid = False

    def add_product(self, product, quantity):
        self.items.append((product, quantity))

    def calculate_total(self):
        self.total = sum(product.price * quantity for product, quantity in self.items)
        if isinstance(self.customer, VIPCustomer):
            self.total *= (1 - self.customer.get_discount_rate())
        return self.total
"""

    tree = ast.parse(code)
    mutator = AORMutator(tree, n=None)  # Or n=float('inf')
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_AOR()
