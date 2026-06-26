antena_norte = [ -85, -90, -105, -78, -92, -110, -88]
antena_sul = [-95, -88, -102, -79, -85,  -91, -97]
antena_leste = [-80, -75, -108, -93, -86, -103, -82]
limiar = -100

logs = []
logs.extend(antena_sul)
logs.extend(antena_norte)
logs.extend(antena_leste)

cobertura = 0
pior = logs[1]
for i in range(len(logs)):
    if logs[i] >= -100:
        cobertura += 1
    if logs[i] < pior:
        pior = logs[i]
    
taxa_cobertura = ((cobertura/len(logs))*100)


media = sum(logs)/len(logs)

print(logs)
print(f"Amostras: {len(logs)}")
print(f"Em cobertura: {cobertura}")
print(f"Taxa de cobertura: {taxa_cobertura}")
print(f"Pior sinal: {pior}")
print(f"Média: {media}")