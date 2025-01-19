import os
import ast
import subprocess
import difflib
import Mutators


class MutationFramework:
    def __init__(self, source_file, test_file, mutators):
        self.source_file = source_file
        self.test_file = test_file
        self.mutators = mutators

    def run_tests(self):
        # Use python to run tests and capture the output
        result = subprocess.run(['python', self.test_file], capture_output=True, text=True)
        return result.returncode == 0, result.stderr

    def revert_code(self, original_code):
        # Revert the source file to its original code
        with open(self.source_file, 'w') as f:
            f.write(original_code)

    def execute(self):
        # Clear mutation_log
        with open('mutation_log.txt', 'w') as f:
            f.write('')
        
        # Read the original code
        with open(self.source_file, 'r') as f:
            original_code = f.read()
        
        # Parse the code into an AST
        tree = ast.parse(original_code)

        # Initialize the n & mutation score
        n = 1000
        kill = 0
        total = 0

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

            this_kill = 0
            for code in mutated_codes:
                # Write the mutated code to the source file
                with open(self.source_file, 'w') as f:
                    f.write(code)
                
                # Run the tests
                success, output = self.run_tests()
                if success:
                    # save in mutation_log.txt just diff this code with string original code and type of mutatnt
                    with open('mutation_log.txt', 'a') as f:
                        f.write(f"Mutant Type: {mutator}\n")
                        diff = difflib.unified_diff(
                            code.splitlines(),     # Split file content into lines
                            original_code.splitlines(), # Split string into lines
                            fromfile="mutant_code",
                            tofile="original_code",
                            lineterm=""                     # No line terminator in output
                        )
                        f.write('\n'.join(diff))
                        f.write('\n')
                        f.write(f"Output: {output}\n")
                        f.write('-' * 64)
                        f.write('\n')
                    #print(output)
                else:
                    this_kill += 1
                
            total += len(mutated_codes)
            kill += this_kill

            print(f'{mutator} Mutants: {len(mutated_codes)}, Killed: {this_kill}')

        # Calculate Mutation Score
        if total == 0:
            print("Mutation Score: 0")
        else:
            print(f"Mutation Score: {kill/total}")

        # Revert the code
        self.revert_code(original_code)


if __name__ == "__main__":
    DEFAULT_VAR = True
    source_file = "../test_file/example2.py"
    test_file = "../test_file/test_example2.py"

    while not DEFAULT_VAR:
        source_file = input("Enter source file path: ")
        if not os.path.isfile(source_file):
            print("Source file not found")
        else:
            break

    while not DEFAULT_VAR:
        test_file = input("Enter test file path: ")
        if not os.path.isfile(test_file):
            print("Test file not found")
        else:
            break
    
    if not DEFAULT_VAR:
        selcet_mutators = input("Enter mutators: [AOD, AOR, ASR, BCR, CDI, COD, COI, CRP, DDL, EHD, EXS, IHD, IOD, IOP, LOD, LOI, LOR, ROR, SCD, SCI, SDI, SIR]: ")
        mutators = selcet_mutators.split(',')
    else:
        mutators = ['AOD', 'AOR', 'ASR', 'BCR', 'CDI', 'COD', 'COI', 'CRP', 'DDL', 'EHD', 'EXS', 'IHD', 'IOD', 'IOP', 'LOD', 'LOI', 'LOR', 'ROR', 'SCD', 'SDI']

    framework = MutationFramework(source_file, test_file, mutators)
    framework.execute()
