from datetime import datetime, timedelta
from typing import Optional

def parse_data(valor: Optional[str]) -> Optional[datetime]:
    
    if isinstance(valor, datetime):
        return valor
    
    if not valor:
        return None

    valor = valor.strip()

    formatos = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d/%m/%Y",
    )

    for fmt in formatos:
        try:
            return datetime.strptime(valor, fmt)
        except ValueError:
            continue 

    return None


def is_ativo_por_data_leilao(
    agora: datetime,
    inicio: Optional[str],
    fim: Optional[str],
    dias_remover: int,
) -> bool:
    """
    Regras:
    - Sem data de leilão → ativo
    - Se agora > data_leilao E agora > data_leilao_final → inativo
    - Se passou mais de X dias após data_leilao → inativo
    """    

    # Sem data de leilão → ativo
    if not inicio:
        return 1

    # Se ambas as datas existem e agora passou das duas → inativo
    if fim and agora > inicio and agora > fim:
        return 0

    # Se excedeu o prazo após o leilão → inativo
    limite = parse_data(inicio) + timedelta(days=dias_remover)
    if limite < agora:
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
        novo["ativo"] = is_ativo_por_data_leilao(
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
        
        
        # if antigo.get("modelo") == "320I M SPORT FLEX":
        #     print("DEBUG")
        #     print(agora)
        #     print(antigo.get("data_leilao"))
        #     print(antigo.get("data_leilao_final"))
        #     isAtivo = is_ativo_por_data_leilao(
        #             agora,
        #             antigo.get("data_leilao"),
        #             antigo.get("data_leilao_final"),
        #             dias_remover
        #         )
        #     print("ATIVO: ", isAtivo)
    
                
        #     exit(0)

        # Recalcular ativo do antigo também
        isAtivo = is_ativo_por_data_leilao(
            agora,
            antigo.get("data_leilao"),
            antigo.get("data_leilao_final"),
            dias_remover
        )
        
        if isAtivo == 0:
            antigo["ativo"] = 0                
            remover.append(antigo)
            continue    
            
        # Se já não é ativo → ignora
        if antigo["ativo"] == 0:
            continue

        # Se não existe mais nos novos → remover
        if chave not in novos_map:
            remover.append(antigo)

    return inserir, atualizar, remover