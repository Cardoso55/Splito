from decimal import Decimal, ROUND_HALF_UP

def reais_para_centavos(valor: float | str) -> int:
    return int(Decimal(str(valor)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) * 100)

def centavos_para_reais(valor: int) -> str:
    negativo = '-' if valor < 0 else ''
    valor = abs(valor)
    valor_reais = valor // 100
    valor_centavos = valor % 100
    return f"{negativo}{valor_reais}.{valor_centavos:02d}"

def dividir_igualmente(total_centavos: int, participantes: list[dict]) -> list[dict]:
    total_participantes = len(participantes)
    if total_participantes == 0:
        raise ValueError("A lista de participantes não pode estar vazia.")

    if total_centavos < 0:
        raise ValueError("O valor da despesa não pode ser negativo.")
    
    despesas_divididas = []

    valor_por_participante, resto = divmod(total_centavos, total_participantes)

    for i, participante in enumerate(participantes):
        despesas_divididas.append({
            "participante": participante["participante"],
            "valor": valor_por_participante + (1 if i < resto else 0)
        })
    return despesas_divididas