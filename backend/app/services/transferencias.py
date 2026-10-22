def calcular_transferencias(grupo: list[dict]) -> list[dict]:
    total = sum(participante["valor"] for participante in grupo)
    media = total / len(grupo)

    credores = []
    devedores = []

    for participante in grupo:
        saldo = participante["valor"] - media
        if saldo > 0:
            credor = participante["participante"]
            credores.append({"participante": credor, "valor": saldo})
        elif saldo == 0:
            continue
        else:
            devedor = participante["participante"]
            devedores.append({"participante": devedor, "valor": abs(saldo)})

    transferencias = []

    while credores and devedores:
        credor = max(credores, key=lambda c: c["valor"])
        devedor = max(devedores, key=lambda d: d["valor"])

        valor_transferencia = min(credor["valor"], devedor["valor"])

        transferencias.append({
            "devedor": devedor["participante"],
            "credor": credor["participante"],
            "valor": valor_transferencia
        })

        credor["valor"] -= valor_transferencia
        devedor["valor"] -= valor_transferencia

        if credor["valor"] == 0:
            credores.remove(credor)
        if devedor["valor"] == 0:
            devedores.remove(devedor)

    return transferencias