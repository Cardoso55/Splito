from backend.app.services.divisao import reais_para_centavos, centavos_para_reais
from backend.app.services.saldos import calcular_saldos
from backend.app.services.transferencias import calcular_transferencias


def montar_despesa(pagador_id, valor_em_reais, participantes_ids):
    """Monta uma despesa como a route vai montar: valor já convertido para centavos."""
    return {
        "pagador_id": pagador_id,
        "valor": reais_para_centavos(valor_em_reais),
        "participantes": [{"id": pid} for pid in participantes_ids],
    }


def aplicar_transferencias(saldos, transferencias):
    """Simula o pagamento das transferências e devolve os saldos finais."""
    finais = dict(saldos)
    for t in transferencias:
        finais[t["devedor"]] += t["valor"]
        finais[t["credor"]] -= t["valor"]
    return finais


def test_fluxo_completo_viagem_de_tres_amigos():
    # 0 = Ana, 1 = Bruno, 2 = Carla
    despesas = [
        montar_despesa(0, "90.00", [0, 1, 2]),   # hotel, dividido por todos
        montar_despesa(1, "45.50", [0, 1, 2]),   # jantar, não divide certo (resto)
        montar_despesa(2, "10.00", [1, 2]),      # táxi, só Bruno e Carla
    ]

    saldos = calcular_saldos(despesas)
    assert saldos == {0: 4483, 1: -467, 2: -4016}
    assert sum(saldos.values()) == 0

    transferencias = calcular_transferencias(saldos)
    assert {"devedor": 2, "credor": 0, "valor": 4016} in transferencias
    assert {"devedor": 1, "credor": 0, "valor": 467} in transferencias
    assert len(transferencias) == 2


def test_fluxo_completo_todo_mundo_termina_quite():
    despesas = [
        montar_despesa(0, "100.00", [0, 1, 2, 3]),
        montar_despesa(1, "33.33", [0, 1, 2]),
        montar_despesa(2, "0.05", [1, 2, 3]),
        montar_despesa(3, "250.99", [0, 1, 2, 3]),
        montar_despesa(0, "19.99", [2, 3]),
    ]

    saldos = calcular_saldos(despesas)
    transferencias = calcular_transferencias(saldos)
    finais = aplicar_transferencias(saldos, transferencias)

    assert all(valor == 0 for valor in finais.values())


def test_fluxo_completo_numero_de_transferencias_e_minimo_razoavel():
    despesas = [
        montar_despesa(0, "100.00", [0, 1, 2, 3, 4]),
        montar_despesa(1, "60.00", [0, 1, 2, 3, 4]),
    ]

    saldos = calcular_saldos(despesas)
    transferencias = calcular_transferencias(saldos)

    # no máximo (pessoas com saldo diferente de zero - 1) transferências
    com_saldo = [s for s in saldos.values() if s != 0]
    assert len(transferencias) <= len(com_saldo) - 1


def test_fluxo_completo_quando_cada_um_pagou_sua_parte_nao_ha_transferencia():
    despesas = [
        montar_despesa(0, "30.00", [0, 1, 2]),
        montar_despesa(1, "30.00", [0, 1, 2]),
        montar_despesa(2, "30.00", [0, 1, 2]),
    ]

    saldos = calcular_saldos(despesas)
    assert calcular_transferencias(saldos) == []


def test_fluxo_completo_valores_formatados_para_exibicao():
    despesas = [montar_despesa(0, "90.00", [0, 1, 2])]

    transferencias = calcular_transferencias(calcular_saldos(despesas))

    textos = sorted(centavos_para_reais(t["valor"]) for t in transferencias)
    assert textos == ["30.00", "30.00"]