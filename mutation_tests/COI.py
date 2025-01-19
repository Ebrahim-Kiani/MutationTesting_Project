import ast
import astor
import random
from copy import deepcopy


class COIMutator():
    """
    A class to perform Conditional Operator Insertion (COI) mutation on a given AST.
    """
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleCOIMutator(ast.NodeTransformer):
        """
        A class to perform a single Conditional Operator Insertion (COI) mutation.
        """
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_BoolOp(self, node):
            """
            Visit BoolOp nodes ('and', 'or') and insert additional conditions.
            """
            self.current_index += 1
            if self.current_index == self.target_index:
                # Insert a new condition into the BoolOp
                if isinstance(node.op, ast.And):
                    new_condition = ast.Constant(value=False)  # Insert 'False' for 'and'
                elif isinstance(node.op, ast.Or):
                    new_condition = ast.Constant(value=True)  # Insert 'True' for 'or'
                node.values.append(new_condition)
            return self.generic_visit(node)

        def visit_Compare(self, node):
            """
            Visit Compare nodes and convert them into BoolOps (with an additional condition).
            """
            self.current_index += 1
            if self.current_index == self.target_index:
                # Wrap the comparison into a BoolOp ('x < y and True')
                #new_condition = ast.Constant(value=random.choice([True, False]))
                return random.choice([ast.BoolOp(op=ast.And(), values=[node, ast.Constant(value=False)]), 
                                      ast.BoolOp(op=ast.Or(), values=[node, ast.Constant(value=True)])])
            return self.generic_visit(node)

    def find_conditional_operators(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.operators = []

            def visit_BoolOp(self, node):
                self.operators.append(node)
                self.generic_visit(node)

            def visit_Compare(self, node):
                self.operators.append(node)
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
            mutator = self.SingleCOIMutator(target_index=i)
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


def test_COI():
    # Example usage of COI Mutator
    code = """
def check_value(x):
    if x > 5:
        return True
    elif x < 3 and x > 0:
        return False
    else:
        return x == 4
"""

    tree = ast.parse(code)
    mutator = COIMutator(tree, n=2)
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


if __name__ == "__main__":
    test_COI()
