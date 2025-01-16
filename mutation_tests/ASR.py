import ast
import random
from copy import deepcopy
import astor


class ASRMutator:
    """
    A class to perform Arithmetic Statement Replacement (ASR) mutation on a given AST.
    """

    def __init__(self, tree, n=None):
        """
        Initialize the mutator.

        Args:
            tree: The AST tree of the code.
            n: The maximum number of mutations to apply. If None or float('inf'), mutate all possible statements.
        """
        self.tree = tree
        self.n = float('inf') if n is None else n
        self.mutated_codes = []

    class SingleASRMutator(ast.NodeTransformer):
        """
        A class to perform single Arithmetic Statement Replacement (ASR) mutation.
        """

        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_Assign(self, node):
            """
            Replace the target arithmetic statement with a constant or a variable.
            """
            self.current_index += 1
            if self.current_index == self.target_index:
                if isinstance(node.value, ast.BinOp):  # Ensure it's an arithmetic statement
                    # Replace with either a constant or a variable (randomly chosen)
                    replacement = random.choice([
                        ast.Constant(value=random.randint(0, 100)),  # Replace with a constant
                        ast.Name(id="replacement_var", ctx=ast.Load())  # Replace with a variable
                    ])
                    node.value = replacement
            return self.generic_visit(node)

    def find_arithmetic_statements(self):
        """
        Identify all arithmetic assignments in the AST.
        """
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.statements = []

            def visit_Assign(self, node):
                if isinstance(node.value, ast.BinOp):  # Look for arithmetic assignments
                    self.statements.append(('arithmetic_assign', node.lineno))
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.statements

    def generate_mutated_codes(self):
        """
        Generate mutated versions of the code.
        """
        self.mutated_codes = []
        statements = self.find_arithmetic_statements()

        random_indices = list(range(len(statements)))
        random.shuffle(random_indices)

        n = min(self.n, len(statements))  # Limit n to the total number of operators
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target arithmetic statement
            mutator = self.SingleASRMutator(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes
class ASRMutator:
    """
    A class to perform Arithmetic Statement Replacement (ASR) mutation on a given AST.
    """

    def __init__(self, tree, n=None):
        """
        Initialize the mutator.

        Args:
            tree: The AST tree of the code.
            n: The maximum number of mutations to apply. If None or float('inf'), mutate all possible statements.
        """
        self.tree = tree
        self.n = float('inf') if n is None else n
        self.mutated_codes = []

    class SingleASRMutator(ast.NodeTransformer):
        """
        A class to perform single Arithmetic Statement Replacement (ASR) mutation.
        """

        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_Assign(self, node):
            """
            Replace the target arithmetic statement with a constant or a variable.
            """
            self.current_index += 1
            if self.current_index == self.target_index:
                if isinstance(node.value, ast.BinOp):  # Ensure it's an arithmetic statement
                    # Replace with either a constant or a variable (randomly chosen)
                    replacement = random.choice([
                        ast.Constant(value=random.randint(0, 100)),  # Replace with a constant
                        ast.Name(id="replacement_var", ctx=ast.Load())  # Replace with a variable
                    ])
                    node.value = replacement
            return self.generic_visit(node)

    def find_arithmetic_statements(self):
        """
        Identify all arithmetic assignments in the AST.
        """
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.statements = []

            def visit_Assign(self, node):
                if isinstance(node.value, ast.BinOp):  # Look for arithmetic assignments
                    self.statements.append(('arithmetic_assign', node.lineno))
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.statements

    def generate_mutated_codes(self):
        """
        Generate mutated versions of the code.
        """
        self.mutated_codes = []
        statements = self.find_arithmetic_statements()

        random_indices = list(range(len(statements)))
        random.shuffle(random_indices)

        n = min(self.n, len(statements))  # Limit n to the total number of operators
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target arithmetic statement
            mutator = self.SingleASRMutator(target_index=i)
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


def test_ASR():
    code = """
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

    # Example 1: Limit to 2 mutations
    # mutator = ASRMutator(tree, n=2)
    # mutated_codes = mutator.generate_mutated_codes()
    # print_codes(code, mutated_codes)

    # Example 2: Mutate all operators
    mutator = ASRMutator(tree, n=None)  # Or n=float('inf')
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_ASR()
