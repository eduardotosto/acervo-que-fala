"""Gera as duas páginas do teste com leitor de tela (E10, frente 3).

O teste é a experiência auditiva real: o NVDA lendo o alt-text no lugar da imagem, em
contexto de página. São duas páginas com os mesmos objetos, na mesma ordem:

    avaliacao/painel/teste_nvda_gerado.html    — alt = alt-text gerado pelo sistema
    avaliacao/painel/teste_nvda_baseline.html  — alt = descrição curatorial (baseline)

As imagens vêm direto do site do museu (por URL), como no acervo publicado.

Uso:
    python avaliacao/gerar_pagina_nvda.py
"""
import html
import json
import os

AVAL_DIR = os.path.dirname(os.path.abspath(__file__))
PAINEL_DIR = os.path.join(AVAL_DIR, "painel")

CSS = """
:root { color-scheme: light dark; }
body { font: 18px/1.6 system-ui, sans-serif; max-width: 46rem; margin: 0 auto; padding: 1.5rem 1rem 4rem; }
h1 { font-size: 1.6rem; line-height: 1.25; }
h2 { font-size: 1.2rem; margin: 3rem 0 .5rem; }
img { max-width: 100%; height: auto; display: block; border-radius: 6px; }
.como { border: 1px solid; border-radius: 8px; padding: .25rem 1rem; opacity: .85; }
.povo { margin: 0 0 .75rem; opacity: .75; }
a { color: inherit; }
"""

COMO = """
<section class="como" aria-labelledby="como">
<h2 id="como" style="margin-top:1rem">Como fazer o teste</h2>
<ol>
<li>Abra o NVDA (Ctrl+Alt+N) e esta página no navegador.</li>
<li>Tecla <kbd>H</kbd>: pula para o próximo objeto. Tecla <kbd>G</kbd>: pula para a próxima imagem, e o NVDA fala o texto alternativo.</li>
<li>Seta para baixo: continua a leitura depois da imagem.</li>
<li>Ouça sem olhar a foto. Depois olhe, e anote o que o texto deixou de dizer ou disse errado.</li>
</ol>
</section>
"""


def pagina(titulo, explicacao, dossies, alt_de, com_descricao, outra):
    partes = [f"<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
              f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
              f"<title>{html.escape(titulo)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n<main>\n"
              f"<h1>{html.escape(titulo)}</h1>\n<p>{html.escape(explicacao)} "
              f"<a href=\"{outra[0]}\">{html.escape(outra[1])}</a>.</p>\n{COMO}"]
    for n, d in enumerate(dossies, 1):
        partes.append(
            f"<article>\n<h2>{n}. {html.escape(d['titulo'])}</h2>\n"
            f"<p class=\"povo\">Povo {html.escape(d['povo'])}</p>\n"
            f"<img src=\"{html.escape(d['foto_url'])}\" alt=\"{html.escape(alt_de(d))}\" loading=\"lazy\">\n"
            + (f"<p>{html.escape(d['descricao_objeto']).replace(chr(10) * 2, '</p><p>')}</p>\n"
               if com_descricao else "")
            + "</article>\n")
    partes.append("</main>\n</body>\n</html>\n")
    return "".join(partes)


def main():
    with open(os.path.join(PAINEL_DIR, "dossies.json"), encoding="utf-8") as f:
        dossies = [d for d in json.load(f) if d["situacao"] == "descrição gerada"]

    paginas = {
        "teste_nvda_gerado.html": pagina(
            "Acervo que Fala — teste com leitor de tela: texto gerado",
            f"{len(dossies)} objetos. O texto alternativo de cada imagem é o alt-text gerado pelo "
            "sistema, e abaixo da imagem vem a descrição do objeto. Para comparar, abra a",
            dossies, lambda d: d["alt_text"], True,
            ("teste_nvda_baseline.html", "página com a descrição curatorial")),
        "teste_nvda_baseline.html": pagina(
            "Acervo que Fala — teste com leitor de tela: descrição curatorial",
            f"{len(dossies)} objetos, na mesma ordem. O texto alternativo de cada imagem é a "
            "descrição curatorial do catálogo (a baseline). Para comparar, abra a",
            dossies, lambda d: d["baseline"], False,
            ("teste_nvda_gerado.html", "página com o texto gerado")),
    }
    for nome, conteudo in paginas.items():
        with open(os.path.join(PAINEL_DIR, nome), "w", encoding="utf-8", newline="\n") as f:
            f.write(conteudo)
        print(f"{nome}: {len(dossies)} objetos, {len(conteudo)} caracteres")


if __name__ == "__main__":
    main()
