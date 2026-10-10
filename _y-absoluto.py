# -*- coding: utf-8 -*-
"""
_y-absoluto.py — descobre o y REAL de cada <text>, somando os <g transform>.

Por que existe: o _validar-short.py pega texto abaixo de y=645 lendo o atributo
`y` do proprio <text>. Mas quando o texto esta dentro de
    <g transform="translate(0,392)">
        <text y="0">...</text>
    </g>
o y real e 392, e o validador ve "0" — passa limpo e o texto fica escondido
atras da barra de legenda. Este script acumula os translate() aninhados.

Uso:
    python _y-absoluto.py arquivo.html              # so o que invade y>=647
    python _y-absoluto.py arquivo.html --todos      # lista tudo
    python _y-absoluto.py arquivo.html --limite 640
"""
import io
import os
import re
import sys

TAG = re.compile(r'<(/?)g\b([^>]*)>|<text\b([^>]*)>', re.S)
TRANS = re.compile(r'transform\s*=\s*"([^"]*)"')
TRANSLA = re.compile(r'translate\(\s*(-?[\d.]+)[\s,]+(-?[\d.]+)\s*\)')
ATRY = re.compile(r'\by\s*=\s*"(-?[\d.]+)"')


def y_dos_textos(corpo):
    """Devolve [(y_absoluto, trecho_do_texto)] na ordem do documento."""
    pilha = [0.0]      # deslocamento vertical acumulado
    saida = []
    for m in TAG.finditer(corpo):
        fecha, attr_g, attr_t = m.group(1), m.group(2), m.group(3)
        if attr_g is not None:                      # <g ...> ou </g>
            if fecha:
                if len(pilha) > 1:
                    pilha.pop()
            else:
                dy = 0.0
                tr = TRANS.search(attr_g)
                if tr:
                    for t in TRANSLA.finditer(tr.group(1)):
                        dy += float(t.group(2))
                pilha.append(pilha[-1] + dy)
        elif attr_t is not None:                    # <text ...>
            my = ATRY.search(attr_t)
            if my:
                fim = corpo.find('</text>', m.end())
                conteudo = re.sub(r'<[^>]+>', '', corpo[m.end():fim]).strip()
                saida.append((pilha[-1] + float(my.group(1)), conteudo[:46]))
    return saida


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        return 1
    limite = 647.0
    if '--limite' in sys.argv:
        limite = float(sys.argv[sys.argv.index('--limite') + 1])
    todos = '--todos' in sys.argv

    arquivo = args[0]
    d = io.open(arquivo, encoding='utf-8').read()
    corpos = re.findall(r'body:`(.*?)`', d, re.S)
    print('%s — %d cena(s) com body:' % (os.path.basename(arquivo), len(corpos)))
    print('limite: y >= %.0f  (a barra .ncap cobre 647..720)\n' % limite)

    ruins = 0
    for i, corpo in enumerate(corpos):
        itens = y_dos_textos(corpo)
        if not itens:
            continue
        altos = [(y, t) for y, t in itens if y >= limite]
        if todos:
            print('cena %d: %s' % (i, ', '.join('%.0f' % y for y, _ in itens)))
        if altos:
            ruins += 1
            print('[X] cena %d — %d texto(s) dentro da barra:' % (i, len(altos)))
            for y, t in altos:
                print('      y=%.0f  %s' % (y, t))

    if not ruins:
        print('OK — nenhum texto invade a barra de legenda.')
    else:
        print('\n%d cena(s) com texto escondido atras da legenda.' % ruins)
    return 1 if ruins else 0


if __name__ == '__main__':
    sys.exit(main())
