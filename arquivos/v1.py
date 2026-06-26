import math
import random
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output


def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def rota_original(pontos):
    origem = (0, 0)
    distancia_total = 0
    
    atual = origem
    
    for p in pontos:
        distancia_total += distancia(atual, p)
        atual = p
    
    # volta à origem
    distancia_total += distancia(atual, origem)
    
    return distancia_total

def vizinho_mais_proximo(pontos):
    origem = (0, 0)
    nao_visitados = pontos.copy()
    rota = []
    
    atual = origem
    distancia_total = 0
    
    while nao_visitados:
        proximo = min(nao_visitados, key=lambda p: distancia(atual, p))
        distancia_total += distancia(atual, proximo)
        
        rota.append(proximo)
        atual = proximo
        nao_visitados.remove(proximo)
    
    # volta à origem
    distancia_total += distancia(atual, origem)
    
    return rota, distancia_total

def consumo(distancia_total, consumo_por_km=0.35):
    return distancia_total * consumo_por_km

def verifica_combustivel(distancia_total, capacidade=80, consumo_por_km=0.35):
    consumo_total = consumo(distancia_total, consumo_por_km)
    
    if consumo_total <= capacidade:
        return False, consumo_total
    else:
        return True, consumo_total

def plotar_rotas(pontos, rota_otimizada):
    origem = (0, 0)
    
    plt.figure(figsize=(10, 5))

    # --- Rota original ---
    plt.subplot(1, 2, 1)
    x = [origem[0]] + [p[0] for p in pontos] + [origem[0]]
    y = [origem[1]] + [p[1] for p in pontos] + [origem[1]]
    
    plt.plot(x, y, marker='o')
    plt.title("Rota Original")
    plt.grid()

    # --- Rota otimizada ---
    plt.subplot(1, 2, 2)
    x_opt = [origem[0]] + [p[0] for p in rota_otimizada] + [origem[0]]
    y_opt = [origem[1]] + [p[1] for p in rota_otimizada] + [origem[1]]
    
    plt.plot(x_opt, y_opt, marker='o', color='green')
    plt.title("Rota Otimizada (Vizinho Mais Próximo)")
    plt.grid()

    plt.show()

# Gerar pontos aleatórios (ou substitua pelos seus dados)
def gerar_pontos(n=10, limite=50):
    return [(random.randint(0, limite), random.randint(0, limite)) for _ in range(n)]

num_pontos_slider = widgets.IntSlider(value=10, min=3, max=30, step=1, description='Nº Pontos:')
limite_slider = widgets.IntSlider(value=50, min=10, max=200, step=5, description='Área (km):')
consumo_slider = widgets.FloatSlider(value=0.35, min=0.2, max=0.6, step=0.01, description='Consumo:')
tanque_slider = widgets.IntSlider(value=80, min=40, max=150, step=5, description='Tanque:')

botao = widgets.Button(description="🚚 Executar", button_style='success')
saida = widgets.Output()

def ao_clicar(b):
    with saida:
        clear_output()
        
        pontos = gerar_pontos(num_pontos_slider.value, limite_slider.value)

        dist_original = rota_original(pontos)
        consumo_original = consumo(dist_original, consumo_slider.value)

        rota_opt, dist_opt = vizinho_mais_proximo(pontos)
        consumo_opt = consumo(dist_opt, consumo_slider.value)

        precisa, consumo_total = verifica_combustivel(
            dist_opt, tanque_slider.value, consumo_slider.value
        )

        print("Pontos:", pontos)

        print("\n--- RESULTADOS ---")
        print(f"Distância original: {dist_original:.2f} km")
        print(f"Distância otimizada: {dist_opt:.2f} km")

        print(f"\nConsumo original: {consumo_original:.2f} L")
        print(f"Consumo otimizado: {consumo_opt:.2f} L")

        if precisa:
            print("⚠️ Precisa reabastecer")
        else:
            print("✅ Não precisa reabastecer")

        plotar_rotas(pontos, rota_opt)
        print(f"\n💰 Economia: {consumo_original - consumo_opt:.2f} L")

botao.on_click(ao_clicar)


# Execução completa
def executar_simulacao(pontos):
    print("Pontos de entrega:")
    print(pontos)
    
    # Rota original
    dist_original = rota_original(pontos)
    consumo_original = consumo(dist_original)
    
    # Rota otimizada
    rota_opt, dist_opt = vizinho_mais_proximo(pontos)
    consumo_opt = consumo(dist_opt)
    
    # Combustível
    precisa_reabastecer, consumo_total = verifica_combustivel(dist_opt)
    
    print("\n--- RESULTADOS ---")
    print(f"Distância original: {dist_original:.2f} km")
    print(f"Consumo original: {consumo_original:.2f} L")
    
    print(f"\nDistância otimizada: {dist_opt:.2f} km")
    print(f"Consumo otimizado: {consumo_opt:.2f} L")
    
    print(f"\nEconomia de combustível: {consumo_original - consumo_opt:.2f} L")
    
    if precisa_reabastecer:
        print("⚠️ O caminhão PRECISA reabastecer!")
    else:
        print("✅ O caminhão NÃO precisa reabastecer.")
    
    # Plot
    plotar_rotas(pontos, rota_opt)

display(num_pontos_slider, limite_slider, consumo_slider, tanque_slider, botao, saida)