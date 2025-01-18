import ast
from copy import deepcopy
import astor


class IHDMutator:
    def __init__(self, tree):
        self.tree = tree
        self.mutated_codes = []
        self.class_variables = {}
        self._collect_init_variables()

    def _collect_init_variables(self):
        class InitVariableCollector(ast.NodeVisitor):
            def __init__(self):
                self.current_class = None
                self.in_init = False
                self.class_variables = {}

            def visit_ClassDef(self, node):
                previous_class = self.current_class
                self.current_class = node.name
                if self.current_class not in self.class_variables:
                    self.class_variables[self.current_class] = set()

                # Visit all nodes in the class
                for n in node.body:
                    self.visit(n)

                self.current_class = previous_class

            def visit_FunctionDef(self, node):
                if self.current_class and node.name == '__init__':
                    self.in_init = True
                    # Visit the function body
                    for n in node.body:
                        self.visit(n)
                    self.in_init = False

            def visit_Assign(self, node):
                if self.current_class and self.in_init:
                    for target in node.targets:
                        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                            if target.value.id == 'self':
                                self.class_variables[self.current_class].add(target.attr)

            def visit_AnnAssign(self, node):
                if self.current_class and self.in_init:
                    if isinstance(node.target, ast.Attribute) and isinstance(node.target.value, ast.Name):
                        if node.target.value.id == 'self':
                            self.class_variables[self.current_class].add(node.target.attr)

        collector = InitVariableCollector()
        collector.visit(self.tree)
        self.class_variables = collector.class_variables

    class IHD(ast.NodeTransformer):
        def __init__(self, target_index, class_variables):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1
            self.parent_vars = set()
            self.in_child_init = False
            self.class_variables = class_variables
            self.init_var_removed = False

        def visit_ClassDef(self, node):
            if node.bases:
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        parent_class = base.id
                        if parent_class in self.class_variables:
                            self.parent_vars = set()
                            self.parent_vars.update(self.class_variables[parent_class])

                node.body = [self.visit(n) for n in node.body]
            return node

        def visit_FunctionDef(self, node):
            if node.name == '__init__' and self.parent_vars:
                self.in_child_init = True
                self.init_var_removed = False
                node.body = [self.visit(n) for n in node.body]

                # If we removed something and the body is empty, add 'pass'
                if self.init_var_removed and not node.body:
                    node.body = [ast.Pass()]

                self.in_child_init = False
            return node

        def visit_Assign(self, node):
            if self.in_child_init:
                for target in node.targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                        if target.value.id == 'self':
                            var_name = target.attr
                            if var_name in self.parent_vars:
                                self.current_index += 1
                                if self.current_index == self.target_index:
                                    self.init_var_removed = True
                                    return None
            return node

        def visit_AnnAssign(self, node):
            if self.in_child_init:
                if isinstance(node.target, ast.Attribute) and isinstance(node.target.value, ast.Name):
                    if node.target.value.id == 'self':
                        var_name = node.target.attr
                        if var_name in self.parent_vars:
                            self.current_index += 1
                            if self.current_index == self.target_index:
                                self.init_var_removed = True
                                return None
            return node

    def find_hiding_variables(self):
        class Finder(ast.NodeVisitor):
            def __init__(self, class_variables):
                self.hiding_vars = []
                self.parent_vars = set()
                self.in_init = False
                self.class_variables = class_variables

            def visit_ClassDef(self, node):
                if node.bases:
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            parent_class = base.id
                            if parent_class in self.class_variables:
                                self.parent_vars = set()
                                self.parent_vars.update(self.class_variables[parent_class])

                    for n in node.body:
                        self.visit(n)

            def visit_FunctionDef(self, node):
                if node.name == '__init__' and self.parent_vars:
                    self.in_init = True
                    for n in node.body:
                        self.visit(n)
                    self.in_init = False

            def visit_Assign(self, node):
                if self.in_init:
                    for target in node.targets:
                        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                            if target.value.id == 'self':
                                var_name = target.attr
                                if var_name in self.parent_vars:
                                    self.hiding_vars.append((var_name, node.lineno))

            def visit_AnnAssign(self, node):
                if self.in_init:
                    if isinstance(node.target, ast.Attribute) and isinstance(node.target.value, ast.Name):
                        if node.target.value.id == 'self':
                            var_name = node.target.attr
                            if var_name in self.parent_vars:
                                self.hiding_vars.append((var_name, node.lineno))

        finder = Finder(self.class_variables)
        finder.visit(self.tree)
        return finder.hiding_vars

    def generate_mutated_codes(self):
        self.mutated_codes = []
        hiding_vars = self.find_hiding_variables()

        for i in range(len(hiding_vars)):
            try:
                # Deep copy the original tree
                mutated_tree = deepcopy(self.tree)

                # Mutate the target statement
                mutator = self.IHD(target_index=i, class_variables=self.class_variables)
                mutator.visit(mutated_tree)

                # Fix the tree and convert back to code
                ast.fix_missing_locations(mutated_tree)
                mutated_code = astor.to_source(mutated_tree)
                self.mutated_codes.append(mutated_code)
            except:
                pass

        return self.mutated_codes
