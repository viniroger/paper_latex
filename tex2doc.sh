pandoc elsarticle-double-blind.tex \
  --bibliography=cas-refs.bib \
  --citeproc \
  --csl=elsevier-with-titles.csl \
  -t docx \
  -f latex \
  -o elsarticle-double-blind.docx
