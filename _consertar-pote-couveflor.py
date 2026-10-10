# -*- coding: utf-8 -*-
"""
_consertar-pote-couveflor.py — o pote lia como CAIXA VERDE, nao como vidro.

A salmoura herdada do template ia de y=-30 a y=100 num jarro que termina em 110.
Sobravam 10 unidades de vidro — invisiveis. Como o liquido cobre quase todo o
corpo do jarro e a tampa (`#c9d9a4`) fica a distancia 31 da salmoura (`#b9cd8c`,
ou seja, some), o conjunto virou um retangulo verde chapado.

No template do #18 o pote lia bem porque sobrava uma FAIXA BRANCA na base — e' o
que faz o olho ler "vidro". Conserto: salmoura ate' y=86, deixando 24 unidades de
`#fdfcf7` aparecendo embaixo.

Medido: salmoura `#b9cd8c` x vidro `#fdfcf7` = 135 (acima do limiar de ~130).
"""
import io
import sys

ARQ = 'couve-flor/shorts-cauliflower-apple-en.html'

VELHO = '<path d="M-104,100 L-104,-14 Q-104,-30 -86,-30 L86,-30 Q104,-30 104,-14 L104,100 Z" fill="#b9cd8c"/>'
NOVO = '<path d="M-104,86 L-104,-14 Q-104,-30 -86,-30 L86,-30 Q104,-30 104,-14 L104,86 Z" fill="#b9cd8c"/>'


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()

    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('fim de linha: %d CRLF / %d LF' % (crlf, lf))

    q = d.count(VELHO)
    print('ancora da salmoura casou %d vez(es)' % q)
    if q != 1:
        print('ABORTADO — nada foi gravado.')
        return 1

    d = d.replace(VELHO, NOVO, 1)

    with io.open(ARQ + '.antes-do-pote', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: %s (backup .antes-do-pote)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())
