

def getMonta(monta: str):
    if not monta:
        return "Não Informada"

    texto = monta.lower().strip()

    # categorias diretas
    if texto in ["pequena", "pequena monta"]:
        return "Pequena Monta"

    if texto in ["média", "media", "média monta", "media monta"]:
        return "Média Monta"

    if texto in ["grande", "grande monta"]:
        return "Grande Monta"

    # padrões compostos
    if "pequena" in texto or "recuperável" in texto or "conservado" in texto:
        return "Pequena Monta"

    if "média" in texto or "media" in texto:
        return "Média Monta"

    if "grande" in texto or "sucata" in texto:
        return "Grande Monta"

    if texto == "no estado que se encontra":
        return "No estado que se encontra"

    return "Não Informada"
     