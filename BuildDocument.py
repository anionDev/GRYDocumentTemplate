import subprocess
import os
import time
from pathlib import Path
pdfLatexArgument="\"\input{Template.tex}\" -synctex=1 -interaction=nonstopmode -job-name letter -halt-on-error -output-directory .."
subprocess.call("pdflatex " + pdfLatexArgument)
project_folder_name=os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir("..")
os.rename("letter.pdf",project_folder_name+".pdf")
