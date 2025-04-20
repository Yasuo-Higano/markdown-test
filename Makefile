.PHONY: all generate clean

all: generate

generate:
	python make-README.py --dir folio-scientia/ --title "Folio Scientia"
	python make-sitemap.py --dir folio-scientia/ --base-url "https://gitmarkdown.com/Yasuo-Higano/markdown-test/folio-scientia"
clean:
	rm -f folio-scientia/README.md 