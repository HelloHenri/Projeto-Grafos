import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import os
import time
import random

from core.gerador import carregar_instancia_json, gerar_instancia_massiva
from core.algoritmos import welsh_powell, dsatur, validar_coloracao

# Configuração da página
st.set_page_config(
    page_title="Alocação de Turnos Hospitalares - Coloração de Grafos",
    page_icon="🏥",
    layout="wide"
)

st.title("Sistema de Alocação de Turnos Hospitalares via Coloração de Grafos")
st.markdown("**Disciplina:** Teoria dos Grafos | **Tema 8:** Coloração de Grafos")
st.markdown("---")

# ==========================================
# 1. SELEÇÃO DE DADOS NA PRÓPRIA PÁGINA
# ==========================================
st.subheader("1. Seleção da Instância do Problema")

opcao_instancia = st.radio(
    "Escolha o Cenário:",
    [
        "Caso 1: Posto de Saúde (Pequeno - 6 Turnos)",
        "Caso 2: Hospital Municipal (Médio - 15 Turnos)",
        "Caso 3: Crise de Escala (Inviável - K4)",
        "Caso 4: Hospital Regional (Massivo - 120 Turnos)"
    ],
    index=0,
    horizontal=True
)

# Função auxiliar para gerar um grafo totalmente novo com base no tipo escolhido
def criar_nova_instancia(opcao):
    if "Caso 1" in opcao:
        n = 6
        G = nx.erdos_renyi_graph(n=n, p=0.5, seed=random.randint(1, 1000))
        mapping = {i: f"Turno_{i+1}" for i in G.nodes()}
        G = nx.relabel_nodes(G, mapping)
        return {
            "nome": "Posto de Saúde Bairro (Variação Gerada)",
            "descricao": "6 turnos semanais com nova rede de conflitos gerada estocasticamente.",
            "limite_equipes": 3,
            "grafo": G
        }
    elif "Caso 2" in opcao:
        n = 15
        G = nx.erdos_renyi_graph(n=n, p=0.35, seed=random.randint(1, 1000))
        mapping = {i: f"T{i+1:02d}_Plantao" for i in G.nodes()}
        G = nx.relabel_nodes(G, mapping)
        return {
            "nome": "Hospital Municipal (Variação Gerada)",
            "descricao": "15 turnos com topologia de conflitos rede-aleatória recriada do zero.",
            "limite_equipes": 4,
            "grafo": G
        }
    elif "Caso 3" in opcao:
        caminho = os.path.join("dados", "caso3_inviavel.json")
        return carregar_instancia_json(caminho)
    else:
        return gerar_instancia_massiva(num_turnos=120, probabilidade_conflito=random.uniform(0.06, 0.10))

# Inicializa ou altera a instância se o usuário trocar no rádio
if "ultima_opcao" not in st.session_state or st.session_state.ultima_opcao != opcao_instancia:
    st.session_state.ultima_opcao = opcao_instancia
    dados_atuais = criar_nova_instancia(opcao_instancia)
    st.session_state.dados_atuais = dados_atuais
    st.session_state.G_ativo = dados_atuais["grafo"].copy()

dados = st.session_state.dados_atuais
G = st.session_state.G_ativo
limite_equipes = dados["limite_equipes"]

st.info(f"**Cenário Atual:** {dados['nome']} — {dados['descricao']}")

st.markdown("---")

# ==========================================
# 2. EXECUTAR OS ALGORITMOS ANTES DO PAINEL PARA TER OS DADOS PRONTOS
# ==========================================
# Executa Welsh-Powell
t_inicio = time.perf_counter()
res_wp = welsh_powell(G)
t_wp = (time.perf_counter() - t_inicio) * 1000

if isinstance(res_wp, dict):
    col_wp = res_wp["coloring"]
    num_wp = res_wp["num_colors"]
else:
    col_wp, num_wp = res_wp[0], res_wp[1]
valido_wp = validar_coloracao(G, col_wp)

# Executa DSATUR
t_inicio = time.perf_counter()
res_ds = dsatur(G)
t_ds = (time.perf_counter() - t_inicio) * 1000

if isinstance(res_ds, dict):
    col_ds = res_ds["coloring"]
    num_ds = res_ds["num_colors"]
else:
    col_ds, num_ds = res_ds[0], res_ds[1]
valido_ds = validar_coloracao(G, col_ds)

grau_max = max(dict(G.degree()).values()) if G.number_of_nodes() > 0 else 0

# ==========================================
# 3. TELA PRINCIPAL: COMPARAÇÃO VISUAL LADO A LADO E PAINEL DE CONTROLE
# ==========================================
col_grafo1, col_grafo2, col_controles = st.columns([1.2, 1.2, 1])

paleta = ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33F3", "#33FFF3", "#FFA533", "#A533FF"]

# Layout inteligente e adaptativo (evita aglomeração no caso massivo)
num_nos = G.number_of_nodes()
exibir_labels = num_nos <= 30  

if num_nos > 50:
    pos = nx.spring_layout(G, seed=42, k=0.45, iterations=300)
    tamanho_no = 140
    tamanho_fonte = 6
    fig_size = (6, 5)
else:
    pos = nx.spring_layout(G, seed=42)
    tamanho_no = 600
    tamanho_fonte = 8
    fig_size = (5, 4)

