import ast
from copy import deepcopy
import astor


def is_super_call(node):
    if isinstance(node, ast.Expr):
        node = node.value

    if not isinstance(node, ast.Call):
        return False

    if not isinstance(node.func, ast.Attribute):
        return False

    if not isinstance(node.func.value, ast.Call):
        return False

    if not isinstance(node.func.value.func, ast.Name):
        return False

    return node.func.value.func.id == 'super'


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

        def visit_FunctionDef(self, node: ast.FunctionDef):
            if not self.current_class:
                return node

            # Find super() calls in the method body
            super_calls = []
            other_statements = []

            for stmt in node.body:
                if is_super_call(stmt):
                    super_calls.append(stmt)
                else:
                    other_statements.append(stmt)

            # If super calls found, move them to end
            if super_calls:
                self.current_index += 1
                if self.current_index == self.target_index:
                    # Reconstruct method body with super calls at end
                    node.body = other_statements + super_calls

            return node

    def find_super_calls(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.super_calls = []
                self.current_class = None

            def visit_ClassDef(self, node):
                self.current_class = node
                node = self.generic_visit(node)
                self.current_class = None

                return node

            def visit_FunctionDef(self, node: ast.FunctionDef):
                if not self.current_class:
                    return node

                for stmt in node.body:
                    if is_super_call(stmt):
                        self.super_calls.append((self.current_class.name,node.lineno))

                return node

        finder = Finder()
        finder.visit(self.tree)
        return finder.super_calls

    def generate_mutated_codes(self):
        self.mutated_codes = []
        calls = self.find_super_calls()

        # Generate mutated codes
        for i in range(len(calls)):
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target statement
            mutator = self.IOP(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes
