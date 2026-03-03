#!/usr/bin/env python3
"""
Script: latex_flatten_submission.py

Objetivo
--------
Preparar automaticamente um pacote de submissão LaTeX para revistas que
NÃO permitem estrutura de pastas no upload.

O script:

1. Analisa o arquivo principal (ex: manuscript.tex)
2. Encontra dependências:
   - \input
   - \include
   - \subfile
   - \includegraphics
   - \bibliography
   - \addbibresource
   - \bibliographystyle
   - \documentclass
3. Copia todos os arquivos para um diretório "submission/"
   SEM subpastas
4. Cria um novo manuscript.tex onde os caminhos são removidos
   (ex: figures/fig1.pdf -> fig1.pdf)
5. Gera submission.zip pronto para upload.

Uso
---
python latex_flatten_submission.py manuscript.tex
"""

import re
import shutil
import zipfile
import sys
from pathlib import Path


# ---------------------------------------------------------
# Padrões LaTeX que referenciam arquivos externos
# ---------------------------------------------------------

PATTERNS = {
    "input": r"\\input\{([^}]*)\}",
    "include": r"\\include\{([^}]*)\}",
    "subfile": r"\\subfile\{([^}]*)\}",
    "graphics": r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}",
    "bibliography": r"\\bibliography\{([^}]*)\}",
    "addbibresource": r"\\addbibresource(?:\[[^\]]*\])?\{([^}]*)\}",
    "documentclass": r"\\documentclass(?:\[[^\]]*\])?\{([^}]*)\}",
    "bibliographystyle": r"\\bibliographystyle\{([^}]*)\}",
}

DEFAULT_EXT = {
    "input": ".tex",
    "include": ".tex",
    "subfile": ".tex",
    "bibliography": ".bib",
    "addbibresource": ".bib",
    "documentclass": ".cls",
    "bibliographystyle": ".bst",
}

GRAPHIC_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg", ".eps"]


# ---------------------------------------------------------
# Resolve figuras sem extensão explícita
# ---------------------------------------------------------

def resolve_graphic(path_base):
    """
    Procura o arquivo de figura testando extensões comuns
    quando a extensão não é explicitada no LaTeX.
    """

    p = Path(path_base)

    if p.suffix:
        if p.exists():
            return p
        return None

    for ext in GRAPHIC_EXTENSIONS:
        candidate = p.with_suffix(ext)
        if candidate.exists():
            return candidate

    return None


# ---------------------------------------------------------
# Parser recursivo de arquivos .tex
# ---------------------------------------------------------

def parse_tex_file(tex_path, visited, collected):
    """
    Lê um arquivo .tex e encontra dependências.

    - visited evita loops infinitos
    - collected armazena todos os arquivos necessários
    """

    tex_path = tex_path.resolve()

    if tex_path in visited:
        return

    visited.add(tex_path)
    collected.add(tex_path)

    if not tex_path.exists():
        return

    content = tex_path.read_text(encoding="utf8", errors="ignore")
    base_dir = tex_path.parent

    for key, pattern in PATTERNS.items():

        matches = re.findall(pattern, content)

        for m in matches:

            for item in m.split(","):

                item = item.strip()

                if key in DEFAULT_EXT and not Path(item).suffix:
                    item += DEFAULT_EXT[key]

                target = base_dir / item

                if key in ["input", "include", "subfile"]:
                    parse_tex_file(target, visited, collected)

                elif key == "graphics":
                    g = resolve_graphic(target)
                    if g:
                        collected.add(g.resolve())

                else:
                    if target.exists():
                        collected.add(target.resolve())


# ---------------------------------------------------------
# Coleta todas as dependências
# ---------------------------------------------------------

def collect_dependencies(main_tex):
    """
    Função principal que inicia o parser recursivo.
    """

    visited = set()
    collected = set()

    parse_tex_file(Path(main_tex), visited, collected)

    return sorted(collected)


# ---------------------------------------------------------
# Remove caminhos de subpastas no código LaTeX
# ---------------------------------------------------------

def flatten_tex_paths(content):
    """
    Remove caminhos como:

    figures/fig1.pdf -> fig1.pdf
    sections/methods.tex -> methods.tex
    """

    pattern = r"\{([^{}]*/)([^{}]+)\}"

    return re.sub(pattern, r"{\2}", content)


# ---------------------------------------------------------
# Cria diretório de submissão
# ---------------------------------------------------------

def create_submission_folder(files, main_tex):

    submission_dir = Path("submission")

    if submission_dir.exists():
        shutil.rmtree(submission_dir)

    submission_dir.mkdir()

    for f in files:

        f = Path(f)
        target = submission_dir / f.name

        shutil.copy2(f, target)

        if f.name == Path(main_tex).name:

            content = target.read_text(encoding="utf8", errors="ignore")
            content = flatten_tex_paths(content)

            target.write_text(content, encoding="utf8")

    return submission_dir


# ---------------------------------------------------------
# Gera ZIP final
# ---------------------------------------------------------

def create_zip(folder):

    zip_name = "submission.zip"

    with zipfile.ZipFile(zip_name, "w") as z:

        for f in folder.iterdir():
            z.write(f, f.name)

    print(f"\nZIP criado: {zip_name}\n")


# ---------------------------------------------------------
# Execução principal
# ---------------------------------------------------------

def main():

    if len(sys.argv) < 2:
        print("Uso: python latex_flatten_submission.py manuscript.tex")
        sys.exit(1)

    main_tex = sys.argv[1]

    print("\nAnalisando dependências...\n")

    files = collect_dependencies(main_tex)

    for f in files:
        print(f)

    submission_dir = create_submission_folder(files, main_tex)

    create_zip(submission_dir)

    print("Pacote de submissão criado em ./submission/\n")


if __name__ == "__main__":
    main()