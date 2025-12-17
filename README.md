# Elsevier LaTeX Article – Double blind and DOCX generation

This repository contains the source files and auxiliary scripts used to produce an Elsevier-format journal article using LaTeX, BibTeX, and automated build tools. The project is designed to be cleanly versioned with Git, tracking only the scientifically relevant inputs and final outputs. See more at [Monolito Nimbus - Artigo duplo cego com LaTeX](https://www.monolitonimbus.com.br/artigo-duplo-cego-com-latex) (in portuguese).

## Project Structure

### Core LaTeX files

- **`elsarticle-double-blind.tex`**  
  Main LaTeX source file of the manuscript, written using the `elsarticle` class and configured for double-blind review: Title page (author's info and optional acknowledgements), Highlights, Manuscript (abstract, keywords, text with examples and numbered lines, acknowledgements commented). All things in the same file.

- **`titlepage.tex`**  
  LaTeX source file of the Title page (author's info and optional acknowledgements).

- **`highlights.tex`**  
  LaTeX source file of the Highlights.

- **`manuscript.tex`**  
  Main LaTeX source file of the Manuscript (abstract, keywords, text with examples and numbered lines, acknowledgements commented).

- **`elsarticle.cls`**  
  Official Elsevier LaTeX document class, responsible for layout, formatting, and structural rules of the article.

- **`elsarticle-num-names.bst`**  
  BibTeX bibliography style file defining a numeric citation scheme with full author names in the reference list.

- **`cas-refs.bib`**  
  BibTeX database containing all bibliographic entries cited in the manuscript.

### Citation and conversion styles

- **`renewable-energy.csl`**  
  CSL (Citation Style Language) file corresponding to the *Renewable Energy* journal, used in Pandoc-based workflows - its style relies entirely on the independent "elsevier-with-titles" style.

- **`elsevier-with-titles.csl`**  
  Independente/Complete CSL file that formats references including article titles, useful for document conversions or alternative outputs.

Both were obtained from [CSL Github](https://github.com/citation-style-language/styles) via [Zootero](https://www.zotero.org/styles).

### Figures and diagrams

- **`figs/flowchart`**  
  Workflow diagram.

- **`figs/flowchart.png`**  
  Rendered flowchart illustrating the LaTeX → BibTeX → PDF build process.

### Scripts and utilities

- **`flowchart.py`**  
  Python script (Graphviz-based) used to generate the compilation workflow diagram programmatically.

- **`texcount.pl`**  
  Perl script to perform a word count in the body text and in different parts of the .tex document - this is part of the package `texlive-extra-utils` and can be downloaded directly from [The Comprehensive TeX Archive Network (CTAN)](https://mirrors.ctan.org/support/texcount/texcount.pl). Change te executable script using `chmod +x texcount.pl` and execute using `./texcount.pl elsarticle-double-blind.tex`.

- **`tex2doc.sh`**  
  Shell script to automate conversions from LaTeX to other document formats (e.g., via Pandoc).

### Output files

- **`*.pdf`**  
  Compiled PDFs of the TEX files - just for view, they can be regenerated from the source.

- **`*.docx`**  
  Generated DOCXs from the TEX files - just for view, they can be regenerated from the source.

## Version Control Policy

- **`.gitignore`**  
  The `.gitignore` file is configured to exclude all auxiliary files generated during LaTeX compilation (e.g., `.aux`, `.log`, `.bbl`, `.blg`, `.fdb_latexmk`) as well as temporary files produced by Pandoc and editors. This ensures the repository remains clean, reproducible, and focused on source files rather than build artifacts.

## Build Instructions

To compile the manuscript locally:

```bash
latexmk -pdf titlepage.tex
latexmk -pdf highlights.tex
latexmk -pdf manuscript.tex
bash tex2doc.sh