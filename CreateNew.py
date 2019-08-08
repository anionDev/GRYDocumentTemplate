import argparse
import os
import sys
import shutil
parser = argparse.ArgumentParser(description='Creates a new formal letter.')

parser.add_argument('--folder_for_new_document', help='Specifies the folder where the new document should be stored')
parser.add_argument('--document_name', help='Specifies the name of the new document')

args = parser.parse_args()

def execute(command:str, argument:str):
    print(subprocess.getoutput(command+" "+argument))

new_document_folder=os.path.combine(args.folder_for_new_document,args.document_name)
if(os.path.isdir(new_document_folder)):
    println(new_document_folder + " does already exist")
    sys.exit(1)
os.makedir(new_document_folder)
os.chdir(new_document_folder)
execute("git", "init")
execute("git", "submodule add https://github.com/anionDev/formalLetter.git template")
content_file="documentcontent.tex"
content_file_content="TODO"
with open(content_file,'w') as f:
    f.write(content_file_content)
with open("License.txt",'w') as f:
    f.write("Only the author of the content of '"+content_file+"' is allowed to use the content of this repository.")
os.chdir("template")
execute("Build.py")
os.chdir("..")
execute("git", 'commit -m "Initial commit"')

