import pytest

from backend.app.services.divisao import (
    reais_para_centavos,
    centavos_para_reais,
    dividir_igualmente,
)


# ---------- reais_para_centavos ----------

def test_reais_para_centavos_valor_simples():
    assert reais_para_centavos("10.50") == 1050


def test_reais_para_centavos_centavos_com_zero_a_esquerda():
    assert reais_para_centavos("0.05") == 5


def test_reais_para_centavos_evita_erro_de_float():
    # 19.99 * 100 em float dá 1998.9999999999998
    assert reais_para_centavos("19.99") == 1999
    assert reais_para_centavos(19.99) == 1999


def test_reais_para_centavos_arredonda_meio_centavo_para_cima():
    assert reais_para_centavos(2.675) == 268


def test_reais_para_centavos_retorna_int():
    assert isinstance(reais_para_centavos("19.99"), int)


def test_reais_para_centavos_zero():
    assert reais_para_centavos("0") == 0


# ---------- centavos_para_reais ----------

def test_centavos_para_reais_valor_simples():
    assert centavos_para_reais(1050) == "10.50"


def test_centavos_para_reais_menos_de_um_real():
    assert centavos_para_reais(5) == "0.05"


def test_centavos_para_reais_reais_exatos():
    assert centavos_para_reais(100) == "1.00"


def test_centavos_para_reais_zero_nao_tem_sinal():
    assert centavos_para_reais(0) == "0.00"


def test_centavos_para_reais_negativo():
    assert centavos_para_reais(-1050) == "-10.50"
    assert centavos_para_reais(-5) == "-0.05"


def test_ida_e_volta_reais_centavos():
    for valor in ["0.01", "0.99", "1.00", "19.99", "1234.56"]:
        assert centavos_para_reais(reais_para_centavos(valor)) == valor


# ---------- dividir_igualmente ----------

def montar_participantes(qtd):
    return [{"id": i} for i in range(qtd)]


def valores(resultado):
    return [parte["valor"] for parte in resultado]


def test_dividir_igualmente_com_resto():
    resultado = dividir_igualmente(1000, montar_participantes(3))
    assert valores(resultado) == [334, 333, 333]


def test_dividir_igualmente_resto_maior():
    resultado = dividir_igualmente(5, montar_participantes(3))
    assert valores(resultado) == [2, 2, 1]


def test_dividir_igualmente_sem_resto():
    resultado = dividir_igualmente(900, montar_participantes(3))
    assert valores(resultado) == [300, 300, 300]


def test_dividir_igualmente_um_centavo_entre_quatro():
    resultado = dividir_igualmente(1, montar_participantes(4))
    assert valores(resultado) == [1, 0, 0, 0]


def test_dividir_igualmente_total_zero():
    resultado = dividir_igualmente(0, montar_participantes(2))
    assert valores(resultado) == [0, 0]


def test_dividir_igualmente_um_participante_paga_tudo():
    resultado = dividir_igualmente(1234, montar_participantes(1))
    assert valores(resultado) == [1234]


def test_dividir_igualmente_regra_de_ouro_soma_bate_com_total():
    for total, qtd in [(1000, 3), (5, 3), (1, 4), (0, 2), (999, 7), (10000, 6)]:
        resultado = dividir_igualmente(total, montar_participantes(qtd))
        assert sum(valores(resultado)) == total


def test_dividir_igualmente_diferenca_maxima_de_um_centavo():
    resultado = dividir_igualmente(999, montar_participantes(7))
    assert max(valores(resultado)) - min(valores(resultado)) <= 1


def test_dividir_igualmente_devolve_participante_id():
    resultado = dividir_igualmente(1000, [{"id": 10}, {"id": 20}])
    assert [parte["participante_id"] for parte in resultado] == [10, 20]


def test_dividir_igualmente_nao_altera_lista_original():
    participantes = montar_participantes(3)
    dividir_igualmente(1000, participantes)
    assert participantes == [{"id": 0}, {"id": 1}, {"id": 2}]


def test_dividir_igualmente_lista_vazia_levanta_erro():
    with pytest.raises(ValueError):
        dividir_igualmente(1000, [])


def test_dividir_igualmente_total_negativo_levanta_erro():
    with pytest.raises(ValueError):
        dividir_igualmente(-1000, montar_participantes(3))