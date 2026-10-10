# -*- coding: utf-8 -*-
"""_melhorar-melao2.py — 2a passada no melao INTEIRO do short maca+melao.

O zoom em 3x mostrou: bola bege com GRADE SIMETRICA = **waffle / bola de tenis**.

O que faz ler "melao" nao e' a grade — sao as **SUTURAS**: as lombadas que vao de
cima a baixo e dao a forma. Com as lombadas, a rede pode ser ESPARSA e ONDULADA
por cima, que e' como o cantalupo realmente parece.

    python _melhorar-melao2.py
"""
import io
import re
import sys

ALVO = '_criar-kombucha-melao.py'

NOVO = '''def melao_inteiro(x, y, s=1.0):
    """Melao inteiro: casca BEGE, com SUTURAS e uma rede esparsa por cima.

    Grade simetrica le' como WAFFLE (2o render); bola lisa le' como bola. O que
    faz ler "melao" sao as LOMBADAS de cima a baixo (as suturas). Com elas, a
    rede pode ser ondulada e irregular — que e' como o cantalupo parece.
    """
    R = 76
    p = []
    for c, bojo in ((-44, 12), (-16, 14), (16, 14), (44, 12)):
        p.append(f'<path d="M{c},-64 C{c + bojo},-24 {c + bojo},24 {c},64"'
                 ' fill="none" stroke="#c0ab7d" stroke-width="2.4" opacity=".75"/>')
    for c, bojo in ((-56, 5), (-30, 9), (-6, 6), (18, 10), (42, 7), (58, 4)):
        h = (R * R - c * c) ** 0.5 * 0.93
        p.append(f'<path d="M{c},{-h:.1f} C{c + bojo},{-h * 0.45:.1f}'
                 f' {c - bojo * 0.6:.1f},{h * 0.45:.1f} {c},{h:.1f}" fill="none"'
                 ' stroke="#f7f0dc" stroke-width="3.4" opacity=".92"'
                 ' stroke-linecap="round"/>')
    for c, bojo in ((-48, 6), (-22, 5), (2, 9), (26, 6), (48, 5)):
        h = (R * R - c * c) ** 0.5 * 0.93
        p.append(f'<path d="M{-h:.1f},{c} C{-h * 0.45:.1f},{c + bojo:.1f}'
                 f' {h * 0.45:.1f},{c - bojo * 0.6:.1f} {h:.1f},{c}" fill="none"'
                 ' stroke="#f7f0dc" stroke-width="3.4" opacity=".92"'
                 ' stroke-linecap="round"/>')
    return (f'<g transform="translate({x:g},{y:g}) scale({s:g})">'
            f'<circle r="{R}" fill="#cbb98c" stroke="#a8935f" stroke-width="3.5"/>'
            f'<circle r="{R - 3}" fill="#e2d3ad"/>'
            + ''.join(p) +
            '<ellipse cy="-71" rx="8" ry="5.5" fill="#a8935f"/>'
            '</g>')'''


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    # ATENCAO: o `.*?\n` JA' consome um \n — no lookahead sobram DOIS, nao tres.
    pat = re.compile(r'def melao_inteiro\(.*?\n(?=\n\ndef maca\()', re.S)
    if len(pat.findall(d)) != 1:
        print('ERRO: bloco melao_inteiro casou %d vez(es)' % len(pat.findall(d)))
        return 1
    d = pat.sub(lambda m: NOVO + '\n', d, count=1)

    for nome in ('melao_metade', 'melao_inteiro', 'maca', 'faca'):
        if len(re.findall(r'^def %s\(' % nome, d, re.M)) != 1:
            print('ERRO: `def %s` sumiu ou duplicou' % nome)
            return 1
    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as exc:
        print('ERRO: nao compila: linha %s: %s' % (exc.lineno, exc.msg))
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: melao_inteiro trocado | %d bytes' % len(d.encode('utf-8')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
