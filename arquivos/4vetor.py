vibracao = [0.12, 0.34, -999.0, 0.28, 0.91, -999.0, 1.42, 0.67]

while -999.0 in vibracao:
    vibracao.remove(-999.0)

print(vibracao)
print(f"Amostras: {len(vibracao)}")