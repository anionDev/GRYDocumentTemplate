import subprocess
from pathlib import Path
pdfLatexArgument="\"\input{Template.tex}\" -synctex=1 -interaction=nonstopmode -job-name letter -halt-on-error -output-directory .."
project_folder_name=os.path.basename(os.path.dirname(os.path.abspath(__file__)))
os.rename("../Document.tex","../"+project_folder_name+".pdf")
subprocess.call("pdflatex " + pdfLatexArgument)
