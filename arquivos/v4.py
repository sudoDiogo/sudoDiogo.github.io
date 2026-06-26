!pip install folium

import math
import random
import folium
import ipywidgets as widgets
import pandas as pd
from IPython.display import display, clear_output

# =========================
# PORTOS REAIS (JAPÃO + COREIA DO SUL)
# =========================
PORTOS_BASE = [
    # Japão
    (34.980225, 132.173437),  # Kobe
    (34.361102, 130.893138),  # Osaka
    (33.5904, 130.4017),  # Fukuoka
    (33.523968, 129.877691),  # Hiroshima

    # Coreia do Sul
    (35.1796, 129.0756),  # Busan
    (34.931613, 128.210290),  # Incheon
    (34.7604, 127.6622),  # Yeosu
]

# Hub logístico principal (rota marítima central)
HUB = (35.0, 130.0)  # Mar entre Japão e Coreia

# =========================
# ESTADO GLOBAL
# =========================
ultima_rota = None
ultima_dist = None
ultimo_consumo = None

# =========================
# FUNÇÕES
# =========================
def distancia(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) * 111


def gerar_portos(n=6):
    # escolhe aleatoriamente portos reais da lista
    return random.sample(PORTOS_BASE, min(n, len(PORTOS_BASE)))


def rota_original(pontos):
    dist = 0
    atual = HUB

    for p in pontos:
        dist += distancia(atual, p)
        atual = p

    dist += distancia(atual, HUB)
    return dist


def vizinho_mais_proximo(pontos):
    nao_visitados = pontos.copy()
    rota = []
    atual = HUB
    dist = 0

    while nao_visitados:
        prox = min(nao_visitados, key=lambda p: distancia(atual, p))
        dist += distancia(atual, prox)
        rota.append(prox)
        atual = prox
        nao_visitados.remove(prox)

    dist += distancia(atual, HUB)
    return rota, dist


def consumo(dist, consumo_km=0.9):
    # navios pesados (container ship)
    return dist * consumo_km


def verifica_combustivel(dist, capacidade=150):
    c = consumo(dist)
    return c > capacidade, c


# =========================
# MAPA MARÍTIMO REAL
# =========================
def plotar_mapa(pontos, rota):
    mapa = folium.Map(location=HUB, zoom_start=6)

    # HUB marítimo
    folium.Marker(
        HUB,
        tooltip="🌊 Hub Marítimo (Mar Japão-Coreia)",
        icon=folium.Icon(color='red')
    ).add_to(mapa)

    # portos reais
    for i, p in enumerate(pontos):
        folium.Marker(
            p,
            tooltip=f"🚢 Porto {i+1}",
            icon=folium.Icon(color='blue')
        ).add_to(mapa)

    # ROTAS NO MAR (linha cruzando oceano)
    folium.PolyLine(
        [HUB] + rota + [HUB],
        color='darkblue',
        weight=3,
        tooltip="🚢 Rota de Contêineres Marítimos"
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
        atual = HUB

        for i, p in enumerate(ultima_rota):
            d = distancia(atual, p)
            dados.append([f"Porto {i+1}", round(d,2)])
            atual = p

        df = pd.DataFrame(dados, columns=[
            "Porto", "Distância marítima (km)"
        ])

        print("📊 LOGÍSTICA MARÍTIMA JAPÃO ↔ COREIA\n")
        display(df)

        print("\n📦 RESUMO")
        print(f"Distância total marítima: {ultima_dist:.2f} km")
        print(f"Consumo estimado do navio: {ultimo_consumo:.2f} L")


# =========================
# GERENCIAMENTO DE FROTA
# =========================
saida_frota = widgets.Output()

def gerenciamento_frota(b):
    with saida_frota:
        clear_output()

        frota = [
            {"Navio": "Pacific Carrier", "Carga": random.randint(500, 2000), "Status": "Em rota"},
            {"Navio": "Korea Express", "Carga": random.randint(300, 1500), "Status": "Carregando"},
            {"Navio": "Japan Sea Line", "Carga": random.randint(400, 1800), "Status": "Disponível"},
            {"Navio": "Blue Ocean", "Carga": random.randint(600, 2200), "Status": "Manutenção"},
        ]

        df = pd.DataFrame(frota)

        print("🚢 GERENCIAMENTO DE FROTA DE CONTÊINERES\n")
        display(df)


botao_frota = widgets.Button(
    description="🚢 Gerenciamento de Frota",
    button_style='warning'
)

botao_frota.on_click(gerenciamento_frota)


# =========================
# INTERFACE
# =========================
num_portos = widgets.IntSlider(value=5, min=2, max=7, description='Portos')
consumo_slider = widgets.FloatSlider(value=0.9, min=0.5, max=1.5, step=0.1, description='Consumo')
capacidade_slider = widgets.IntSlider(value=150, min=50, max=300, description='Capacidade')

botao = widgets.Button(description="🚢 Simular Rotas", button_style='success')
botao_dashboard = widgets.Button(description="📊 Dashboard", button_style='info')

saida = widgets.Output()


# =========================
# SIMULAÇÃO
# =========================
def ao_clicar(b):
    global ultima_rota, ultima_dist, ultimo_consumo

    with saida:
        clear_output()

        portos = gerar_portos(num_portos.value)

        dist_original = rota_original(portos)
        rota_opt, dist_opt = vizinho_mais_proximo(portos)

        consumo_original = consumo(dist_original, consumo_slider.value)
        consumo_opt = consumo(dist_opt, consumo_slider.value)

        precisa, c = verifica_combustivel(dist_opt, capacidade_slider.value)

        ultima_rota = rota_opt
        ultima_dist = dist_opt
        ultimo_consumo = consumo_opt

        print("🚢 LOGÍSTICA MARÍTIMA INTERNACIONAL")
        print(f"Distância original: {dist_original:.2f} km")
        print(f"Rota otimizada marítima: {dist_opt:.2f} km")
        print(f"Economia de combustível: {consumo_original - consumo_opt:.2f} L")

        if precisa:
            print("⚠️ Navio precisa reabastecer")
        else:
            print("✅ Viagem eficiente")

        display(plotar_mapa(portos, rota_opt))


botao.on_click(ao_clicar)


# =========================
# DASHBOARD
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
    widgets.HTML("<h2>🚢 Logística Marítima Japão ↔ Coreia do Sul</h2>"),
    num_portos,
    consumo_slider,
    capacidade_slider,
    widgets.HBox([botao, botao_dashboard, botao_frota]),
    saida,
    saida_dashboard,
    saida_frota
])

display(ui)