import ast
import astor
import random
from copy import deepcopy


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
            try:
                mutated_code = astor.to_source(mutated_tree)
                self.mutated_codes.append(mutated_code)
            except:
                pass

        return self.mutated_codes
    

def print_codes(code, mutated_codes):
    print("Original Code:")
    print(code)

    for i, mutated_code in enumerate(mutated_codes):
        print(f"\nMutated Code {i + 1}:")
        print(mutated_code)
    print(64*'-')


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


if __name__ == "__main__":
    test_DDL()
