import argparse
import sys
import os
from ScriptCollection.core import write_message_to_stderr, execute_and_raise_exception_if_exit_code_is_not_zero, write_exception_to_stderr

parser = argparse.ArgumentParser(description="Creates a new repository with an example-thesis")
parser.add_argument("folder")
parser.add_argument('-a', '--author')
parser.add_argument('-t', '--title')
parser.add_argument('-d', '--date')
parser.add_argument('-y', '--documenttype')
args = parser.parse_args()

def process(arguments):
    try:
        if(os.path.isdir(arguments.folder)):
            write_message_to_stderr(f"The directory '{arguments.folder}' already exists")
            return 1
        else:
            os.makedirs(arguments.folder)
        execute_and_raise_exception_if_exit_code_is_not_zero("git","init", arguments.folder)
        
        # TODO
        
    except Exception as exception:
        write_exception_to_stderr(exception)
        return 1
    return 0

sys.exit(process(args))