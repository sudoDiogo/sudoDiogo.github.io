"""
Analisador de Potência de Sinal em dBm
Analisa leituras de potência recebida, calcula estatísticas,
classifica limiares e identifica sequências críticas.
"""

import math


# ─────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────
DBM_MIN = -120
DBM_MAX = 0
LIMIAR_ALERTA = -85
LIMIAR_CRITICO = -100


# ─────────────────────────────────────────────
# 1. Validação e conversão de entradas
# ─────────────────────────────────────────────

def tentar_converter_para_float(valor) -> float | None:
    """Tenta converter um valor para float. Retorna None se não for possível."""
    try:
        return float(valor)
    except (ValueError, TypeError):
        return None


def converter_para_dbm(valor: float) -> float:
    """
    Converte para dBm caso o valor esteja em Watts (positivo e > 1e-20).
    Valores já negativos ou zero são assumidos como já sendo dBm.
    """
    if valor > 0:
        # Assume que é potência em Watts — converte para dBm
        return 10 * math.log10(valor * 1000)
    return valor  # já está em dBm


def validar_dbm(valor: float) -> bool:
    """Verifica se o valor (após conversão) está no intervalo válido de dBm."""
    return DBM_MIN <= valor <= DBM_MAX


def processar_leituras(leituras_brutas: list) -> tuple[list[float], list]:
    """
    Processa uma lista de leituras brutas:
      - Tenta conversão numérica
      - Converte para dBm se necessário
      - Valida o intervalo [-120, 0]

    Retorna:
      validas   — lista de floats em dBm aceitos
      descartados — lista dos valores originais rejeitados
    """
    validas: list[float] = []
    descartados: list = []

    for entrada in leituras_brutas:
        valor = tentar_converter_para_float(entrada)

        if valor is None:
            descartados.append(entrada)
            continue

        valor_dbm = converter_para_dbm(valor)

        if validar_dbm(valor_dbm):
            validas.append(valor_dbm)
        else:
            descartados.append(entrada)

    return validas, descartados


# ─────────────────────────────────────────────
# 2. Estatísticas
# ─────────────────────────────────────────────

def calcular_estatisticas(validas: list[float], descartados: list) -> dict:
    """
    Calcula: média, mínimo, máximo, desvio padrão,
    quantidade de amostras válidas e descartadas.
    """
    n = len(validas)

    if n == 0:
        return {
            "media": None,
            "minimo": None,
            "maximo": None,
            "desvio_padrao": None,
            "qtd_validas": 0,
            "qtd_descartadas": len(descartados),
        }

    media = sum(validas) / n
    minimo = min(validas)
    maximo = max(validas)
    variancia = sum((x - media) ** 2 for x in validas) / n
    desvio_padrao = math.sqrt(variancia)

    return {
        "media": media,
        "minimo": minimo,
        "maximo": maximo,
        "desvio_padrao": desvio_padrao,
        "qtd_validas": n,
        "qtd_descartadas": len(descartados),
    }


# ─────────────────────────────────────────────
# 3. Classificação por limiar
# ─────────────────────────────────────────────

def classificar_medicao(valor_dbm: float) -> str:
    """Classifica uma medição individual conforme os limiares definidos."""
    if valor_dbm < LIMIAR_CRITICO:
        return "crítico"
    if valor_dbm < LIMIAR_ALERTA:
        return "alerta"
    return "normal"


def classificar_todas(validas: list[float]) -> list[dict]:
    """
    Retorna uma lista de dicionários com valor e classificação
    para cada medição válida.
    """
    return [
        {"valor": v, "classificacao": classificar_medicao(v)}
        for v in validas
    ]


# ─────────────────────────────────────────────
# 4. Análise de sequências críticas
# ─────────────────────────────────────────────

def analisar_criticos(classificacoes: list[dict]) -> dict:
    """
    Contabiliza medições críticas e identifica
    a maior sequência consecutiva de críticos.
    """
    total_criticos = 0
    maior_sequencia = 0
    sequencia_atual = 0

    for item in classificacoes:
        if item["classificacao"] == "crítico":
            total_criticos += 1
            sequencia_atual += 1
            maior_sequencia = max(maior_sequencia, sequencia_atual)
        else:
            sequencia_atual = 0

    return {
        "total_criticos": total_criticos,
        "maior_sequencia_consecutiva": maior_sequencia,
    }


# ─────────────────────────────────────────────
# 5. Relatório
# ─────────────────────────────────────────────

def _linha(char: str = "─", largura: int = 55) -> str:
    return char * largura


