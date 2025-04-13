.PHONY: all generate clean

all: generate

generate:
	python main.py --dir folio-scientia/

clean:
	rm -f folio-scientia/README.md 