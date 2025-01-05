import ast
import astor
import subprocess
import random
from copy import deepcopy
from mutpy.operators import MutationOperator


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
        n = min(self.n, len(statements))

        random_indices = list(range(len(statements)))
        random.shuffle(random_indices)

        # Generate mutated versions
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
        n = min(self.n, len(operators))
        print(n)

        random_indices = list(range(len(operators)))
        random.shuffle(random_indices)

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

        n = min(self.n, len(operators))

        random_indices = list(range(len(operators)))
        random.shuffle(random_indices)  

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

        n = min(self.n, len(constants))  

        random_indices = list(range(len(constants)))
        random.shuffle(random_indices)  

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
            mutated_tree = deepcopy(self.tree)  # Deep copy the original tree

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
    A class to perform transformation by removing all `try` blocks
    and their associated `except`, `else`, and `finally` sections.
    """
    def __init__(self, tree, n):
        self.tree = tree
        self.n = n
        self.mutated_codes = []

    class SingleTryRemover(ast.NodeTransformer):
        """
        A class to remove a single `try` block, leaving only its body.
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
                return node.body  # Replace the `try` block with its body
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
        self.mutated_codes = []  # Clear previous results
        try_blocks = self.find_try_blocks()

        n = min(self.n, len(try_blocks))  # Limit `n` to the number of try blocks

        indices = list(range(len(try_blocks)))
        random.shuffle(indices)  # Shuffle indices for randomness

        # Generate mutated versions
        for i in indices[:n]:
            mutated_tree = deepcopy(self.tree)  # Deep copy the original tree

            # Remove the target `try` block
            remover = self.SingleTryRemover(target_index=i)
            remover.visit(mutated_tree)

            # Fix the tree and convert back to code
            ast.fix_missing_locations(mutated_tree)
            mutated_code = astor.to_source(mutated_tree)
            self.mutated_codes.append(mutated_code)

        return self.mutated_codes
    

class MutationOperator(ast.NodeTransformer):
    def __init__(self, operator_type):
        self.operator_type = operator_type
        self.mutation_points = []

    def visit_BinOp(self, node):
        """
        Visit binary operation nodes in the AST and perform mutations
        based on the selected operator type (AOR).
        """
        if self.operator_type == "AOR":
            original_operator = type(node.op).__name__  # Get the original operator's type name
            if isinstance(node.op, ast.Add):
                self.mutation_points.append(
                    ("AOR", original_operator, node.lineno, node.col_offset)
                )
                print(f"Mutating + to - at line {node.lineno}, column {node.col_offset}")
                node.op = ast.Sub()  # Replace + with -
            elif isinstance(node.op, ast.Sub):
                self.mutation_points.append(
                    ("AOR", original_operator, node.lineno, node.col_offset)
                )
                print(f"Mutating - to + at line {node.lineno}, column {node.col_offset}")
                node.op = ast.Add()  # Replace - with +
            elif isinstance(node.op, ast.Mult):
                self.mutation_points.append(
                    ("AOR", original_operator, node.lineno, node.col_offset)
                )
                print(f"Mutating * to / at line {node.lineno}, column {node.col_offset}")
                node.op = ast.Div()  # Replace * with /
            elif isinstance(node.op, ast.Div):
                self.mutation_points.append(
                    ("AOR", original_operator, node.lineno, node.col_offset)
                )
                print(f"Mutating / to * at line {node.lineno}, column {node.col_offset}")
                node.op = ast.Mult()  # Replace / with *

        # Recursively visit all children of the current node
        return self.generic_visit(node)

    def visit_Assign(self, node):
        if self.operator_type == "ASR" and isinstance(node.value, ast.BinOp):
            self.mutation_points.append(("ASR", node))
            node.value = ast.Num(n=42)  # Replace assignment with a constant
        return self.generic_visit(node)

class MutationFramework:
    def __init__(self, source_file, test_file):
        self.source_file = source_file
        self.test_file = test_file

    def apply_mutation(self, operator):
        # Read the source code
        with open(self.source_file, 'r') as f:
            source_code = f.read()

        # Parse the source code into an AST
        tree = ast.parse(source_code)

        # Apply the selected mutation operator
        mutator = MutationOperator(operator)
        mutated_tree = mutator.visit(tree)

        # Write the mutated code to the source file
        mutated_code = astor.to_source(mutated_tree)
        with open(self.source_file, 'w') as f:
            f.write(mutated_code)

        # Return mutation points
        return mutator.mutation_points

    def run_tests(self):
        # Use pytest to run tests and capture the output
        result = subprocess.run(['pytest', self.test_file, '--disable-warnings'], capture_output=True, text=True)
        return result.returncode == 0, result.stdout

    def revert_code(self, original_code):
        # Revert the source file to its original code
        with open(self.source_file, 'w') as f:
            f.write(original_code)

    def execute(self):
        # Ask the user to select a mutation operator
        operator = input("Select mutation operator (AOR/ASR): ").strip()

        # Read and backup the original source code
        with open(self.source_file, 'r') as f:
            original_code = f.read()

        # Apply mutation
        mutation_points = self.apply_mutation(operator)
        print(f"Mutation points for {operator}: {mutation_points}")

        # Run tests
        success, test_output = self.run_tests()

        # Check mutation results
        if success:
            print(f"Mutation survived!\n{test_output}")
        else:
            print(f"Mutation killed!\n{test_output}")

        # Revert code to its original state
        self.revert_code(original_code)

        # Calculate and display mutation score
        killed = int(not success)
        total = len(mutation_points)
        score = (killed / total) * 100 if total else 0
        print(f"Mutation Score: {score:.2f}%")


if __name__ == "__main__":
    framework = MutationFramework(source_file="../project_module/order_management_system.py", test_file='../tests_module/tests.py')
    framework.execute()