def imprimir_relatorio(
    estatisticas: dict,
    classificacoes: list[dict],
    analise_criticos: dict,
) -> None:
    """Imprime o relatório completo de análise de sinal."""

    sep = _linha()
    sep2 = _linha("═")

    print(f"\n{sep2}")
    print("       RELATÓRIO DE ANÁLISE DE SINAL (dBm)")
    print(sep2)

    # — Amostras —
    print("\n📊  AMOSTRAS")
    print(sep)
    print(f"  Válidas   : {estatisticas['qtd_validas']}")
    print(f"  Descartadas: {estatisticas['qtd_descartadas']}")

    # — Estatísticas —
    print(f"\n📈  ESTATÍSTICAS")
    print(sep)
    if estatisticas["media"] is None:
        print("  Sem amostras válidas para calcular estatísticas.")
    else:
        print(f"  Média        : {estatisticas['media']:.2f} dBm")
        print(f"  Mínimo       : {estatisticas['minimo']:.2f} dBm")
        print(f"  Máximo       : {estatisticas['maximo']:.2f} dBm")
        print(f"  Desvio Padrão: {estatisticas['desvio_padrao']:.2f} dBm")

    # — Classificações —
    print(f"\n🔍  CLASSIFICAÇÃO DAS MEDIÇÕES")
    print(sep)
    contagem = {"normal": 0, "alerta": 0, "crítico": 0}
    for item in classificacoes:
        contagem[item["classificacao"]] += 1

    total = len(classificacoes)
    for cat, qtd in contagem.items():
        pct = (qtd / total * 100) if total > 0 else 0
        icone = {"normal": "✅", "alerta": "⚠️ ", "crítico": "🔴"}[cat]
        print(f"  {icone} {cat.capitalize():10s}: {qtd:4d}  ({pct:5.1f}%)")

    print(f"\n  Limiares de referência:")
    print(f"    Alerta  → abaixo de {LIMIAR_ALERTA} dBm")
    print(f"    Crítico → abaixo de {LIMIAR_CRITICO} dBm")

    # — Análise de críticos —
    print(f"\n🚨  ANÁLISE DE EVENTOS CRÍTICOS")
    print(sep)
    print(f"  Total de medições críticas       : {analise_criticos['total_criticos']}")
    print(f"  Maior sequência consecutiva crítica: {analise_criticos['maior_sequencia_consecutiva']}")

    # — Lista detalhada —
    print(f"\n📋  DETALHAMENTO (primeiras 20 amostras)")
    print(sep)
    print(f"  {'#':>4}  {'Valor (dBm)':>12}  {'Classificação'}")
    print(f"  {'─'*4}  {'─'*12}  {'─'*14}")
    for i, item in enumerate(classificacoes[:20], start=1):
        icone = {"normal": "✅", "alerta": "⚠️", "crítico": "🔴"}[item["classificacao"]]
        print(f"  {i:>4}  {item['valor']:>11.2f}  {icone} {item['classificacao']}")
    if len(classificacoes) > 20:
        print(f"  ... ({len(classificacoes) - 20} amostras omitidas)")

    print(f"\n{sep2}\n")


# ─────────────────────────────────────────────
# 6. Pipeline principal
# ─────────────────────────────────────────────

def executar_analise(leituras_brutas: list) -> None:
    """
    Orquestra todo o pipeline: validação → estatísticas
    → classificação → análise crítica → relatório.
    """
    validas, descartados = processar_leituras(leituras_brutas)
    estatisticas = calcular_estatisticas(validas, descartados)
    classificacoes = classificar_todas(validas)
    analise_criticos = analisar_criticos(classificacoes)
    imprimir_relatorio(estatisticas, classificacoes, analise_criticos)


# ─────────────────────────────────────────────
# 7. Entrada interativa
# ─────────────────────────────────────────────

def coletar_leituras_interativo() -> list:
    """
    Coleta leituras do usuário via terminal.
    Digite 'fim' para encerrar a entrada.
    """
    print("\n=== Entrada de Leituras de Potência ===")
    print("Digite os valores em dBm (ou Watts).")
    print("Digite 'fim' para encerrar.\n")

    leituras = []
    while True:
        entrada = input("Leitura: ").strip()
        if entrada.lower() == "fim":
            break
        leituras.append(entrada)

    return leituras


# ─────────────────────────────────────────────
# Execução
# ─────────────────────────────────────────────

if __name__ == "__main__":
    leituras = coletar_leituras_interativo()
    executar_analise(leituras)