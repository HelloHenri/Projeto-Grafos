import json
import os
import networkx as nx

def carregar_instancia_json(caminho_arquivo):
    """
    Carrega uma instância de grafo a partir de um arquivo JSON estruturado.
    """
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo de instância não encontrado: {caminho_arquivo}")
        
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    G = nx.Graph()
    # Adiciona nós e arestas descritos no JSON
    for no in data.get("vertices", []):
        G.add_node(no)
    for aresta in data.get("arestas", []):
        G.add_edge(aresta[0], aresta[1])
        
    return {
        "nome": data.get("nome", "Instância Desconhecida"),
        "descricao": data.get("descricao", ""),
        "limite_equipes": data.get("limite_equipes", 5),
        "grafo": G
    }

def gerar_instancia_massiva(num_turnos=120, probabilidade_conflito=0.08):
    """
    Gera uma instância massiva de grande escala usando modelo de Erdos-Renyi 
    (grafo aleatório) para cumprir a exigência de cenário inviável/manual complexo.
    """
    G = nx.erdos_renyi_graph(n=num_turnos, p=probabilidade_conflito, seed=42)
    
    # Renomeia os nós para o contexto hospitalar
    mapping = {i: f"Turno_{i+1:03d}" for i in G.nodes()}
    G = nx.relabel_nodes(G, mapping)
    
    return {
        "nome": "Hospital Regional (Instância Massiva)",
        "descricao": f"Cenário de grande porte com {num_turnos} turnos gerado estocasticamente para validação de desempenho.",
        "limite_equipes": 12,
        "grafo": G
    }