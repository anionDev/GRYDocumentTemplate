import argparse
import sys
import datetime
import os
from distutils.dir_util import copy_tree
from ScriptCollection.core import write_message_to_stderr, string_is_none_or_whitespace, read_lines_from_file, execute_and_raise_exception_if_exit_code_is_not_zero, write_exception_to_stderr, ensure_directory_exists, resolve_relative_path, git_commit, resolve_relative_path_from_current_working_directory, read_text_from_file, write_text_to_file

parser = argparse.ArgumentParser(description="Creates a new repository for a document")
parser.add_argument('-t', '--template', required=True)
parser.add_argument('-f', '--folder', required=True)
parser.add_argument('-a', '--author', required=True)
parser.add_argument('-n', '--name', required=True)
args = parser.parse_args()

def replace_underscores_in_text(text: str, replacements: dict):
    changed = True
    while changed:
        changed = False
        for key, value in replacements.items():
            previousValue = text
            text = text.replace(f"__{key}__", value)
            if(not text == previousValue):
                changed = True
    return text

def replace_underscores_in_file(file: str, replacements: dict, encoding:str="utf-8"):
    text=read_text_from_file(file,encoding)
    text=replace_underscores_in_text(text,replacements)
    write_text_to_file(file,text,encoding)

def process(arguments):
    try:
        folder=os.path.join(resolve_relative_path_from_current_working_directory(arguments.folder),arguments.name.replace(" ","-"))
        folder_of_current_file = os.path.dirname(os.path.realpath(__file__))
        folder_of_current_repository=resolve_relative_path(f"..",folder_of_current_file)
        folder_of_common_files=resolve_relative_path(f"CommonFiles",folder_of_current_repository)
        folder_of_concrete_template=resolve_relative_path(f"Templates{os.path.sep}{arguments.template}",folder_of_current_repository)
        if(os.path.isdir(folder)):
            write_message_to_stderr(f"The directory '{folder}' already exists")
            return 2
        else:
            ensure_directory_exists(folder)
            
            execute_and_raise_exception_if_exit_code_is_not_zero("git","init", folder)
            copy_tree(folder_of_common_files, folder)
            document_folder=os.path.join(folder, "Document")
            
            execute_and_raise_exception_if_exit_code_is_not_zero("git",f'submodule add -b development "{folder_of_current_repository}" Document{os.path.sep}GRYDocumentTemplate', folder)
            copy_tree(os.path.join(folder_of_concrete_template, "TemplateFiles", "Copy"), document_folder)            
            
            replacements=dict()
            replacements["author"]=arguments.author
            replacements["name"]=arguments.name
            replacements["documenttype"]=arguments.template
            replacements["day"]='{:02d}'.format(datetime.date.today().day)
            replacements["month"]='{:02d}'.format(datetime.date.today().month)
            replacements["year"]=str(datetime.date.today().year)
            
            replace_underscores_in_file(os.path.join(folder, "License.txt"),replacements)
            replace_underscores_in_file(os.path.join(folder, "ReadMe.md"),replacements)
            for line in read_lines_from_file(os.path.join(folder_of_concrete_template,"FilesWithReplacements.txt")):
                if not string_is_none_or_whitespace(line):
                    replace_underscores_in_file(os.path.join(document_folder, line),replacements)
            
            execute_and_raise_exception_if_exit_code_is_not_zero("arara","document.tex", document_folder)            
            git_commit(folder, "Initial commit")
        
    except Exception as exception:
        write_exception_to_stderr(exception)
        return 1
    return 0

sys.exit(process(args))