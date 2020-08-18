import argparse

parser = argparse.ArgumentParser(description="Creates a new repository with an example-thesis")
parser.add_argument(required=True)
parser.add_argument('-a', '--author', required=False)
parser.add_argument('-t', '--title', required=False)
parser.add_argument('-d', '--documenttype', required=False)
args = parser.parse_args()

def execute_program(folder:str,program:str,arguments:str)
    pass


