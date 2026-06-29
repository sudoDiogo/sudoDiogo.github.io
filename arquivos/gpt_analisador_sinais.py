from statistics import mean, stdev


# =========================
# Conversão e validação
# =========================

def converter_para_dbm(valor):
    """
    Converte valores para dBm caso necessário.
    Atualmente assume que o valor já está em dBm.
    Adapte esta função para outros formatos (mW, W, etc.).
    """
    return valor


def validar_leitura(valor):
    """
    Verifica se o valor é numérico e está no intervalo válido.
    """
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return False

    return -120 <= valor <= 0


# =========================
# Processamento das leituras
# =========================

def processar_leituras(leituras):
    """
    Converte e filtra leituras inválidas.
    """
    validas = []
    descartadas = 0

    for leitura in leituras:
        try:
            valor = converter_para_dbm(float(leitura))

            if validar_leitura(valor):
                validas.append(valor)
            else:
                descartadas += 1

        except (ValueError, TypeError):
            descartadas += 1

    return validas, descartadas


# =========================
# Estatísticas
# =========================

def calcular_estatisticas(leituras_validas, descartadas):
    """
    Calcula estatísticas básicas.
    """
    if not leituras_validas:
        return {
            "media": None,
            "minimo": None,
            "maximo": None,
            "desvio_padrao": None,
            "validas": 0,
            "descartadas": descartadas
        }

    return {
        "media": mean(leituras_validas),
        "minimo": min(leituras_validas),
        "maximo": max(leituras_validas),
        "desvio_padrao": (
            stdev(leituras_validas)
            if len(leituras_validas) > 1
            else 0
        ),
        "validas": len(leituras_validas),
        "descartadas": descartadas
    }


# =========================
# Classificação
# =========================

def classificar_medicao(valor):
    """
    Classifica uma única medição.
    """
    if valor < -100:
        return "CRITICO"

    if valor < -85:
        return "ALERTA"

    return "NORMAL"


def classificar_todas(leituras):
    """
    Retorna lista de classificações.
    """
    return [(valor, classificar_medicao(valor))
            for valor in leituras]


# =========================
# Análise de limiar crítico
# =========================

def analisar_criticos(leituras):
    """
    Conta quantas medições ficaram abaixo do limiar crítico
    e encontra a maior sequência consecutiva.
    """
    total_criticos = 0
    maior_sequencia = 0
    sequencia_atual = 0

    for valor in leituras:

        if valor < -100:
            total_criticos += 1
            sequencia_atual += 1

            if sequencia_atual > maior_sequencia:
                maior_sequencia = sequencia_atual

        else:
            sequencia_atual = 0

    return total_criticos, maior_sequencia


# =========================
# Relatório
# =========================

def imprimir_relatorio(
    estatisticas,
    classificacoes,
    total_criticos,
    maior_sequencia
):
    """
    Exibe relatório final.
    """

    print("\n" + "=" * 50)
    print("RELATÓRIO DE POTÊNCIA RECEBIDA")
    print("=" * 50)

    print("\nESTATÍSTICAS")
    print(f"Média: {estatisticas['media']:.2f} dBm"
          if estatisticas['media'] is not None
          else "Média: N/A")

    print(f"Mínimo: {estatisticas['minimo']} dBm")
    print(f"Máximo: {estatisticas['maximo']} dBm")
    print(f"Desvio padrão: {estatisticas['desvio_padrao']:.2f} dB"
          if estatisticas['desvio_padrao'] is not None
          else "Desvio padrão: N/A")

    print(f"Válidas: {estatisticas['validas']}")
    print(f"Descartadas: {estatisticas['descartadas']}")

    print("\nCLASSIFICAÇÕES")

    for valor, classe in classificacoes:
        print(f"{valor:7.2f} dBm -> {classe}")

    print("\nANÁLISE DE CRÍTICOS")
    print(f"Quantidade crítica: {total_criticos}")
    print(f"Maior sequência crítica consecutiva: {maior_sequencia}")

    print("=" * 50)


# =========================
# Programa principal
# =========================

def main():

    leituras = []

    print("Digite valores de potência (dBm).")
    print("Digite 'fim' para encerrar.\n")

    while True:

        entrada = input("Leitura: ")

        if entrada.lower() == "fim":
            break

        leituras.append(entrada)

    leituras_validas, descartadas = processar_leituras(leituras)

    estatisticas = calcular_estatisticas(
        leituras_validas,
        descartadas
    )

    classificacoes = classificar_todas(
        leituras_validas
    )

    total_criticos, maior_sequencia = analisar_criticos(
        leituras_validas
    )

    imprimir_relatorio(
        estatisticas,
        classificacoes,
        total_criticos,
        maior_sequencia
    )


if __name__ == "__main__":
    main()