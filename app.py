import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from core.gerador import carregar_instancia_json, gerar_instancia_massiva
from core.algoritmos import welsh_powell, dsatur, validar_coloracao

st.set_page_config(page_title="Escalonamento Hospitalar - Grafos", layout="wide")

st.title("Sistema de Alocação de Turnos Hospitalares via Coloração de Grafos")
st.markdown("**Disciplina:** Teoria dos Grafos | **Tema 8:** Coloração de Grafos")
st.divider()

# Barra Lateral: Controles de Entrada
st.sidebar.header("1. Seleção de Dados (Instâncias)")
opcao_entrada = st.sidebar.radio(
    "Escolha a fonte dos dados:",
    [
        "Caso 1: Posto de Saúde (Pequeno - 6 Turnos)",
        "Caso 2: Hospital Municipal (Médio - 15 Turnos)",
        "Caso 3: Crise de Escala (Caso Sem Solução)",
        "Caso 4: Hospital Regional (Grande - Gerado por Script)"
    ]
)

if "Caso 1" in opcao_entrada:
    instancia = carregar_instancia_json("dados/caso1_pequeno.json")
elif "Caso 2" in opcao_entrada:
    instancia = carregar_instancia_json("dados/caso2_medio.json")
elif "Caso 3" in opcao_entrada:
    instancia = carregar_instancia_json("dados/caso3_inviavel.json")
else:
    qtd_nos = st.sidebar.slider("Quantidade de Turnos:", min_value=50, max_value=300, value=120, step=10)
    densidade = st.sidebar.slider("Probabilidade de Conflito:", min_value=0.02, max_value=0.30, value=0.08, step=0.02)
    instancia = gerar_instancia_massiva(qtd_nos, densidade)

G = instancia["grafo"]

# Funcionalidade Extra: Adicionar conflito ao vivo (para testes do professor)
st.sidebar.divider()
st.sidebar.header("2. Teste Dinâmico ao Vivo")
st.sidebar.caption("Adicione um novo conflito entre turnos para testar a adaptação do algoritmo:")
nos_lista = list(G.nodes())
t1 = st.sidebar.selectbox("Turno A:", nos_lista, index=0)
t2 = st.sidebar.selectbox("Turno B:", nos_lista, index=min(1, len(nos_lista)-1))

if "conflitos_extras" not in st.session_state:
    st.session_state.conflitos_extras = []

if st.sidebar.button("Adicionar Conflito"):
    if t1 != t2:
        st.session_state.conflitos_extras.append((t1, t2))

if st.sidebar.button("Resetar Conflitos Extras"):
    st.session_state.conflitos_extras = []

for u, v in st.session_state.conflitos_extras:
    if u in G and v in G:
        G.add_edge(u, v)

# Painel Principal: Informações da Instância
col_info1, col_info2, col_info3, col_info4 = st.columns(4)
col_info1.metric("Turnos (Vértices)", len(G.nodes()))
col_info2.metric("Conflitos (Arestas)", len(G.edges()))
col_info3.metric("Equipes Disponíveis (Limite)", instancia["limite_equipes"])
col_info4.metric("Grau Máximo do Grafo", max(dict(G.degree()).values()) if len(G.nodes()) > 0 else 0)

st.info(f"**Cenário Atual:** {instancia['nome']} — *{instancia['descricao']}*")

# Execução dos Algoritmos
if st.button("Executar Algoritmos de Coloração", type="primary"):
    cores_wp, qtd_wp, tempo_wp = welsh_powell(G)
    cores_ds, qtd_ds, tempo_ds = dsatur(G)
    
    valido, msg_validacao = validar_coloracao(G, cores_ds)
    
    st.subheader("Comparação de Desempenho entre Heurísticas")
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.markdown("#### Heurística 1: Welsh-Powell")
        st.write(f"- **Equipes/Slots Necessários (Cores):** `{qtd_wp}`")
        st.write(f"- **Tempo de Execução:** `{tempo_wp*1000:.4f} ms`")
        
    with col_res2:
        st.markdown("#### Heurística 2: DSATUR")
        st.write(f"- **Equipes/Slots Necessários (Cores):** `{qtd_ds}`")
        st.write(f"- **Tempo de Execução:** `{tempo_ds*1000:.4f} ms`")

    # Validação das Restrições do Problema
    st.subheader("Validação da Solução")
    if valido:
        st.success(f"Integridade Matemática: {msg_validacao}")
    else:
        st.error(f"Erro na Coloração: {msg_validacao}")
        
    if qtd_ds > instancia["limite_equipes"]:
        st.warning(
            f"**ALERTA DE VIABILIDADE:** O hospital precisa de no mínimo **{qtd_ds} equipes**, "
            f"mas possui apenas **{instancia['limite_equipes']} equipes disponíveis**. "
            "Não há solução possível sem contratar mais profissionais ou reduzir conflitos!"
        )
    else:
        st.success(
            f"**ESCALA VIÁVEL:** As **{instancia['limite_equipes']} equipes disponíveis** são suficientes "
            f"(utilizadas **{qtd_ds} equipes**)."
        )

    # Visualização Gráfica e Tabela de Alocação
    st.divider()
    col_vis1, col_vis2 = st.columns([1.4, 1])
    
    with col_vis1:
        st.subheader("Visualização do Grafo Colorido (DSATUR)")
        if len(G.nodes()) <= 60:
            fig, ax = plt.subplots(figsize=(8, 6))
            pos = nx.spring_layout(G, seed=42)
            lista_cores = [cores_ds[no] for no in G.nodes()]
            
            nx.draw(
                G, pos, with_labels=True, node_color=lista_cores,
                cmap=plt.cm.Set3, node_size=900, font_size=8,
                font_weight="bold", edge_color="#888888", ax=ax
            )
            st.pyplot(fig)
        else:
            st.info(
                "Como este grafo possui mais de 60 turnos, a renderização visual dos nós foi omitida "
                "para evitar poluição visual. Consulte a tabela de alocação ao lado."
            )
            
    with col_vis2:
        st.subheader("Escala Final Gerada")
        df_resultado = pd.DataFrame([
            {"Turno": turno, "Equipe / Horário Alocado": f"Equipe {cor + 1}"}
            for turno, cor in sorted(cores_ds.items(), key=lambda x: x[1])
        ])
        st.dataframe(df_resultado, use_container_width=True, height=400)