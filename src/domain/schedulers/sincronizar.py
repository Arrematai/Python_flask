from datetime import datetime, timedelta

def parse_data(valor):
    if not valor:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(valor, fmt)
        except:
            pass
    return None


def checkAtivoByDataLeilao(agora, data_leilao, data_leilao_final, dias_remover):
    
    data_leilao = parse_data(data_leilao)
    data_leilao_final = parse_data(data_leilao_final)
    
    # Se não houver data de leilão → não desativa
    if not data_leilao:
        return 1

    # Se houver data de final e for maior que agora → bloqueia
    if data_leilao_final and data_leilao_final > agora:
        return 0

    # Se passaram mais de X dias → inativo
    if data_leilao + timedelta(days=dias_remover) < agora:
        return 0

    return 1


def sincronizar(dados_db, dados_novos, dias_remover=7):

    def chave_composta(item):
        # "ativo" removido da chave (evita duplicações indevidas)
        return (str(item['descricao']).strip().upper(), str(item['lote']).strip())

    agora = datetime.now()

    antigo_map = {chave_composta(item): item for item in dados_db}
    novos_map = {chave_composta(item): item for item in dados_novos}

    inserir = []
    atualizar = []
    remover = []

    campos_para_verificar = ['descricao', "lote", "ativo"]
    

    # --- 1) INSERÇÃO E ATUALIZAÇÃO ---
    for chave, novo in novos_map.items():

        # recalcular ativo baseado na data
        novo["ativo"] = checkAtivoByDataLeilao(
            agora,
            novo.get("data_leilao"),
            novo.get("data_leilao_final"),
            dias_remover
        )

        # Se não existe no banco → inserir
        if chave not in antigo_map:
            inserir.append(novo)
            continue

        antigo = antigo_map[chave]

        # Verificar diferenças
        diff = any(novo.get(k) != antigo.get(k) for k in campos_para_verificar)

        if diff:
            novo["id"] = antigo.get("id")
            novo["uuid"] = antigo.get("uuid")
            atualizar.append(novo)

    # --- 2) REMOVER ITENS QUE SUMIRAM NA API ---
    for chave, antigo in antigo_map.items():

        # Recalcular ativo do antigo também
        antigo["ativo"] = checkAtivoByDataLeilao(
            agora,
            antigo.get("data_leilao"),
            antigo.get("data_leilao_final"),
            dias_remover
        )

        # Se já não é ativo → ignora
        if antigo["ativo"] == 0:
            continue

        # Se não existe mais nos novos → remover
        if chave not in novos_map:
            remover.append(antigo)

    return inserir, atualizar, remover