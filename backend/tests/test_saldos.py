from backend.app.services.saldos import (
    calcular_pagos,
    calcular_devidos,
    calcular_saldos,
)


def montar_despesa(pagador_id, valor, participantes_ids):
    return {
        "pagador_id": pagador_id,
        "valor": valor,
        "participantes": [{"id": pid} for pid in participantes_ids],
    }


def despesas_exemplo():
    # 0 pagou 3000 dividido entre 0, 1 e 2; 1 pagou 1000 dividido entre 0 e 1
    return [
        montar_despesa(0, 3000, [0, 1, 2]),
        montar_despesa(1, 1000, [0, 1]),
    ]


# ---------- calcular_pagos ----------

def test_calcular_pagos_uma_despesa():
    despesas = [montar_despesa(0, 3000, [0, 1, 2])]
    assert calcular_pagos(despesas) == {0: 3000}


def test_calcular_pagos_mesmo_pagador_soma():
    despesas = [
        montar_despesa(0, 3000, [0, 1]),
        montar_despesa(1, 1200, [0, 1]),
        montar_despesa(0, 500, [0, 1]),
    ]
    assert calcular_pagos(despesas) == {0: 3500, 1: 1200}


def test_calcular_pagos_pagadores_diferentes():
    assert calcular_pagos(despesas_exemplo()) == {0: 3000, 1: 1000}


def test_calcular_pagos_lista_vazia():
    assert calcular_pagos([]) == {}


def test_calcular_pagos_quem_nunca_pagou_nao_aparece():
    resultado = calcular_pagos(despesas_exemplo())
    assert 2 not in resultado


# ---------- calcular_devidos ----------

def test_calcular_devidos_exemplo():
    assert calcular_devidos(despesas_exemplo()) == {0: 1500, 1: 1500, 2: 1000}


def test_calcular_devidos_com_resto():
    despesas = [montar_despesa(0, 1000, [0, 1, 2])]
    assert calcular_devidos(despesas) == {0: 334, 1: 333, 2: 333}


def test_calcular_devidos_soma_bate_com_total_das_despesas():
    despesas = [
        montar_despesa(0, 1000, [0, 1, 2]),
        montar_despesa(1, 999, [0, 1, 2, 3, 4, 5, 6]),
        montar_despesa(2, 5, [1, 2, 3]),
    ]
    total_despesas = sum(d["valor"] for d in despesas)
    assert sum(calcular_devidos(despesas).values()) == total_despesas


def test_calcular_devidos_lista_vazia():
    assert calcular_devidos([]) == {}


# ---------- calcular_saldos ----------

def test_calcular_saldos_exemplo():
    assert calcular_saldos(despesas_exemplo()) == {0: 1500, 1: -500, 2: -1000}


def test_calcular_saldos_quem_so_deve_aparece_negativo():
    saldos = calcular_saldos(despesas_exemplo())
    assert saldos[2] == -1000


def test_calcular_saldos_pagador_que_nao_participa():
    # 0 paga a conta, mas só 1 e 2 dividem
    despesas = [montar_despesa(0, 1000, [1, 2])]
    assert calcular_saldos(despesas) == {0: 1000, 1: -500, 2: -500}


def test_calcular_saldos_quem_pagou_exatamente_sua_parte_fica_zerado():
    despesas = [
        montar_despesa(0, 1000, [0, 1]),
        montar_despesa(1, 1000, [0, 1]),
    ]
    assert calcular_saldos(despesas) == {0: 0, 1: 0}


def test_calcular_saldos_regra_de_ouro_soma_sempre_zero():
    despesas = [
        montar_despesa(0, 1000, [0, 1, 2]),
        montar_despesa(1, 999, [0, 1, 2, 3, 4, 5, 6]),
        montar_despesa(2, 5, [1, 2, 3]),
        montar_despesa(3, 1, [0, 1, 2, 3]),
    ]
    assert sum(calcular_saldos(despesas).values()) == 0


def test_calcular_saldos_lista_vazia():
    assert calcular_saldos([]) == {}