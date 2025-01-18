import ast
import random
from copy import deepcopy
import astor  # For converting AST back to source code


class SDIMutator:
    """
    A class to perform Static Method Decorator Insertion (SDI) mutation on a given AST.
    """

    def __init__(self, tree, n):
        self.tree = tree
        self.n = float('inf') if n is None else n
        self.mutated_codes = []

    class SingleSDIMutator(ast.NodeTransformer):
        """
        A class to perform single Static Method Decorator Insertion (SDI) mutation.
        """

        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_FunctionDef(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                # Inserting the @staticmethod decorator before the function definition
                node.decorator_list.insert(0, ast.Name(id='staticmethod', ctx=ast.Load()))
            return self.generic_visit(node)

    def find_methods(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.methods = []

            def visit_ClassDef(self, node):
                # When we find a class, we visit its methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        self.methods.append(item)
                self.generic_visit(node)

        # Traverse the AST to find all methods
        finder = Finder()
        finder.visit(self.tree)

        return finder.methods

    def generate_mutated_codes(self):
        self.mutated_codes = []
        methods = self.find_methods()

        random_indices = list(range(len(methods)))
        random.shuffle(random_indices)

        n = min(self.n, len(methods))
        # Generate mutated versions
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target method by inserting @staticmethod
            mutator = self.SingleSDIMutator(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert it back to source code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes


def print_codes(code, mutated_codes):
    """
    Print the original code and the mutated versions.
    """
    print("Original Code:")
    print(code)

    for i, mutated_code in enumerate(mutated_codes):
        print(f"\nMutated Code {i + 1}:")
        print(mutated_code)
    print(64 * '-')


def test_SDI():
    code = """
class MyClass:
    def method1(self):
        print("This is method1")

    def method2(self):
        print("This is method2")

    def method3(self):
        print("This is method3")
    """

    tree = ast.parse(code)

    mutator = SDIMutator(tree, n=None)  # Or n=float('inf')
    mutated_codes = mutator.generate_mutated_codes()

    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_SDI()
