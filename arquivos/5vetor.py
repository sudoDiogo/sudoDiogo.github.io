cargas = [15.0, 22.5, 8.0, 40.0, 12.5, 30.0]
removida = []
antes = sum(cargas)

removida.append(8.0)
removida.append(40.0)
cargas.remove(8.0)
cargas.remove(40.0)

depois = sum(cargas)
total_removida = sum(removida)

print(f"Antes: {antes} kW")
print(f"Depois: {depois} kW")
print(f"Total emovida: {total_removida}")