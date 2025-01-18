import ast
import random
from copy import deepcopy

import astor


class RORMutator:
    def __init__(self, tree, n):
        self.tree = tree
        self. n = n
        self.mutated_codes = []

    class ROR(ast.NodeTransformer):
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1
            self.operators = {
                ast.Eq: [ast.NotEq(), ast.Lt(), ast.LtE(), ast.Gt(), ast.GtE()],
                ast.NotEq: [ast.Eq(), ast.Lt(), ast.LtE(), ast.Gt(), ast.GtE()],
                ast.Lt: [ast.Eq(), ast.NotEq(), ast.Gt(), ast.GtE()],
                ast.LtE: [ast.Eq(), ast.NotEq(), ast.Gt(), ast.GtE()],
                ast.Gt: [ast.Eq(), ast.NotEq(), ast.Lt, ast.LtE()],
                ast.GtE: [ast.Eq(), ast.NotEq(), ast.Lt(), ast.LtE()]
            }

        def visit_Compare(self, node):
            if len(node.ops) != 1:
                return node

            op = node.ops[0]
            op_type = type(op)

            if isinstance(op, ast.LtE) or \
                    isinstance(op, ast.Lt) or \
                    isinstance(op, ast.GtE) or \
                    isinstance(op, ast.Gt) or \
                    isinstance(op, ast.Eq) or \
                    isinstance(op, ast.NotEq):

                self.current_index += 1
                if self.current_index == self.target_index:
                    replacements = self.operators[op_type]
                    random_replacement = random.choice(replacements)
                    node.ops = [random_replacement]

            return node

    def find_relation_operator(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.operators = []

            def visit_Compare(self, node):
                if len(node.ops) != 1:
                    return node

                op = node.ops[0]

                if isinstance(op, ast.LtE) or \
                        isinstance(op, ast.Lt) or \
                        isinstance(op, ast.GtE) or \
                        isinstance(op, ast.Gt) or \
                        isinstance(op, ast.Eq) or \
                        isinstance(op, ast.NotEq):

                    self.operators.append((
                        type(op).__name__,
                        node.lineno
                    ))

                return node

        finder = Finder()
        finder.visit(self.tree)
        return finder.operators

    def generate_mutated_codes(self):
        self.mutated_codes = []
        operators = self.find_relation_operator()

        # Generate mutated codes
        for i in range(len(operators)):
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target statement
            mutator = self.ROR(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes
