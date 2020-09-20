import argparse
import sys
import os
from distutils.dir_util import copy_tree
from ScriptCollection.core import write_message_to_stderr, execute_and_raise_exception_if_exit_code_is_not_zero, write_exception_to_stderr, ensure_directory_exists, resolve_relative_path, git_commit, resolve_relative_path_from_current_working_directory

parser = argparse.ArgumentParser(description="Creates a new repository for a thesis")
parser.add_argument("folder")
parser.add_argument('-a', '--author')
parser.add_argument('-t', '--title')
parser.add_argument('-d', '--date')
parser.add_argument('-y', '--documenttype')
args = parser.parse_args()

def process(arguments):
    try:
        folder=resolve_relative_path_from_current_working_directory(arguments.folder)
        folder_of_current_file = os.path.dirname(os.path.realpath(__file__))
        folder_of_current_repository=resolve_relative_path(f"..{os.path.sep}..",folder_of_current_file)
        if(os.path.isdir(folder)):
            write_message_to_stderr(f"The directory '{folder}' already exists")
            return 2
        else:
            ensure_directory_exists(folder)
            execute_and_raise_exception_if_exit_code_is_not_zero("git","init", folder)
            copy_tree(os.path.join(folder_of_current_file, "Template"), folder)
            execute_and_raise_exception_if_exit_code_is_not_zero("git",f'submodule add -b development "{folder_of_current_repository}" Thesis{os.path.sep}GRYThesisTemplate', folder)
            execute_and_raise_exception_if_exit_code_is_not_zero("arara","document.tex", os.path.join(folder, "Thesis"))
            git_commit(folder, "Initial commit")
        
    except Exception as exception:
        write_exception_to_stderr(exception)
        return 1
    return 0

sys.exit(process(args))