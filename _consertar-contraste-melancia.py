# -*- coding: utf-8 -*-
"""_consertar-contraste-melancia.py — o copo de SUGAR estava invisivel.

So' o ZOOM mostrou (a folha de contato nao denuncia): o copo e os graos de acucar
eram `#fbf7ea` sobre o fundo `#fdf6f8` — praticamente a MESMA cor. O desenho
existia e nao se via. E' a regra do projeto: "da' pra ver" nao e' medida.

Conserto: o copo fica creme QUENTE (`#f2ead6`) com contorno tan escuro
(`#a8935f`), o rotulo SUGAR escurece para `#6b5a3a` e os graos ficam brancos com
contorno tan — assim aparecem sobre o circulo rosa.

    python _consertar-contraste-melancia.py            # dry-run
    python _consertar-contraste-melancia.py --apply
"""
import io
import sys

GERADOR = '_criar-kombucha-beterraba-melancia.py'

TRABALHO = [
    # o copo: creme quente + contorno escuro
    ('<path d="M-30,-32 L30,-32 L23,26 Q0,38 -23,26 Z" fill="#fbf7ea"'
     ' stroke="#c9bfa4" stroke-width="3"/>',
     '<path d="M-30,-32 L30,-32 L23,26 Q0,38 -23,26 Z" fill="#f2ead6"'
     ' stroke="#a8935f" stroke-width="3.5"/>'),
    # o rotulo SUGAR
    ('font-weight="800" fill="#8a7a5c" font-family="system-ui">SUGAR</text>',
     'font-weight="800" fill="#6b5a3a" font-family="system-ui">SUGAR</text>'),
    # os graos caindo
    ("'<circle cx=\"%d\" cy=\"%d\" r=\"%s\" fill=\"#fdfbf4\" stroke=\"#c9bfa4\"'\n"
     "         ' stroke-width=\"1.6\"/>' % (x, y, r)",
     "'<circle cx=\"%d\" cy=\"%d\" r=\"%s\" fill=\"#ffffff\" stroke=\"#a8935f\"'\n"
     "         ' stroke-width=\"1.8\"/>' % (x, y, r)"),
]


def main():
    aplicar = '--apply' in sys.argv
    with io.open(GERADOR, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    antes = len(d)

    for velho, _ in TRABALHO:
        n = d.count(velho)
        print('  ancora %-56s %d vez(es)' % (velho.split('\n')[0][:56], n))
        if n != 1:
            print('ABORTA: ancora casou %d vez(es), esperava 1.' % n)
            return 1
    for velho, novo in TRABALHO:
        d = d.replace(velho, novo, 1)

    for trecho in ('#f2ead6', '#6b5a3a', 'fill="#ffffff" stroke="#a8935f"'):
        if trecho not in d:
            print('ABORTA: nao achei "%s" depois da troca.' % trecho)
            return 1
    for velho in ('#fbf7ea', '#fdfbf4'):
        if velho in d:
            print('ABORTA: sobrou a cor apagada "%s".' % velho)
            return 1
    try:
        compile(d, GERADOR, 'exec')
    except SyntaxError as e:
        print('ABORTA: sintaxe invalida — %s' % e)
        return 1

    print('%s: %d -> %d bytes' % (GERADOR, antes, len(d)))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(GERADOR, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
