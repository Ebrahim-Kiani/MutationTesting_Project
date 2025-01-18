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
        self.n = float('inf') if n is None else n
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


def print_ast_tree(node, level=0):
    """Recursively prints the AST in a tree-like format."""
    indent = "    " * level  # Indentation based on the level of the tree
    node_type = type(node).__name__  # Get the type of the node

    # Print the current node type
    print(f"{indent}{node_type}:")

    # Check if the node has any fields to print (i.e., attributes or children)
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):  # If it's a list of nodes, print each element
            for item in value:
                if isinstance(item, ast.AST):  # If the item is an AST node, recursively print it
                    print_ast_tree(item, level + 1)
                else:
                    print(f"{indent}    {field} = {item}")  # Print simple values (constants)
        elif isinstance(value, ast.AST):  # If the value is an AST node, recursively print it
            print_ast_tree(value, level + 1)
        else:
            print(f"{indent}    {field} = {value}")  # Print simple values




def test_AOD():
    # Example usage of AOD Mutator
    code = """
# Module: orders.py
x = 10
y = 5
z = x + y
u = x / y
    
    
    """

    tree = ast.parse(code)

    # Print the AST tree
    #print(ast.dump(tree, indent=10))
    # Print the AST in a tree-like structure
    #print_ast_tree(tree)

    mutator = AODMutator(tree, n=None)  # Or n=float('inf')
    mutated_codes = mutator.generate_mutated_codes()

    print_codes(code, mutated_codes)
    # Add nodes starting from the root (the module)


if __name__ == "__main__":
    test_AOD()
