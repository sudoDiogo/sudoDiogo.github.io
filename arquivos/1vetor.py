temperaturas = []
leituras = [820, 835, 848, 791, 812, 856]

for i in range(len(leituras)):
  temperaturas.append(leituras[i])

max = max(leituras)
min = min(leituras)

print(f"A lista completa e {temperaturas} e os maximos e minimos foram {max} e {min}")