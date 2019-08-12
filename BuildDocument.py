from argparse import ArgumentParser
import os
import subprocess
parser = ArgumentParser()
parser.add_argument("-pdf", dest="pdflatexfile", help="pdfLatex file with full path", default="pdflatex")
args = parser.parse_args()
pdfLatexArgument="\"\input{Thesis.tex}\" -synctex=1 -interaction=nonstopmode -job-name Thesis -halt-on-error -output-directory .."
subprocess.call(args.pdflatexfile + " " + pdfLatexArgument)
