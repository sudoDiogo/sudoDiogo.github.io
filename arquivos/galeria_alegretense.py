import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
import webbrowser
import threading

from provedores import WikimediaCommonsProvedor
from categorias import CATEGORIAS


class GaleriaAlegretense(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Galeria Alegretense")
        self.geometry("1200x800")

        self.provedor = WikimediaCommonsProvedor()

        self.imagens_tk = []

        self.criar_interface()

    def criar_interface(self):

        topo = ttk.Frame(self)
        topo.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            topo,
            text="Categoria:"
        ).pack(side="left")

        self.combo_categoria = ttk.Combobox(
            topo,
            values=[c.nome for c in CATEGORIAS],
            state="readonly",
            width=40
        )

        self.combo_categoria.current(0)
        self.combo_categoria.pack(side="left", padx=5)

        ttk.Button(
            topo,
            text="Buscar Imagens",
            command=self.buscar
        ).pack(side="left", padx=5)

        self.status = ttk.Label(topo, text="")
        self.status.pack(side="left", padx=20)

        self.canvas = tk.Canvas(self)
        self.scroll = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.frame_resultados = ttk.Frame(self.canvas)

        self.frame_resultados.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.frame_resultados,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scroll.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scroll.pack(
            side="right",
            fill="y"
        )

    def buscar(self):
        threading.Thread(
            target=self._buscar_thread,
            daemon=True
        ).start()

    def _buscar_thread(self):

        for w in self.frame_resultados.winfo_children():
            w.destroy()

        self.imagens_tk.clear()

        categoria = CATEGORIAS[
            self.combo_categoria.current()
        ]

        self.status.config(text="Buscando...")

        linha = 0

        for termo in categoria.termos_locais:

            resultados = self.provedor.buscar(
                termo,
                15
            )

            for img in resultados:

                try:

                    ###
                    headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/137.0 Safari/537.36"
                    ),
                    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                    "Referer": "https://commons.wikimedia.org/"
                    }

                    r = requests.get(
                        img.url_thumbnail,
                        headers=headers,
                        timeout=20
                    )

                    print(r.status_code)
                    print(r.headers.get("Content-Type"))
                    ###

                    ###
                    print("=" * 50)
                    print(img.titulo)
                    print(img.url_thumbnail)
                    print(r.status_code)
                    print(r.headers.get("content-type"))
                    print("=" * 50)

                    imagem = Image.open(BytesIO(r.content))
                    ###

                    imagem.thumbnail((250, 250))

                    foto = ImageTk.PhotoImage(imagem)

                    self.imagens_tk.append(foto)

                    card = ttk.Frame(
                        self.frame_resultados,
                        relief="ridge",
                        padding=10
                    )

                    card.grid(
                        row=linha,
                        column=0,
                        sticky="ew",
                        padx=5,
                        pady=5
                    )

                    ttk.Label(
                        card,
                        image=foto
                    ).pack()

                    ttk.Label(
                        card,
                        text=img.titulo,
                        wraplength=500,
                        font=(
                            "Arial",
                            11,
                            "bold"
                        )
                    ).pack()

                    ttk.Label(
                        card,
                        text=f"Autor: {img.autor}"
                    ).pack()

                    ttk.Label(
                        card,
                        text=f"Licença: {img.licenca}"
                    ).pack()

                    ttk.Label(
                        card,
                        text=img.url_imagem,
                        foreground="blue",
                        wraplength=600
                    ).pack()

                    botoes = ttk.Frame(card)
                    botoes.pack(pady=5)

                    ttk.Button(
                        botoes,
                        text="Abrir Imagem",
                        command=lambda u=img.url_imagem:
                        webbrowser.open(u)
                    ).pack(side="left", padx=5)

                    ttk.Button(
                        botoes,
                        text="Página Wikimedia",
                        command=lambda u=img.url_pagina:
                        webbrowser.open(u)
                    ).pack(side="left", padx=5)

                    linha += 1

                except Exception as e:
                    print(e)

        self.status.config(
            text=f"{linha} imagens encontradas"
        )


if __name__ == "__main__":
    app = GaleriaAlegretense()
    app.mainloop()