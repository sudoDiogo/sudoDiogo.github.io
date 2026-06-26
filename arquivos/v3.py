!pip install folium

import math
import random
import folium
import ipywidgets as widgets
import pandas as pd
from IPython.display import display, clear_output

# =========================
# BASE: ATENAS (IFOOD)
# =========================
CENTRO_CIDADE = (37.9838, 23.7275)  # Athens, Greece

# =========================
# VARIÁVEIS GLOBAIS
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
    # restaurantes / clientes de comida
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
# MAPA (IFOOD STYLE)
# =========================
def plotar_mapa(pontos, rota):
    mapa = folium.Map(location=CENTRO_CIDADE, zoom_start=13)

    # Central iFood (restaurante principal / hub)
    folium.Marker(
        CENTRO_CIDADE,
        tooltip="🏪 Centro de Distribuição iFood",
        icon=folium.Icon(color='red')
    ).add_to(mapa)

    # Restaurantes / pedidos
    for i, p in enumerate(pontos):
        folium.Marker(
            p,
            tooltip=f"🍔 Pedido {i+1}",
            icon=folium.Icon(color='blue')
        ).add_to(mapa)

    # Rota do entregador
    folium.PolyLine(
        [CENTRO_CIDADE] + rota + [CENTRO_CIDADE],
        color='green',
        weight=3,
        tooltip="🚴 Rota do Entregador"
    ).add_to(mapa)

    return mapa

# =========================
# DASHBOARD (PEDIDOS)
# =========================
saida_dashboard = widgets.Output()

def mostrar_dashboard():
    with saida_dashboard:
        clear_output()

        dados = []
        atual = CENTRO_CIDADE

        for i, p in enumerate(ultima_rota):
            d = distancia(atual, p)
            dados.append([f"Pedido {i+1}", round(d,2)])
            atual = p

        df = pd.DataFrame(dados, columns=[
            "Pedido", "Distância do ponto anterior (km)"
        ])

        print("📊 DASHBOARD - PEDIDOS iFOOD\n")
        display(df)

        print("\n📈 RESUMO DA ENTREGA")
        print(f"Distância total: {ultima_dist:.2f} km")
        print(f"Consumo do entregador: {ultimo_consumo:.2f} L")
        print(f"Tempo estimado (proxy): {ultima_dist * 2:.0f} min")

# =========================
# GERENCIAMENTO DE ENTREGADORES
# =========================
saida_entregadores = widgets.Output()

def gerenciamento_entregadores(b):
    with saida_entregadores:
        clear_output()

        entregadores = [
            {"Nome": "Alex", "Status": "Disponível", "Pedidos": random.randint(0,5)},
            {"Nome": "Maria", "Status": "Em entrega", "Pedidos": random.randint(1,3)},
            {"Nome": "João", "Status": "Disponível", "Pedidos": random.randint(0,4)},
            {"Nome": "Elena", "Status": "Offline", "Pedidos": 0},
        ]

        df = pd.DataFrame(entregadores)

        print("🚴 GERENCIAMENTO DE ENTREGADORES\n")
        display(df)

botao_entregadores = widgets.Button(
    description="🚴 Gerenciamento de Entregadores",
    button_style='warning'
)

botao_entregadores.on_click(gerenciamento_entregadores)

# =========================
# INTERFACE
# =========================
num_pontos_slider = widgets.IntSlider(value=10, min=3, max=30, description='Pedidos')
raio_slider = widgets.IntSlider(value=10, min=2, max=30, description='Raio (km)')
consumo_slider = widgets.FloatSlider(value=0.35, min=0.2, max=0.6, step=0.01, description='Consumo')
tanque_slider = widgets.IntSlider(value=80, min=40, max=150, description='Energia')

botao = widgets.Button(description="🍔 Iniciar Entrega", button_style='success')
botao_dashboard = widgets.Button(description="📊 Dashboard Pedidos", button_style='info')

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

        print("🍔 RESULTADOS DO IFOOD")
        print(f"Distância original: {dist_original:.2f} km")
        print(f"Distância otimizada do entregador: {dist_opt:.2f} km")
        print(f"Economia de energia: {consumo_original - consumo_opt:.2f} L")

        if precisa:
            print("⚠️ Entregador precisa recarregar energia")
        else:
            print("✅ Entrega dentro da capacidade")

        display(plotar_mapa(pontos, rota_opt))

botao.on_click(ao_clicar)

# =========================
# DASHBOARD BOTÃO
# =========================
def abrir_dashboard(b):
    if ultima_rota is None:
        with saida_dashboard:
            clear_output()
            print("⚠️ Faça uma entrega primeiro!")
        return

    mostrar_dashboard()

botao_dashboard.on_click(abrir_dashboard)

# =========================
# UI FINAL
# =========================
ui = widgets.VBox([
    widgets.HTML("<h2>🍔 iFood - Sistema de Entregas em Atenas</h2>"),
    num_pontos_slider,
    raio_slider,
    consumo_slider,
    tanque_slider,
    widgets.HBox([botao, botao_dashboard, botao_entregadores]),
    saida,
    saida_dashboard,
    saida_entregadores
])

display(ui)