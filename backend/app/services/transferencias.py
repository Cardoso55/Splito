def separar_credores_devedores(saldos: dict) -> tuple[list[dict], list[dict]]:
    """Separa quem tem saldo positivo (credores) de quem tem saldo negativo (devedores).

    Entrada: {participante_id: saldo_em_centavos}
    Saída: duas listas de {"participante_id": id, "valor": centavos}, com valor sempre positivo.
    Quem tem saldo 0 não entra em nenhuma das listas.
    """
    credores = []
    devedores = []

    for participante_id, saldo in saldos.items():
        if saldo > 0:
            credores.append({"participante_id": participante_id, "valor": saldo})
        elif saldo < 0:
            devedores.append({"participante_id": participante_id, "valor": abs(saldo)})

    return credores, devedores


def calcular_transferencias(saldos: dict) -> list[dict]:
    """Gera a lista de transferências que zera todos os saldos.

    Algoritmo guloso: o maior devedor paga o maior credor, repetidamente,
    até ninguém dever mais nada. Tudo em centavos inteiros.

    Entrada: {participante_id: saldo_em_centavos} (positivo = tem a receber)
    Saída: [{"devedor": id, "credor": id, "valor": centavos}, ...]
    """
    if sum(saldos.values()) != 0:
        raise ValueError("A soma dos saldos deve ser zero.")

    credores, devedores = separar_credores_devedores(saldos)

    transferencias = []

    while credores and devedores:
        credor = max(credores, key=lambda c: c["valor"])
        devedor = max(devedores, key=lambda d: d["valor"])

        valor_transferencia = min(credor["valor"], devedor["valor"])

        transferencias.append({
            "devedor": devedor["participante_id"],
            "credor": credor["participante_id"],
            "valor": valor_transferencia
        })

        credor["valor"] -= valor_transferencia
        devedor["valor"] -= valor_transferencia

        if credor["valor"] == 0:
            credores.remove(credor)
        if devedor["valor"] == 0:
            devedores.remove(devedor)

    return transferencias