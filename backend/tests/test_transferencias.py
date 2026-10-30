import pytest

from backend.app.services.transferencias import (
    separar_credores_devedores,
    calcular_transferencias,
)


def aplicar_transferencias(saldos, transferencias):
    """Simula o pagamento das transferências e devolve os saldos finais."""
    finais = dict(saldos)
    for t in transferencias:
        finais[t["devedor"]] += t["valor"]
        finais[t["credor"]] -= t["valor"]
    return finais


# ---------- separar_credores_devedores ----------

def test_separar_saldo_positivo_vira_credor():
    credores, devedores = separar_credores_devedores({0: 1500, 1: -1500})
    assert credores == [{"participante_id": 0, "valor": 1500}]


def test_separar_saldo_negativo_vira_devedor_com_valor_positivo():
    credores, devedores = separar_credores_devedores({0: 1500, 1: -1500})
    assert devedores == [{"participante_id": 1, "valor": 1500}]


def test_separar_saldo_zero_nao_entra_em_nenhuma_lista():
    credores, devedores = separar_credores_devedores({0: 0, 1: 500, 2: -500})
    ids = [c["participante_id"] for c in credores] + [d["participante_id"] for d in devedores]
    assert 0 not in ids


def test_separar_todos_zerados():
    assert separar_credores_devedores({0: 0, 1: 0}) == ([], [])


# ---------- calcular_transferencias ----------

def test_transferencias_um_credor_dois_devedores():
    transferencias = calcular_transferencias({0: 2000, 1: -1000, 2: -1000})
    assert len(transferencias) == 2
    assert all(t["credor"] == 0 for t in transferencias)
    assert sorted(t["devedor"] for t in transferencias) == [1, 2]
    assert all(t["valor"] == 1000 for t in transferencias)


def test_transferencias_exemplo_do_saldos():
    saldos = {0: 1500, 1: -500, 2: -1000}
    transferencias = calcular_transferencias(saldos)
    assert {"devedor": 2, "credor": 0, "valor": 1000} in transferencias
    assert {"devedor": 1, "credor": 0, "valor": 500} in transferencias
    assert len(transferencias) == 2


def test_transferencias_um_para_um():
    transferencias = calcular_transferencias({0: 700, 1: -700})
    assert transferencias == [{"devedor": 1, "credor": 0, "valor": 700}]


def test_transferencias_dois_credores_dois_devedores():
    saldos = {0: 700, 1: 300, 2: -600, 3: -400}
    transferencias = calcular_transferencias(saldos)
    # no máximo (credores + devedores - 1) transferências
    assert len(transferencias) <= 3


def test_transferencias_todos_zerados_retorna_lista_vazia():
    assert calcular_transferencias({0: 0, 1: 0}) == []


def test_transferencias_dicionario_vazio():
    assert calcular_transferencias({}) == []


def test_transferencias_soma_diferente_de_zero_levanta_erro():
    with pytest.raises(ValueError):
        calcular_transferencias({0: 100, 1: -50})


def test_transferencias_valores_sempre_positivos_e_inteiros():
    transferencias = calcular_transferencias({0: 700, 1: 300, 2: -600, 3: -400})
    for t in transferencias:
        assert isinstance(t["valor"], int)
        assert t["valor"] > 0


def test_transferencias_ninguem_paga_a_si_mesmo():
    transferencias = calcular_transferencias({0: 700, 1: 300, 2: -600, 3: -400})
    assert all(t["devedor"] != t["credor"] for t in transferencias)


def test_transferencias_nao_altera_o_dicionario_de_entrada():
    saldos = {0: 700, 1: 300, 2: -600, 3: -400}
    copia = dict(saldos)
    calcular_transferencias(saldos)
    assert saldos == copia


@pytest.mark.parametrize("saldos", [
    {0: 1500, 1: -500, 2: -1000},
    {0: 2000, 1: -1000, 2: -1000},
    {0: 700, 1: 300, 2: -600, 3: -400},
    {0: 1, 1: 1, 2: 1, 3: -3},
    {0: 857, 1: -143, 2: -143, 3: -143, 4: -143, 5: -143, 6: -142, 7: 0},
])
def test_transferencias_teste_de_ouro_todos_os_saldos_zeram(saldos):
    transferencias = calcular_transferencias(saldos)
    finais = aplicar_transferencias(saldos, transferencias)
    assert all(valor == 0 for valor in finais.values())