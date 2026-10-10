# -*- coding: utf-8 -*-
"""
_consertar-salmoura-cenoura.py — o liquido do pote da cenoura estava INVISIVEL.

Medido em _revisao/shorts-carrot-apple-en-2-final.png (nao "achei que dava
pra ver"):

    template (pepino)   salmoura #83d6b9 x jarro #f4faf3 -> distancia 132  OK
    cenoura (antes)     salmoura #fbd69a x jarro #fdf9f2 -> distancia  95  fraco

O `#fac775` com `opacity=".7"` sobre um jarro creme quase nao muda o pixel.
A cena 4 diz "everything under the brine" e o pote parecia VAZIO — a mensagem
se perdia. (A ordem de desenho estava certa: e' contraste, nao ordem.)

Conserto — seguir a logica do template (legume ESCURO + salmoura CLARA):
    jarro    #fdf9f2 -> #fffdf7   (mais branco, pra salmoura aparecer)
    salmoura #fac775 @ .7 -> #fac775 @ 1   (mesma cor da tampa = pote cheio)
    palitos  #f0a03c/#c2701a -> #e0801f/#8a4b12  (mais escuros, pra nao
             sumirem dentro da salmoura agora clara)

Distancias depois: salmoura x jarro 142 | salmoura x palito 114 |
palito x contorno 194. Todas acima do limiar de 132 do template.

NAO toca no legume das cenas 0/1/3 (mesma cor, mas e' outro elemento).
"""
import io
import sys

ARQ = 'cenoura/shorts-carrot-apple-en.html'

# ---------------------------------------------------------------- ancoras
# (rotulo, antigo, novo) — cada antigo tem de casar EXATAMENTE 1 vez.
ANCORAS = [
    (
        'jarro + salmoura (s4)',
        '            fill="#fdf9f2" stroke="#ba7517" stroke-width="4"/>\n'
        '      <rect x="-104" y="-58" width="208" height="24" rx="6" fill="#fac775" stroke="#ba7517" stroke-width="4"/>\n'
        '      <path d="M-104,50 L-104,-14 Q-104,-30 -86,-30 L86,-30 Q104,-30 104,-14 L104,50 Z" fill="#fac775" opacity=".7"/>',
        '            fill="#fffdf7" stroke="#ba7517" stroke-width="4"/>\n'
        '      <rect x="-104" y="-58" width="208" height="24" rx="6" fill="#fac775" stroke="#ba7517" stroke-width="4"/>\n'
        '      <path d="M-104,50 L-104,-14 Q-104,-30 -86,-30 L86,-30 Q104,-30 104,-14 L104,50 Z" fill="#fac775"/>',
    ),
    (
        'palitos de cenoura no pote (s4)',
        '      <g fill="#f0a03c" stroke="#c2701a" stroke-width="2">',
        '      <g fill="#e0801f" stroke="#8a4b12" stroke-width="2">',
    ),
]


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()

    # Detectar o fim de linha real — nunca supor (a serie e' mista).
    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('fim de linha: %d CRLF / %d LF' % (crlf, lf))
    if crlf and lf:
        print('AVISO: arquivo MISTO — as ancoras de varias linhas podem nao casar.')
        return 1

    eol = '\r\n' if crlf else '\n'

    falhou = False
    for rotulo, velho, novo in ANCORAS:
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        quantos = d.count(v)
        print('%-32s casou %d vez(es)' % (rotulo, quantos))
        if quantos != 1:
            falhou = True
            continue
        d = d.replace(v, n, 1)

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    with io.open(ARQ + '.antes-da-salmoura', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())

    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)

    print('\ngravado: %s (backup .antes-da-salmoura)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())
