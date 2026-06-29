"""
Gerador de Leituras Aleatórias de Potência em dBm
Gera X valores simulando medições reais de sinal recebido.

Distribuição realista:
  - 60% valores normais   (-85 a  0 dBm)
  - 25% valores de alerta (-100 a -85 dBm)
  - 15% valores críticos  (-120 a -100 dBm)
"""

import random


DBM_MIN = -120
DBM_MAX = 0

FAIXAS = [
    (0.60, -85,  0),    # normal
    (0.25, -100, -85),  # alerta
    (0.15, -120, -100), # crítico
]


def gerar_valor_dbm() -> float:
    """Gera um único valor aleatório de dBm com distribuição realista."""
    sorteio = random.random()
    acumulado = 0.0
    for peso, minimo, maximo in FAIXAS:
        acumulado += peso
        if sorteio < acumulado:
            return round(random.uniform(minimo, maximo), 2)
    return round(random.uniform(DBM_MIN, DBM_MAX), 2)


def gerar_leituras(quantidade: int) -> list[float]:
    """Gera uma lista com `quantidade` valores de dBm."""
    return [gerar_valor_dbm() for _ in range(quantidade)]


def main() -> None:
    print("=== Gerador de Leituras de Potência (dBm) ===\n")

    while True:
        entrada = input("Quantos valores deseja gerar? ").strip()
        try:
            quantidade = int(entrada)
            if quantidade <= 0:
                print("  ⚠  Digite um número inteiro positivo.\n")
                continue
            break
        except ValueError:
            print("  ⚠  Entrada inválida. Digite um número inteiro.\n")

    leituras = gerar_leituras(quantidade)

    print(f"\n{quantidade} valor(es) gerado(s):\n")
    for i, v in enumerate(leituras, start=1):
        print(f"  {v:>8.2f}")

    # Salva em arquivo de texto para uso externo
    nome_arquivo = "leituras_geradas.txt"
    with open(nome_arquivo, "w") as f:
        for v in leituras:
            f.write(f"{v}\n")

    print(f"\n✅  Valores salvos em '{nome_arquivo}'")
    print("     (Use esse arquivo como entrada para o analisador_sinal.py)\n")


if __name__ == "__main__":
    main()