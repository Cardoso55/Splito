from backend.app.services.divisao import dividir_igualmente


def calcular_pagos(despesas: list[dict]) -> dict:
    pagos = {}
    for despesa in despesas:
        if despesa["pagador_id"] not in pagos:
            pagos[despesa["pagador_id"]] = despesa["valor"]
        else:
            pagos[despesa["pagador_id"]] += despesa["valor"]
    return pagos

def calcular_devidos(despesas: list[dict]) -> dict:
    devidos = {}
    for despesa in despesas:
        partes = dividir_igualmente(despesa["valor"], despesa["participantes"])
        for parte in partes:
            if parte["participante_id"] not in devidos:
                devidos[parte["participante_id"]] = parte["valor"]
            else:
                devidos[parte["participante_id"]] += parte["valor"]
    return devidos

def calcular_saldos(despesas: list[dict]) -> dict:
    pagos = calcular_pagos(despesas)
    devidos = calcular_devidos(despesas)

    saldos = {}
    participantes_ids = set(pagos) | set(devidos)

    for participante_id in participantes_ids:
        saldo = pagos.get(participante_id, 0) - devidos.get(participante_id, 0)
        saldos[participante_id] = saldo

    return saldos