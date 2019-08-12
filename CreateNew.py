import argparse
import os
import sys
import subprocess
import urllib.request
import shutil

parser = argparse.ArgumentParser(description='Creates a new thesis.')

parser.add_argument('folder_for_new_document', help='Specifies the folder where the thesis should be stored')
parser.add_argument('document_name', help='Specifies the name of the thesis')

args = parser.parse_args()
template_repository=os.path.dirname(os.path.abspath(__file__))

template_remote_repository=template_repository# use this path to use this (local) repository as remote for the submodule
#template_remote_repository="https://github.com/anionDev/gryThesis.git"

def execute(command:str, argument:str):
    print(subprocess.getoutput(command+" "+argument))

new_document_folder=os.path.join(args.folder_for_new_document,args.document_name)
if(os.path.isdir(new_document_folder)):
    print(new_document_folder + " does already exist")
    sys.exit(1)
os.makedirs(new_document_folder)
os.chdir(new_document_folder)
execute("git", "init")
execute("git", "submodule add "+template_remote_repository+" template")
content_file_content="\\input{../content/thesis-content}"
with open("License.txt",'w') as f:
    f.write("Only the author of the content of this thesis is allowed to use the content of this repository.")
with open("metadata.tex",'w') as f:
    f.write("\\newcommand{\\thesiscreator}{authorname}\n"+
    "\\newcommand{\\thesisname}{"+args.document_name+"}\n"+
    "\\newcommand{\\customfooter}{Please report any mistakes here: \\url{https://example.com/mythesis}}")
    urllib.request.urlretrieve('https://raw.githubusercontent.com/github/gitignore/master/TeX.gitignore', os.path.join(new_document_folder,".gitignore"))
shutil.copytree(os.path.join(template_repository,"Template"), os.path.join(new_document_folder,"Content"))
os.chdir("template")
execute("Python", "BuildDocument.py")
os.chdir("..")
execute("git", "add -A")
execute("git", 'commit -m "Initial commit"')

