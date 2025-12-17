pandoc titlepage.tex \
  -t docx \
  -f latex \
  -o titlepage.docx
pandoc highlights.tex \
  -t docx \
  -f latex \
  -o highlights.docx
pandoc manuscript.tex \
  --bibliography=cas-refs.bib \
  --filter pandoc-crossref \
  --citeproc \
  --csl=elsevier-with-titles.csl \
  --number-sections \
  -t docx \
  -f latex \
  -o manuscript.docx
