import ast
from copy import deepcopy
import astor


class EXSMutator:
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class EXS(ast.NodeTransformer):
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit(self, node):
            if isinstance(node, ast.ExceptHandler):
                self.current_index += 1
                if self.current_index == self.target_index:
                    if node.body:
                        node.body = [ast.Pass()]

            elif isinstance(node, ast.Raise):
                self.current_index += 1
                if self.current_index == self.target_index:
                    node = ast.Pass()

            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)

    def find_exception(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.exception = []
                self.current_class = None

            def visit(self, node):
                if isinstance(node, ast.ExceptHandler):
                    if node.body:
                        self.exception.append(
                            (node.name, node.lineno)
                        )
                elif isinstance(node, ast.Raise):
                    self.exception.append(
                        ("Raise", node.lineno)
                    )

                method = 'visit_' + node.__class__.__name__
                visitor = getattr(self, method, self.generic_visit)
                return visitor(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.exception

    def generate_mutated_codes(self):
        self.mutated_codes = []
        exceptions = self.find_exception()

        # Generate mutated codes
        for i in range(len(exceptions)):
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target statement
            mutator = self.EXS(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes
