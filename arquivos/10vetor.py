sensorA =[3.2, 3.4, 3.1, 3.5]
sensorB =[4.1, 4.0, 4.3, 3.9]
sensorC =[2.8, 2.9, 3.0, 2.7]
total = []

total.extend(sensorA)
total.extend(sensorB)
total.extend(sensorC)

media = (sum(total))/len(total)

max = total[0]
min = total[0]
for i in range(0,len(total)):
    if total[i] >= max:
        max = total[i]

for i in range(0,len(total)):
    if total[i] <= min:
        min = total[i]

print(f"Total de leituras: {len(total)}")
print(f"Média: {media}")
print(f"Máximo: {max}")
print(f"Mínimo: {min}")