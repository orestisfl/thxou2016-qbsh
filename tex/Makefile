MAINDOC = thxou
LTXARGS = -pdf -xelatex -use-make --shell-escape -silent

.PHONY: $(MAINDOC).pdf all clean embed

all: $(MAINDOC).pdf

$(MAINDOC).pdf: $(MAINDOC).tex
	latexmk $(LTXARGS) $(MAINDOC).tex
	latexmk $(LTXARGS) $(MAINDOC).tex
	latexmk $(LTXARGS) $(MAINDOC).tex


embed: $(MAINDOC).pdf
	gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite -sOutputFile=$(MAINDOC)-embed.pdf $(MAINDOC).pdf

clean:
	latexmk -CA
	rm -rf *_minted* *.aux *.log *.out *.bbl
