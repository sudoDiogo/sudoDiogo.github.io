params_originais = [120.0, 150.0, 95.0, 200.0, 110.0]

backup = params_originais.copy()

params_originais[0] = 130

print(f"Original alterada: {params_originais}")
print(f"Backup: {backup}")

