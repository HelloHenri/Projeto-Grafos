import json
import networkx as nx

def carregar_instancia_json(caminho_arquivo):
    """Lê um arquivo JSON de cenário hospitalar e monta o grafo."""
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
        
    G = nx.Graph()
    G.add_nodes_from(dados["turnos"])
    G.add_edges_from(dados["conflitos"])
    
    return {
        "grafo": G,
        "nome": dados["nome"],
        "descricao": dados["descricao"],
        "limite_equipes": dados["limite_equipes_disponiveis"]
    }

def gerar_instancia_massiva(num_turnos=150, probabilidade_conflito=0.08):
    """
    Gera um grafo aleatório de grande porte (Erdos-Renyi) simulando um hospital regional.
    Atende ao requisito 4.3 (instância inviável para resolução manual).
    """
    G_numerico = nx.erdos_renyi_graph(n=num_turnos, p=probabilidade_conflito, seed=42)
    
    # Renomeia os nós para nomes de turnos reais
    mapeamento = {i: f"Turno_{i+1:03d}" for i in G_numerico.nodes()}
    G = nx.relabel_nodes(G_numerico, mapeamento)
    
    return {
        "grafo": G,
        "nome": f"Hospital Regional Massivo ({num_turnos} Turnos)",
        "descricao": "Instância gerada computacionalmente com alta densidade de conflitos. Resolução manual inviável.",
        "limite_equipes": 20
    }