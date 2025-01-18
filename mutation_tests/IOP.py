import ast
from copy import deepcopy
import astor


def is_super_call(node):
    """Check if a node contains a super() call in any context"""

    def has_super(node):
        # Check for direct super() call
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return node.func.id == 'super'
            # Handle method calls on super()
            if isinstance(node.func, ast.Attribute):
                return has_super(node.func.value)

        # Handle super() in attribute access
        if isinstance(node, ast.Attribute):
            return has_super(node.value)

        return False

    # Handle expression statements
    if isinstance(node, ast.Expr):
        return has_super(node.value)

    # Handle assignments
    if isinstance(node, ast.Assign):
        # Check both targets and value for super()
        for target in node.targets:
            if has_super(target):
                return True
        return has_super(node.value)

    # Direct node check
    return has_super(node)


class IOPMutator:
    def __init__(self, tree):
        self.tree = tree
        self.mutated_codes = []

    class IOP(ast.NodeTransformer):
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1
            self.current_class = None

        def visit_ClassDef(self, node):
            self.current_class = node
            node = self.generic_visit(node)
            self.current_class = None
            return node

        def visit_FunctionDef(self, node):
            if not self.current_class:
                return node

            super_positions = []
            for i, stmt in enumerate(node.body):
                if is_super_call(stmt):
                    super_positions.append(i)

            if not super_positions:
                return node

            new_body = []
            moved_supers = []

            for i, stmt in enumerate(node.body):
                if is_super_call(stmt):
                    self.current_index += 1
                    if self.current_index == self.target_index:
                        moved_supers.append(stmt)
                    else:
                        new_body.append(stmt)
                else:
                    new_body.append(stmt)

            new_body.extend(moved_supers)
            node.body = new_body
            return node

    def find_super_calls(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.super_calls = []
                self.current_class = None

            def visit_ClassDef(self, node):
                self.current_class = node
                self.generic_visit(node)
                self.current_class = None

            def visit_FunctionDef(self, node: ast.FunctionDef):
                if not self.current_class:
                    return

                super_count = 0
                for stmt in node.body:
                    if is_super_call(stmt):
                        super_count += 1

                if super_count > 0:
                    self.super_calls.append((self.current_class.name, node.lineno, super_count))

        finder = Finder()
        finder.visit(self.tree)
        return finder.super_calls

    def generate_mutated_codes(self):
        self.mutated_codes = []
        calls = self.find_super_calls()
        counter = 0

        for class_info in calls:
            super_count = class_info[2]

            for i in range(super_count):
                try:
                    # Move single super call
                    mutated_tree = deepcopy(self.tree)
                    mutator = self.IOP(target_index=counter)
                    mutator.visit(mutated_tree)

                    ast.fix_missing_locations(mutated_tree)
                    mutated_code = astor.to_source(mutated_tree)
                    self.mutated_codes.append(mutated_code)
                except:
                    pass

                counter += 1

        return self.mutated_codes
