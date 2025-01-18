import ast
from copy import deepcopy
import astor


class LORMutator:
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class LOR(ast.NodeTransformer):
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_BinOp(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                if isinstance(node.op, ast.BitAnd):
                    node.op = ast.BitOr()  # Replace & with |
                elif isinstance(node.op, ast.BitOr):
                    node.op = ast.BitAnd()  # Replace | with &

            # Recursively visit all children of the current node
            return self.generic_visit(node)

    def find_operators(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.operators = []

            def visit_BinOp(self, node):
                if isinstance(node.op, ast.BitAnd) or isinstance(node.op, ast.BitOr) \
                        or isinstance(node.op, ast.BitXor):
                    self.operators.append((node.op, node.lineno))
                return self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.operators

    def generate_mutated_codes(self):
        self.mutated_codes = []
        operators = self.find_operators()

        # Generate mutated codes
        for i in range(len(operators)):
            try:
                # Deep copy the original tree
                mutated_tree = deepcopy(self.tree)

                # Mutate the target statement
                mutator = self.LOR(target_index=i)
                mutator.visit(mutated_tree)

                # Fix the tree and convert back to code
                ast.fix_missing_locations(mutated_tree)
                mutated_code = astor.to_source(mutated_tree)
                self.mutated_codes.append(mutated_code)
            except:
                pass

        return self.mutated_codes
