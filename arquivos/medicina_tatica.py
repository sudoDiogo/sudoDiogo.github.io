

"""
╔══════════════════════════════════════════════════════════════════╗
║         MEDICINA TÁTICA E CONTROLE DE MISSÃO                    ║
║         Suporte Médico Inteligente em Zonas de Conflito         ║
╚══════════════════════════════════════════════════════════════════╝

DEPENDÊNCIAS NECESSÁRIAS (instale antes de rodar):
  pip install pillow requests matplotlib numpy tkintermapview

EXECUÇÃO:
  python medicina_tatica.py
"""

import tkinter as tk
from tkinter import ttk, font
import math
import time
import threading
import webbrowser
import subprocess
import sys
import os
import geopandas as gpd

# ─────────────────────────────────────────────
#  Verificação e instalação de dependências
# ─────────────────────────────────────────────
def check_and_install(package, import_name=None):
    import_name = import_name or package
    try:
        __import__(import_name)
    except ImportError:
        print(f"[INSTALANDO] {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

check_and_install("pillow", "PIL")
check_and_install("requests")
check_and_install("matplotlib")
check_and_install("numpy")

# Tentar instalar tkintermapview (pode falhar em alguns sistemas)
try:
    check_and_install("tkintermapview")
    import tkintermapview
    HAS_MAPVIEW = True
except Exception:
    HAS_MAPVIEW = False

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageFont
import requests
import io
import json

# ─────────────────────────────────────────────
#  PALETA DE CORES — "Medicina no meio da Guerra"
# ─────────────────────────────────────────────
C = {
    "bg_deep":      "#0a0c0f",   # Preto profundo / bunker
    "bg_panel":     "#0f1318",   # Painel escuro
    "bg_sidebar":   "#080b0e",   # Sidebar ainda mais escura
    "accent_red":   "#c8102e",   # Vermelho sangue / Cruz vermelha
    "accent_green": "#1aff6a",   # Verde rádio militar
    "accent_amber": "#ffb300",   # Âmbar / alerta
    "accent_blue":  "#1e90ff",   # Azul operações
    "text_main":    "#e8e8e8",   # Texto principal
    "text_dim":     "#6b7280",   # Texto secundário
    "text_green":   "#4ade80",   # Verde claro
    "border":       "#1f2937",   # Borda sutil
    "border_bright":"#374151",   # Borda visível
    "red_zone":     "#c8102e",
    "yellow_zone":  "#b8860b",
    "purple_zone":  "#7c3aed",
    "safe_zone":    "#1f3a1f",
    "hover":        "#1a2030",
    "btn_active":   "#c8102e",
}

# ─────────────────────────────────────────────
#  DADOS GEOPOLÍTICOS
# ─────────────────────────────────────────────
CONFLICT_ZONES = {
    "red": ["Rússia", "Ucrânia", "Israel", "Irã", "Líbano", "Estados Unidos"],
    "yellow": ["Sudão", "Myanmar", "Síria", "Iêmen", "Somália", "Etiópia", "Haiti", "República Democrática do Congo"],
    "purple": ["Paquistão", "Afeganistão", "Venezuela", "Mali", "Burkina Faso", "Níger", "Taiwan", "Coreia do Norte", "México", "Líbia"],
}

# Coordenadas aproximadas dos países (centro) para o mapa de situação
COUNTRY_COORDS = {
    # VERMELHO
    "Rússia":          (62.0, 95.0),
    "Ucrânia":         (49.0, 32.0),
    "Israel":          (31.5, 34.8),
    "Irã":             (32.0, 53.0),
    "Líbano":          (33.9, 35.5),
    "Estados Unidos":  (38.0, -97.0),
    # AMARELO
    "Sudão":           (15.0, 30.0),
    "Myanmar":         (19.0, 96.0),
    "Síria":           (34.8, 38.9),
    "Iêmen":           (15.5, 48.0),
    "Somália":         (5.5, 46.2),
    "Etiópia":         (9.1, 40.5),
    "Haiti":           (18.9, -72.3),
    "República Democrática do Congo": (-4.0, 21.8),
    # ROXO
    "Paquistão":       (30.0, 69.0),
    "Afeganistão":     (33.0, 65.0),
    "Venezuela":       (6.4, -66.6),
    "Mali":            (17.5, -4.0),
    "Burkina Faso":    (12.4, -1.6),
    "Níger":           (17.6, 8.1),
    "Taiwan":          (23.7, 121.0),
    "Coreia do Norte": (40.3, 127.5),
    "México":          (23.6, -102.6),
    "Líbia":           (26.3, 17.2),
}

# ─────────────────────────────────────────────
#  EQUIPAMENTOS MÉDICOS
# ─────────────────────────────────────────────
EQUIPAMENTOS = [
    {
        "nome": "Torniquete SOFTT-W",
        "categoria": "Controle de Hemorragia",
        "descricao": "Torniquete tático de uma mão, padrão TCCC. Controla hemorragias em extremidades com eficácia superior.",
        "nivel": "CRÍTICO",
        "cor_nivel": "#c8102e",
        "emoji": "🩸",
        "specs": ["Material: Alumínio + Nylon", "Tempo de aplicação: <30s", "Peso: 155g"],
    },
    {
        "nome": "Curativo Hemostático",
        "categoria": "Controle de Hemorragia",
        "descricao": "Curativo impregnado com agente hemostático QuikClot. Controla sangramento em feridas de cavidade.",
        "nivel": "CRÍTICO",
        "cor_nivel": "#c8102e",
        "emoji": "🩹",
        "specs": ["Agente: Caulim zeólita", "Absorção: 3x maior", "Validade: 5 anos"],
    },
    {
        "nome": "Descompressor de Tórax",
        "categoria": "Via Aérea / Respiração",
        "descricao": "Agulha de descompressão para pneumotórax hipertensivo. 14G, 3.25 polegadas.",
        "nivel": "CRÍTICO",
        "cor_nivel": "#c8102e",
        "emoji": "🫁",
        "specs": ["Calibre: 14G", "Comprimento: 8.3cm", "Uso: Imediato"],
    },
    {
        "nome": "Selante de Tórax",
        "categoria": "Via Aérea / Respiração",
        "descricao": "Curativo oclusivo com válvula unidirecional para feridas abertas de tórax. Impede pneumotórax.",
        "nivel": "URGENTE",
        "cor_nivel": "#ff6b35",
        "emoji": "🔴",
        "specs": ["Tipo: Hyfin Chest Seal", "Válvulas: 3 canais", "Aderência: Máxima"],
    },
    {
        "nome": "Bandagem Israelense",
        "categoria": "Controle de Hemorragia",
        "descricao": "Emergency Pressure Dressing. Curativo de pressão com aplicador integrado para feridas de grande volume.",
        "nivel": "URGENTE",
        "cor_nivel": "#ff6b35",
        "emoji": "🏥",
        "specs": ["Tamanho: 6 e 4 polegadas", "Pressão: Aplicador duplo", "Esteril: Sim"],
    },
    {
        "nome": "Colar Cervical",
        "categoria": "Imobilização",
        "descricao": "Colar cervical tático dobrável. Imobilização de coluna cervical em pacientes com mecanismo de trauma.",
        "nivel": "PADRÃO",
        "cor_nivel": "#ffb300",
        "emoji": "🦴",
        "specs": ["Tipo: Semi-rígido", "Regulável: Sim", "Radiopaco: Sim"],
    },
    {
        "nome": "Oxímetro Tático",
        "categoria": "Monitoramento",
        "descricao": "Oxímetro de pulso para uso em campo. Resistente à água e impacto. Leitura mesmo em hipoperfusão.",
        "nivel": "PADRÃO",
        "cor_nivel": "#ffb300",
        "emoji": "📡",
        "specs": ["IP: 22", "Bateria: 12h", "Precisão: ±2%"],
    },
    {
        "nome": "Kit de Via Aérea",
        "categoria": "Via Aérea / Respiração",
        "descricao": "NPA (Nasopharyngeal Airway) 28Fr com gel lubrificante. Mantém via aérea em paciente inconsciente.",
        "nivel": "CRÍTICO",
        "cor_nivel": "#c8102e",
        "emoji": "💨",
        "specs": ["Calibre: 28Fr", "Material: PVC macio", "Uso: Pré-hospitalar"],
    },
    {
        "nome": "Maca Dobravél SKED",
        "categoria": "Transporte",
        "descricao": "Maca de resgate ultracompacta. Transporta paciente em qualquer terreno. Compatível com evacuação aérea.",
        "nivel": "PADRÃO",
        "cor_nivel": "#ffb300",
        "emoji": "🚁",
        "specs": ["Carga: 272kg", "Peso: 3.2kg", "Material: Polietileno"],
    },
    {
        "nome": "Morphine Autoinjector",
        "categoria": "Analgesia",
        "descricao": "Autoinjector de morfina para uso em campo. Alívio imediato de dor intensa em combatentes feridos.",
        "nivel": "RESTRITO",
        "cor_nivel": "#7c3aed",
        "emoji": "💉",
        "specs": ["Dose: 10mg/0.7ml", "Via: IM", "Ação: 3-5 min"],
    },
    {
        "nome": "Rolo Hemostático",
        "categoria": "Controle de Hemorragia",
        "descricao": "Gaze impregnada com chitosan. Preenche feridas de cavidade para controle de hemorragia interna.",
        "nivel": "URGENTE",
        "cor_nivel": "#ff6b35",
        "emoji": "🌀",
        "specs": ["Agente: Chitosano", "Tamanho: 7.6x3.7m", "Hemostasia: 3min"],
    },
    {
        "nome": "Desfibrilador DEA",
        "categoria": "Suporte Avançado",
        "descricao": "Desfibrilador externo automático portátil. Para uso em parada cardiorrespiratória no campo de batalha.",
        "nivel": "AVANÇADO",
        "cor_nivel": "#1e90ff",
        "emoji": "⚡",
        "specs": ["Energia: 200J bifásico", "IP: 55", "Bateria: 200 choques"],
    },
]


# ══════════════════════════════════════════════════════════════════
#  CLASSE PRINCIPAL DA APLICAÇÃO
# ══════════════════════════════════════════════════════════════════
class MedicinaTatica:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MEDICINA TÁTICA — Sistema de Controle de Missão")
        self.root.configure(bg=C["bg_deep"])
        self._setup_window()
        self._load_fonts()
        self._build_ui()
        self._animate_loop()

    # ─── Configuração da Janela ───────────────────────────────────
    def _setup_window(self):
        w, h = 1400, 860
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.minsize(1100, 700)
        self.root.resizable(True, True)
        # Ícone (cruz médica desenhada)
        try:
            icon = self._make_cross_icon()
            self.root.iconphoto(True, icon)
        except Exception:
            pass

    def _make_cross_icon(self):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rectangle([20, 8, 44, 56], fill="#c8102e")
        d.rectangle([8, 20, 56, 44], fill="#c8102e")
        return ImageTk.PhotoImage(img)

    def _load_fonts(self):
        self.fnt = {
            "title":    ("Courier New", 22, "bold"),
            "subtitle": ("Courier New", 11, "italic"),
            "nav":      ("Courier New", 12, "bold"),
            "nav_sm":   ("Courier New", 10),
            "mono":     ("Courier New", 9),
            "label":    ("Courier New", 10, "bold"),
            "body":     ("Courier New", 9),
            "h2":       ("Courier New", 16, "bold"),
            "h3":       ("Courier New", 13, "bold"),
            "tag":      ("Courier New", 8, "bold"),
        }

    # ─── Construção da UI principal ───────────────────────────────
    def _build_ui(self):
        # Frame raiz
        self.root_frame = tk.Frame(self.root, bg=C["bg_deep"])
        self.root_frame.pack(fill="both", expand=True)

        # Cabeçalho global
        self._build_header()

        # Corpo: sidebar + content
        self.body = tk.Frame(self.root_frame, bg=C["bg_deep"])
        self.body.pack(fill="both", expand=True)

        self._build_sidebar()
        self._build_content_area()

        # Rodapé
        self._build_footer()

        # Mostrar Home por padrão
        self._show_home()

    def _build_header(self):
        hdr = tk.Frame(self.root_frame, bg=C["bg_panel"], height=90)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)

        # Linha vermelha superior
        tk.Frame(hdr, bg=C["accent_red"], height=3).pack(fill="x", side="top")

        inner = tk.Frame(hdr, bg=C["bg_panel"])
        inner.pack(fill="both", expand=True, padx=20, pady=8)

        left = tk.Frame(inner, bg=C["bg_panel"])
        left.pack(side="left", fill="y")

        # Logo — cruz médica
        self.logo_canvas = tk.Canvas(left, width=60, height=60, bg=C["bg_panel"],
                                     highlightthickness=0)
        self.logo_canvas.pack(side="left", padx=(0, 16))
        self._draw_cross(self.logo_canvas, 30, 30, 22)

        title_frame = tk.Frame(inner, bg=C["bg_panel"])
        title_frame.pack(side="left", fill="y")

        tk.Label(title_frame, text="MEDICINA TÁTICA E CONTROLE DE MISSÃO",
                 font=self.fnt["title"], fg=C["accent_red"],
                 bg=C["bg_panel"]).pack(anchor="w")

        tk.Label(title_frame,
                 text="tornando o suporte médico mais inteligente",
                 font=self.fnt["subtitle"], fg=C["text_dim"],
                 bg=C["bg_panel"]).pack(anchor="w")

        # Status direita
        right = tk.Frame(inner, bg=C["bg_panel"])
        right.pack(side="right", fill="y", padx=10)

        self.clock_var = tk.StringVar(value="00:00:00")
        tk.Label(right, textvariable=self.clock_var,
                 font=("Courier New", 18, "bold"),
                 fg=C["accent_green"], bg=C["bg_panel"]).pack(anchor="e")

        self.status_var = tk.StringVar(value="● SISTEMA OPERACIONAL")
        tk.Label(right, textvariable=self.status_var,
                 font=self.fnt["mono"], fg=C["accent_green"],
                 bg=C["bg_panel"]).pack(anchor="e")

        tk.Label(right, text="NÍVEL DE AMEAÇA: ELEVADO",
                 font=self.fnt["mono"], fg=C["accent_amber"],
                 bg=C["bg_panel"]).pack(anchor="e")

    def _draw_cross(self, canvas, cx, cy, size, color="#c8102e"):
        t = size // 3
        canvas.delete("cross")
        # Sombra
        canvas.create_rectangle(cx-t+2, cy-size+2, cx+t+2, cy+size+2,
                                 fill="#5a0010", outline="", tags="cross")
        canvas.create_rectangle(cx-size+2, cy-t+2, cx+size+2, cy+t+2,
                                 fill="#5a0010", outline="", tags="cross")
        # Cruz
        canvas.create_rectangle(cx-t, cy-size, cx+t, cy+size,
                                 fill=color, outline="", tags="cross")
        canvas.create_rectangle(cx-size, cy-t, cx+size, cy+t,
                                 fill=color, outline="", tags="cross")

    def _build_sidebar(self):
        sidebar = tk.Frame(self.body, bg=C["bg_sidebar"],
                           width=240, relief="flat")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Borda direita
        tk.Frame(sidebar, bg=C["accent_red"], width=2).pack(side="right", fill="y")

        inner = tk.Frame(sidebar, bg=C["bg_sidebar"])
        inner.pack(fill="both", expand=True, padx=0, pady=0)

        # Título da nav
        tk.Frame(inner, bg=C["border_bright"], height=1).pack(fill="x", pady=(16, 0))
        tk.Label(inner, text="◈ CONTROLES DE MISSÃO",
                 font=self.fnt["mono"], fg=C["text_dim"],
                 bg=C["bg_sidebar"]).pack(anchor="w", padx=16, pady=(6, 4))
        tk.Frame(inner, bg=C["border_bright"], height=1).pack(fill="x")

        # Botões de navegação
        self.nav_buttons = {}
        nav_items = [
            ("🏠", "HOME",               self._show_home),
            ("🌍", "SITUAÇÃO ATUAL",     self._show_situacao),
            ("🗺️", "PLANEJAMENTO",       self._show_planejamento),
            ("⚕️", "EQUIPAMENTOS",       self._show_equipamentos),
        ]

        for icon, label, cmd in nav_items:
            btn_frame = tk.Frame(inner, bg=C["bg_sidebar"], cursor="hand2")
            btn_frame.pack(fill="x", pady=1)

            icon_lbl = tk.Label(btn_frame, text=icon, font=("Segoe UI Emoji", 14),
                                bg=C["bg_sidebar"], fg=C["text_main"], width=3)
            icon_lbl.pack(side="left", padx=(12, 4), pady=12)

            text_lbl = tk.Label(btn_frame, text=label, font=self.fnt["nav"],
                                bg=C["bg_sidebar"], fg=C["text_main"], anchor="w")
            text_lbl.pack(side="left", fill="x", expand=True)

            indicator = tk.Frame(btn_frame, bg=C["bg_sidebar"], width=4)
            indicator.pack(side="right", fill="y")

            self.nav_buttons[label] = (btn_frame, icon_lbl, text_lbl, indicator)

            for widget in (btn_frame, icon_lbl, text_lbl):
                widget.bind("<Enter>", lambda e, bf=btn_frame, il=icon_lbl,
                            tl=text_lbl, ind=indicator: self._nav_hover(bf, il, tl, ind, True))
                widget.bind("<Leave>", lambda e, bf=btn_frame, il=icon_lbl,
                            tl=text_lbl, ind=indicator, lbl=label: self._nav_hover(
                            bf, il, tl, ind, False, lbl))
                widget.bind("<Button-1>", lambda e, c=cmd, lbl=label: self._nav_click(c, lbl))

        # Info extra sidebar
        tk.Frame(inner, bg=C["border"], height=1).pack(fill="x", pady=(20, 0))

        info_frame = tk.Frame(inner, bg=C["bg_sidebar"])
        info_frame.pack(fill="x", padx=16, pady=10)

        status_items = [
            ("PESSOAL", "12 / 14 ativo"),
            ("SUPRIMENTOS", "73% disponível"),
            ("EVAC", "2 pend."),
            ("COMUNICAÇÃO", "ATIVA"),
        ]
        for k, v in status_items:
            row = tk.Frame(info_frame, bg=C["bg_sidebar"])
            row.pack(fill="x", pady=2)
            tk.Label(row, text=k, font=self.fnt["tag"], fg=C["text_dim"],
                     bg=C["bg_sidebar"], anchor="w").pack(side="left")
            color = C["accent_green"] if v not in ["2 pend.", "73% disponível"] else C["accent_amber"]
            tk.Label(row, text=v, font=self.fnt["tag"], fg=color,
                     bg=C["bg_sidebar"], anchor="e").pack(side="right")

    def _nav_hover(self, bf, il, tl, ind, on, label=None):
        if on:
            bf.config(bg=C["hover"])
            il.config(bg=C["hover"])
            tl.config(bg=C["hover"])
        else:
            is_active = (label == getattr(self, "_active_nav", None))
            bg = C["btn_active"] if is_active else C["bg_sidebar"]
            text_bg = "#1a0a0a" if is_active else C["bg_sidebar"]
            bf.config(bg=text_bg)
            il.config(bg=text_bg)
            tl.config(bg=text_bg)

    def _nav_click(self, cmd, label):
        self._active_nav = label
        for lbl, (bf, il, tl, ind) in self.nav_buttons.items():
            if lbl == label:
                bf.config(bg="#1a0a0a")
                il.config(bg="#1a0a0a")
                tl.config(bg="#1a0a0a")
                tl.config(fg=C["accent_red"])
                ind.config(bg=C["accent_red"])
            else:
                bf.config(bg=C["bg_sidebar"])
                il.config(bg=C["bg_sidebar"])
                tl.config(bg=C["bg_sidebar"])
                tl.config(fg=C["text_main"])
                ind.config(bg=C["bg_sidebar"])
        cmd()

    def _build_content_area(self):
        self.content = tk.Frame(self.body, bg=C["bg_deep"])
        self.content.pack(side="left", fill="both", expand=True)

    def _build_footer(self):
        footer = tk.Frame(self.root_frame, bg=C["bg_panel"], height=28)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Frame(footer, bg=C["accent_red"], height=2).pack(fill="x", side="top")
        finner = tk.Frame(footer, bg=C["bg_panel"])
        finner.pack(fill="both", expand=True, padx=16)
        tk.Label(finner, text="SISTEMA MEDICINA TÁTICA v2.1 | NATO STANAG 2348 | TCCC APPROVED",
                 font=self.fnt["mono"], fg=C["text_dim"],
                 bg=C["bg_panel"]).pack(side="left", pady=4)
        self.footer_right = tk.StringVar(value="COORDENADAS: ---.--N / ---.--W")
        tk.Label(finner, textvariable=self.footer_right,
                 font=self.fnt["mono"], fg=C["accent_green"],
                 bg=C["bg_panel"]).pack(side="right", pady=4)

    # ─── Limpeza de conteúdo ──────────────────────────────────────
    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()
        # Fechar figuras matplotlib abertas
        plt.close("all")

    # ══════════════════════════════════════════════════════════════
    #  HOME — Mapa Múndi Estilizado + Símbolo piscando
    # ══════════════════════════════════════════════════════════════
    # ══════════════════════════════════════════════════════════════
