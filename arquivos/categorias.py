# -*- coding: utf-8 -*-
"""
categorias.py
==============
Define as categorias de uso (cards da home, páginas temáticas, notícias,
eventos, turismo, cultura, esporte e educação) e os termos de busca usados
para encontrar imagens relacionadas a Alegrete-RS em cada uma delas.

Cada categoria tem:
    nome:              rótulo de exibição
    termos_locais:     termos para buscar imagens GEOGRAFICAMENTE de Alegrete
                        (usados no Wikimedia Commons / Flickr com geolocalização)
    termos_genericos:  termos temáticos para usar como banco de imagens de apoio
                        (estoque genérico, usado quando não há fotos locais
                        suficientes; ex.: Unsplash/Pexels/Pixabay)
    minimo_local:      quantidade mínima desejável de fotos genuinamente locais
                        antes de recorrer ao estoque genérico

Ajuste livremente os termos abaixo: eles refletem pontos de referência
conhecidos de Alegrete (Pampa gaúcho, fronteira oeste do RS, charqueadas,
Rio Ibirapuitã, tradição campeira), mas a cidade real tem muito mais
particularidades que vale a pena incorporar aqui.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Categoria:
    chave: str
    nome: str
    termos_locais: List[str] = field(default_factory=list)
    termos_genericos: List[str] = field(default_factory=list)
    minimo_local: int = 3


CATEGORIAS: List[Categoria] = [
    Categoria(
        chave="cards_pagina_inicial",
        nome="Cards da Página Inicial",
        termos_locais=[
            "Alegrete Rio Grande do Sul",
            "Alegrete RS cidade",
            "Alegrete RS praça",
            "Alegrete RS pôr do sol",
        ],
        termos_genericos=[
            "pampa gaúcho paisagem",
            "cidade pequena Rio Grande do Sul",
            "campo gaúcho entardecer",
        ],
        minimo_local=4,
    ),
    Categoria(
        chave="paginas_tematicas",
        nome="Páginas Temáticas",
        termos_locais=[
            "Alegrete RS panorama",
            "Alegrete RS centro histórico",
            "Rio Ibirapuitã Alegrete",
        ],
        termos_genericos=[
            "pampa bioma campos sulinos",
            "fronteira oeste Rio Grande do Sul",
        ],
        minimo_local=3,
    ),
    Categoria(
        chave="noticias",
        nome="Notícias",
        termos_locais=[
            "Alegrete RS prefeitura",
            "Alegrete RS rua centro",
            "Alegrete RS Câmara de Vereadores",
        ],
        termos_genericos=[
            "prefeitura cidade brasileira",
            "centro urbano Brasil rua",
        ],
        minimo_local=3,
    ),
    Categoria(
        chave="eventos",
        nome="Eventos",
        termos_locais=[
            "Rodeio Crioulo Internacional Alegrete",
            "Alegrete RS Semana Farroupilha",
            "Alegrete RS Parque de Exposições",
        ],
        termos_genericos=[
            "rodeio gaúcho tradicionalista",
            "festa popular ao ar livre Brasil",
            "show palco evento público",
        ],
        minimo_local=3,
    ),
    Categoria(
        chave="turismo",
        nome="Turismo",
        termos_locais=[
            "Parque Rui Ramos Alegrete",
            "Barragem do Ibirapuitã Alegrete",
            "Alegrete RS turismo rural",
            "Alegrete RS monumento histórico",
        ],
        termos_genericos=[
            "turismo rural Pampa",
            "fazenda gaúcha estância",
            "paisagem campo aberto Brasil sul",
        ],
        minimo_local=4,
    ),
    Categoria(
        chave="cultura",
        nome="Cultura",
        termos_locais=[
            "CTG Alegrete RS",
            "Alegrete RS tradição gaúcha",
            "Alegrete RS charqueada história",
        ],
        termos_genericos=[
            "tradição gaúcha churrasco chimarrão",
            "dança gaúcha trajes típicos",
            "centro de tradições gaúchas CTG",
        ],
        minimo_local=3,
    ),
    Categoria(
        chave="esporte",
        nome="Esporte",
        termos_locais=[
            "Alegrete RS estádio futebol",
            "Alegrete RS time futebol",
        ],
        termos_genericos=[
            "futebol amador campo Brasil",
            "rodeio prova campeira laço",
            "competição esportiva ao ar livre",
        ],
        minimo_local=2,
    ),
    Categoria(
        chave="educacao",
        nome="Educação",
        termos_locais=[
            "Alegrete RS escola",
            "URCAMP Alegrete campus",
        ],
        termos_genericos=[
            "escola pública sala de aula Brasil",
            "estudantes universidade campus",
            "biblioteca escolar Brasil",
        ],
        minimo_local=2,
    ),
]


def obter_categoria(chave: str) -> Categoria:
    """Retorna a categoria correspondente à chave informada."""
    for categoria in CATEGORIAS:
        if categoria.chave == chave:
            return categoria
    raise KeyError(f"Categoria desconhecida: {chave}")


def chaves_categorias() -> List[str]:
    return [c.chave for c in CATEGORIAS]