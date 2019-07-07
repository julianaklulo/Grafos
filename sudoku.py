import networkx as nx
from collections import OrderedDict


def remove_cor_vizinhos(G, node):
    """
        Atualiza os vizinhos de um nó que já foi colorido
    """
    # gera lista com os números possíveis
    cores = list(range(1, 10))
    # pega a cor do nó
    cor = G.node[node].get("cor")
    # percorre todos os vizinhos do nó
    for vizinho in G.neighbors(node):
        # se o vizinho já estiver colorido
        if G.node[vizinho].get("cor"):
            continue  # pula para o próximo
        # caso o vizinho ainda não tenha sido inicializado
        if G.node[vizinho].get("lista_cores") is None:
            G.node[vizinho]["lista_cores"] = cores[:]  # inicia com as possíveis cores
        # remove a cor do nó das possíveis cores do vizinho
        if cor in G.node[vizinho]["lista_cores"]:
            G.node[vizinho]["lista_cores"].remove(cor)


def colorir(G, node):
    """
        Colore o nó e atualiza os vizinhos
    """
    # verifica se o nó não tem cor
    cor = G.node[node].get("cor")
    if cor:  # já colorido, não precisa continuar
        return
    # pega a primeira opção de cor para o nó
    nova_cor = G.node[node]["lista_cores"][0]
    # atualiza a cor do nó
    G.node[node]["cor"] = nova_cor
    # limpa a lista de possíveis cores
    G.node[node]["lista_cores"] = []
    # atualiza todos os vizinhos do nó
    remove_cor_vizinhos(G, node)


# inicializa o grafo
G = nx.Graph()

quadrado = 1
contador = 0

# cria os nós do grafo 20-regular para armazenar o sudoku
for i in range(0, 9):
    quadrado = 0
    if i % 3 == 0 and i > 0:
        contador += 3
    for j in range(0, 9):
        if j == 0:
            quadrado = contador
        if j % 3 == 0:
            quadrado += 1
        G.add_node("v{}{}".format(i, j), linha=i, coluna=j, quadrado=quadrado)

# cria as arestas que liga cada linha, coluna e quadrado 3x3
for node1, data1 in G.nodes(data=True):
    for node2, data2 in G.nodes(data=True):
        if (data1["quadrado"] == data2["quadrado"] or
            data1["linha"] == data2["linha"] or
            data1["coluna"] == data2["coluna"]):
            G.add_edge(node1, node2)

# exemplo de sudoku a ser resolvido
sudoku_exemplo = [
    ("v00", 9), ("v01", 5), ("v05", 1), ("v08", 8),
    ("v11", 2), ("v12", 1), ("v13", 8), ("v14", 9), ("v16", 6),
    ("v20", 3), ("v24", 4), ("v25", 2), ("v26", 1), ("v27", 5), ("v28", 9),
    ("v30", 2), ("v31", 4), ("v34", 7), ("v35", 8), ("v38", 1),
    ("v40", 1), ("v42", 9), ("v43", 3), ("v44", 2), ("v47", 6), ("v48", 5),
    ("v50", 8), ("v53", 1), ("v57", 7), ("v58", 2),
    ("v60", 4), ("v61", 9), ("v64", 1), ("v66", 5), ("v67", 8),
    ("v70", 6), ("v71", 8), ("v72", 2), ("v73", 9), ("v78", 4),
    ("v83", 4), ("v84", 8), ("v85", 3), ("v87", 9), ("v88", 6)]

# pré colore os nós com os valores dados
for valor in sudoku_exemplo:
    G.node[valor[0]]["cor"] = valor[1]
    G.node[valor[0]]["lista_cores"] = []
    # atualiza as possíveis cores dos vizinhos
    remove_cor_vizinhos(G, valor[0])

# ordena os nós que ainda faltam serem coloridos
nos_sem_cores = {}
for node, data in G.nodes(data=True):
    tamanho = len(G.node[node]["lista_cores"])
    if tamanho != 0:
        if not nos_sem_cores.get(tamanho):
            nos_sem_cores[tamanho] = []
        # agrupa os nós com a mesma quantidade de cores possíveis
        nos_sem_cores[tamanho].append(node)

# ordena pela quantidade de possíveis cores
ordenado = OrderedDict(sorted(nos_sem_cores.items()))

# colore todos os nós restantes
for chave, valor in ordenado.items():
    for n in valor:
        colorir(G, n)

# imprime o resultado
for i in range(0, 9):
    linha = ""
    if i % 3 == 0 and i > 0:
        print()
    for j in range(0, 9):
        if j % 3 == 0 and j > 0:
            linha += "  "
        linha += str(G.node["v{}{}".format(i, j)]['cor'])
        linha += " "
    print(linha)
