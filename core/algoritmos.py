import networkx as nx

def validar_coloracao(G, coloring):
    """
    Verifica se a coloração é válida para o grafo (nenhum par de vértices 
    conectados por aresta possui a mesma cor).
    """
    for u, v in G.edges():
        if coloring.get(u) == coloring.get(v):
            return False
    return True


def welsh_powell(G):
    """
    Implementação manual da heurística de Welsh-Powell.
    Retorna explicitamente um dicionário contendo o mapeamento de cores e o total de cores.
    """
    nos_ordenados = sorted(G.nodes(), key=lambda node: G.degree(node), reverse=True)
    
    coloring = {}
    current_color = 0
    
    while nos_ordenados:
        uncolored_nodes = list(nos_ordenados)
        
        for node in uncolored_nodes:
            pode_colorir = True
            for neighbor in G.neighbors(node):
                if neighbor in coloring and coloring[neighbor] == current_color:
                    pode_colorir = False
                    break
            
            if pode_colorir:
                coloring[node] = current_color
                nos_ordenados.remove(node)
                
        current_color += 1
        
    return {
        "coloring": coloring,
        "num_colors": current_color
    }


def dsatur(G):
    """
    Implementação manual da heurística DSATUR (Degree of Saturation).
    Retorna explicitamente um dicionário contendo o mapeamento de cores e o total de cores.
    """
    coloring = {}
    grau_saturacao = {node: 0 for node in G.nodes()}
    
    while len(coloring) < len(G.nodes()):
        no_selecionado = max(
            [n for n in G.nodes() if n not in coloring],
            key=lambda n: (grau_saturacao[n], G.degree(n))
        )
        
        cores_vizinhos = {coloring[v] for v in G.neighbors(no_selecionado) if v in coloring}
        
        cor = 0
        while cor in cores_vizinhos:
            cor += 1
            
        coloring[no_selecionado] = cor
        
        for v in G.neighbors(no_selecionado):
            if v not in coloring:
                cores_v_vizinhos = {coloring[w] for w in G.neighbors(v) if w in coloring}
                grau_saturacao[v] = len(cores_v_vizinhos)
                
    num_colors = max(coloring.values()) + 1 if coloring else 0
    return {
        "coloring": coloring,
        "num_colors": num_colors
    }