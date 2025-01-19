import ast
import astor
import random
from copy import deepcopy


class EHDMutator():
    """
    A class to perform Decorator Deletion (DDL) mutation on a given AST.
    """
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleEHDMutator(ast.NodeTransformer):
        """
        A class to perform a single Decorator Deletion (DDL).
        """
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_Try(self, node):
            """
            Visit Try nodes and replace the target `try` block with its body.
            """
            self.current_index += 1
            if self.current_index == self.target_index:
                return node.body  # Replace the 'try' block with its body
            return self.generic_visit(node)

        def visit_Module(self, node):
            """
            Handle the Module node to flatten lists returned by replaced Try nodes.
            """
            new_body = []
            for stmt in node.body:
                result = self.visit(stmt)
                if isinstance(result, list):
                    new_body.extend(result)
                elif result is not None:
                    new_body.append(result)
            node.body = new_body
            return node

    def find_try_blocks(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.try_blocks = []

            def visit_Try(self, node):
                self.try_blocks.append(node)
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.try_blocks

    def generate_mutated_codes(self):
        self.mutated_codes = []
        try_blocks = self.find_try_blocks()

        indices = list(range(len(try_blocks)))
        random.shuffle(indices)

        n = min(self.n, len(try_blocks))
        # Generate mutated versions
        for i in indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Remove the target 'try' block
            mutator = self.SingleEHDMutator(target_index=i)
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


def test_EHD():
    # Example usage of EHD Mutator
    code = """
try:
    print("Attempting risky operation.")
    result = 10 / 0
except ZeroDivisionError:
    print("Caught division by zero!")
except Exception as e:
    print(f"Other exception: {e}")
else:
    print("No exceptions occurred.")
finally:
    print("Cleanup actions.")

try:
    print("Another block.")
except ValueError:
    print("Caught ValueError.")
"""

    tree = ast.parse(code)
    mutator = EHDMutator(tree, n=2)
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_EHD()
