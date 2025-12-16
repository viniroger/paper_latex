from graphviz import Digraph

# Criação do grafo
g = Digraph(format='png')
g.attr(rankdir='TB', fontsize='12', fontname='Helvetica')
g.attr('node', shape='box', style='rounded,filled', fillcolor='#E0F2F1', fontname='Helvetica')

# Função para aplicar negrito na primeira linha do texto de cada nó
def format_node(label):
    lines = label.split('\n')
    if lines:
        lines[0] = f"<b>{lines[0]}</b>"
    return f'<<TABLE BORDER="0" CELLBORDER="0"><TR><TD ALIGN="LEFT">{r"<BR/>".join(lines)}</TD></TR></TABLE>>'

# Nós com a primeira linha em negrito
g.node('1', format_node(
    "1. Arquivo fonte LaTeX\n"
    "- Documento principal (.tex)\n"
    "- Classe elsarticle (.cls)\n"
    "- Estilo bibliográfico (.bst)\n"
    "- Base de referências (.bib)"
))

g.node('2', format_node(
    "2. Primeira compilação LaTeX\n"
    "- Execução do pdflatex\n"
    "- Leitura de .tex e .cls\n"
    "- Escrita de citações e rótulos"
))

g.node('3', format_node(
    "3. Arquivos auxiliares iniciais\n"
    "- aux: citações e referências cruzadas\n"
    "- log: registro da compilação\n"
    "- out: informações para hyperlinks\n"
    "- toc/lof/lot: listas e sumário (se existirem)"
))

g.node('4', format_node(
    "4. Processamento BibTeX\n"
    "- Leitura de aux, bib e bst\n"
    "- Seleção e formatação das referências\n"
    "- Geração da bibliografia em LaTeX"
))

g.node('5', format_node(
    "5. Arquivos da bibliografia\n"
    "- bbl: referências formatadas\n"
    "- blg: log do BibTeX"
))

g.node('6', format_node(
    "6. Segunda compilação LaTeX\n"
    "- Incorporação do bbl ao texto\n"
    "- Resolução inicial das citações\n"
    "- Atualização dos rótulos"
))

g.node('7', format_node(
    "7. Compilação final LaTeX\n"
    "- Estabilização da numeração\n"
    "- Resolução de referências cruzadas\n"
    "- Ativação de links (hyperref)"
))

g.node('8', format_node(
    "8. Arquivos finais e de controle\n"
    "- pdf: documento final\n"
    "- synctex.gz: sincronização editor-PDF\n"
    "- fls: arquivos lidos\n"
    "- fdb_latexmk: dependências do latexmk"
))

# Conexões
with g.subgraph() as s:
    s.attr(rank='same')
    s.node('1')
    s.node('5')

with g.subgraph() as s:
    s.attr(rank='same')
    s.node('2')
    s.node('6')

with g.subgraph() as s:
    s.attr(rank='same')
    s.node('3')
    s.node('7')

with g.subgraph() as s:
    s.attr(rank='same')
    s.node('4')
    s.node('8')

g.edge('1', '2')
g.edge('2', '3')
g.edge('3', '4')

g.edge('5', '6')
g.edge('6', '7')
g.edge('7', '8')

g.edge('4', '5')

# Exporta a imagem
output_path = 'figs/flowchart'
g.render(output_path, cleanup=False)
output_path + '.png'
