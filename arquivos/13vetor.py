medicoes = [50.02, 49.97, 50.06, 49.94, 50.00, 50.08, 49.99, 50.01, 49.92, 50.04]
aprovadas = []
reprovadas = []
diametro = 50
tolerancia = 0.05

for i in range(len(medicoes)):
    if medicoes[i] > diametro + tolerancia or medicoes[i] < diametro - tolerancia:
        reprovadas.append(medicoes[i])
    else:
        aprovadas.append(medicoes[i])

taxa = len(aprovadas)/len(medicoes) * 100

print(f"Aprovadas: {aprovadas}")
print(f"Reprovadas: {reprovadas}")
print(f"Taxa de aprovação: {taxa}")