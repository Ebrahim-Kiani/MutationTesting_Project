import ast
import astor
import random
from copy import deepcopy
import subprocess
from mutpy.operators import MutationOperator
import Mutators

class MutationFramework:
    def __init__(self, source_file, test_file, mutators):
        self.source_file = source_file
        self.test_file = test_file
        self.mutators = mutators

    def run_tests(self):
        # Use pytest to run tests and capture the output
        result = subprocess.run(['pytest', self.test_file, '--disable-warnings'], capture_output=True, text=True)
        return result.returncode == 0, result.stdout

    def revert_code(self, original_code):
        # Revert the source file to its original code
        with open(self.source_file, 'w') as f:
            f.write(original_code)

    def execute(self):
        # Read the original code
        with open(self.source_file, 'r') as f:
            original_code = f.read()
        
        # Parse the code into an AST
        tree = ast.parse(original_code)

        # S n
        n = 1000
        kill = 0
        totol = 0

        for mutator in self.mutators:
            if mutator == 'AOD':
                mutator_class = Mutators.AODMutator(tree, n)
            elif mutator == 'AOR': 
                mutator_class = Mutators.AORMutator(tree, n)
            elif mutator == 'ASR':
                mutator_class = Mutators.ASRMutator(tree, n)
            elif mutator == 'BCR':
                mutator_class = Mutators.BCRMutator(tree, n)
            elif mutator == 'CDI':
                mutator_class = Mutators.CDIMutator(tree, n)
            elif mutator == 'COD':
                mutator_class = Mutators.CODMutator(tree, n)
            elif mutator == 'COI':
                mutator_class = Mutators.COIMutator(tree, n)
            elif mutator == 'CRP':
                mutator_class = Mutators.CRPMutator(tree, n)
            elif mutator == 'DDL':
                mutator_class = Mutators.DDLMutator(tree, n)
            elif mutator == 'EHD':
                mutator_class = Mutators.EHDMutator(tree, n)
            elif mutator == 'EXS':
                mutator_class = Mutators.EXSMutator(tree, n)
            elif mutator == 'IHD':
                mutator_class = Mutators.IHDMutator(tree, n)
            elif mutator == 'IOD':
                mutator_class = Mutators.IODMutator(tree, n)
            elif mutator == 'IOP':
                mutator_class = Mutators.IOPMutator(tree, n)
            elif mutator == 'LOD':
                mutator_class = Mutators.LODMutator(tree, n)
            elif mutator == 'LOI':
                mutator_class = Mutators.LOIMutator(tree, n)
            elif mutator == 'LOR':
                mutator_class = Mutators.LORMutator(tree, n)
            elif mutator == 'ROR':
                mutator_class = Mutators.RORMutator(tree, n)
            elif mutator == 'SCD':
                mutator_class = Mutators.SCDMutator(tree, n)
            elif mutator == 'SCI':
                mutator_class = Mutators.SCIMutator(tree, n)
            elif mutator == 'SDI':
                mutator_class = Mutators.SDIMutator(tree, n)
            elif mutator == 'SIR':
                mutator_class = Mutators.SIRMutator(tree, n)
            
            mutated_codes = mutator_class.generate_mutated_codes()

            totol += len(mutated_codes)
            for code in mutated_codes:
                # Write the mutated code to the source file
                with open(self.source_file, 'w') as f:
                    f.write(code)
                
                # Run the tests
                success, output = self.run_tests()
                if success:
                    print("Mutant survived!")
                else:
                    print("Mutant killed!")
                    print(output)
                    kill += 1
                
        # Calculate Mutation Score
        if totol == 0:
            print("Mutation Score: 0")
        else:
            print(f"Mutation Score: {kill/totol}")

        # Revert the code
        self.revert_code(original_code)


if __name__ == "__main__":
    framework = MutationFramework(source_file="../project_module/order_management_system.py", test_file='../tests_module/tests.py', None)
    framework.execute()
