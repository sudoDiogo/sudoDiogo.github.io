import random


def gerar_medicoes(quantidade):
    """
    Gera medições realistas de RSSI em dBm.
    Faixa típica:
    -110 dBm (muito ruim)
    -40 dBm (excelente)
    """

    return [
        round(random.uniform(-110, -40), 2)
        for _ in range(quantidade)
    ]


def main():

    quantidade = int(
        input("Quantas medições deseja gerar? ")
    )

    medicoes = gerar_medicoes(quantidade)

    print("\nMedições geradas:")

    for valor in medicoes:
        print(valor)


if __name__ == "__main__":
    main()