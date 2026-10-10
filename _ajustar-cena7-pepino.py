# -*- coding: utf-8 -*-
"""_ajustar-cena7-pepino.py — troca o conselho fraco da cena 7 do pepino+alho.

A cena 7 dizia "DO NOT BLANCH IT / you would only lose the flavour". Isso e' um
espantalho: ninguem escalda pepino em conserva. O conselho de verdade — e que
ninguem espera — e' **cortar a ponta da flor**: e' ali que ficam as enzimas que
amolecem a conserva. Substancia no lugar de verniz.

    python _ajustar-cena7-pepino.py
"""
import io
import sys

ALVO = '_criar-pepino-alho.py'

TROCAS = [
    # 1) o cartao da cena 7
    ('<text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" '
     'fill="#2f5c0d" font-family="system-ui">DO NOT BLANCH IT</text>\n'
     '      <text x="0" y="14" text-anchor="middle" font-size="13" font-weight="600" '
     'fill="#6b8f3a" font-family="system-ui">you would only lose the flavour</text>',
     '<text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" '
     'fill="#2f5c0d" font-family="system-ui">TRIM THE BLOSSOM END</text>\n'
     '      <text x="0" y="14" text-anchor="middle" font-size="13" font-weight="600" '
     'fill="#6b8f3a" font-family="system-ui">that end holds the softening enzyme</text>',
     1),
    # 2) a legenda da cena 7
    ("('s6', 6400, '%s 7 / 7' % TAG, 'So eat it',\n"
     "         'the colour changes nothing', '#2f5c0d'),",
     "('s6', 6400, '%s 7 / 7' % TAG, 'One last thing',\n"
     "         'trim the blossom end before you start', '#2f5c0d'),",
     1),
]


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    print('%s: %d bytes' % (ALVO, len(d.encode('utf-8'))))

    for velho, novo, esperado in TROCAS:
        c = d.count(velho)
        if c != esperado:
            print('ERRO: ancora casou %d (esperado %d): %r'
                  % (c, esperado, velho[:70]))
            return 1
        d = d.replace(velho, novo)
        print('  ok: %r' % novo[:60])

    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as exc:
        print('ERRO: nao compila: linha %s: %s' % (exc.lineno, exc.msg))
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: -> %d bytes' % len(d.encode('utf-8')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
