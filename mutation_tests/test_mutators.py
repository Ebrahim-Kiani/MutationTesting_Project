import ast
import astor
import random
from copy import deepcopy


class BCRMutator():
    """
    A class to perform Break Continue Replacement (BCR) mutation on a given AST.
    """
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleBCRMutator(ast.NodeTransformer):
        """
        A class to perform single Break Continue Replacement (BCR) mutation.
        """
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_Break(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                return ast.Continue()  # Replace 'break' with 'continue'
            return node

        def visit_Continue(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                return ast.Break()  # Replace 'continue' with 'break'
            return node

    def find_break_continue_statements(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.statements = []

            def visit_Break(self, node):
                self.statements.append(('break', node.lineno))
                self.generic_visit(node)

            def visit_Continue(self, node):
                self.statements.append(('continue', node.lineno))
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.statements

    def generate_mutated_codes(self):
        self.mutated_codes = []
        statements = self.find_break_continue_statements()

        random_indices = list(range(len(statements)))
        random.shuffle(random_indices)

        n = min(self.n, len(statements))
        # Generate mutated codes
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target statement
            mutator = self.SingleBCRMutator(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes


class CODMutator():
    """
    A class to perform Conditional Operator Deletion (COD) mutation on a given AST.
    """
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleCODMutator(ast.NodeTransformer):
        """
        A class to perform single Conditional Operator Deletion (COD) mutation.
        """
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_Compare(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                return ast.Constant(value=random.choice([True, False]))  # Replace with a valid constant
            return node

    def find_conditional_operators(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.operators = []

            def visit_Compare(self, node):
                self.operators.append(('compare', node.lineno))
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
            mutator = self.SingleCODMutator(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)
    
        return self.mutated_codes


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
                new_condition = ast.Constant(value=random.choice([True, False])) 
                node.values.append(new_condition)
            return self.generic_visit(node)

        def visit_Compare(self, node):
            """
            Visit Compare nodes and convert them into BoolOps (with an additional condition).
            """
            self.current_index += 1
            if self.current_index == self.target_index:
                # Wrap the comparison into a BoolOp ('x < y and True')
                new_condition = ast.Constant(value=random.choice([True, False]))
                return ast.BoolOp(op=random.choice([ast.And(), ast.Or()]), values=[node, new_condition])
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
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes


class CRPMutator():
    """
    A class to perform Constant Replacement (CRP) mutation on a given AST.
    """
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleCRPMutator(ast.NodeTransformer):
        """
        A class to perform a single Constant Replacement (CRP) mutation.
        """
        def __init__(self, target_index, start, end):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1
            self.start = start
            self.end = end

        def visit_Constant(self, node):
            self.current_index += 1
            if self.current_index == self.target_index:
                # Replace the constant with the new value
                return ast.Constant(value=random.randint(self.start, self.end))
            return node

    def find_constants(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.constants = []

            def visit_Constant(self, node):
                self.constants.append(node)
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.constants

    def generate_mutated_codes(self, start, end):
        self.mutated_codes = []  
        constants = self.find_constants()

        random_indices = list(range(len(constants)))
        random.shuffle(random_indices)  

        n = min(self.n, len(constants))  
        # Generate mutated versions
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)  

            # Mutate the target constant
            mutator = self.SingleCRPMutator(target_index=i, start=start, end=end)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes


class DDLMutator():
    """
    A class to perform Decorator Deletion (DDL) mutation on a given AST.
    """
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleDDLMutator(ast.NodeTransformer):
        """
        A class to perform a single Decorator Deletion Mutation (DDL).
        """
        def __init__(self, target_index):
            super().__init__()
            self.target_index = target_index
            self.current_index = -1

        def visit_FunctionDef(self, node):
            if node.decorator_list:
                self.current_index += 1
                if self.current_index == self.target_index:
                    # Remove one decorator randomly if there are multiple
                    if len(node.decorator_list) > 1:
                        removal_index = random.randint(0, len(node.decorator_list) - 1)
                        del node.decorator_list[removal_index]
                    else:
                        # Remove the only decorator
                        node.decorator_list = []
            return self.generic_visit(node)

        def visit_ClassDef(self, node):
            if node.decorator_list:
                self.current_index += 1
                if self.current_index == self.target_index:
                    # Remove one decorator randomly if there are multiple
                    if len(node.decorator_list) > 1:
                        removal_index = random.randint(0, len(node.decorator_list) - 1)
                        del node.decorator_list[removal_index]
                    else:
                        # Remove the only decorator
                        node.decorator_list = []
            return self.generic_visit(node)

    def find_decorators(self):
        class Finder(ast.NodeVisitor):
            def __init__(self):
                self.decorators = []

            def visit_FunctionDef(self, node):
                if node.decorator_list:
                    self.decorators.append(('function', node.lineno))
                self.generic_visit(node)

            def visit_ClassDef(self, node):
                if node.decorator_list:
                    self.decorators.append(('class', node.lineno))
                self.generic_visit(node)

        finder = Finder()
        finder.visit(self.tree)
        return finder.decorators

    def generate_mutated_codes(self):
        self.mutated_codes = []  
        decorators = self.find_decorators()

        n = min(self.n, len(decorators))  

        random_indices = list(range(len(decorators)))
        random.shuffle(random_indices)

        # Generate mutated versions
        for i in random_indices[:n]:
            # Deep copy the original tree
            mutated_tree = deepcopy(self.tree)

            # Mutate the target decorator
            mutator = self.SingleDDLMutator(target_index=i)
            mutator.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes
    

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
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes


def print_codes(code, mutated_codes):
    print("Original Code:")
    print(code)

    for i, mutated_code in enumerate(mutated_codes):
        print(f"\nMutated Code {i + 1}:")
        print(mutated_code)
    print(64*'-')


def test_BCR():
    # Example usage of BCR Mutator
    code = """
for i in range(10):
    if i == 5:
        break
    if i % 2 == 0:
        continue
        break
        break
    print(i)
"""

    tree = ast.parse(code)
    mutator = BCRMutator(tree, n=2)
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


def test_COD():
    # Example usage of COD Mutator
    code = """
if x == 5:
    print("x is 5")
elif x == 10:
    print("x is 10")
else:
    print("x is neither 5 nor 10")
"""

    tree = ast.parse(code)
    mutator = CODMutator(tree, n=2)
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


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


def test_CRP():
    # Example usage of CRP Mutator
    code = """
def check_value(x):
    x = 12
    y = 13
    if x > 5:
        return True
    elif x < 3 and x > 0:
        return False
    else:
        return x == 4
"""

    tree = ast.parse(code)
    mutator = CRPMutator(tree, n=2)
    mutated_codes = mutator.generate_mutated_codes(1, 100)
    print_codes(code, mutated_codes)


def test_DDL():
    # Example usage of DDL Mutator
    code = """
@decorator_one
@decorator_two
def my_function():
    pass

@decorator_class1
@decorator_class2
class MyClass:
    pass
"""

    tree = ast.parse(code)
    mutator = DDLMutator(tree, n=2)
    mutated_codes = mutator.generate_mutated_codes()
    print_codes(code, mutated_codes)


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
    test_BCR() 
    test_COD()
    test_COI()
    test_CRP()
    test_DDL()
    test_EHD()
