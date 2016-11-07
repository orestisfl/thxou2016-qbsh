MAINDOC = $(shell basename "$$(pwd)")
LTXARGS = -pdf -xelatex -use-make --shell-escape -silent

.PHONY: $(MAINDOC).pdf all clean

all: $(MAINDOC).pdf

$(MAINDOC).pdf: $(MAINDOC).tex
	latexmk $(LTXARGS) $(MAINDOC).tex

clean:
	latexmk -CA
	rm -rf *_minted* *.aux *.log *.out
