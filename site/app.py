"""Acervo que Fala — site de demonstração (E11).

O site serve o lote pré-computado (site/dados.json): nenhum modelo roda aqui. A inferência
aconteceu no Colab; este app só mostra, objeto a objeto, o que foi gerado e o que a
avaliação apontou. Por isso cabe na CPU gratuita do Hugging Face Spaces.

Toda a renderização está em cartoes.py; aqui ficam só os controles.
"""
import gradio as gr

import cartoes

PRIMEIRO = cartoes.DADOS["objetos"][0]["id"]

TEMA = gr.themes.Base(
    font=[gr.themes.GoogleFont("Google Sans Flex"), "Segoe UI", "system-ui", "sans-serif"],
).set(
    body_background_fill="#f7f4ee", body_background_fill_dark="#17140f",
    block_background_fill="#f1ede3", block_background_fill_dark="#1e1a14",
    color_accent="#2f5d8f", color_accent_soft="#d3e4ff", color_accent_soft_dark="#114881",
    border_color_primary="#d8cfc0", border_color_primary_dark="#4d463b",
)


def trocar_conjunto(conjunto):
    opcoes = cartoes.opcoes(conjunto)
    primeiro = opcoes[0][1]
    return gr.Dropdown(choices=opcoes, value=primeiro), cartoes.cartao(primeiro)


with gr.Blocks(title="Acervo que Fala") as demo:
    gr.HTML(cartoes.cabecalho())
    with gr.Tabs():
        with gr.Tab("Objetos"):
            with gr.Row():
                conjunto = gr.Radio(list(cartoes.CONJUNTOS), value="Todos", label="Conjunto")
                objeto = gr.Dropdown(cartoes.opcoes("Todos"), value=PRIMEIRO, label="Objeto",
                                     filterable=True)
            cartao = gr.HTML(cartoes.cartao(PRIMEIRO))
        with gr.Tab("Resultados"):
            gr.HTML(cartoes.resultados())
        with gr.Tab("Como funciona"):
            gr.HTML(cartoes.como_funciona())

    conjunto.change(trocar_conjunto, conjunto, [objeto, cartao])
    objeto.change(cartoes.cartao, objeto, cartao)

if __name__ == "__main__":
    demo.launch(theme=TEMA, css=cartoes.CSS)
