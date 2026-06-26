tamanho = [512, 1024, 1500, 1518, 256, 1500, 2048, 64, 1500, 1024]
buffer = []
maiores_1500 = []

for i in range(len(tamanho)):
    buffer.append(tamanho[i])
    if tamanho[i] > 1500:
        maiores_1500.append(buffer)

tamanho_total = sum(buffer)

print(f"Quantidade: {len(buffer)}")
print(f"Tamanho total: {tamanho_total}")
print(f"Quantidade de maiores de 1500: {len(maiores_1500)}")