with col_grafo1:
    st.subheader("🔵 Welsh-Powell")
    fig1, ax1 = plt.subplots(figsize=fig_size)
    node_colors_wp = [paleta[col_wp[node] % len(paleta)] for node in G.nodes()]
    
    nx.draw(
        G, pos=pos, with_labels=exibir_labels, node_color=node_colors_wp, node_size=tamanho_no,
        font_size=tamanho_fonte, font_weight="bold", font_color="white",
        edge_color="#444444", width=0.8 if num_nos > 50 else 1.2, ax=ax1, node_shape='o'
    )
    ax1.set_title(f"WP: {num_wp} Equipes Alocadas", fontsize=10, color="white")
    fig1.patch.set_facecolor('#0e1117')
    ax1.set_facecolor('#0e1117')
    st.pyplot(fig1)

with col_grafo2:
    st.subheader("🟢 DSATUR")
    fig2, ax2 = plt.subplots(figsize=fig_size)
    node_colors_ds = [paleta[col_ds[node] % len(paleta)] for node in G.nodes()]
    
    nx.draw(
        G, pos=pos, with_labels=exibir_labels, node_color=node_colors_ds, node_size=tamanho_no,
        font_size=tamanho_fonte, font_weight="bold", font_color="white",
        edge_color="#444444", width=0.8 if num_nos > 50 else 1.2, ax=ax2, node_shape='o'
    )
    ax2.set_title(f"DSATUR: {num_ds} Equipes Alocadas", fontsize=10, color="white")
    fig2.patch.set_facecolor('#0e1117')
    ax2.set_facecolor('#0e1117')
    st.pyplot(fig2)

if not exibir_labels:
    st.info("ℹ️ **Modo de Visualização Massiva Ativado:** Rótulos de texto ocultados automaticamente para evitar sobreposição visual (clutter) em redes complexas de alta densidade. O foco está na distribuição topológica e no desempenho das heurísticas.")

with col_controles:
    st.markdown("### Painel de Controle")
    
    if st.button("🎲 Gerar Novo Grafo Aleatório", type="primary", use_container_width=True):
        novo_dados = criar_nova_instancia(opcao_instancia)
        st.session_state.dados_atuais = novo_dados
        st.session_state.G_ativo = novo_dados["grafo"].copy()
        st.success("Um novo grafo foi gerado com sucesso!")
        st.rerun()

    st.markdown("---")
    st.markdown("#### Teste Dinâmico (Adicionar Conflito)")
    
    if "conflitos_extras" not in st.session_state:
        st.session_state.conflitos_extras = []

    turnos_lista = list(G.nodes())
    t1 = st.selectbox("Turno A:", turnos_lista, key="t_a")
    t2 = st.selectbox("Turno B:", [t for t in turnos_lista if t != t1], key="t_b")

    if st.button("Adicionar Conflito ao Vivo", use_container_width=True):
        if (t1, t2) not in G.edges() and (t2, t1) not in G.edges():
            G.add_edge(t1, t2)
            st.session_state.conflitos_extras.append((t1, t2))
            st.success(f"Conflito adicionado entre {t1} e {t2}!")
            st.rerun()
        else:
            st.warning("Já existe conflito entre estes turnos.")

    if st.button("Resetar Conflitos Extras", use_container_width=True):
        for edge in st.session_state.conflitos_extras:
            if G.has_edge(edge[0], edge[1]):
                G.remove_edge(edge[0], edge[1])
        st.session_state.conflitos_extras = []
        st.success("Conflitos extras removidos.")
        st.rerun()

# ==========================================
# 4. MÉTRICAS E RESULTADOS (EXIBIDOS DIRETAMENTE)
# ==========================================
st.markdown("---")
st.markdown("## 📊 Relatório Analítico de Desempenho")

# Blocos de métricas
m1, m2, m3, m4 = st.columns(4)
m1.metric("Turnos (Vértices)", G.number_of_nodes())
m2.metric("Conflitos (Arestas)", G.number_of_edges())
m3.metric("Limite de Equipes", limite_equipes)
m4.metric("Grau Máximo ($\Delta$)", grau_max)

st.markdown("---")

col_res1, col_res2 = st.columns(2)

with col_res1:
    st.subheader("🔵 Heurística: Welsh-Powell")
    st.write(f"• **Equipes Necessárias:** {num_wp}")
    st.write(f"• **Tempo de Processamento:** {t_wp:.4f} ms")
    st.write(f"• **Integridade da Alocação:** {'100% Válida ✅' if valido_wp else 'Inválida ❌'}")
    
    if num_wp <= limite_equipes:
        st.success(f"STATUS: ESCALA VIÁVEL! (Utilizou {num_wp} de {limite_equipes} equipes).")
    else:
        st.error(f"STATUS: ESCALA INVIÁVEL! (Exige {num_wp} equipes, mas o hospital dispõe apenas de {limite_equipes}).")

with col_res2:
    st.subheader("🟢 Heurística: DSATUR (Recomendado)")
    st.write(f"• **Equipes Necessárias:** {num_ds}")
    st.write(f"• **Tempo de Processamento:** {t_ds:.4f} ms")
    st.write(f"• **Integridade da Alocação:** {'100% Válida ✅' if valido_ds else 'Inválida ❌'}")
    
    if num_ds <= limite_equipes:
        st.success(f"STATUS: ESCALA VIÁVEL! (Utilizou {num_ds} de {limite_equipes} equipes).")
    else:
        st.error(f"STATUS: ESCALA INVIÁVEL! (Exige {num_ds} equipes, mas o hospital dispõe apenas de {limite_equipes}).")