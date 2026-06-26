cenario_atual = [15.0, 22.5, 8.0, 40.0, 12.5, 30.0]
novas_cargas = [55.0, 18.0, 75.0]
maior_futuro = 0
maior_atual = 0

cenario_atual_backup = cenario_atual.copy()
cenario_futuro = cenario_atual + novas_cargas

soma_atual = sum(cenario_atual_backup)
soma_futura = sum(cenario_futuro)

media_atual = sum(cenario_atual_backup)/len(cenario_atual_backup)
media_futuro = sum(cenario_futuro)/len(cenario_futuro)

for i in range(len(cenario_atual_backup)):
    if cenario_atual_backup[i] > maior_atual:
        maior_atual = cenario_atual_backup[i]

for i in range(len(cenario_futuro)):
    if cenario_futuro[i] > maior_futuro:
        maior_futuro = cenario_futuro[i]

print(f"Cenario atual - Soma: {soma_atual} Media: {media_atual} Maior: {maior_atual}")
print(f"Cenario futuro - Soma: {soma_futura} Media {media_futuro} Maior: {maior_futuro}")