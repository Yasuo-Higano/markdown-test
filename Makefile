.PHONY: all generate clean

all: generate

generate:
	python make-README.py --dir folio-scientia/ --title "Folio Scientia"

clean:
	rm -f folio-scientia/README.md 