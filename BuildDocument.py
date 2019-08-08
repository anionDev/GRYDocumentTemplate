import subprocess
pdfLatexArgument="\"\input{document.tex}\" -synctex=1 -interaction=nonstopmode -job-name letter -halt-on-error -output-directory .."
subprocess.call("pdflatex " + pdfLatexArgument)
