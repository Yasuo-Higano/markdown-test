.PHONY: all generate clean

all: generate

generate:
	python make-README.py --dir folio-scientia/ --title "Folio Scientia(フォリオ・サイエンティア)"
	python make-sitemap.py --dir folio-scientia/ --base-url "https://gitmarkdown.com/Yasuo-Higano/markdown-test/folio-scientia"
	python make-sitemap.py --dir ./ --base-url "https://gitmarkdown.com/Yasuo-Higano/markdown-test"
	python trim-charcode.py --dir folio-scientia/
	python trim-charcode.py --dir ./
	python modify-meta.py --dir folio-scientia/
clean:
	rm -f folio-scientia/README.md 