#  HOME — MAPA SATELITAL REAL
# ══════════════════════════════════════════════════════════════
    def _show_home(self):

        self._clear_content()

        # marca nav ativa
        self._active_nav = "HOME"

        frame = tk.Frame(self.content, bg=C["bg_deep"])
        frame.pack(fill="both", expand=True)

        # ─────────────────────────────────────────
        # HEADER
        # ─────────────────────────────────────────
        title_bar = tk.Frame(frame, bg="#100505", height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text="🌍 MAPA GLOBAL TÁTICO — SATÉLITE EM TEMPO REAL",
            font=self.fnt["h3"],
            fg=C["accent_red"],
            bg="#100505"
        ).pack(side="left", padx=16, pady=8)

        tk.Label(
            title_bar,
            text="GOOGLE SATELLITE • LIVE MAP SYSTEM",
            font=self.fnt["mono"],
            fg=C["text_dim"],
            bg="#100505"
        ).pack(side="right", padx=16)

        # linha vermelha
        tk.Frame(frame, bg=C["accent_red"], height=2).pack(fill="x")

        # ─────────────────────────────────────────
        # CONTROLES
        # ─────────────────────────────────────────
        controls = tk.Frame(frame, bg=C["bg_panel"], height=42)
        controls.pack(fill="x")
        controls.pack_propagate(False)

        tk.Label(
            controls,
            text="CAMADAS:",
            font=self.fnt["label"],
            fg=C["text_dim"],
            bg=C["bg_panel"]
        ).pack(side="left", padx=(16, 8))

        # ─────────────────────────────────────────
        # MAPA
        # ─────────────────────────────────────────
        import tkintermapview

        self.home_map = tkintermapview.TkinterMapView(
            frame,
            corner_radius=0,
            bg_color=C["bg_deep"]
        )

        self.home_map.pack(fill="both", expand=True)

        # posição inicial
        self.home_map.set_position(20, 0)

        # zoom global
        self.home_map.set_zoom(2)

        # ─────────────────────────────────────────
        # TILES
        # ─────────────────────────────────────────

        def set_satellite():
            self.home_map.set_tile_server(
                "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga"
            )

        def set_hybrid():
            self.home_map.set_tile_server(
                "https://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga"
            )

        def set_terrain():
            self.home_map.set_tile_server(
                "https://mt0.google.com/vt/lyrs=p&hl=en&x={x}&y={y}&z={z}&s=Ga"
            )

        def set_normal():
            self.home_map.set_tile_server(
                "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
            )

        # satélite por padrão
        set_hybrid()

        # ─────────────────────────────────────────
        # BOTÕES
        # ─────────────────────────────────────────
        btn_style = {
            "font": self.fnt["tag"],
            "fg": C["text_main"],
            "bg": C["border"],
            "activebackground": C["accent_red"],
            "activeforeground": "white",
            "relief": "flat",
            "cursor": "hand2",
            "padx": 10,
            "pady": 4
        }

        tk.Button(
            controls,
            text="SATÉLITE",
            command=set_satellite,
            **btn_style
        ).pack(side="left", padx=2)

        tk.Button(
            controls,
            text="HÍBRIDO",
            command=set_hybrid,
            **btn_style
        ).pack(side="left", padx=2)

        tk.Button(
            controls,
            text="TERRENO",
            command=set_terrain,
            **btn_style
        ).pack(side="left", padx=2)

        tk.Button(
            controls,
            text="PADRÃO",
            command=set_normal,
            **btn_style
        ).pack(side="left", padx=2)

        # ─────────────────────────────────────────
        # MARCADORES
        # ─────────────────────────────────────────

        self.map_markers = []

        # vermelho
        # ─────────────────────────────────────────
