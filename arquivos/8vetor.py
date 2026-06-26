nominal = [47, 100, 220, 33, 68]
falha = []

r_antes = sum(nominal)

for i in range(0, len(nominal)):
    falha.append(nominal[i])
    if falha[i] == 100:
        falha[i] = 0

r_depois = sum(falha)
delta = r_antes - r_depois

print(f"Nominal: {nominal}")
print(f"Falha: {falha}")

print(f"{r_antes} e {r_depois}, com diferença de {delta}")