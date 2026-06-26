!pip install folium

import math
import random
import folium
import ipywidgets as widgets
import pandas as pd
from IPython.display import display, clear_output

CENTRO_CIDADE = (-29.7833, -55.7919)

# =========================
# VARIÁVEIS GLOBAIS DASHBOARD
# =========================
ultima_rota = None
ultima_dist = None
ultimo_consumo = None

# =========================
# FUNÇÕES BASE
# =========================
def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) * 111


def gerar_pontos(n=10, raio_km=10):
    return [
        (
            CENTRO_CIDADE[0] + random.uniform(-raio_km/111, raio_km/111),
            CENTRO_CIDADE[1] + random.uniform(-raio_km/111, raio_km/111)
        )
        for _ in range(n)
    ]


def rota_original(pontos):
    origem = CENTRO_CIDADE
    dist = 0
    atual = origem

    for p in pontos:
        dist += distancia(atual, p)
        atual = p

    dist += distancia(atual, origem)
    return dist


def vizinho_mais_proximo(pontos):
    origem = CENTRO_CIDADE
    nao_visitados = pontos.copy()
    rota = []

    atual = origem
    dist = 0

    while nao_visitados:
        prox = min(nao_visitados, key=lambda p: distancia(atual, p))
        dist += distancia(atual, prox)

        rota.append(prox)
        atual = prox
        nao_visitados.remove(prox)

    dist += distancia(atual, origem)
    return rota, dist


def consumo(dist, consumo_km=0.35):
    return dist * consumo_km


def verifica_combustivel(dist, capacidade=80, consumo_km=0.35):
    c = consumo(dist, consumo_km)
    return c > capacidade, c

# =========================
# MAPA
# =========================
def plotar_mapa(pontos, rota):
    mapa = folium.Map(location=CENTRO_CIDADE, zoom_start=13)

    folium.Marker(
        CENTRO_CIDADE,
        tooltip="Depósito",
        icon=folium.Icon(color='red')
    ).add_to(mapa)

    for i, p in enumerate(pontos):
        folium.Marker(
            p,
            tooltip=f"Entrega {i+1}",
            icon=folium.Icon(color='blue')
        ).add_to(mapa)

    folium.PolyLine(
        [CENTRO_CIDADE] + rota + [CENTRO_CIDADE],
        color='green',
        weight=3
    ).add_to(mapa)

    return mapa

# =========================
# DASHBOARD
# =========================
saida_dashboard = widgets.Output()

def mostrar_dashboard():
    with saida_dashboard:
        clear_output()

        dados = []
        atual = CENTRO_CIDADE

        for i, p in enumerate(ultima_rota):
            d = distancia(atual, p)
            dados.append([i+1, round(d,2)])
            atual = p

        df = pd.DataFrame(dados, columns=["Entrega", "Distância do ponto anterior (km)"])

        print("📊 DASHBOARD\n")
        display(df)

        print("\n📈 RESUMO")
        print(f"Distância total: {ultima_dist:.2f} km")
        print(f"Consumo total: {ultimo_consumo:.2f} L")

# =========================
# INTERFACE
# =========================
num_pontos_slider = widgets.IntSlider(value=10, min=3, max=30, description='Nº Pontos')
raio_slider = widgets.IntSlider(value=10, min=2, max=30, description='Raio (km)')
consumo_slider = widgets.FloatSlider(value=0.35, min=0.2, max=0.6, step=0.01, description='Consumo')
tanque_slider = widgets.IntSlider(value=80, min=40, max=150, description='Tanque')

botao = widgets.Button(description="🚚 Simular", button_style='success')
botao_dashboard = widgets.Button(description="📊 Dashboard", button_style='info')

saida = widgets.Output()

# =========================
# SIMULAÇÃO
# =========================
def ao_clicar(b):
    global ultima_rota, ultima_dist, ultimo_consumo

    with saida:
        clear_output()

        pontos = gerar_pontos(num_pontos_slider.value, raio_slider.value)

        dist_original = rota_original(pontos)
        rota_opt, dist_opt = vizinho_mais_proximo(pontos)

        consumo_original = consumo(dist_original, consumo_slider.value)
        consumo_opt = consumo(dist_opt, consumo_slider.value)

        precisa, c = verifica_combustivel(dist_opt, tanque_slider.value, consumo_slider.value)

        ultima_rota = rota_opt
        ultima_dist = dist_opt
        ultimo_consumo = consumo_opt

        print("📍 RESULTADOS")
        print(f"Distância original: {dist_original:.2f} km")
        print(f"Distância otimizada: {dist_opt:.2f} km")
        print(f"Economia: {consumo_original - consumo_opt:.2f} L")

        if precisa:
            print("⚠️ Precisa reabastecer")
        else:
            print("✅ Não precisa reabastecer")

        display(plotar_mapa(pontos, rota_opt))

botao.on_click(ao_clicar)

# =========================
# DASHBOARD BOTÃO
# =========================
def abrir_dashboard(b):
    if ultima_rota is None:
        with saida_dashboard:
            clear_output()
            print("⚠️ Rode uma simulação primeiro!")
        return

    mostrar_dashboard()

botao_dashboard.on_click(abrir_dashboard)

# =========================
# UI FINAL
# =========================
ui = widgets.VBox([
    widgets.HTML("<h2>🚚 Otimização de Rotas</h2>"),
    num_pontos_slider,
    raio_slider,
    consumo_slider,
    tanque_slider,
    widgets.HBox([botao, botao_dashboard]),
    saida,
    saida_dashboard
])

display(ui)