#!/usr/bin/env python3
"""
Gera o site como HTML estático, pronto para o GitHub Pages.

Diferente do app.py (que precisa de um servidor rodando o tempo todo), este
script roda uma vez, lê data/oportunidades.json e escreve um arquivo
docs/index.html já pronto — sem precisar de Flask nem de servidor.

Os filtros (nível, área, busca) funcionam com JavaScript direto no
navegador (client-side), então continuam funcionando mesmo sem nenhum
servidor por trás.
"""

import json
import os
import shutil
from datetime import date, datetime

from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "oportunidades.json")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
OUTPUT_DIR = os.path.join(BASE_DIR, "docs")  # pasta que o GitHub Pages publica


def esta_expirado(item):
    prazo_iso = (item.get("prazo_iso") or "").strip()
    if not prazo_iso:
        return False
    try:
        return datetime.strptime(prazo_iso, "%Y-%m-%d").date() < date.today()
    except ValueError:
        return False


def dias_restantes(item):
    prazo_iso = (item.get("prazo_iso") or "").strip()
    if not prazo_iso:
        return None
    try:
        return (datetime.strptime(prazo_iso, "%Y-%m-%d").date() - date.today()).days
    except ValueError:
        return None


def urgencia(dias):
    if dias is None:
        return "prazo-desconhecido"
    if dias <= 7:
        return "prazo-urgente"
    if dias <= 30:
        return "prazo-atencao"
    return "prazo-tranquilo"


def main():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = {"atualizado_em": None, "total": 0, "oportunidades": []}

    itens = [i for i in dados.get("oportunidades", []) if not esta_expirado(i)]
    for i in itens:
        d = dias_restantes(i)
        i["_dias_restantes"] = d
        i["_urgencia"] = urgencia(d)
    itens.sort(key=lambda i: i["_dias_restantes"] if i["_dias_restantes"] is not None else 99999)

    niveis_disponiveis = sorted({i.get("nivel", "") for i in dados.get("oportunidades", []) if i.get("nivel")})

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("index_static.html")
    html = template.render(
        itens=itens,
        total=len(itens),
        atualizado_em=dados.get("atualizado_em"),
        niveis_disponiveis=niveis_disponiveis,
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    dest_static = os.path.join(OUTPUT_DIR, "static")
    if os.path.exists(dest_static):
        shutil.rmtree(dest_static)
    shutil.copytree(STATIC_DIR, dest_static)

    # arquivo .nojekyll evita que o GitHub Pages tente processar a pasta
    # como um site Jekyll (o que pode esconder pastas que começam com "_")
    open(os.path.join(OUTPUT_DIR, ".nojekyll"), "w").close()

    print(f"Site estático gerado em {OUTPUT_DIR}/ com {len(itens)} oportunidade(s).")


if __name__ == "__main__":
    main()
