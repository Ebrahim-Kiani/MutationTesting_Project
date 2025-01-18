import ast
from copy import deepcopy

import astor


def collect_class_methods(node):
    # this code collect all method names defined in a class
    methods = set()
    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            methods.add(item.name)
    return methods


class IODMutator:
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class IOD(ast.NodeTransformer):
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1
            self.current_class = None
            self.classes = {}
            self.parent_methods = set()

        def visit_ClassDef(self, node):
            previous_class = self.current_class
            self.current_class = node

            # collect and store this class's methods
            methods = collect_class_methods(node)
            self.classes[node.name] = methods

            # collect parent methods if bases exist
            self.parent_methods = set()
            for base in node.bases:
                if isinstance(base, ast.Name):
                    parent_name = base.id
                    parent_methods = self.classes.get(parent_name, set())
                    self.parent_methods.update(parent_methods)

            node = self.generic_visit(node)
            self.current_class = previous_class

            return node

        def visit_FunctionDef(self, node: ast.FunctionDef):
            if (self.current_class and
                    not node.name.startswith('_') and
                    node.name in self.parent_methods):
                self.current_index += 1
                if self.current_index == self.target_index:
                    return None

            return node

    def find_override_method(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.methods = []
                self.current_class = None
                self.classes = {}
                self.parent_methods = set()

            def visit_ClassDef(self, node):
                previous_class = self.current_class
                self.current_class = node

                # collect and store this class's methods
                methods = collect_class_methods(node)
                self.classes[node.name] = methods

                # collect parent methods if bases exist
                self.parent_methods = set()
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        parent_name = base.id
                        parent_methods = self.classes.get(parent_name, set())
                        self.parent_methods.update(parent_methods)

                node = self.generic_visit(node)
                self.current_class = previous_class

                return node

            def visit_FunctionDef(self, node: ast.FunctionDef):
                if (self.current_class and
                        not node.name.startswith('_') and
                        node.name in self.parent_methods):
                    self.methods.append(
                        (self.current_class.name, node.lineno)
                    )

                return node

        finder = Finder()
        finder.visit(self.tree)
        return finder.methods

    def generate_mutated_codes(self):
        self.mutated_codes = []
        methods = self.find_override_method()

        # Generate mutated codes
        for i in range(len(methods)):
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target statement
            mutator = self.IOD(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes
