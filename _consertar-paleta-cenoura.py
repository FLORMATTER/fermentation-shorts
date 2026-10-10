# -*- coding: utf-8 -*-
"""
_consertar-paleta-cenoura.py — tirar o VERDE que sobrou do template do pepino.

O short da cenoura nasceu do `pepino/shorts-pepino-apple-en.html`. Duas pecas
do cenario continuavam com a cor do PEPINO, nao do legume novo:

    cena 5  pilula "ONLY 4 TO 5 DAYS"  #e1f5ee / #1d9e75 / #04342c  (verde)
    cena 2  jato do liquido            #5dcaa5                      (verde)

O projeto tem regra propria: **cor por ingrediente, para os videos nao ficarem
iguais no feed** (SKILL.md). Pilula verde num video de cenoura faz o short
parecer re-skin do pepino — e' exatamente o que a regra existe para evitar.

Verde -> ambar (paleta que ja' existe no arquivo): #ba7517 / #faeeda / #4a2606.
Jato -> azul #378add (a cena 2 e' a cena da AGUA; verde ali nao significa nada).

A folha da cenoura (#97c459 / #639922) NAO se toca — e' verde de proposito.
"""
import io
import sys

ARQ = 'cenoura/shorts-carrot-apple-en.html'

ANCORAS = [
    (
        'pilula da cena 5 (verde -> ambar)',
        '      <rect x="-116" y="-32" width="232" height="64" rx="12" fill="#e1f5ee" stroke="#1d9e75" stroke-width="3"/>\n'
        '      <text x="0" y="9" text-anchor="middle" font-size="22" font-weight="800" fill="#04342c" font-family="system-ui">ONLY 4 TO 5 DAYS</text>',
        '      <rect x="-116" y="-32" width="232" height="64" rx="12" fill="#faeeda" stroke="#ba7517" stroke-width="3"/>\n'
        '      <text x="0" y="9" text-anchor="middle" font-size="22" font-weight="800" fill="#4a2606" font-family="system-ui">ONLY 4 TO 5 DAYS</text>',
    ),
    (
        'jato da cena 2 (verde -> azul da agua)',
        '      <rect x="196" y="316" width="12" height="54" rx="6" fill="#5dcaa5" opacity=".8"/>',
        '      <rect x="196" y="316" width="12" height="54" rx="6" fill="#378add" opacity=".8"/>',
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
        quantos = d.count(v)
        print('%-40s casou %d vez(es)' % (rotulo, quantos))
        if quantos != 1:
            falhou = True
            continue
        d = d.replace(v, n, 1)

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    with io.open(ARQ + '.antes-da-paleta', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())

    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)

    print('\ngravado: %s (backup .antes-da-paleta)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())
