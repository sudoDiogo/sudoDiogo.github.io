# -*- coding: utf-8 -*-
"""
provedores.py
=============
Modelo de dados de imagem (ImagemResultado) e os "provedores" de busca:
cada provedor sabe consultar uma fonte de imagens e devolver resultados
no formato padronizado.

Provedores incluídos:
    - WikimediaCommons : sem necessidade de chave de API. Boa fonte para
                          fotos genuinamente locais (categorias geográficas
                          do Commons), com licença sempre explícita.
    - Flickr            : busca geolocalizada (bounding box) perto de
                          Alegrete, filtrando por licença Creative Commons.
                          Requer chave de API gratuita.
    - Pexels            : banco de imagens de estoque, bom para temas
                          genéricos (esporte, educação, cultura) quando
                          não há foto local suficiente. Requer chave.
    - Unsplash           : idem Pexels. Requer chave (Access Key).
    - Pixabay            : idem Pexels. Requer chave.

IMPORTANTE sobre relevância geográfica
---------------------------------------
Alegrete é uma cidade média (~75 mil habitantes). Bancos de imagem de
estoque (Pexels/Unsplash/Pixabay) quase nunca têm fotos *especificamente*
de Alegrete — eles retornam fotos *temáticas* (pampa, rodeio, escola etc.)
que servem como apoio visual, não como retrato real do município. Por
isso cada resultado é marcado com o campo `tipo`:
    "local"     -> imagem geograficamente/textualmente associada a Alegrete
                   (Wikimedia Commons, Flickr geolocalizado)
    "generico"  -> imagem de estoque temática, sem garantia de ser de
                   Alegrete

Use esse campo para decidir o que pode ir, por exemplo, num card que diz
"Conheça Alegrete" (deveria ser só "local") versus uma ilustração de apoio
num texto sobre tradição gaúcha em geral (pode ser "generico").
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, asdict
from typing import List, Optional

import requests

logger = logging.getLogger("alegrete_galeria.provedores")

TIMEOUT_PADRAO = 15  # segundos


@dataclass
class ImagemResultado:
    id: str
    titulo: str
    descricao: str
    url_imagem: str
    url_thumbnail: str
    largura: Optional[int]
    altura: Optional[int]
    fonte: str            # nome do provedor, ex.: "Wikimedia Commons"
    autor: str
    url_autor: Optional[str]
    licenca: str
    url_pagina: str        # página de origem da imagem (para crédito/clique)
    tipo: str               # "local" ou "generico"
    termo_busca: str
    categoria: str = ""
    pontuacao_qualidade: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)


class ProvedorBase:
    """Interface comum a todos os provedores de busca de imagens."""

    nome_provedor = "Base"

    def disponivel(self) -> bool:
        """Indica se o provedor está pronto para uso (ex.: chave configurada)."""
        return True

    def buscar(self, termo: str, max_resultados: int, tipo: str) -> List[ImagemResultado]:
        raise NotImplementedError


class WikimediaCommonsProvedor(ProvedorBase):
    """
    Busca no Wikimedia Commons (https://commons.wikimedia.org).
    Não exige chave de API. Excelente para imagens locais com licença clara
    (CC-BY-SA, CC0, domínio público etc.), pois é um acervo colaborativo
    que costuma ter fotos de praticamente qualquer município brasileiro.
    """

    nome_provedor = "Wikimedia Commons"
    ENDPOINT = "https://commons.wikimedia.org/w/api.php"

    def buscar(self, termo: str, max_resultados: int, tipo: str = "local") -> List[ImagemResultado]:
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": f"{termo} filetype:bitmap",
            "gsrnamespace": 6,  # namespace de arquivos (File:)
            "gsrlimit": max_resultados,
            "prop": "imageinfo",
            "iiprop": "url|size|extmetadata|user",
            "iiurlwidth": 800,
        }
        try:
            ########
            headers = {
                "User-Agent": (
                    "AlegreteGaleria/1.0 "
                    "(contato: seuemail@exemplo.com)"
                )
            }

            resp = requests.get(
                self.ENDPOINT,
                params=params,
                headers=headers,
                timeout=TIMEOUT_PADRAO
            )
            ####
            resp.raise_for_status()
            dados = resp.json()
        except requests.RequestException as exc:
            logger.warning("Falha ao consultar Wikimedia Commons para '%s': %s", termo, exc)
            return []

        paginas = dados.get("query", {}).get("pages", {})
        resultados: List[ImagemResultado] = []
        for pagina in paginas.values():
            infos = pagina.get("imageinfo")
            if not infos:
                continue
            info = infos[0]
            meta = info.get("extmetadata", {})
            licenca = meta.get("LicenseShortName", {}).get("value", "Ver página de origem")
            autor = meta.get("Artist", {}).get("value", "Desconhecido")
            # remove eventuais tags HTML simples do campo de autor
            autor = _limpar_html(autor)
            descricao = _limpar_html(meta.get("ImageDescription", {}).get("value", ""))

            resultados.append(
                ImagemResultado(
                    id=f"commons-{pagina.get('pageid')}",
                    titulo=pagina.get("title", termo).replace("File:", ""),
                    descricao=descricao[:280],
                    url_imagem=info.get("url", ""),
                    url_thumbnail=info.get("thumburl", info.get("url", "")),
                    largura=info.get("width"),
                    altura=info.get("height"),
                    fonte=self.nome_provedor,
                    autor=autor or "Desconhecido",
                    url_autor=None,
                    licenca=licenca,
                    url_pagina=info.get("descriptionurl", ""),
                    tipo=tipo,
                    termo_busca=termo,
                )
            )
        return resultados


class FlickrProvedor(ProvedorBase):
    """
    Busca geolocalizada no Flickr, restrita a uma caixa (bounding box) em
    torno das coordenadas de Alegrete-RS, filtrando por fotos com licença
    Creative Commons. Requer FLICKR_API_KEY.
    """

    nome_provedor = "Flickr"
    ENDPOINT = "https://api.flickr.com/services/rest/"
    # Coordenadas aproximadas do centro de Alegrete-RS
    LAT, LON = -29.7878, -55.7894
    RAIO_KM = 25

    def __init__(self, api_key: Optional[str]):
        self.api_key = api_key

    def disponivel(self) -> bool:
        return bool(self.api_key)

    def buscar(self, termo: str, max_resultados: int, tipo: str = "local") -> List[ImagemResultado]:
        if not self.disponivel():
            return []
        params = {
            "method": "flickr.photos.search",
            "api_key": self.api_key,
            "text": termo,
            "lat": self.LAT,
            "lon": self.LON,
            "radius": self.RAIO_KM,
            "radius_units": "km",
            "license": "1,2,3,4,5,6,9,10",  # licenças Creative Commons + CC0/PD
            "sort": "relevance",
            "per_page": max_resultados,
            "format": "json",
            "nojsoncallback": 1,
            "extras": "owner_name,url_l,url_o,url_c,license,description",
        }
        try:
            resp = requests.get(self.ENDPOINT, params=params, timeout=TIMEOUT_PADRAO)
            resp.raise_for_status()
            dados = resp.json()
        except requests.RequestException as exc:
            logger.warning("Falha ao consultar Flickr para '%s': %s", termo, exc)
            return []

        fotos = dados.get("photos", {}).get("photo", [])
        resultados: List[ImagemResultado] = []
        for foto in fotos:
            url_imagem = foto.get("url_l") or foto.get("url_o") or foto.get("url_c")
            if not url_imagem:
                continue
            resultados.append(
                ImagemResultado(
                    id=f"flickr-{foto.get('id')}",
                    titulo=foto.get("title", termo),
                    descricao=_limpar_html(foto.get("description", {}).get("_content", "")),
                    url_imagem=url_imagem,
                    url_thumbnail=foto.get("url_c", url_imagem),
                    largura=foto.get("width_l"),
                    altura=foto.get("height_l"),
                    fonte=self.nome_provedor,
                    autor=foto.get("ownername", "Desconhecido"),
                    url_autor=f"https://www.flickr.com/photos/{foto.get('owner')}",
                    licenca=_traduzir_licenca_flickr(foto.get("license")),
                    url_pagina=f"https://www.flickr.com/photos/{foto.get('owner')}/{foto.get('id')}",
                    tipo=tipo,
                    termo_busca=termo,
                )
            )
        return resultados


class PexelsProvedor(ProvedorBase):
    """Banco de imagens de estoque Pexels. Requer PEXELS_API_KEY."""

    nome_provedor = "Pexels"
    ENDPOINT = "https://api.pexels.com/v1/search"

    def __init__(self, api_key: Optional[str]):
        self.api_key = api_key

    def disponivel(self) -> bool:
        return bool(self.api_key)

    def buscar(self, termo: str, max_resultados: int, tipo: str = "generico") -> List[ImagemResultado]:
        if not self.disponivel():
            return []
        headers = {"Authorization": self.api_key}
        params = {"query": termo, "per_page": max_resultados, "locale": "pt-BR"}
        try:
            resp = requests.get(self.ENDPOINT, headers=headers, params=params, timeout=TIMEOUT_PADRAO)
            resp.raise_for_status()
            dados = resp.json()
        except requests.RequestException as exc:
            logger.warning("Falha ao consultar Pexels para '%s': %s", termo, exc)
            return []

        resultados: List[ImagemResultado] = []
        for foto in dados.get("photos", []):
            src = foto.get("src", {})
            resultados.append(
                ImagemResultado(
                    id=f"pexels-{foto.get('id')}",
                    titulo=foto.get("alt") or termo,
                    descricao=foto.get("alt", ""),
                    url_imagem=src.get("original", src.get("large2x", "")),
                    url_thumbnail=src.get("medium", ""),
                    largura=foto.get("width"),
                    altura=foto.get("height"),
                    fonte=self.nome_provedor,
                    autor=foto.get("photographer", "Desconhecido"),
                    url_autor=foto.get("photographer_url"),
                    licenca="Licença Pexels (uso gratuito, atribuição não obrigatória)",
                    url_pagina=foto.get("url", ""),
                    tipo=tipo,
                    termo_busca=termo,
                )
            )
        return resultados


class UnsplashProvedor(ProvedorBase):
    """Banco de imagens de estoque Unsplash. Requer UNSPLASH_ACCESS_KEY."""

    nome_provedor = "Unsplash"
    ENDPOINT = "https://api.unsplash.com/search/photos"

    def __init__(self, access_key: Optional[str]):
        self.access_key = access_key

    def disponivel(self) -> bool:
        return bool(self.access_key)

    def buscar(self, termo: str, max_resultados: int, tipo: str = "generico") -> List[ImagemResultado]:
        if not self.disponivel():
            return []
        headers = {"Authorization": f"Client-ID {self.access_key}"}
        params = {"query": termo, "per_page": max_resultados}
        try:
            resp = requests.get(self.ENDPOINT, headers=headers, params=params, timeout=TIMEOUT_PADRAO)
            resp.raise_for_status()
            dados = resp.json()
        except requests.RequestException as exc:
            logger.warning("Falha ao consultar Unsplash para '%s': %s", termo, exc)
            return []

        resultados: List[ImagemResultado] = []
        for foto in dados.get("results", []):
            urls = foto.get("urls", {})
            usuario = foto.get("user", {})
            resultados.append(
                ImagemResultado(
                    id=f"unsplash-{foto.get('id')}",
                    titulo=foto.get("description") or foto.get("alt_description") or termo,
                    descricao=foto.get("alt_description", "") or "",
                    url_imagem=urls.get("full", urls.get("raw", "")),
                    url_thumbnail=urls.get("small", ""),
                    largura=foto.get("width"),
                    altura=foto.get("height"),
                    fonte=self.nome_provedor,
                    autor=usuario.get("name", "Desconhecido"),
                    url_autor=usuario.get("links", {}).get("html"),
                    licenca="Licença Unsplash (uso gratuito, atribuição apreciada)",
                    url_pagina=foto.get("links", {}).get("html", ""),
                    tipo=tipo,
                    termo_busca=termo,
                )
            )
        return resultados


class PixabayProvedor(ProvedorBase):
    """Banco de imagens de estoque Pixabay. Requer PIXABAY_API_KEY."""

    nome_provedor = "Pixabay"
    ENDPOINT = "https://pixabay.com/api/"

    def __init__(self, api_key: Optional[str]):
        self.api_key = api_key

    def disponivel(self) -> bool:
        return bool(self.api_key)

    def buscar(self, termo: str, max_resultados: int, tipo: str = "generico") -> List[ImagemResultado]:
        if not self.disponivel():
            return []
        params = {
            "key": self.api_key,
            "q": termo,
            "lang": "pt",
            "per_page": max(3, min(max_resultados, 200)),
            "image_type": "photo",
            "safesearch": "true",
        }
        try:
            resp = requests.get(self.ENDPOINT, params=params, timeout=TIMEOUT_PADRAO)
            resp.raise_for_status()
            dados = resp.json()
        except requests.RequestException as exc:
            logger.warning("Falha ao consultar Pixabay para '%s': %s", termo, exc)
            return []

        resultados: List[ImagemResultado] = []
        for foto in dados.get("hits", [])[:max_resultados]:
            resultados.append(
                ImagemResultado(
                    id=f"pixabay-{foto.get('id')}",
                    titulo=foto.get("tags", termo),
                    descricao=foto.get("tags", ""),
                    url_imagem=foto.get("largeImageURL", foto.get("webformatURL", "")),
                    url_thumbnail=foto.get("webformatURL", ""),
                    largura=foto.get("imageWidth"),
                    altura=foto.get("imageHeight"),
                    fonte=self.nome_provedor,
                    autor=foto.get("user", "Desconhecido"),
                    url_autor=f"https://pixabay.com/users/{foto.get('user')}-{foto.get('user_id')}/",
                    licenca="Licença Pixabay (uso gratuito, atribuição não obrigatória)",
                    url_pagina=foto.get("pageURL", ""),
                    tipo=tipo,
                    termo_busca=termo,
                )
            )
        return resultados


def _limpar_html(texto: str) -> str:
    """Remove tags HTML simples que às vezes vêm em campos de metadados."""
    import re

    if not texto:
        return ""
    texto = re.sub(r"<[^>]+>", "", texto)
    return texto.strip()


def _traduzir_licenca_flickr(codigo) -> str:
    """Mapa simplificado dos códigos de licença do Flickr para texto legível."""
    mapa = {
        "0": "Todos os direitos reservados",
        "1": "CC BY-NC-SA 2.0",
        "2": "CC BY-NC 2.0",
        "3": "CC BY-NC-ND 2.0",
        "4": "CC BY 2.0",
        "5": "CC BY-SA 2.0",
        "6": "CC BY-ND 2.0",
        "7": "Sem restrições conhecidas de copyright",
        "8": "Governo dos EUA - Trabalho",
        "9": "Domínio Público (CC0)",
        "10": "Domínio Público (PDM)",
    }
    return mapa.get(str(codigo), "Ver página de origem")