# MARCADOR SIMPLES (CENTRAL)
# ─────────────────────────────────────────

        self.home_map.set_marker(
            -30, -55,
            text="⚕ Centro de Operações",
            text_color=C["accent_red"],
           # marker_color_circle=C["accent_red"],
            #marker_color_outside="#220000"
        )

        # ─────────────────────────────────────────
        # FOOTER INFO
        # ─────────────────────────────────────────
        info_bar = tk.Frame(frame, bg="#0a0505", height=30)
        info_bar.pack(fill="x")
        info_bar.pack_propagate(False)

        total = (
            len(CONFLICT_ZONES["red"]) +
            len(CONFLICT_ZONES["yellow"]) +
            len(CONFLICT_ZONES["purple"])
        )

        tk.Label(
            info_bar,
            text=(
                f"  MONITORANDO {total} ZONAS GLOBAIS  |  "
                f"MAPA SATELITAL OPERACIONAL  |  "
                f"SCROLL = ZOOM  |  ARRASTAR = NAVEGAR"
            ),
            font=self.fnt["mono"],
            fg=C["text_dim"],
            bg="#0a0505"
        ).pack(side="left", pady=6)

    def _blink_cross(self):
        if not hasattr(self, '_blink_canvas') or not self._blink_canvas.winfo_exists():
            return
        self._blink_canvas.delete("all")
        if self._blink_state:
            c = self._blink_canvas
            # Círculo externo pulsante
            c.create_oval(5, 5, 75, 75, outline=C["accent_red"], width=2)
            c.create_oval(15, 15, 65, 65, fill="#3a0010", outline=C["accent_red"], width=1)
            # Cruz
            c.create_rectangle(33, 18, 47, 62, fill=C["accent_red"], outline="")
            c.create_rectangle(18, 33, 62, 47, fill=C["accent_red"], outline="")
            c.create_text(40, 40, text="+", fill="white",
                          font=("Courier New", 8, "bold"))
        self._blink_state = not self._blink_state
        self.root.after(700, self._blink_cross)

    def _draw_world_map_base(self, ax, highlight_conflicts=False,
                              red=None, yellow=None, purple=None):
        """Desenha mapa simplificado via dados embutidos (polígonos dos continentes)."""
        # Continentes aproximados como polígonos
        continents = [
            # América do Norte
            [(-170,70),(-55,70),(-55,15),(-85,10),(-95,17),(-115,22),(-120,30),
             (-130,40),(-140,55),(-155,60),(-170,65),(-170,70)],
            # América do Sul
            [(-80,10),(-50,10),(-35,-5),(-35,-15),(-45,-23),(-55,-35),
             (-65,-55),(-75,-50),(-80,-20),(-80,10)],
            # Europa
            [(0,50),(30,70),(30,60),(40,55),(35,45),(25,38),(10,38),(-5,36),
             (-10,38),(-8,44),(-5,48),(0,50)],
            # África
            [(-18,15),(50,15),(52,10),(42,-12),(35,-35),(18,-35),(12,-20),
             (8,5),(10,8),(2,6),(-18,8),(-18,15)],
            # Ásia
            [(25,70),(180,70),(180,0),(140,-10),(120,20),(100,10),(80,10),
             (60,22),(50,30),(40,36),(35,45),(40,55),(25,70)],
            # Oceania
            [(115,-20),(155,-20),(155,-45),(140,-45),(115,-35),(110,-25),(115,-20)],
        ]
        for poly in continents:
            xs, ys = zip(*poly)
            if highlight_conflicts:
                ax.fill(xs, ys, color="#0d1a0d", alpha=0.7, zorder=1)
            else:
                ax.fill(xs, ys, color="#0d1f0d", alpha=0.8, zorder=1)
            ax.plot(list(xs) + [xs[0]], list(ys) + [ys[0]],
                    color="#1a3a1a", linewidth=0.6, zorder=2)

        # Oceanos
        ax.set_facecolor("#080c14")

        if highlight_conflicts and red and yellow and purple:
            for country in red:
                if country in COUNTRY_COORDS:
                    lat, lon = COUNTRY_COORDS[country]
                    ax.scatter(lon, lat, s=800, c=C["accent_red"],
                               alpha=0.35, zorder=4, edgecolors=C["accent_red"],
                               linewidths=0)
                    ax.scatter(lon, lat, s=120, c=C["accent_red"],
                               alpha=0.9, zorder=5, marker="*")
                    ax.annotate(country, (lon, lat),
                                xytext=(5, 5), textcoords="offset points",
                                fontsize=6.5, color=C["accent_red"],
                                fontfamily="Courier New", fontweight="bold",
                                zorder=6)
            for country in yellow:
                if country in COUNTRY_COORDS:
                    lat, lon = COUNTRY_COORDS[country]
                    ax.scatter(lon, lat, s=600, c=C["yellow_zone"],
                               alpha=0.35, zorder=4, edgecolors=C["yellow_zone"],
                               linewidths=0)
                    ax.scatter(lon, lat, s=80, c=C["yellow_zone"],
                               alpha=0.9, zorder=5, marker="D")
                    ax.annotate(country, (lon, lat),
                                xytext=(5, 5), textcoords="offset points",
                                fontsize=6, color=C["yellow_zone"],
                                fontfamily="Courier New", zorder=6)
            for country in purple:
                if country in COUNTRY_COORDS:
                    lat, lon = COUNTRY_COORDS[country]
                    ax.scatter(lon, lat, s=500, c=C["purple_zone"],
                               alpha=0.35, zorder=4, edgecolors=C["purple_zone"],
                               linewidths=0)
                    ax.scatter(lon, lat, s=70, c=C["purple_zone"],
                               alpha=0.9, zorder=5, marker="^")
                    ax.annotate(country, (lon, lat),
                                xytext=(5, 5), textcoords="offset points",
                                fontsize=6, color=C["purple_zone"],
                                fontfamily="Courier New", zorder=6)

    # ══════════════════════════════════════════════════════════════
    #  SITUAÇÃO ATUAL — Mapa com zonas de conflito
    # ══════════════════════════════════════════════════════════════
    def _show_situacao(self):

        self._clear_content()

        frame = tk.Frame(self.content, bg=C["bg_deep"])
        frame.pack(fill="both", expand=True)

        title_bar = tk.Frame(frame, bg="#100505", height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text="⚠ SITUAÇÃO GLOBAL — MAPA POLÍTICO",
            font=self.fnt["h3"],
            fg=C["accent_red"],
            bg="#100505"
        ).pack(side="left", padx=16, pady=8)

        import geopandas as gpd

        map_frame = tk.Frame(frame, bg=C["bg_deep"])
        map_frame.pack(fill="both", expand=True)

        fig, ax = plt.subplots(figsize=(14, 8))
        fig.patch.set_facecolor("#08080f")
        ax.set_facecolor("#08080f")

        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        # cor padrão
        world["color"] = "#1b2631"

        # países vermelhos
        for c in CONFLICT_ZONES["red"]:
            world.loc[world["name"] == c, "color"] = "#c8102e"

        # amarelos
        for c in CONFLICT_ZONES["yellow"]:
            world.loc[world["name"] == c, "color"] = "#ffb300"

        # roxos
        for c in CONFLICT_ZONES["purple"]:
            world.loc[world["name"] == c, "color"] = "#7c3aed"

        world.plot(
            color=world["color"],
            edgecolor="#202020",
            linewidth=0.4,
            ax=ax
        )

        ax.axis("off")

        canvas = FigureCanvasTkAgg(fig, master=map_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        legend_frame = tk.Frame(frame, bg="#050505", height=34)
        legend_frame.pack(fill="x")
        legend_frame.pack_propagate(False)

        tk.Label(
            legend_frame,
            text="VERMELHO = CONFLITO ATIVO   |   AMARELO = INSTABILIDADE   |   ROXO = RISCO ELEVADO",
            font=self.fnt["mono"],
            fg=C["text_dim"],
            bg="#050505"
        ).pack(pady=8)

    ###############

    def _update_situacao_time(self):
        now = time.strftime("ATUALIZADO: %d/%m/%Y %H:%M:%S UTC")
        if hasattr(self, "update_time_var"):
            try:
                self.update_time_var.set(now)
                self.root.after(1000, self._update_situacao_time)
            except Exception:
                pass

    # ══════════════════════════════════════════════════════════════
    #  PLANEJAMENTO — Mapa interativo com tkintermapview ou fallback
    # ══════════════════════════════════════════════════════════════
    def _show_planejamento(self):
        self._clear_content()

        frame = tk.Frame(self.content, bg=C["bg_deep"])
        frame.pack(fill="both", expand=True)

        # Barra de título
        title_bar = tk.Frame(frame, bg="#050a14", height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar,
                 text="🗺  PLANEJAMENTO DE MISSÃO — MAPA TÁTICO INTERATIVO",
                 font=self.fnt["h3"], fg=C["accent_blue"],
                 bg="#050a14").pack(side="left", padx=16, pady=8)

        if HAS_MAPVIEW:
            self._build_mapview(frame)
        else:
            self._build_map_fallback(frame)

    def _build_mapview(self, parent):
        """Mapa real com satélite usando tkintermapview."""
        controls = tk.Frame(parent, bg=C["bg_panel"])
        controls.pack(fill="x")
        tk.Frame(controls, bg=C["border_bright"], height=1).pack(fill="x")
        ctrl_inner = tk.Frame(controls, bg=C["bg_panel"])
        ctrl_inner.pack(pady=6, padx=16, anchor="w")

        tk.Label(ctrl_inner, text="TILE:", font=self.fnt["label"],
                 fg=C["text_dim"], bg=C["bg_panel"]).pack(side="left")

        self._map_widget = None

        def set_tile(tile_server, name):
            if self._map_widget:
                self._map_widget.set_tile_server(tile_server)

        tile_btns = [
            ("SATÉLITE", "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga"),
            ("TERRENO",  "https://mt0.google.com/vt/lyrs=p&hl=en&x={x}&y={y}&z={z}&s=Ga"),
            ("HÍBRIDO",  "https://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga"),
            ("PADRÃO",   "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"),
        ]

        tk.Label(
            title_bar,
            text="⚠ SITUAÇÃO GLOBAL — MAPA POLÍTICO (PAÍSES POR NÍVEL DE RISCO)",
            font=self.fnt["h3"],
            fg=C["accent_red"],
            bg="#100505"
        ).pack(side="left", padx=16, pady=8)

        tk.Button(
            ctrl_inner,
            text="CRIAR MISSÃO",
            font=self.fnt["tag"],
            fg="white",
            bg=C["accent_red"],
            activebackground="#ff2a2a",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
            command=self._create_mission
        ).pack(side="left", padx=10)
        for name, url in tile_btns:
            btn = tk.Button(ctrl_inner, text=name, font=self.fnt["tag"],
                            fg=C["text_main"], bg=C["border"],
                            activebackground=C["accent_blue"],
                            activeforeground="white",
                            relief="flat", padx=8, pady=3, cursor="hand2",
                            command=lambda u=url, n=name: set_tile(u, n))
            btn.pack(side="left", padx=4)

        tk.Frame(controls, bg=C["border_bright"], height=1).pack(fill="x")

        map_frame = tk.Frame(parent, bg=C["bg_deep"])
        map_frame.pack(fill="both", expand=True)

        import tkintermapview as mapview
        self._map_widget = mapview.TkinterMapView(
            map_frame, corner_radius=0,
            bg_color=C["bg_deep"]
        )
        self._map_widget.pack(fill="both", expand=True)
        self._map_widget.set_position(20, 10)
        self._map_widget.set_zoom(3)
        # Satélite por padrão
        self._map_widget.set_tile_server(
            "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga"
        )

    def _build_map_fallback(self, parent):
        """Fallback: mapa interativo simples com zoom/pan via matplotlib."""
        info = tk.Frame(parent, bg="#050a14")
        info.pack(fill="x")
        tk.Label(info,
                 text="  ⓘ  Modo offline — instale 'tkintermapview' para mapa satélite real  |  Use scroll para zoom, clique+arraste para mover",
                 font=self.fnt["mono"], fg=C["accent_amber"],
                 bg="#050a14").pack(pady=6, anchor="w")

        map_frame = tk.Frame(parent, bg=C["bg_deep"])
        map_frame.pack(fill="both", expand=True)

        self._plan_fig, self._plan_ax = plt.subplots(
            figsize=(13, 7.5), facecolor="#08080f"
        )
        self._plan_ax.set_facecolor("#0a1018")

        # Estado de zoom/pan
        self._plan_xlim = [-180.0, 180.0]
        self._plan_ylim = [-90.0, 90.0]
        self._pan_start = None

        self._redraw_plan_map()

        canvas = FigureCanvasTkAgg(self._plan_fig, master=map_frame)
        canvas.draw()
        self._plan_canvas_widget = canvas.get_tk_widget()
        self._plan_canvas_widget.pack(fill="both", expand=True)
        self._plan_mpl_canvas = canvas

        # Eventos
        canvas.mpl_connect("scroll_event", self._plan_zoom)
        canvas.mpl_connect("button_press_event", self._plan_press)
        canvas.mpl_connect("button_release_event", self._plan_release)
        canvas.mpl_connect("motion_notify_event", self._plan_drag)
        canvas.mpl_connect("motion_notify_event", self._plan_coords)

        # Controles de zoom
        ctrl = tk.Frame(map_frame, bg=C["bg_panel"])
        ctrl.pack(fill="x", side="bottom")
        for txt, factor in [("  +  ", 0.6), ("  −  ", 1.4), ("RESET", None)]:
            def zoom_btn(f=factor):
                if f is None:
                    self._plan_xlim = [-180.0, 180.0]
                    self._plan_ylim = [-90.0, 90.0]
                else:
                    cx = (self._plan_xlim[0] + self._plan_xlim[1]) / 2
                    cy = (self._plan_ylim[0] + self._plan_ylim[1]) / 2
                    xr = (self._plan_xlim[1] - self._plan_xlim[0]) / 2 * f
                    yr = (self._plan_ylim[1] - self._plan_ylim[0]) / 2 * f
                    self._plan_xlim = [cx - xr, cx + xr]
                    self._plan_ylim = [cy - yr, cy + yr]
                self._redraw_plan_map()
                self._plan_mpl_canvas.draw()
            tk.Button(ctrl, text=txt, font=self.fnt["nav"],
                      fg=C["text_main"], bg=C["border"],
                      activebackground=C["accent_blue"],
                      relief="flat", padx=12, pady=4, cursor="hand2",
                      command=zoom_btn).pack(side="left", padx=2, pady=4)

        self._plan_coord_var = tk.StringVar(value="LAT: ---.-- | LON: ---.--")
        tk.Label(ctrl, textvariable=self._plan_coord_var,
                 font=self.fnt["mono"], fg=C["accent_green"],
                 bg=C["bg_panel"]).pack(side="right", padx=16)

    def _redraw_plan_map(self):
        ax = self._plan_ax
        ax.cla()
        ax.set_facecolor("#0a1018")

        # Grade
        xl, yl = self._plan_xlim, self._plan_ylim
        step_x = self._nice_step((xl[1] - xl[0]) / 6)
        step_y = self._nice_step((yl[1] - yl[0]) / 5)

        for x in self._range_steps(xl[0], xl[1], step_x):
            ax.axvline(x, color="#0d2030", linewidth=0.5, linestyle="--")
        for y in self._range_steps(yl[0], yl[1], step_y):
            ax.axhline(y, color="#0d2030", linewidth=0.5, linestyle="--")

        self._draw_world_map_base(ax)

        # Marcadores das zonas de conflito
        for country in CONFLICT_ZONES["red"]:
            if country in COUNTRY_COORDS:
                lat, lon = COUNTRY_COORDS[country]
                if xl[0] < lon < xl[1] and yl[0] < lat < yl[1]:
                    ax.scatter(lon, lat, s=100, c=C["accent_red"],
                               zorder=5, marker="*", edgecolors="white", linewidths=0.3)

        ax.set_xlim(xl)
        ax.set_ylim(yl)
        ax.tick_params(colors="#334455", labelsize=6)
        for spine in ax.spines.values():
            spine.set_edgecolor("#1a2a3a")
        ax.set_xlabel("Longitude", fontsize=7, color="#334455", fontfamily="Courier New")
        ax.set_ylabel("Latitude", fontsize=7, color="#334455", fontfamily="Courier New")
        self._plan_fig.tight_layout(pad=0.3)

    def _nice_step(self, raw):
        for s in [0.5, 1, 2, 5, 10, 15, 20, 30, 45, 60, 90, 120, 180]:
            if raw <= s:
                return s
        return 180

    def _range_steps(self, lo, hi, step):
        import math
        start = math.ceil(lo / step) * step
        vals = []
        v = start
        while v <= hi:
            vals.append(v)
            v += step
        return vals

    def _plan_zoom(self, event):
        if event.xdata is None or event.ydata is None:
            return
        factor = 0.7 if event.button == "up" else 1.3
        cx, cy = event.xdata, event.ydata
        xl, yl = self._plan_xlim, self._plan_ylim
        new_xr = (xl[1] - xl[0]) / 2 * factor
        new_yr = (yl[1] - yl[0]) / 2 * factor
        self._plan_xlim = [cx - new_xr, cx + new_xr]
        self._plan_ylim = [cy - new_yr, cy + new_yr]
        self._clip_plan_limits()
        self._redraw_plan_map()
        self._plan_mpl_canvas.draw()

    def _plan_press(self, event):
        if event.button == 1 and event.xdata:
            self._pan_start = (event.xdata, event.ydata,
                               self._plan_xlim[:], self._plan_ylim[:])

    def _plan_release(self, event):
        self._pan_start = None

    def _plan_drag(self, event):
        if self._pan_start and event.xdata:
            dx = self._pan_start[0] - event.xdata
            dy = self._pan_start[1] - event.ydata
            ox, oy = self._pan_start[2], self._pan_start[3]
            self._plan_xlim = [ox[0] + dx, ox[1] + dx]
            self._plan_ylim = [oy[0] + dy, oy[1] + dy]
            self._clip_plan_limits()
            self._redraw_plan_map()
            self._plan_mpl_canvas.draw()

    def _plan_coords(self, event):
        if event.xdata and event.ydata and hasattr(self, "_plan_coord_var"):
            self._plan_coord_var.set(
                f"LAT: {event.ydata:+.2f}° | LON: {event.xdata:+.2f}°"
            )

    def _clip_plan_limits(self):
        xw = self._plan_xlim[1] - self._plan_xlim[0]
        yw = self._plan_ylim[1] - self._plan_ylim[0]
        xw = max(xw, 2); yw = max(yw, 2)
        if self._plan_xlim[0] < -180:
            self._plan_xlim = [-180.0, -180.0 + xw]
        if self._plan_xlim[1] > 180:
            self._plan_xlim = [180.0 - xw, 180.0]
        if self._plan_ylim[0] < -90:
            self._plan_ylim = [-90.0, -90.0 + yw]
        if self._plan_ylim[1] > 90:
            self._plan_ylim = [90.0 - yw, 90.0]

    # ══════════════════════════════════════════════════════════════
    #  EQUIPAMENTOS — Grid com cards clicáveis
    # ══════════════════════════════════════════════════════════════
    def _show_equipamentos(self):
        self._clear_content()

        frame = tk.Frame(self.content, bg=C["bg_deep"])
        frame.pack(fill="both", expand=True)

        # Barra de título
        title_bar = tk.Frame(frame, bg="#050a05", height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar,
                 text="⚕  EQUIPAMENTOS MÉDICOS — SUPORTE TÁTICO DE CAMPO",
                 font=self.fnt["h3"], fg=C["accent_green"],
                 bg="#050a05").pack(side="left", padx=16, pady=8)
        tk.Label(title_bar,
                 text=f"  {len(EQUIPAMENTOS)} itens no inventário  |  Clique para detalhes",
                 font=self.fnt["mono"], fg=C["text_dim"],
                 bg="#050a05").pack(side="right", padx=16)

        tk.Frame(frame, bg=C["accent_green"], height=2).pack(fill="x")

        # Filtros rápidos
        filter_bar = tk.Frame(frame, bg=C["bg_panel"])
        filter_bar.pack(fill="x")
        f_inner = tk.Frame(filter_bar, bg=C["bg_panel"])
        f_inner.pack(padx=16, pady=6, anchor="w")
        tk.Label(f_inner, text="FILTRAR:", font=self.fnt["label"],
                 fg=C["text_dim"], bg=C["bg_panel"]).pack(side="left")

        cats = sorted(set(e["categoria"] for e in EQUIPAMENTOS))
        self._filter_var = tk.StringVar(value="TODOS")

        for cat in ["TODOS"] + cats:
            btn = tk.Button(f_inner, text=cat, font=self.fnt["tag"],
                            fg=C["text_main"], bg=C["border"],
                            activebackground=C["accent_green"],
                            activeforeground="black",
                            relief="flat", padx=8, pady=3, cursor="hand2",
                            command=lambda c=cat: self._filter_equip(c, scroll_frame))
            btn.pack(side="left", padx=3)

        tk.Frame(filter_bar, bg=C["border_bright"], height=1).pack(fill="x")

        # Scrollable grid
        scroll_wrapper = tk.Frame(frame, bg=C["bg_deep"])
        scroll_wrapper.pack(fill="both", expand=True)

        vscroll = tk.Scrollbar(scroll_wrapper, orient="vertical",
                               bg=C["bg_panel"], troughcolor=C["bg_deep"],
                               activebackground=C["accent_green"])
        vscroll.pack(side="right", fill="y")

        self._equip_canvas = tk.Canvas(scroll_wrapper, bg=C["bg_deep"],
                                       yscrollcommand=vscroll.set,
                                       highlightthickness=0)
        self._equip_canvas.pack(side="left", fill="both", expand=True)
        vscroll.config(command=self._equip_canvas.yview)

        scroll_frame = tk.Frame(self._equip_canvas, bg=C["bg_deep"])
        self._equip_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def on_configure(e):
            self._equip_canvas.configure(scrollregion=self._equip_canvas.bbox("all"))
        scroll_frame.bind("<Configure>", on_configure)

        # Scroll com roda do mouse
        def on_mousewheel(e):
            self._equip_canvas.yview_scroll(-1 * (e.delta // 120), "units")
        self._equip_canvas.bind("<MouseWheel>", on_mousewheel)

        self._equip_scroll_frame = scroll_frame
        self._render_equip_grid(scroll_frame, EQUIPAMENTOS)

    def _filter_equip(self, category, scroll_frame):
        for w in scroll_frame.winfo_children():
            w.destroy()
        if category == "TODOS":
            items = EQUIPAMENTOS
        else:
            items = [e for e in EQUIPAMENTOS if e["categoria"] == category]
        self._render_equip_grid(scroll_frame, items)

    def _render_equip_grid(self, parent, items):
        cols = 3
        for i, equip in enumerate(items):
            row = i // cols
            col = i % cols
            card = self._make_equip_card(parent, equip)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

        for c in range(cols):
            parent.columnconfigure(c, weight=1)

    def _make_equip_card(self, parent, equip):
        card = tk.Frame(parent, bg="#0d1117", relief="flat",
                        highlightbackground=C["border_bright"],
                        highlightthickness=1, cursor="hand2")

        # Header do card com emoji grande
        header = tk.Frame(card, bg="#111820", height=120)
        header.pack(fill="x")
        header.pack_propagate(False)

        emoji_canvas = tk.Canvas(header, width=80, height=80,
                                 bg="#111820", highlightthickness=0)
        emoji_canvas.pack(pady=10)

        # Emoji + background circular
        emoji_canvas.create_oval(5, 5, 75, 75,
                                 fill="#1a2030", outline=C["border_bright"], width=1)
        emoji_canvas.create_text(40, 42, text=equip["emoji"],
                                 font=("Segoe UI Emoji", 28))

        # Badge de nível
        badge = tk.Label(header, text=f"  {equip['nivel']}  ",
                         font=self.fnt["tag"],
                         fg="black" if equip["nivel"] != "RESTRITO" else "white",
                         bg=equip["cor_nivel"])
        badge.place(relx=1.0, y=4, anchor="ne", x=-4)

        # Nome
        tk.Label(card, text=equip["nome"],
                 font=self.fnt["h3"], fg=C["text_main"],
                 bg="#0d1117", wraplength=220).pack(pady=(8, 2), padx=12)

        # Categoria
        tk.Label(card, text=equip["categoria"],
                 font=self.fnt["tag"], fg=C["accent_green"],
                 bg="#0d1117").pack()

        # Separador
        tk.Frame(card, bg=C["border"], height=1).pack(fill="x", padx=12, pady=6)

        # Descrição
        tk.Label(card, text=equip["descricao"],
                 font=self.fnt["body"], fg=C["text_dim"],
                 bg="#0d1117", wraplength=220,
                 justify="left").pack(padx=12, anchor="w")

        # Specs
        for spec in equip["specs"]:
            tk.Label(card, text=f"• {spec}",
                     font=self.fnt["mono"], fg="#445566",
                     bg="#0d1117", anchor="w").pack(padx=16, anchor="w")

        # Botão
        btn_frame = tk.Frame(card, bg="#0d1117")
        btn_frame.pack(fill="x", padx=12, pady=10)
        btn = tk.Button(btn_frame,
                        text="▶ VER DETALHES",
                        font=self.fnt["tag"],
                        fg=equip["cor_nivel"], bg="#0d1117",
                        activebackground="#1a1a2a",
                        activeforeground=equip["cor_nivel"],
                        relief="flat", cursor="hand2",
                        command=lambda e=equip: self._open_equip_detail(e))
        btn.pack(fill="x")

        # Hover
        def on_enter(e, c=card):
            c.config(highlightbackground=C["accent_green"])
        def on_leave(e, c=card):
            c.config(highlightbackground=C["border_bright"])
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e, eq=equip: self._open_equip_detail(eq))

        return card

    def _open_equip_detail(self, equip):
        """Abre janela de detalhes do equipamento."""
        win = tk.Toplevel(self.root)
        win.title(f"DETALHES — {equip['nome'].upper()}")
        win.configure(bg=C["bg_deep"])
        win.geometry("560x520")
        win.resizable(False, False)
        win.grab_set()

        # Centralizar
        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 560) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 520) // 2
        win.geometry(f"560x520+{x}+{y}")

        # Header
        hdr = tk.Frame(win, bg=equip["cor_nivel"], height=6)
        hdr.pack(fill="x")

        main = tk.Frame(win, bg=C["bg_deep"])
        main.pack(fill="both", expand=True, padx=30, pady=20)

        # Emoji
        tk.Label(main, text=equip["emoji"],
                 font=("Segoe UI Emoji", 56),
                 bg=C["bg_deep"]).pack()

        tk.Label(main, text=equip["nome"].upper(),
                 font=self.fnt["h2"], fg=C["text_main"],
                 bg=C["bg_deep"]).pack(pady=(8, 2))

        tk.Label(main, text=equip["categoria"],
                 font=self.fnt["label"], fg=equip["cor_nivel"],
                 bg=C["bg_deep"]).pack()

        tk.Frame(main, bg=C["border_bright"], height=1).pack(fill="x", pady=12)

        # Nível
        level_frame = tk.Frame(main, bg=C["bg_deep"])
        level_frame.pack(anchor="w")
        tk.Label(level_frame, text="NÍVEL DE PRIORIDADE: ",
                 font=self.fnt["label"], fg=C["text_dim"],
                 bg=C["bg_deep"]).pack(side="left")
        tk.Label(level_frame, text=f"  {equip['nivel']}  ",
                 font=self.fnt["label"],
                 fg="white", bg=equip["cor_nivel"]).pack(side="left")

        tk.Frame(main, bg=C["border"], height=1).pack(fill="x", pady=8)

        tk.Label(main, text="DESCRIÇÃO TÉCNICA:",
                 font=self.fnt["label"], fg=C["text_dim"],
                 bg=C["bg_deep"], anchor="w").pack(anchor="w")
        tk.Label(main, text=equip["descricao"],
                 font=("Courier New", 10), fg=C["text_main"],
                 bg=C["bg_deep"], wraplength=500,
                 justify="left").pack(anchor="w", pady=(4, 12))

        tk.Label(main, text="ESPECIFICAÇÕES:",
                 font=self.fnt["label"], fg=C["text_dim"],
                 bg=C["bg_deep"], anchor="w").pack(anchor="w")
        for spec in equip["specs"]:
            row = tk.Frame(main, bg=C["bg_deep"])
            row.pack(fill="x", pady=1)
            tk.Label(row, text="▪", fg=equip["cor_nivel"],
                     bg=C["bg_deep"], font=self.fnt["nav"]).pack(side="left")
            tk.Label(row, text=f" {spec}",
                     font=self.fnt["mono"], fg=C["text_main"],
                     bg=C["bg_deep"]).pack(side="left")

        tk.Frame(main, bg=C["border_bright"], height=1).pack(fill="x", pady=12)

        tk.Button(main, text="✕  FECHAR",
                  font=self.fnt["nav"],
                  fg=C["text_dim"], bg=C["border"],
                  activebackground=C["accent_red"],
                  activeforeground="white",
                  relief="flat", padx=20, pady=6, cursor="hand2",
                  command=win.destroy).pack()

    # ─── Loop de animação / relógio ───────────────────────────────
    def _animate_loop(self):
        now = time.strftime("%H:%M:%S")
        self.clock_var.set(now)
        self.root.after(1000, self._animate_loop)

    # ─── Iniciar ──────────────────────────────────────────────────
    def run(self):
        self.root.mainloop()
    
    def _create_mission(self):
        win = tk.Toplevel(self.root)
        win.title("CRIAR MISSÃO")
        win.geometry("400x300")
        win.configure(bg=C["bg_deep"])
        win.grab_set()

        tk.Label(
            win,
            text="NOVA MISSÃO TÁTICA",
            font=self.fnt["h3"],
            fg=C["accent_red"],
            bg=C["bg_deep"]
        ).pack(pady=10)

        tk.Label(
            win,
            text="Interface de criação em desenvolvimento...",
            font=self.fnt["mono"],
            fg=C["text_dim"],
            bg=C["bg_deep"]
        ).pack(pady=20)

        tk.Button(
            win,
            text="FECHAR",
            command=win.destroy,
            bg=C["border"],
            fg=C["text_main"],
            relief="flat"
        ).pack(pady=10)


# ══════════════════════════════════════════════════════════════════
#  PONTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  MEDICINA TÁTICA — Controle de Missão  ")
    print("  Iniciando sistema...")
    print("=" * 60)
    app = MedicinaTatica()
    app.run()   