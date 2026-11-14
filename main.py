from core.gerador import carregar_instancia_json, gerar_instancia_massiva
from core.algoritmos import welsh_powell, dsatur, validar_coloracao

def executar_teste(caminho_ou_dict, eh_json=True):
    # Carrega a instância (arquivo JSON ou gerador automático)
    if eh_json:
        instancia = carregar_instancia_json(caminho_ou_dict)
    else:
        instancia = caminho_ou_dict
        
    G = instancia["grafo"]
    
    print(f"\n{'='*60}")
    print(f"ANÁLISE DE CENÁRIO: {instancia['nome']}")
    print(f"Descrição: {instancia['descricao']}")
    print(f"{'='*60}")
    print(f"• Total de Turnos (Vértices): {len(G.nodes)}")
    print(f"• Total de Conflitos (Arestas): {len(G.edges)}")
    print(f"• Limite de Equipes do Hospital: {instancia['limite_equipes']}")
    
    # Executa Algoritmo 1: Welsh-Powell
    cores_wp, qtd_wp, tempo_wp = welsh_powell(G)
    
    # Executa Algoritmo 2: DSATUR
    cores_ds, qtd_ds, tempo_ds = dsatur(G)
    
    print("\n--- RESULTADOS DA COMPARAÇÃO ---")
    print(f"[Welsh-Powell]")
    print(f"  -> Equipes necessárias: {qtd_wp}")
    print(f"  -> Tempo de execução: {tempo_wp * 1000:.4f} ms")
    
    print(f"\n[DSATUR (Recomendado)]")
    print(f"  -> Equipes necessárias: {qtd_ds}")
    print(f"  -> Tempo de execução: {tempo_ds * 1000:.4f} ms")
    
    # Validação matemática da integridade da coloração (DSATUR)
    valido, msg = validar_coloracao(G, cores_ds)
    print(f"\nValidação de Conflitos: {msg}")
    
    # Verificação de restrição de viabilidade do hospital
    if qtd_ds > instancia["limite_equipes"]:
        print(f"STATUS: ESCALA INVIÁVEL! (Exige {qtd_ds} equipes, mas o hospital só tem {instancia['limite_equipes']}).")
    else:
        print(f"STATUS: ESCALA VIÁVEL! (Utilizou {qtd_ds} de {instancia['limite_equipes']} equipes disponíveis).")


if __name__ == "__main__":
    print("Iniciando testes automatizados do Sistema de Escalonamento Hospitalar...")
    
    # Teste 1: Caso Pequeno (Validação manual)
    executar_teste("dados/caso1_pequeno.json")
    
    # Teste 2: Caso Médio (Hospital Municipal)
    executar_teste("dados/caso2_medio.json")
    
    # Teste 3: Caso Sem Solução (Fronteira / Inviável)
    executar_teste("dados/caso3_inviavel.json")
    
    # Teste 4: Caso Grande (Gerado por script - Inviável manualmente)
    instancia_massiva = gerar_instancia_massiva(num_turnos=120, probabilidade_conflito=0.08)
    executar_teste(instancia_massiva, eh_json=False)
    
    print(f"\n{'='*60}")
    print("Todos os testes via terminal foram concluídos com sucesso!")