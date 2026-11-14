import time

def welsh_powell(grafo):
    """
    Implementação manual do algoritmo de coloração Welsh-Powell.
    Ordena os vértices por grau decrescente e atribui a menor cor disponível.
    """
    inicio = time.perf_counter()
    
    # Ordena os vértices do maior grau (mais conflitos) para o menor
    vertices_ordenados = sorted(grafo.nodes(), key=lambda v: grafo.degree(v), reverse=True)
    
    cores = {}
    cor_atual = 0
    
    while len(cores) < len(vertices_ordenados):
        for v in vertices_ordenados:
            if v not in cores:
                # Verifica se algum vizinho já possui a cor_atual
                vizinhos = list(grafo.neighbors(v))
                if not any(cores.get(viz) == cor_atual for viz in vizinhos):
                    cores[v] = cor_atual
        cor_atual += 1
        
    tempo_execucao = time.perf_counter() - inicio
    num_cores = max(cores.values()) + 1 if cores else 0
    
    return cores, num_cores, tempo_execucao


def dsatur(grafo):
    """
    Implementação manual do algoritmo DSATUR (Degree of Saturation).
    Escolhe dinamicamente o vértice não colorido com maior número de cores distintas na vizinhança.
    """
    inicio = time.perf_counter()
    
    cores = {}
    nao_coloridos = set(grafo.nodes())
    
    # Grau inicial de cada vértice
    graus = {v: grafo.degree(v) for v in grafo.nodes()}
    # Conjunto de cores adjacentes para cada vértice
    cores_vizinhas = {v: set() for v in grafo.nodes()}
    
    while nao_coloridos:
        # Escolhe o vértice com maior saturação; em caso de empate, maior grau
        escolhido = max(
            nao_coloridos,
            key=lambda v: (len(cores_vizinhas[v]), graus[v])
        )
        
        # Encontra a menor cor inteira (0, 1, 2...) não usada pelos vizinhos
        cor = 0
        while cor in cores_vizinhas[escolhido]:
            cor += 1
            
        cores[escolhido] = cor
        nao_coloridos.remove(escolhido)
        
        # Atualiza a saturação dos vizinhos não coloridos
        for vizinho in grafo.neighbors(escolhido):
            if vizinho in nao_coloridos:
                cores_vizinhas[vizinho].add(cor)
                
    tempo_execucao = time.perf_counter() - inicio
    num_cores = max(cores.values()) + 1 if cores else 0
    
    return cores, num_cores, tempo_execucao


def validar_coloracao(grafo, cores):
    """
    Verifica matematicamente se a solução respeita a restrição fundamental:
    nenhuma aresta pode conectar dois vértices com a mesma cor.
    """
    for u, v in grafo.edges():
        if cores.get(u) == cores.get(v):
            return False, f"Conflito detectado entre '{u}' e '{v}' (ambos na Equipe {cores.get(u) + 1})"
    return True, "Solução 100% válida! Nenhum conflito de turno encontrado."