"""
╔══════════════════════════════════════════════════════════════════╗
║         MEDICINA TÁTICA E CONTROLE DE MISSÃO                    ║
║         Suporte Médico Inteligente em Zonas de Conflito         ║
╚══════════════════════════════════════════════════════════════════╝

DEPENDÊNCIAS:
  pip install pillow requests matplotlib numpy tkintermapview geopandas geodatasets

EXECUÇÃO:
  python medicina_tatica.py
"""

import tkinter as tk
from tkinter import ttk, font, simpledialog, colorchooser
import math
import time
import threading
import sys
import subprocess

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
check_and_install("geodatasets")
check_and_install("geopandas")

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
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
from PIL import Image, ImageTk, ImageDraw
import geopandas as gpd

# ─────────────────────────────────────────────
#  PALETA DE CORES
# ─────────────────────────────────────────────
C = {
    "bg_deep":      "#0a0c0f",
    "bg_panel":     "#0f1318",
    "bg_sidebar":   "#080b0e",
    "accent_red":   "#c8102e",
    "accent_green": "#1aff6a",
    "accent_amber": "#ffb300",
    "accent_blue":  "#1e90ff",
    "text_main":    "#e8e8e8",
    "text_dim":     "#6b7280",
    "text_green":   "#4ade80",
    "border":       "#1f2937",
    "border_bright":"#374151",
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
    "red": [
        "Russia", "Ukraine", "Israel", "Iran",
        "Lebanon", "United States of America"
    ],
    "yellow": [
        "Sudan", "Myanmar", "Syria", "Yemen",
        "Somalia", "Ethiopia", "Haiti", "Dem. Rep. Congo"
    ],
    "purple": [
        "Pakistan", "Afghanistan", "Venezuela", "Mali",
        "Burkina Faso", "Niger", "Taiwan", "North Korea",
        "Mexico", "Libya"
    ],
}

COUNTRY_COORDS = {
    "Rússia": (62.0, 95.0), "Ucrânia": (49.0, 32.0),
    "Israel": (31.5, 34.8), "Irã": (32.0, 53.0),
    "Líbano": (33.9, 35.5), "Estados Unidos": (38.0, -97.0),
    "Sudão": (15.0, 30.0), "Myanmar": (19.0, 96.0),
    "Síria": (34.8, 38.9), "Iêmen": (15.5, 48.0),
    "Somália": (5.5, 46.2), "Etiópia": (9.1, 40.5),
    "Haiti": (18.9, -72.3), "República Democrática do Congo": (-4.0, 21.8),
    "Paquistão": (30.0, 69.0), "Afeganistão": (33.0, 65.0),
    "Venezuela": (6.4, -66.6), "Mali": (17.5, -4.0),
    "Burkina Faso": (12.4, -1.6), "Níger": (17.6, 8.1),
    "Taiwan": (23.7, 121.0), "Coreia do Norte": (40.3, 127.5),
    "México": (23.6, -102.6), "Líbia": (26.3, 17.2),
}

# ─────────────────────────────────────────────
#  EQUIPAMENTOS
# ─────────────────────────────────────────────
EQUIPAMENTOS = [
    {
        "nome": "Torniquete SOFTT-W", "categoria": "Controle de Hemorragia",
        "descricao": "Torniquete tático de uma mão, padrão TCCC.",
        "nivel": "CRÍTICO", "cor_nivel": "#c8102e", "emoji": "🩸",
        "specs": ["Material: Alumínio + Nylon", "Tempo: <30s", "Peso: 155g"],
    },
    {
        "nome": "Curativo Hemostático", "categoria": "Controle de Hemorragia",
        "descricao": "Curativo com QuikClot para feridas de cavidade.",
        "nivel": "CRÍTICO", "cor_nivel": "#c8102e", "emoji": "🩹",
        "specs": ["Agente: Caulim zeólita", "Absorção: 3x", "Validade: 5 anos"],
    },
    {
        "nome": "Descompressor de Tórax", "categoria": "Via Aérea / Respiração",
        "descricao": "Agulha 14G para pneumotórax hipertensivo.",
        "nivel": "CRÍTICO", "cor_nivel": "#c8102e", "emoji": "🫁",
        "specs": ["Calibre: 14G", "Comprimento: 8.3cm", "Uso: Imediato"],
    },
    {
        "nome": "Selante de Tórax", "categoria": "Via Aérea / Respiração",
        "descricao": "Curativo oclusivo com válvula unidirecional.",
        "nivel": "URGENTE", "cor_nivel": "#ff6b35", "emoji": "🔴",
        "specs": ["Tipo: Hyfin Chest Seal", "Válvulas: 3", "Aderência: Máxima"],
    },
    {
        "nome": "Bandagem Israelense", "categoria": "Controle de Hemorragia",
        "descricao": "Emergency Pressure Dressing com aplicador integrado.",
        "nivel": "URGENTE", "cor_nivel": "#ff6b35", "emoji": "🏥",
        "specs": ["Tamanho: 6/4 pol.", "Pressão: Dupla", "Estéril: Sim"],
    },
    {
        "nome": "Colar Cervical", "categoria": "Imobilização",
        "descricao": "Colar cervical tático dobrável, semi-rígido.",
        "nivel": "PADRÃO", "cor_nivel": "#ffb300", "emoji": "🦴",
        "specs": ["Tipo: Semi-rígido", "Regulável: Sim", "Radiopaco: Sim"],
    },
    {
        "nome": "Oxímetro Tático", "categoria": "Monitoramento",
        "descricao": "Oxímetro resistente à água e impacto.",
        "nivel": "PADRÃO", "cor_nivel": "#ffb300", "emoji": "📡",
        "specs": ["IP: 22", "Bateria: 12h", "Precisão: ±2%"],
    },
    {
        "nome": "Kit de Via Aérea", "categoria": "Via Aérea / Respiração",
        "descricao": "NPA 28Fr com gel lubrificante.",
        "nivel": "CRÍTICO", "cor_nivel": "#c8102e", "emoji": "💨",
        "specs": ["Calibre: 28Fr", "Material: PVC", "Uso: Pré-hospitalar"],
    },
    {
        "nome": "Maca Dobrável SKED", "categoria": "Transporte",
        "descricao": "Maca de resgate ultracompacta.",
        "nivel": "PADRÃO", "cor_nivel": "#ffb300", "emoji": "🚁",
        "specs": ["Carga: 272kg", "Peso: 3.2kg", "Material: Polietileno"],
    },
    {
        "nome": "Morphine Autoinjector", "categoria": "Analgesia",
        "descricao": "Autoinjector de morfina para campo.",
        "nivel": "RESTRITO", "cor_nivel": "#7c3aed", "emoji": "💉",
        "specs": ["Dose: 10mg/0.7ml", "Via: IM", "Ação: 3-5 min"],
    },
    {
        "nome": "Rolo Hemostático", "categoria": "Controle de Hemorragia",
        "descricao": "Gaze com chitosan para feridas de cavidade.",
        "nivel": "URGENTE", "cor_nivel": "#ff6b35", "emoji": "🌀",
        "specs": ["Agente: Chitosano", "Tamanho: 7.6x3.7m", "Hemostasia: 3min"],
    },
    {
        "nome": "Desfibrilador DEA", "categoria": "Suporte Avançado",
        "descricao": "DEA portátil para PCR no campo de batalha.",
        "nivel": "AVANÇADO", "cor_nivel": "#1e90ff", "emoji": "⚡",
        "specs": ["Energia: 200J bifásico", "IP: 55", "Bateria: 200 choques"],
    },
]

DRONES = [
    {"nome": "FPV Recon X1", "categoria": "Reconhecimento FPV",
     "descricao": "Drone FPV de reconhecimento tático.", "emoji": "🚁", "nivel": "TÁTICO"},
    {"nome": "Ghost FPV Raptor", "categoria": "Ataque / Recon",
     "descricao": "FPV de alta velocidade para curta distância.", "emoji": "🛸", "nivel": "AVANÇADO"},
    {"nome": "Silent Observer VTOL", "categoria": "Vigilância",
     "descricao": "VTOL híbrido para observação prolongada.", "emoji": "🛰️", "nivel": "STRATEGIC"},
]

# Adesivos disponíveis para o mapa de missão
STICKERS = [
    {"label": "⚠️ PERIGO",      "color": "#ffb300", "text": "⚠ PERIGO"},
    {"label": "💀 ZONA MORTAL", "color": "#c8102e", "text": "☠ ZONA MORTAL"},
    {"label": "🏥 MED",         "color": "#1aff6a", "text": "✚ POSTO MED"},
    {"label": "🚁 EVAC",        "color": "#1e90ff", "text": "⬆ EVAC"},
    {"label": "🔴 INIMIGO",     "color": "#ff2200", "text": "◉ INIMIGO"},
    {"label": "🟢 AMIGO",       "color": "#00ff88", "text": "◉ AMIGO"},
    {"label": "💣 EXPLOSIVOS",  "color": "#ff6600", "text": "✸ EXPLOSIVOS"},
    {"label": "📡 COMMS",       "color": "#aa44ff", "text": "◈ COMMS"},
]


