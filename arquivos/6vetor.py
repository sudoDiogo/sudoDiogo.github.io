canais = [850, 900, 950, 1800, 2100, 2600]
ativados = []
interferencia = {850:-65, 900:-80,950:-72, 1800:-55,2100:-90,2600:-68}

for canal in canais:
    if interferencia[canal] > - 70:
        print(f"Desativado o {canal}")
    else:
        ativados.append(canal)

print(ativados)
