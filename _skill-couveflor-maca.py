# -*- coding: utf-8 -*-
"""
_skill-couveflor-maca.py — duas licoes de desenho na skill.

1. erro (j) ganha o caso INVERSO: claro sobre claro (florete creme sobre circulo
   palido = 45) e o conserto por CONTORNO, nao por fundo escuro.
2. secao "Vidro com liquido" ganha a licao da SILHUETA: contentor mais largo que
   alto nao le' como pote. Cor nao conserta proporcao.
"""
import io
import sys

ARQ = r'C:\Users\Saxa\.workbuddy-ai\skills\shorts-svg-animado\SKILL.md'

CASO_CLARO = """
**O caso INVERSO — claro sobre claro (19/09, `couve-flor/shorts-cauliflower-apple-en`).**
O mesmo defeito aparece sem nenhuma cor escura envolvida: florete creme `#faf8ee` sobre o
círculo `#d8e3bd` a `opacity=".6"` dá **45** — a couve-flor virou uma mancha sem forma.

**O conserto NÃO é escurecer o fundo** (isso briga com o resto da paleta). É dar **contorno**
ao elemento: `stroke="#93a663" stroke-width="2.5"` → **147** contra o círculo. O contorno é
que define a forma.

> 💡 Efeito colateral bom: círculos **sobrepostos e todos com contorno** passam a ler como
> floretes individuais — que é literalmente o que uma couve-flor é. Quando o objeto é feito
> de partes, desenhar as partes **com contorno** em vez de uma massa só.

**Regra geral:** claro sobre claro é tão ilegível quanto escuro sobre escuro. Antes de
escurecer o fundo, tente **contorno** — muda menos a paleta e resolve mais.
"""

SILHUETA = """
### 📦 A SILHUETA vem antes da cor — contentor largo demais lê como CAIXA

O pote do `couve-flor/shorts-cauliflower-apple-en` lia como **caixa verde**, não como vidro.
Tentei consertar por cor duas vezes — salmoura mais clara, base de vidro aparecendo — e não
adiantou. **A causa não era cor: era a proporção.**

O jarro herdado media **208 de largura × 168 de altura** — deitado. Nenhum ajuste de tom
conserta isso. Refazer como **156 × 224** (mais alto que largo), com uma base de vidro
aparecendo embaixo, resolveu de primeira.

**Antes de mexer em cor, olhar a silhueta:**
- contentor **mais largo que alto** → lê como caixa / tigela / bandeja.
- jarro, garrafa, pote → **sempre mais alto que largo**.
- deixar **vidro aparecendo** na base (o líquido não encosta no fundo) é o que faz o olho
  ler "recipiente" em vez de "bloco colorido".

**E não empilhar conserto em cima de conserto:** se dois ajustes de cor seguidos não
resolveram, o problema é de **forma** — parar de mexer em `fill` e ir para a geometria.
"""

ANCORAS = [
    (
        'erro (j) — caso claro sobre claro',
        '**legume ESCURO + líquido CLARO** — ao trocar a cor do líquido, conferir se o legume\n'
        'continua separando dele.',
        '**legume ESCURO + líquido CLARO** — ao trocar a cor do líquido, conferir se o legume\n'
        'continua separando dele.\n' + CASO_CLARO,
    ),
    (
        'silhueta antes da cor',
        '**Sombra com `opacity` fixa em `<rect>` cria emenda** onde ela encosta no fundo —\n'
        'usar `linearGradient` (de opaco a transparente) em vez de opacidade chapada.\n\n'
        '### Partículas — atenção',
        '**Sombra com `opacity` fixa em `<rect>` cria emenda** onde ela encosta no fundo —\n'
        'usar `linearGradient` (de opaco a transparente) em vez de opacidade chapada.\n'
        + SILHUETA +
        '\n### Partículas — atenção',
    ),
]


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()

    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('fim de linha: %d CRLF / %d LF' % (crlf, lf))
    eol = '\r\n' if crlf else '\n'

    falhou = False
    for rotulo, velho, novo in ANCORAS:
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        q = d.count(v)
        print('%-36s casou %d vez(es)' % (rotulo, q))
        if q != 1:
            falhou = True
            continue
        d = d.replace(v, n, 1)

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    with io.open(ARQ + '.antes-do-20', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('\ngravado: %s (backup .antes-do-20)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())
