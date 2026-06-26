amostras = [11.9, 12.1, 12.0, 13.5, 11.7, 12.3, 10.5, 12.0]

leituras = []
perigos = []

for i in range(len(amostras)):
    leituras.append(amostras[i])
    if amostras[i] >= 13.2 or amostras[i] <= 10.8:
        perigos.append(amostras[i])

media = (sum(amostras)/len(amostras))

print(f"A media e {media}, com leituras perigosas: ({perigos} e leituras {leituras})")