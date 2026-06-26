medidor1 = [48.2, 51.0, 49.7, 47.5, 52.3]
medidor2 = [50.1, 46.8, 53.0, 49.0, 55.2]

medidas = medidor1 + medidor2
medidas.sort()
media = sum(medidas)/len(medidas)
desviantes = []

for i in range(len(medidas)):
    if medidas[i] > media + ((15/100) *media):
        desviantes.append(medidas[i])



print(f"Medidas {medidas}")
print(f"Média {media}")
print(f"Desviantes de mais de 15% da média: ")