# ══════════════════════════════════════════════════════════════════
#  CLASSE PRINCIPAL
# ══════════════════════════════════════════════════════════════════
class MedicinaTatica:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MEDICINA TÁTICA — Sistema de Controle de Missão")
        self.root.configure(bg=C["bg_deep"])
        self._setup_window()
        self._load_fonts()

        # Estado do modo missão
        self.mission_mode = False
        self.mission_draw_mode = "traço"   # "traço" ou "adesivo"
        self.mission_sticker_type = STICKERS[0]
        self.mission_color = C["accent_red"]
        self._draw_points = []             # pontos do traço atual
        self._all_traces = []              # lista de traços completos [(pts, cor)]
        self._all_stickers = []            # lista de adesivos [(x,y, sticker)]
        self._drawing_active = False

        self._build_ui()
        self._animate_loop()

    def _setup_window(self):
        w, h = 1400, 860
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.minsize(1100, 700)
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

    # ─── UI principal ─────────────────────────────────────────────
    def _build_ui(self):
        self.root_frame = tk.Frame(self.root, bg=C["bg_deep"])
        self.root_frame.pack(fill="both", expand=True)
        self._build_header()
        self.body = tk.Frame(self.root_frame, bg=C["bg_deep"])
        self.body.pack(fill="both", expand=True)
        self._build_sidebar()
        self._build_content_area()
        self._build_footer()
        self._show_home()

    def _build_header(self):
        hdr = tk.Frame(self.root_frame, bg=C["bg_panel"], height=90)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C["accent_red"], height=3).pack(fill="x", side="top")
        inner = tk.Frame(hdr, bg=C["bg_panel"])
        inner.pack(fill="both", expand=True, padx=20, pady=8)

        left = tk.Frame(inner, bg=C["bg_panel"])
        left.pack(side="left", fill="y")
        self.logo_canvas = tk.Canvas(left, width=60, height=60,
                                     bg=C["bg_panel"], highlightthickness=0)
        self.logo_canvas.pack(side="left", padx=(0, 16))
        self._draw_cross(self.logo_canvas, 30, 30, 22)

        title_frame = tk.Frame(inner, bg=C["bg_panel"])
        title_frame.pack(side="left", fill="y")
        tk.Label(title_frame, text="MEDICINA TÁTICA E CONTROLE DE MISSÃO",
                 font=self.fnt["title"], fg=C["accent_red"],
                 bg=C["bg_panel"]).pack(anchor="w")
        tk.Label(title_frame, text="tornando o suporte médico mais inteligente",
                 font=self.fnt["subtitle"], fg=C["text_dim"],
                 bg=C["bg_panel"]).pack(anchor="w")

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
        canvas.create_rectangle(cx-t+2, cy-size+2, cx+t+2, cy+size+2,
                                 fill="#5a0010", outline="", tags="cross")
        canvas.create_rectangle(cx-size+2, cy-t+2, cx+size+2, cy+t+2,
                                 fill="#5a0010", outline="", tags="cross")
        canvas.create_rectangle(cx-t, cy-size, cx+t, cy+size,
                                 fill=color, outline="", tags="cross")
        canvas.create_rectangle(cx-size, cy-t, cx+size, cy+t,
                                 fill=color, outline="", tags="cross")

    def _build_sidebar(self):
        sidebar = tk.Frame(self.body, bg=C["bg_sidebar"], width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Frame(sidebar, bg=C["accent_red"], width=2).pack(side="right", fill="y")

        inner = tk.Frame(sidebar, bg=C["bg_sidebar"])
        inner.pack(fill="both", expand=True)

        tk.Frame(inner, bg=C["border_bright"], height=1).pack(fill="x", pady=(16, 0))
        tk.Label(inner, text="◈ CONTROLES DE MISSÃO",
                 font=self.fnt["mono"], fg=C["text_dim"],
                 bg=C["bg_sidebar"]).pack(anchor="w", padx=16, pady=(6, 4))
        tk.Frame(inner, bg=C["border_bright"], height=1).pack(fill="x")

        self.nav_buttons = {}
        nav_items = [
            ("🏠", "HOME",           self._show_home),
            ("🌍", "SITUAÇÃO ATUAL", self._show_situacao),
            ("🗺️", "PLANEJAMENTO",   self._show_planejamento),
            ("⚕️", "EQUIPAMENTOS",   self._show_equipamentos),
            ("🚁", "DRONES",         self._show_drones),
            ("🌐", "ÓRBITA",         self._show_orbita),
        ]

        for icon, label, cmd in nav_items:
            btn_frame = tk.Frame(inner, bg=C["bg_sidebar"], cursor="hand2")
            btn_frame.pack(fill="x", pady=1)

            icon_lbl = tk.Label(btn_frame, text=icon,
                                font=("Segoe UI Emoji", 14),
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
                            tl=text_lbl, ind=indicator:
                            self._nav_hover(bf, il, tl, ind, True))
                widget.bind("<Leave>", lambda e, bf=btn_frame, il=icon_lbl,
                            tl=text_lbl, ind=indicator, lbl=label:
                            self._nav_hover(bf, il, tl, ind, False, lbl))
                widget.bind("<Button-1>", lambda e, c=cmd, lbl=label:
                            self._nav_click(c, lbl))

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
            bf.config(bg=C["hover"]); il.config(bg=C["hover"]); tl.config(bg=C["hover"])
        else:
            is_active = (label == getattr(self, "_active_nav", None))
            bg = "#1a0a0a" if is_active else C["bg_sidebar"]
            bf.config(bg=bg); il.config(bg=bg); tl.config(bg=bg)

    def _nav_click(self, cmd, label):
        self._active_nav = label
        for lbl, (bf, il, tl, ind) in self.nav_buttons.items():
            if lbl == label:
                bf.config(bg="#1a0a0a"); il.config(bg="#1a0a0a"); tl.config(bg="#1a0a0a")
                tl.config(fg=C["accent_red"]); ind.config(bg=C["accent_red"])
            else:
                bf.config(bg=C["bg_sidebar"]); il.config(bg=C["bg_sidebar"])
                tl.config(bg=C["bg_sidebar"]); tl.config(fg=C["text_main"])
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

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()
        plt.close("all")

    # ══════════════════════════════════════════════════════════════
    #  HOME — Mapa satélite
    # ══════════════════════════════════════════════════════════════
    def _show_home(self):
        self._clear_content()
        self._active_nav = "HOME"

        frame = tk.Frame(self.content, bg=C["bg_deep"])
        frame.pack(fill="both", expand=True)

        title_bar = tk.Frame(frame, bg="#100505", height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="🌍 MAPA GLOBAL TÁTICO — SATÉLITE EM TEMPO REAL",
                 font=self.fnt["h3"], fg=C["accent_red"], bg="#100505").pack(side="left", padx=16, pady=8)
        tk.Label(title_bar, text="GOOGLE SATELLITE • LIVE MAP SYSTEM",
                 font=self.fnt["mono"], fg=C["text_dim"], bg="#100505").pack(side="right", padx=16)
        tk.Frame(frame, bg=C["accent_red"], height=2).pack(fill="x")

        controls = tk.Frame(frame, bg=C["bg_panel"], height=42)
        controls.pack(fill="x")
        controls.pack_propagate(False)
        tk.Label(controls, text="CAMADAS:", font=self.fnt["label"],
                 fg=C["text_dim"], bg=C["bg_panel"]).pack(side="left", padx=(16, 8))

        if not HAS_MAPVIEW:
            tk.Label(controls, text="⚠ tkintermapview não instalado — instale com: pip install tkintermapview",
                     font=self.fnt["mono"], fg=C["accent_amber"], bg=C["bg_panel"]).pack(side="left")
            tk.Label(frame, text="MAPA INDISPONÍVEL\npip install tkintermapview",
                     font=self.fnt["h2"], fg=C["accent_amber"], bg=C["bg_deep"]).pack(expand=True)
            return

        self.home_map = tkintermapview.TkinterMapView(
            frame, corner_radius=0, bg_color=C["bg_deep"])
        self.home_map.pack(fill="both", expand=True)
        self.home_map.set_position(20, 0)
        self.home_map.set_zoom(2)

        def set_satellite():
            self.home_map.set_tile_server(
                "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga")
        def set_hybrid():
            self.home_map.set_tile_server(
                "https://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga")
        def set_terrain():
            self.home_map.set_tile_server(
                "https://mt0.google.com/vt/lyrs=p&hl=en&x={x}&y={y}&z={z}&s=Ga")
        def set_normal():
            self.home_map.set_tile_server(
                "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

        set_hybrid()

        btn_style = dict(font=self.fnt["tag"], fg=C["text_main"], bg=C["border"],
                         activebackground=C["accent_red"], activeforeground="white",
                         relief="flat", cursor="hand2", padx=10, pady=4)

        for txt, cmd in [("SATÉLITE", set_satellite), ("HÍBRIDO", set_hybrid),
                         ("TERRENO", set_terrain), ("PADRÃO", set_normal)]:
            tk.Button(controls, text=txt, command=cmd, **btn_style).pack(side="left", padx=2)

        self.home_map.set_marker(-29.790107, -55.767438, text="⚕ Centro de Operações")

        total = sum(len(v) for v in CONFLICT_ZONES.values())
        info_bar = tk.Frame(frame, bg="#0a0505", height=30)
        info_bar.pack(fill="x")
        info_bar.pack_propagate(False)
        tk.Label(info_bar,
                 text=f"  MONITORANDO {total} ZONAS  |  SCROLL = ZOOM  |  ARRASTAR = NAVEGAR",
                 font=self.fnt["mono"], fg=C["text_dim"], bg="#0a0505").pack(side="left", pady=6)

    # ══════════════════════════════════════════════════════════════
    #  SITUAÇÃO ATUAL — Mapa político colorido
    # ══════════════════════════════════════════════════════════════
    def _show_situacao(self):
        self._clear_content()

        frame = tk.Frame(self.content, bg=C["bg_deep"])
        frame.pack(fill="both", expand=True)

        title_bar = tk.Frame(frame, bg="#100505", height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="⚠ SITUAÇÃO GLOBAL — MAPA POLÍTICO INTERATIVO",
                 font=self.fnt["h3"], fg=C["accent_red"], bg="#100505").pack(side="left", padx=16, pady=8)

        # Loading label
        loading = tk.Label(frame, text="⏳ Carregando mapa geopolítico...",
                           font=self.fnt["h3"], fg=C["accent_amber"], bg=C["bg_deep"])
        loading.pack(expand=True)
        self.root.update()

        try:
            fig, ax = plt.subplots(figsize=(15, 8))
            fig.patch.set_facecolor("#08080f")
            ax.set_facecolor("#08080f")

            countries = gpd.read_file(
                "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
            )
            countries["color"] = "#1a1a2a"
            countries.loc[countries["NAME"].isin(CONFLICT_ZONES["red"]), "color"] = "#c8102e"
            countries.loc[countries["NAME"].isin(CONFLICT_ZONES["yellow"]), "color"] = "#b8860b"
            countries.loc[countries["NAME"].isin(CONFLICT_ZONES["purple"]), "color"] = "#5b21b6"

            loading.destroy()

            map_frame = tk.Frame(frame, bg=C["bg_deep"])
            map_frame.pack(fill="both", expand=True)

            countries.plot(ax=ax, color=countries["color"],
                           edgecolor="#303030", linewidth=0.5)
            ax.axis("off")
            fig.tight_layout(pad=0)

            canvas = FigureCanvasTkAgg(fig, master=map_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            loading.config(text=f"❌ Erro ao carregar mapa: {e}\nVerifique conexão com internet.",
                           fg=C["accent_red"])
            return

        legend_frame = tk.Frame(frame, bg="#050505", height=40)
        legend_frame.pack(fill="x")
        legend_frame.pack_propagate(False)
        tk.Label(legend_frame,
                 text="VERMELHO = CONFLITO ATIVO   |   AMARELO = INSTABILIDADE   |   ROXO = RISCO ELEVADO   |   ESCURO = SEM ALERTA",
                 font=self.fnt["mono"], fg=C["text_dim"], bg="#050505").pack(pady=10)

    # ══════════════════════════════════════════════════════════════
    #  PLANEJAMENTO — Mapa com ferramentas de missão
    # ══════════════════════════════════════════════════════════════
    def _show_planejamento(self):
        self._clear_content()

        # Reset estado de missão ao entrar na aba
        self.mission_mode = False
        self._draw_points = []
        self._all_traces = []
        self._all_stickers = []
        self._drawing_active = False

        frame = tk.Frame(self.content, bg=C["bg_deep"])
        frame.pack(fill="both", expand=True)

        title_bar = tk.Frame(frame, bg="#050a14", height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="🗺  PLANEJAMENTO DE MISSÃO — MAPA TÁTICO INTERATIVO",
                 font=self.fnt["h3"], fg=C["accent_blue"], bg="#050a14").pack(side="left", padx=16, pady=8)
        tk.Frame(frame, bg=C["accent_blue"], height=2).pack(fill="x")

        if HAS_MAPVIEW:
            self._build_planejamento_mapview(frame)
        else:
            self._build_planejamento_canvas(frame)

    # ── Planejamento com tkintermapview ───────────────────────────
    def _build_planejamento_mapview(self, parent):
        """
        Com tkintermapview, o mapa real fica ao fundo.
        Um Canvas tk transparente sobreposto captura cliques para
        desenho de traços e adesivos.
        """
        # Barra de controle superior
        ctrl = tk.Frame(parent, bg=C["bg_panel"])
        ctrl.pack(fill="x")
        ctrl_inner = tk.Frame(ctrl, bg=C["bg_panel"])
        ctrl_inner.pack(padx=16, pady=6, fill="x")

        # ── botão CRIAR MISSÃO ────────────────────────────────────
        self._mission_btn_var = tk.StringVar(value="✏  CRIAR MISSÃO")
        self._mission_btn = tk.Button(
            ctrl_inner, textvariable=self._mission_btn_var,
            font=self.fnt["label"],
            fg=C["accent_red"], bg=C["border"],
            activebackground=C["accent_red"], activeforeground="white",
            relief="flat", cursor="hand2", padx=12, pady=5,
            command=self._toggle_mission_mapview)
        self._mission_btn.pack(side="left", padx=(0, 16))

        # ── painel de ferramentas da missão (oculto por padrão) ──
        self._mission_toolbar = tk.Frame(ctrl_inner, bg=C["bg_panel"])
        # não empacotado ainda

        # sub-ferramentas
        tk.Label(self._mission_toolbar, text="FERRAMENTA:",
                 font=self.fnt["tag"], fg=C["text_dim"],
                 bg=C["bg_panel"]).pack(side="left", padx=(0, 6))

        self._tool_var = tk.StringVar(value="traço")
        for txt, val in [("✏ TRAÇO", "traço"), ("📌 ADESIVO", "adesivo"), ("🗑 LIMPAR", "limpar")]:
            tk.Button(self._mission_toolbar, text=txt,
                      font=self.fnt["tag"],
                      fg=C["text_main"], bg="#1a2030",
                      activebackground=C["accent_blue"],
                      relief="flat", cursor="hand2", padx=8, pady=4,
                      command=lambda v=val: self._set_tool_mapview(v)
                      ).pack(side="left", padx=2)

        # cor do traço
        self._color_btn = tk.Button(self._mission_toolbar, text="  COR  ",
                                     font=self.fnt["tag"],
                                     fg="black", bg=self.mission_color,
                                     relief="flat", cursor="hand2", padx=8, pady=4,
                                     command=self._pick_color)
        self._color_btn.pack(side="left", padx=6)

        # tipo de adesivo
        self._sticker_var = tk.StringVar(value=STICKERS[0]["label"])
        sticker_menu = tk.OptionMenu(self._mission_toolbar, self._sticker_var,
                                      *[s["label"] for s in STICKERS],
                                      command=self._set_sticker)
        sticker_menu.config(font=self.fnt["tag"], fg=C["text_main"],
                             bg=C["border"], activebackground=C["hover"],
                             relief="flat", cursor="hand2")
        sticker_menu.pack(side="left", padx=4)

        # ── botões de tile ────────────────────────────────────────
        tk.Label(ctrl_inner, text="CAMADA:", font=self.fnt["tag"],
                 fg=C["text_dim"], bg=C["bg_panel"]).pack(side="left", padx=(16, 4))

        btn_s = dict(font=self.fnt["tag"], fg=C["text_main"], bg=C["border"],
                     activebackground=C["accent_blue"], activeforeground="white",
                     relief="flat", cursor="hand2", padx=8, pady=4)

        # guardamos referência ao widget do mapa para tiles
        self._plan_map_ref = None

        def _tile(url):
            if self._plan_map_ref:
                self._plan_map_ref.set_tile_server(url)

        for txt, url in [
            ("SATÉLITE", "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga"),
            ("HÍBRIDO",  "https://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga"),
            ("PADRÃO",   "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"),
        ]:
            tk.Button(ctrl_inner, text=txt, command=lambda u=url: _tile(u),
                      **btn_s).pack(side="left", padx=2)

        # ── Container do mapa + canvas overlay ───────────────────
        map_container = tk.Frame(parent, bg=C["bg_deep"])
        map_container.pack(fill="both", expand=True)

        self._plan_map_ref = tkintermapview.TkinterMapView(
            map_container, corner_radius=0, bg_color=C["bg_deep"])
        self._plan_map_ref.pack(fill="both", expand=True)
        self._plan_map_ref.set_position(20, 0)
        self._plan_map_ref.set_zoom(3)
        self._plan_map_ref.set_tile_server(
            "https://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga")
        self._plan_map_ref.set_marker(-30, -55, text="⚕ Centro de Operações")

        # Canvas overlay para desenho (invisível, cobre o mapa)
        self._overlay = tk.Canvas(map_container, bg="", highlightthickness=0,
                                   cursor="crosshair")
        self._overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._overlay.config(bg="black")
        self._overlay.attributes = {}   # dummy

        # Começa transparente (não captura eventos)
        self._overlay_active = False
        self._overlay.lower()   # atrás do mapa por enquanto

        # Eventos do overlay
        self._overlay.bind("<ButtonPress-1>",   self._overlay_press)
        self._overlay.bind("<B1-Motion>",        self._overlay_drag)
        self._overlay.bind("<ButtonRelease-1>",  self._overlay_release)

        # Info bar
        info_bar = tk.Frame(parent, bg="#050510", height=28)
        info_bar.pack(fill="x")
        info_bar.pack_propagate(False)
        self._plan_info_var = tk.StringVar(
            value="CLIQUE EM 'CRIAR MISSÃO' PARA ATIVAR FERRAMENTAS DE DESENHO")
        tk.Label(info_bar, textvariable=self._plan_info_var,
                 font=self.fnt["mono"], fg=C["text_dim"], bg="#050510").pack(side="left", pady=6, padx=8)

    def _toggle_mission_mapview(self):
        self.mission_mode = not self.mission_mode
        if self.mission_mode:
            self._mission_btn_var.set("⏹  FINALIZAR MISSÃO")
            self._mission_btn.config(fg=C["accent_green"])
            self._mission_toolbar.pack(side="left")
            self._plan_info_var.set(
                "MODO MISSÃO ATIVO  |  ✏ TRAÇO: clique+arraste  |  📌 ADESIVO: clique  |  ESC = cancelar traço")
            # Ativa overlay
            self._overlay_active = True
            self._overlay.lift()
            self._overlay.config(bg="")
            # torna o canvas realmente transparente
            self._overlay.configure(bg=C["bg_deep"])
            # Hack: canvas TkAgg não tem transparência real; usamos alpha via wm_attributes
            # Em vez disso, deixamos bg igual ao fundo e desenhamos com stipple
            self._overlay.configure(bg="#0a0c0f")
            # Melhor abordagem: canvas com cor próxima de transparente
            # e os traços visíveis em cima
        else:
            self._mission_btn_var.set("✏  CRIAR MISSÃO")
            self._mission_btn.config(fg=C["accent_red"])
            self._mission_toolbar.pack_forget()
            self._plan_info_var.set("MODO MISSÃO DESATIVADO — mapa interativo normal")
            self._overlay_active = False
            self._overlay.lower()

    def _set_tool_mapview(self, tool):
        if tool == "limpar":
            self._all_traces.clear()
            self._all_stickers.clear()
            self._draw_points.clear()
            self._redraw_overlay()
            return
        self._tool_var.set(tool)
        self.mission_draw_mode = tool
        self._plan_info_var.set(
            f"FERRAMENTA: {tool.upper()}  |  {'clique+arraste para traçar' if tool=='traço' else 'clique para colocar adesivo'}")

    def _pick_color(self):
        color = colorchooser.askcolor(color=self.mission_color,
                                       title="Cor do traço")[1]
        if color:
            self.mission_color = color
            self._color_btn.config(bg=color)

    def _set_sticker(self, label):
        for s in STICKERS:
            if s["label"] == label:
                self.mission_sticker_type = s
                break

    def _overlay_press(self, event):
        if not self._overlay_active:
            return
        if self.mission_draw_mode == "traço":
            self._drawing_active = True
            self._draw_points = [(event.x, event.y)]
        elif self.mission_draw_mode == "adesivo":
            self._all_stickers.append((event.x, event.y,
                                        dict(self.mission_sticker_type)))
            self._redraw_overlay()

    def _overlay_drag(self, event):
        if not self._overlay_active or not self._drawing_active:
            return
        if self.mission_draw_mode == "traço":
            self._draw_points.append((event.x, event.y))
            self._redraw_overlay()

    def _overlay_release(self, event):
        if not self._overlay_active:
            return
        if self.mission_draw_mode == "traço" and self._drawing_active:
            if len(self._draw_points) > 1:
                self._all_traces.append((list(self._draw_points), self.mission_color))
            self._draw_points = []
            self._drawing_active = False
            self._redraw_overlay()

    def _redraw_overlay(self):
        self._overlay.delete("all")
        # Traços salvos
        for points, color in self._all_traces:
            if len(points) > 1:
                flat = [coord for pt in points for coord in pt]
                self._overlay.create_line(*flat, fill=color, width=3,
                                           smooth=True, capstyle="round",
                                           joinstyle="round")
        # Traço atual
        if len(self._draw_points) > 1:
            flat = [coord for pt in self._draw_points for coord in pt]
            self._overlay.create_line(*flat, fill=self.mission_color, width=3,
                                       smooth=True, capstyle="round", joinstyle="round",
                                       dash=(6, 3))
        # Adesivos
        for x, y, sticker in self._all_stickers:
            self._overlay.create_oval(x-18, y-18, x+18, y+18,
                                       fill="#000000cc", outline=sticker["color"], width=2)
            self._overlay.create_text(x, y, text=sticker["text"],
                                       fill=sticker["color"],
                                       font=("Courier New", 8, "bold"))

    # ── Planejamento FALLBACK (sem tkintermapview) ─────────────────
    def _build_planejamento_canvas(self, parent):
        info = tk.Frame(parent, bg="#050a14")
        info.pack(fill="x")
        tk.Label(info, text="  ⓘ  Modo offline — instale 'tkintermapview' para mapa satélite",
                 font=self.fnt["mono"], fg=C["accent_amber"], bg="#050a14").pack(pady=4, anchor="w")

        # Barra de ferramentas
        ctrl = tk.Frame(parent, bg=C["bg_panel"])
        ctrl.pack(fill="x")
        ctrl_inner = tk.Frame(ctrl, bg=C["bg_panel"])
        ctrl_inner.pack(padx=16, pady=6, fill="x")

        self._mission_btn_var = tk.StringVar(value="✏  CRIAR MISSÃO")
        self._mission_btn = tk.Button(
            ctrl_inner, textvariable=self._mission_btn_var,
            font=self.fnt["label"], fg=C["accent_red"], bg=C["border"],
            activebackground=C["accent_red"], activeforeground="white",
            relief="flat", cursor="hand2", padx=12, pady=5,
            command=self._toggle_mission_canvas)
        self._mission_btn.pack(side="left", padx=(0, 16))

        self._mission_toolbar_fb = tk.Frame(ctrl_inner, bg=C["bg_panel"])

        tk.Label(self._mission_toolbar_fb, text="FERRAMENTA:",
                 font=self.fnt["tag"], fg=C["text_dim"],
                 bg=C["bg_panel"]).pack(side="left", padx=(0, 6))

        for txt, val in [("✏ TRAÇO", "traço"), ("📌 ADESIVO", "adesivo"), ("🗑 LIMPAR", "limpar")]:
            tk.Button(self._mission_toolbar_fb, text=txt,
                      font=self.fnt["tag"], fg=C["text_main"], bg="#1a2030",
                      activebackground=C["accent_blue"],
                      relief="flat", cursor="hand2", padx=8, pady=4,
                      command=lambda v=val: self._set_tool_canvas(v)
                      ).pack(side="left", padx=2)

        self._color_btn_fb = tk.Button(
            self._mission_toolbar_fb, text="  COR  ",
            font=self.fnt["tag"], fg="black", bg=self.mission_color,
            relief="flat", cursor="hand2", padx=8, pady=4,
            command=self._pick_color_canvas)
        self._color_btn_fb.pack(side="left", padx=6)

        self._sticker_var_fb = tk.StringVar(value=STICKERS[0]["label"])
        sticker_menu = tk.OptionMenu(self._mission_toolbar_fb, self._sticker_var_fb,
                                      *[s["label"] for s in STICKERS],
                                      command=self._set_sticker_canvas)
        sticker_menu.config(font=self.fnt["tag"], fg=C["text_main"],
                             bg=C["border"], activebackground=C["hover"],
                             relief="flat", cursor="hand2")
        sticker_menu.pack(side="left", padx=4)

        # Zoom buttons
        for txt, factor in [("  +  ", 0.65), ("  −  ", 1.35), ("RESET", None)]:
            def zoom_btn(f=factor):
                if f is None:
                    self._fb_xlim = [-180.0, 180.0]
                    self._fb_ylim = [-90.0, 90.0]
                else:
                    cx = (self._fb_xlim[0] + self._fb_xlim[1]) / 2
                    cy = (self._fb_ylim[0] + self._fb_ylim[1]) / 2
                    xr = (self._fb_xlim[1] - self._fb_xlim[0]) / 2 * f
                    yr = (self._fb_ylim[1] - self._fb_ylim[0]) / 2 * f
                    self._fb_xlim = [cx - xr, cx + xr]
                    self._fb_ylim = [cy - yr, cy + yr]
                self._fb_redraw()
            tk.Button(ctrl_inner, text=txt, font=self.fnt["nav"],
                      fg=C["text_main"], bg=C["border"],
                      activebackground=C["accent_blue"],
                      relief="flat", padx=10, pady=4, cursor="hand2",
                      command=zoom_btn).pack(side="right", padx=2)

        # Mapa matplotlib
        map_frame = tk.Frame(parent, bg=C["bg_deep"])
        map_frame.pack(fill="both", expand=True)

        self._fb_fig, self._fb_ax = plt.subplots(figsize=(13, 7), facecolor="#08080f")
        self._fb_ax.set_facecolor("#0a1018")
        self._fb_xlim = [-180.0, 180.0]
        self._fb_ylim = [-90.0, 90.0]
        self._fb_pan_start = None
        self.mission_draw_mode = "traço"
        self._fb_drawing = False
        self._fb_draw_pts = []

        self._fb_redraw()

        self._fb_canvas = FigureCanvasTkAgg(self._fb_fig, master=map_frame)
        self._fb_canvas.draw()
        widget = self._fb_canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)

        self._fb_canvas.mpl_connect("scroll_event",       self._fb_zoom)
        self._fb_canvas.mpl_connect("button_press_event", self._fb_press)
        self._fb_canvas.mpl_connect("button_release_event", self._fb_release)
        self._fb_canvas.mpl_connect("motion_notify_event", self._fb_motion)

        # Info bar
        info_bar = tk.Frame(parent, bg="#050510", height=28)
        info_bar.pack(fill="x")
        info_bar.pack_propagate(False)
        self._fb_info_var = tk.StringVar(value="CLIQUE EM 'CRIAR MISSÃO' PARA ATIVAR FERRAMENTAS")
        tk.Label(info_bar, textvariable=self._fb_info_var,
                 font=self.fnt["mono"], fg=C["text_dim"], bg="#050510").pack(side="left", pady=6, padx=8)
        self._fb_coord_var = tk.StringVar(value="LAT: --- | LON: ---")
        tk.Label(info_bar, textvariable=self._fb_coord_var,
                 font=self.fnt["mono"], fg=C["accent_green"], bg="#050510").pack(side="right", padx=8)

    def _toggle_mission_canvas(self):
        self.mission_mode = not self.mission_mode
        if self.mission_mode:
            self._mission_btn_var.set("⏹  FINALIZAR MISSÃO")
            self._mission_btn.config(fg=C["accent_green"])
            self._mission_toolbar_fb.pack(side="left")
            self._fb_info_var.set("MODO MISSÃO ATIVO | ✏ TRAÇO: arraste | 📌 ADESIVO: clique")
        else:
            self._mission_btn_var.set("✏  CRIAR MISSÃO")
            self._mission_btn.config(fg=C["accent_red"])
            self._mission_toolbar_fb.pack_forget()
            self._fb_info_var.set("MODO MISSÃO DESATIVADO")

    def _set_tool_canvas(self, tool):
        if tool == "limpar":
            self._all_traces.clear()
            self._all_stickers.clear()
            self._fb_draw_pts = []
            self._fb_redraw()
            return
        self.mission_draw_mode = tool

    def _pick_color_canvas(self):
        color = colorchooser.askcolor(color=self.mission_color,
                                       title="Cor do traço")[1]
        if color:
            self.mission_color = color
            self._color_btn_fb.config(bg=color)

    def _set_sticker_canvas(self, label):
        for s in STICKERS:
            if s["label"] == label:
                self.mission_sticker_type = s
                break

    def _fb_press(self, event):
        if event.xdata is None or event.ydata is None:
            return
        if self.mission_mode and self.mission_draw_mode == "adesivo" and event.button == 1:
            self._all_stickers.append((event.xdata, event.ydata,
                                        dict(self.mission_sticker_type)))
            self._fb_redraw()
            return
        if self.mission_mode and self.mission_draw_mode == "traço" and event.button == 1:
            self._fb_drawing = True
            self._fb_draw_pts = [(event.xdata, event.ydata)]
            return
        if event.button == 1:
            self._fb_pan_start = (event.xdata, event.ydata,
                                   self._fb_xlim[:], self._fb_ylim[:])

    def _fb_release(self, event):
        self._fb_pan_start = None
        if self._fb_drawing:
            self._fb_drawing = False
            if len(self._fb_draw_pts) > 1:
                self._all_traces.append((list(self._fb_draw_pts), self.mission_color))
            self._fb_draw_pts = []
            self._fb_redraw()

    def _fb_motion(self, event):
        if event.xdata and event.ydata:
            self._fb_coord_var.set(f"LAT: {event.ydata:+.2f}° | LON: {event.xdata:+.2f}°")

        if self._fb_drawing and event.xdata and event.ydata:
            self._fb_draw_pts.append((event.xdata, event.ydata))
            self._fb_redraw()
            return

        if self._fb_pan_start and event.xdata and event.ydata and not self.mission_mode:
            dx = self._fb_pan_start[0] - event.xdata
            dy = self._fb_pan_start[1] - event.ydata
            ox, oy = self._fb_pan_start[2], self._fb_pan_start[3]
            self._fb_xlim = [ox[0]+dx, ox[1]+dx]
            self._fb_ylim = [oy[0]+dy, oy[1]+dy]
            self._fb_clip()
            self._fb_redraw()

    def _fb_zoom(self, event):
        if event.xdata is None:
            return
        f = 0.7 if event.button == "up" else 1.3
        cx, cy = event.xdata, event.ydata
        xl, yl = self._fb_xlim, self._fb_ylim
        self._fb_xlim = [cx - (xl[1]-xl[0])/2*f, cx + (xl[1]-xl[0])/2*f]
        self._fb_ylim = [cy - (yl[1]-yl[0])/2*f, cy + (yl[1]-yl[0])/2*f]
        self._fb_clip()
        self._fb_redraw()

    def _fb_clip(self):
        xw = max(self._fb_xlim[1]-self._fb_xlim[0], 2)
        yw = max(self._fb_ylim[1]-self._fb_ylim[0], 2)
        if self._fb_xlim[0] < -180: self._fb_xlim = [-180.0, -180.0+xw]
        if self._fb_xlim[1] > 180:  self._fb_xlim = [180.0-xw, 180.0]
        if self._fb_ylim[0] < -90:  self._fb_ylim = [-90.0, -90.0+yw]
        if self._fb_ylim[1] > 90:   self._fb_ylim = [90.0-yw, 90.0]

    def _fb_redraw(self):
        ax = self._fb_ax
        ax.cla()
        ax.set_facecolor("#0a1018")
        xl, yl = self._fb_xlim, self._fb_ylim

        # Grade
        for x in np.arange(math.ceil(xl[0]/30)*30, xl[1], 30):
            ax.axvline(x, color="#0d2030", linewidth=0.4, linestyle="--")
        for y in np.arange(math.ceil(yl[0]/15)*15, yl[1], 15):
            ax.axhline(y, color="#0d2030", linewidth=0.4, linestyle="--")

        # Continentes
        self._draw_continents(ax)

        # Conflitos
        for country in CONFLICT_ZONES["red"]:
            if country in COUNTRY_COORDS:
                lat, lon = COUNTRY_COORDS[country]
                if xl[0] < lon < xl[1] and yl[0] < lat < yl[1]:
                    ax.scatter(lon, lat, s=120, c=C["accent_red"], zorder=5,
                               marker="*", edgecolors="white", linewidths=0.3)

        # Traços da missão
        for pts, color in self._all_traces:
            if len(pts) > 1:
                xs, ys = zip(*pts)
                ax.plot(xs, ys, color=color, linewidth=2.5,
                        solid_capstyle="round", zorder=8)

        # Traço atual
        if len(self._fb_draw_pts) > 1:
            xs, ys = zip(*self._fb_draw_pts)
            ax.plot(xs, ys, color=self.mission_color, linewidth=2,
                    linestyle="--", zorder=9)

        # Adesivos
        for sx, sy, sticker in self._all_stickers:
            ax.scatter(sx, sy, s=300, c=sticker["color"],
                       marker="o", alpha=0.3, zorder=10)
            ax.annotate(sticker["text"], (sx, sy),
                        xytext=(0, 6), textcoords="offset points",
                        fontsize=7, color=sticker["color"],
                        fontfamily="Courier New", fontweight="bold",
                        ha="center", zorder=11)

        ax.set_xlim(xl); ax.set_ylim(yl)
        ax.tick_params(colors="#334455", labelsize=6)
        for spine in ax.spines.values():
            spine.set_edgecolor("#1a2a3a")
        self._fb_fig.tight_layout(pad=0.2)
        self._fb_canvas.draw_idle()

    def _draw_continents(self, ax):
        continents = [
            [(-170,70),(-55,70),(-55,15),(-85,10),(-95,17),(-115,22),
             (-120,30),(-130,40),(-140,55),(-155,60),(-170,65),(-170,70)],
            [(-80,10),(-50,10),(-35,-5),(-35,-15),(-45,-23),(-55,-35),
             (-65,-55),(-75,-50),(-80,-20),(-80,10)],
            [(0,50),(30,70),(30,60),(40,55),(35,45),(25,38),(10,38),
             (-5,36),(-10,38),(-8,44),(-5,48),(0,50)],
            [(-18,15),(50,15),(52,10),(42,-12),(35,-35),(18,-35),(12,-20),
             (8,5),(10,8),(2,6),(-18,8),(-18,15)],
            [(25,70),(180,70),(180,0),(140,-10),(120,20),(100,10),(80,10),
             (60,22),(50,30),(40,36),(35,45),(40,55),(25,70)],
            [(115,-20),(155,-20),(155,-45),(140,-45),(115,-35),(110,-25),(115,-20)],
        ]
        for poly in continents:
            xs, ys = zip(*poly)
            ax.fill(xs, ys, color="#0d1a0d", alpha=0.85, zorder=1)
            ax.plot(list(xs)+[xs[0]], list(ys)+[ys[0]],
                    color="#1a3a1a", linewidth=0.6, zorder=2)
        ax.set_facecolor("#080c14")

    # ══════════════════════════════════════════════════════════════
    #  EQUIPAMENTOS
    # ══════════════════════════════════════════════════════════════
    def _show_equipamentos(self):
        self._clear_content()
        frame = tk.Frame(self.content, bg=C["bg_deep"])
        frame.pack(fill="both", expand=True)

        title_bar = tk.Frame(frame, bg="#050a05", height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="⚕  EQUIPAMENTOS MÉDICOS — SUPORTE TÁTICO DE CAMPO",
                 font=self.fnt["h3"], fg=C["accent_green"], bg="#050a05").pack(side="left", padx=16, pady=8)
        tk.Label(title_bar, text=f"  {len(EQUIPAMENTOS)} itens  |  Clique para detalhes",
                 font=self.fnt["mono"], fg=C["text_dim"], bg="#050a05").pack(side="right", padx=16)
        tk.Frame(frame, bg=C["accent_green"], height=2).pack(fill="x")

        filter_bar = tk.Frame(frame, bg=C["bg_panel"])
        filter_bar.pack(fill="x")
        f_inner = tk.Frame(filter_bar, bg=C["bg_panel"])
        f_inner.pack(padx=16, pady=6, anchor="w")
        tk.Label(f_inner, text="FILTRAR:", font=self.fnt["label"],
                 fg=C["text_dim"], bg=C["bg_panel"]).pack(side="left")
        cats = sorted(set(e["categoria"] for e in EQUIPAMENTOS))

        scroll_frame_holder = [None]

        for cat in ["TODOS"] + cats:
            tk.Button(f_inner, text=cat, font=self.fnt["tag"],
                      fg=C["text_main"], bg=C["border"],
                      activebackground=C["accent_green"], activeforeground="black",
                      relief="flat", padx=8, pady=3, cursor="hand2",
                      command=lambda c=cat: self._filter_equip(
                          c, scroll_frame_holder[0])
                      ).pack(side="left", padx=3)
        tk.Frame(filter_bar, bg=C["border_bright"], height=1).pack(fill="x")

        scroll_wrapper = tk.Frame(frame, bg=C["bg_deep"])
        scroll_wrapper.pack(fill="both", expand=True)
        vscroll = tk.Scrollbar(scroll_wrapper, orient="vertical",
                               bg=C["bg_panel"], troughcolor=C["bg_deep"])
        vscroll.pack(side="right", fill="y")
        equip_canvas = tk.Canvas(scroll_wrapper, bg=C["bg_deep"],
                                  yscrollcommand=vscroll.set, highlightthickness=0)
        equip_canvas.pack(side="left", fill="both", expand=True)
        vscroll.config(command=equip_canvas.yview)

        scroll_frame = tk.Frame(equip_canvas, bg=C["bg_deep"])
        equip_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        scroll_frame_holder[0] = scroll_frame

        def on_configure(e):
            equip_canvas.configure(scrollregion=equip_canvas.bbox("all"))
        scroll_frame.bind("<Configure>", on_configure)
        equip_canvas.bind("<MouseWheel>", lambda e: equip_canvas.yview_scroll(
            -1*(e.delta//120), "units"))

        self._render_equip_grid(scroll_frame, EQUIPAMENTOS)

    def _filter_equip(self, category, scroll_frame):
        if scroll_frame is None:
            return
        for w in scroll_frame.winfo_children():
            w.destroy()
        items = EQUIPAMENTOS if category == "TODOS" else [
            e for e in EQUIPAMENTOS if e["categoria"] == category]
        self._render_equip_grid(scroll_frame, items)

    def _render_equip_grid(self, parent, items):
        cols = 3
        for i, equip in enumerate(items):
            card = self._make_equip_card(parent, equip)
            card.grid(row=i//cols, column=i%cols, padx=12, pady=12, sticky="nsew")
        for c in range(cols):
            parent.columnconfigure(c, weight=1)

    def _make_equip_card(self, parent, equip):
        card = tk.Frame(parent, bg="#0d1117", relief="flat",
                        highlightbackground=C["border_bright"],
                        highlightthickness=1, cursor="hand2")
        header = tk.Frame(card, bg="#111820", height=120)
        header.pack(fill="x")
        header.pack_propagate(False)

        emoji_canvas = tk.Canvas(header, width=80, height=80,
                                  bg="#111820", highlightthickness=0)
        emoji_canvas.pack(pady=10)
        emoji_canvas.create_oval(5, 5, 75, 75, fill="#1a2030",
                                  outline=C["border_bright"], width=1)
        emoji_canvas.create_text(40, 42, text=equip["emoji"],
                                  font=("Segoe UI Emoji", 28))

        badge = tk.Label(header, text=f"  {equip['nivel']}  ",
                         font=self.fnt["tag"],
                         fg="black" if equip["nivel"] != "RESTRITO" else "white",
                         bg=equip["cor_nivel"])
        badge.place(relx=1.0, y=4, anchor="ne", x=-4)

        tk.Label(card, text=equip["nome"], font=self.fnt["h3"],
                 fg=C["text_main"], bg="#0d1117", wraplength=220).pack(pady=(8,2), padx=12)
        tk.Label(card, text=equip["categoria"], font=self.fnt["tag"],
                 fg=C["accent_green"], bg="#0d1117").pack()
        tk.Frame(card, bg=C["border"], height=1).pack(fill="x", padx=12, pady=6)
        tk.Label(card, text=equip["descricao"], font=self.fnt["body"],
                 fg=C["text_dim"], bg="#0d1117", wraplength=220,
                 justify="left").pack(padx=12, anchor="w")
        for spec in equip["specs"]:
            tk.Label(card, text=f"• {spec}", font=self.fnt["mono"],
                     fg="#445566", bg="#0d1117", anchor="w").pack(padx=16, anchor="w")

        btn = tk.Button(card, text="▶ VER DETALHES", font=self.fnt["tag"],
                        fg=equip["cor_nivel"], bg="#0d1117",
                        activebackground="#1a1a2a", relief="flat", cursor="hand2",
                        command=lambda e=equip: self._open_equip_detail(e))
        btn.pack(fill="x", padx=12, pady=10)

        card.bind("<Enter>", lambda e, c=card: c.config(highlightbackground=C["accent_green"]))
        card.bind("<Leave>", lambda e, c=card: c.config(highlightbackground=C["border_bright"]))
        card.bind("<Button-1>", lambda e, eq=equip: self._open_equip_detail(eq))
        return card

    def _open_equip_detail(self, equip):
        win = tk.Toplevel(self.root)
        win.title(f"DETALHES — {equip['nome'].upper()}")
        win.configure(bg=C["bg_deep"])
        win.geometry("560x520")
        win.resizable(False, False)
        win.grab_set()
        x = self.root.winfo_x() + (self.root.winfo_width()-560)//2
        y = self.root.winfo_y() + (self.root.winfo_height()-520)//2
        win.geometry(f"560x520+{x}+{y}")

        tk.Frame(win, bg=equip["cor_nivel"], height=6).pack(fill="x")
        main = tk.Frame(win, bg=C["bg_deep"])
        main.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(main, text=equip["emoji"], font=("Segoe UI Emoji", 56),
                 bg=C["bg_deep"]).pack()
        tk.Label(main, text=equip["nome"].upper(), font=self.fnt["h2"],
                 fg=C["text_main"], bg=C["bg_deep"]).pack(pady=(8,2))
        tk.Label(main, text=equip["categoria"], font=self.fnt["label"],
                 fg=equip["cor_nivel"], bg=C["bg_deep"]).pack()
        tk.Frame(main, bg=C["border_bright"], height=1).pack(fill="x", pady=12)

        lf = tk.Frame(main, bg=C["bg_deep"])
        lf.pack(anchor="w")
        tk.Label(lf, text="NÍVEL: ", font=self.fnt["label"],
                 fg=C["text_dim"], bg=C["bg_deep"]).pack(side="left")
        tk.Label(lf, text=f"  {equip['nivel']}  ", font=self.fnt["label"],
                 fg="white", bg=equip["cor_nivel"]).pack(side="left")

        tk.Frame(main, bg=C["border"], height=1).pack(fill="x", pady=8)
        tk.Label(main, text="DESCRIÇÃO:", font=self.fnt["label"],
                 fg=C["text_dim"], bg=C["bg_deep"], anchor="w").pack(anchor="w")
        tk.Label(main, text=equip["descricao"], font=("Courier New", 10),
                 fg=C["text_main"], bg=C["bg_deep"], wraplength=500,
                 justify="left").pack(anchor="w", pady=(4,12))
        tk.Label(main, text="ESPECIFICAÇÕES:", font=self.fnt["label"],
                 fg=C["text_dim"], bg=C["bg_deep"], anchor="w").pack(anchor="w")
        for spec in equip["specs"]:
            row = tk.Frame(main, bg=C["bg_deep"])
            row.pack(fill="x", pady=1)
            tk.Label(row, text="▪", fg=equip["cor_nivel"],
                     bg=C["bg_deep"], font=self.fnt["nav"]).pack(side="left")
            tk.Label(row, text=f" {spec}", font=self.fnt["mono"],
                     fg=C["text_main"], bg=C["bg_deep"]).pack(side="left")

        tk.Frame(main, bg=C["border_bright"], height=1).pack(fill="x", pady=12)
        tk.Button(main, text="✕  FECHAR", font=self.fnt["nav"],
                  fg=C["text_dim"], bg=C["border"],
                  activebackground=C["accent_red"], activeforeground="white",
                  relief="flat", padx=20, pady=6, cursor="hand2",
                  command=win.destroy).pack()

    # ══════════════════════════════════════════════════════════════
    #  DRONES
    # ══════════════════════════════════════════════════════════════
    def _show_drones(self):
        self._clear_content()
        frame = tk.Frame(self.content, bg=C["bg_deep"])
        frame.pack(fill="both", expand=True)

        title_bar = tk.Frame(frame, bg="#050510", height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="🚁 DRONES FPV — FROTA TÁTICA",
                 font=self.fnt["h3"], fg=C["accent_blue"], bg="#050510").pack(side="left", padx=16, pady=8)
        tk.Frame(frame, bg=C["accent_blue"], height=2).pack(fill="x")

        grid = tk.Frame(frame, bg=C["bg_deep"])
        grid.pack(fill="both", expand=True, padx=20, pady=20)

        for i, d in enumerate(DRONES):
            card = tk.Frame(grid, bg="#0d1117", relief="flat",
                            highlightthickness=1, highlightbackground=C["border_bright"],
                            cursor="hand2")
            card.grid(row=i//3, column=i%3, padx=12, pady=12, sticky="nsew")
            tk.Label(card, text=d["emoji"], font=("Segoe UI Emoji", 30),
                     bg="#0d1117").pack(pady=10)
            tk.Label(card, text=d["nome"], font=self.fnt["h3"],
                     fg=C["text_main"], bg="#0d1117", wraplength=200).pack()
            tk.Label(card, text=d["categoria"], font=self.fnt["tag"],
                     fg=C["accent_blue"], bg="#0d1117").pack()
            tk.Label(card, text=d["descricao"], font=self.fnt["body"],
                     fg=C["text_dim"], bg="#0d1117", wraplength=200,
                     justify="center").pack(pady=6, padx=8)
            tk.Button(card, text="▶ MODELO 3D", font=self.fnt["tag"],
                      fg=C["accent_blue"], bg="#0d1117", relief="flat",
                      cursor="hand2", pady=6,
                      command=lambda dr=d: self._open_drone_3d(dr)).pack(pady=10)
            card.bind("<Button-1>", lambda e, dr=d: self._open_drone_3d(dr))

        for c in range(3):
            grid.columnconfigure(c, weight=1)

    def _open_drone_3d(self, drone):
        win = tk.Toplevel(self.root)
        win.title(f"MODELO 3D — {drone['nome']}")
        win.geometry("700x580")
        win.configure(bg=C["bg_deep"])

        fig = plt.figure(figsize=(8, 6), facecolor="#050510")
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor("#050510")

        # Corpo central
        ax.plot([-0.4, 0.4], [0, 0], [0, 0], color="white", linewidth=5)
        ax.plot([0, 0], [-0.15, 0.15], [0, 0], color="white", linewidth=5)

        # Braços e hélices
        arm_coords = [(1.2,1.2), (-1.2,1.2), (1.2,-1.2), (-1.2,-1.2)]
        colors_arm = [C["accent_blue"], C["accent_green"],
                      C["accent_amber"], C["accent_red"]]
        for (ax_x, ax_y), ac in zip(arm_coords, colors_arm):
            ax.plot([0, ax_x], [0, ax_y], [0, 0], color=ac, linewidth=2.5)
            # Hélice
            theta = np.linspace(0, 2*np.pi, 40)
            hx = ax_x + 0.4 * np.cos(theta)
            hy = ax_y + 0.4 * np.sin(theta)
            hz = np.zeros(40)
            ax.plot(hx, hy, hz, color=ac, linewidth=1.5, alpha=0.6)
            ax.scatter([ax_x], [ax_y], [0], s=60, c=ac, zorder=5)

        # Camera
        ax.plot([0,0],[0,0],[0,-0.3], color="#888", linewidth=2)
        ax.scatter([0],[0],[-0.35], s=80, c="#00ccff")

        # LED corpo
        ax.scatter([0],[0],[0.05], s=200, c=C["accent_red"], alpha=0.8)

        ax.set_title(drone["nome"], color="white", fontfamily="Courier New",
                     fontsize=12, pad=10)
        ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-1, 1)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
            pane.fill = False
            pane.set_edgecolor("#1a2030")
        ax.grid(False)

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        tk.Label(win, text="Arraste para rotacionar | Scroll para zoom",
                 font=self.fnt["mono"], fg=C["text_dim"],
                 bg=C["bg_deep"]).pack(pady=4)

    # ══════════════════════════════════════════════════════════════
    #  ÓRBITA — Terra 3D com 15 satélites
    # ══════════════════════════════════════════════════════════════
    def _show_orbita(self):
        self._clear_content()
        frame = tk.Frame(self.content, bg=C["bg_deep"])
        frame.pack(fill="both", expand=True)

        title_bar = tk.Frame(frame, bg="#05050f", height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="🌐 ÓRBITA — SISTEMA DE SATÉLITES TÁTICOS",
                 font=self.fnt["h3"], fg=C["accent_blue"], bg="#05050f").pack(side="left", padx=16, pady=8)
        tk.Label(title_bar, text="15 SATÉLITES EM OPERAÇÃO  |  ARRASTE PARA ROTACIONAR",
                 font=self.fnt["mono"], fg=C["text_dim"], bg="#05050f").pack(side="right", padx=16)
        tk.Frame(frame, bg=C["accent_blue"], height=2).pack(fill="x")

        # Painel de info dos satélites
        side_panel = tk.Frame(frame, bg="#05050f", width=220)
        side_panel.pack(side="right", fill="y")
        side_panel.pack_propagate(False)
        tk.Frame(side_panel, bg=C["border"], width=1).pack(side="left", fill="y")

        tk.Label(side_panel, text="◈ SATÉLITES ATIVOS",
                 font=self.fnt["label"], fg=C["accent_blue"],
                 bg="#05050f").pack(pady=(12,4), padx=12)
        tk.Frame(side_panel, bg=C["border_bright"], height=1).pack(fill="x", padx=8)

        sat_names = [
            ("SAT-01 RECON",   "LEO",  C["accent_green"]),
            ("SAT-02 COMMS",   "MEO",  C["accent_blue"]),
            ("SAT-03 GPS",     "GEO",  C["accent_amber"]),
            ("SAT-04 INTEL",   "LEO",  C["accent_green"]),
            ("SAT-05 STRIKE",  "LEO",  C["accent_red"]),
            ("SAT-06 COMMS",   "MEO",  C["accent_blue"]),
            ("SAT-07 RADAR",   "LEO",  C["accent_green"]),
            ("SAT-08 GPS",     "GEO",  C["accent_amber"]),
            ("SAT-09 RECON",   "MEO",  C["accent_blue"]),
            ("SAT-10 EW",      "LEO",  C["accent_red"]),
            ("SAT-11 COMMS",   "GEO",  C["accent_amber"]),
            ("SAT-12 INTEL",   "MEO",  C["accent_blue"]),
            ("SAT-13 STRIKE",  "LEO",  C["accent_red"]),
            ("SAT-14 GPS",     "GEO",  C["accent_amber"]),
            ("SAT-15 RECON",   "LEO",  C["accent_green"]),
        ]

        scroll_sat = tk.Frame(side_panel, bg="#05050f")
        scroll_sat.pack(fill="both", expand=True, padx=8, pady=4)

        for name, orbit, color in sat_names:
            row = tk.Frame(scroll_sat, bg="#080b10",
                           highlightbackground=C["border"], highlightthickness=1)
            row.pack(fill="x", pady=2)
            tk.Label(row, text="●", fg=color, bg="#080b10",
                     font=("Courier New", 8)).pack(side="left", padx=4, pady=3)
            tk.Label(row, text=name, fg=C["text_main"], bg="#080b10",
                     font=self.fnt["mono"]).pack(side="left")
            tk.Label(row, text=orbit, fg=C["text_dim"], bg="#080b10",
                     font=self.fnt["tag"]).pack(side="right", padx=4)

        # Frame do globo 3D
        globe_frame = tk.Frame(frame, bg="#000008")
        globe_frame.pack(side="left", fill="both", expand=True)

        fig = plt.figure(figsize=(9, 8), facecolor="#000008")
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor("#000008")

        # ── Terra ───────────────────────────────────────────────
        u = np.linspace(0, 2*np.pi, 80)
        v = np.linspace(0, np.pi, 60)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))

        # Colorir superfície: azul (oceano) base, verde para latitudes médias
        facecolors = np.zeros((*z.shape, 4))
        for i in range(z.shape[0]):
            for j in range(z.shape[1]):
                lat = np.degrees(np.arcsin(z[i,j]))
                lon_deg = np.degrees(np.arctan2(y[i,j], x[i,j]))
                # oceano base
                r, g, b = 0.05, 0.12, 0.35
                # continentes aproximados por latitude/longitude
                if self._is_land(lat, lon_deg):
                    r, g, b = 0.08, 0.28, 0.08
                # calota polar
                if abs(lat) > 70:
                    r, g, b = 0.85, 0.92, 0.95
                # linha do equador
                if abs(lat) < 1:
                    r, g, b = 0.2, 0.6, 0.9
                facecolors[i,j] = [r, g, b, 1.0]

        ax.plot_surface(x, y, z, facecolors=facecolors,
                        shade=True, linewidth=0, antialiased=True,
                        lightsource=matplotlib.colors.LightSource(azdeg=45, altdeg=30))

        # Atmosfera (esfera levemente maior, azul translúcida)
        atm_scale = 1.06
        ax.plot_surface(x*atm_scale, y*atm_scale, z*atm_scale,
                        color=(0.1, 0.4, 0.9), alpha=0.06,
                        linewidth=0, antialiased=True)

        # ── Satélites e órbitas ───────────────────────────────
        sat_configs = [
            # (raio, inclinação_graus, fase_inicial)
            (1.4,  0,   0),   (1.4,  0,   120),  (1.4,  0,   240),
            (1.6,  45,  20),  (1.6,  45,  140),  (1.6,  45,  260),
            (1.6,  90,  60),  (1.6,  90,  180),  (1.6,  90,  300),
            (1.9, -45,  30),  (1.9, -45,  150),  (1.9, -45,  270),
            (2.2,  60,  10),  (2.2,  60,  130),  (2.2,  60,  250),
        ]

        orbit_colors = [
            C["accent_green"], C["accent_green"], C["accent_green"],
            C["accent_blue"],  C["accent_blue"],  C["accent_blue"],
            C["accent_red"],   C["accent_red"],   C["accent_red"],
            C["accent_amber"], C["accent_amber"], C["accent_amber"],
            "#aa44ff",         "#aa44ff",         "#aa44ff",
        ]

        for idx, ((r, inc, phase), color) in enumerate(zip(sat_configs, orbit_colors)):
            inc_r = np.radians(inc)
            phase_r = np.radians(phase)

            # Trajetória da órbita
            theta_orb = np.linspace(0, 2*np.pi, 120)
            ox = r * np.cos(theta_orb)
            oy = r * np.sin(theta_orb) * np.cos(inc_r)
            oz = r * np.sin(theta_orb) * np.sin(inc_r)
            ax.plot(ox, oy, oz, color=color, alpha=0.18, linewidth=0.7)

            # Posição do satélite
            sx = r * np.cos(phase_r)
            sy = r * np.sin(phase_r) * np.cos(inc_r)
            sz = r * np.sin(phase_r) * np.sin(inc_r)

            # Corpo do satélite (ponto grande)
            ax.scatter([sx], [sy], [sz], s=55, c=color, zorder=10,
                       edgecolors="white", linewidths=0.5)

            # Painel solar (linha perpendicular)
            panel_len = 0.12
            ax.plot([sx-panel_len, sx+panel_len],
                    [sy, sy], [sz, sz],
                    color=color, linewidth=2.0, alpha=0.9)

            # Label
            ax.text(sx*1.08, sy*1.08, sz*1.08,
                    f"S{idx+1:02d}", fontsize=5.5,
                    color=color, fontfamily="Courier New")

        # Eixo de rotação (pólos)
        ax.plot([0,0],[0,0],[-2.4,2.4], color="#334455",
                linewidth=0.8, linestyle=":", alpha=0.5)

        # Estrelas de fundo
        np.random.seed(42)
        n_stars = 200
        star_x = np.random.uniform(-3, 3, n_stars)
        star_y = np.random.uniform(-3, 3, n_stars)
        star_z = np.random.uniform(-3, 3, n_stars)
        # só as que estão longe da Terra
        dists = np.sqrt(star_x**2 + star_y**2 + star_z**2)
        mask = dists > 2.5
        ax.scatter(star_x[mask], star_y[mask], star_z[mask],
                   s=0.5, c="white", alpha=0.5, zorder=0)

        # Estilo dos eixos
        ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.5, 2.5); ax.set_zlim(-2.5, 2.5)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
            pane.fill = False; pane.set_edgecolor("#050508")
        ax.grid(False)

        canvas = FigureCanvasTkAgg(fig, master=globe_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Legenda de órbitas
        info_bar = tk.Frame(frame if False else globe_frame, bg="#000008", height=28)
        info_bar.pack(fill="x", side="bottom")
        info_bar.pack_propagate(False)
        orbit_legend = [
            ("LEO", C["accent_green"]), ("MEO", C["accent_blue"]),
            ("GEO", C["accent_amber"]), ("ELÍPTICA", "#aa44ff"),
        ]
        for name, color in orbit_legend:
            lf = tk.Frame(info_bar, bg="#000008")
            lf.pack(side="left", padx=12)
            tk.Label(lf, text="─", fg=color, bg="#000008",
                     font=("Courier New", 12, "bold")).pack(side="left")
            tk.Label(lf, text=name, fg=C["text_dim"], bg="#000008",
                     font=self.fnt["mono"]).pack(side="left", padx=2)

        tk.Label(info_bar, text="ARRASTE PARA ROTACIONAR  |  SCROLL = ZOOM",
                 font=self.fnt["mono"], fg=C["text_dim"],
                 bg="#000008").pack(side="right", padx=12)

    def _is_land(self, lat, lon):
        """Aproximação grosseira de terra/oceano para colorir o globo."""
        # América do Norte
        if -170 < lon < -50 and 15 < lat < 75: return True
        # América do Sul
        if -80 < lon < -35 and -55 < lat < 15: return True
        # Europa
        if -10 < lon < 40 and 35 < lat < 72: return True
        # África
        if -18 < lon < 52 and -35 < lat < 38: return True
        # Ásia
        if 26 < lon < 180 and 0 < lat < 75: return True
        # Oceania
        if 113 < lon < 155 and -45 < lat < -10: return True
        # Antártida
        if lat < -70: return True
        return False

    # ── Relógio ───────────────────────────────────────────────────
    def _animate_loop(self):
        now = time.strftime("%H:%M:%S")
        self.clock_var.set(now)
        if self.root.winfo_exists():
            self.root.after(1000, self._animate_loop)

    def run(self):
        self.root.mainloop()


# ══════════════════════════════════════════════════════════════════
#  PONTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  MEDICINA TÁTICA — Controle de Missão v2.2  ")
    print("  Iniciando sistema...")
    print("  Dependências: pip install pillow requests matplotlib")
    print("                numpy tkintermapview geopandas geodatasets")
    print("=" * 60)
    app = MedicinaTatica()
    app.run()