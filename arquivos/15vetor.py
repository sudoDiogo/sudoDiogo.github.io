import math

canal_I = [0.82, 0.79, 0.85, 5.20, 0.81, 0.78, 0.83]
canal_Q = [0.41, 0.39, 0.43, 0.40, -4.80, 0.42, 0.38]
canais = []
removidos = []
limpo = []

canais.extend(canal_I)
canais.extend(canal_Q)

backup = canais.copy()

media = sum(canais)/len(canais)

antes_raiz = 0
for i in range(len(canais)):
    antes_raiz = antes_raiz + (canais[i]- media)**2
antes_raiz = antes_raiz/(len(canais)-1)
desvio = math.sqrt(antes_raiz)

# pra remover troque de 2 desvios ao invés de 1 pq 3 não eliminava esses maiores
for i in range(len(canais)):
    if canais[i] > (media + 2*(desvio))  or  canais[i] < (media - 2*(desvio)):
        removidos.append(canais[i])
    else:
        limpo.append(canais[i])

print(f"Sinal bruto: {backup}")
print(f"Sinais removidos: {removidos}")
print(f"Sinal limpo: {limpo}")
