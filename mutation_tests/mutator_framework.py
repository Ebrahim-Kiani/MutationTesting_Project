import ast
import subprocess
import astor
from mutpy.operators import MutationOperator


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
