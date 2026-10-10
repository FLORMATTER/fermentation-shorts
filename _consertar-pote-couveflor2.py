# -*- coding: utf-8 -*-
"""
_consertar-pote-couveflor2.py — o jarro era mais LARGO que ALTO.

O jarro herdado do template media 208 de largura por 168 de altura: deitado.
Nenhuma quantidade de vidro na base conserta isso — o olho le' "caixa".

Conserto: jarro de verdade, 156 x 224 (mais alto que largo), com a salmoura ate'
y=124 de um corpo que vai ate' 148 — sobra uma base de vidro de 24 unidades, que
e' o que faz ler "pote". Os floretes se espalham pelo jarro inteiro e a maca fica
no topo, boiando (que e' o ponto da cena).

Medido: salmoura `#b9cd8c` x vidro `#fdfcf7` = 135 | florete `#fbfaf3` x salmoura
= 130 | maca `#e24b4a` x salmoura = 151.
"""
import io
import re
import sys

ARQ = 'couve-flor/shorts-cauliflower-apple-en.html'

S4 = '''<svg class="scene" id="s4" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#eef3e2"/>
    <g transform="translate(202,300)">
      <path d="M-78,148 L-78,-58 Q-78,-76 -60,-76 L60,-76 Q78,-76 78,-58 L78,148 Z"
            fill="#fdfcf7" stroke="#5c7a29" stroke-width="4"/>
      <rect x="-78" y="-76" width="156" height="24" rx="6" fill="#c9d9a4" stroke="#5c7a29" stroke-width="4"/>
      <path d="M-78,124 L-78,-32 Q-78,-48 -60,-48 L60,-48 Q78,-48 78,-32 L78,124 Z" fill="#b9cd8c"/>
      <g fill="#fbfaf3" stroke="#93a663" stroke-width="2.5">
        <ellipse cx="-52" cy="88" rx="24" ry="21" transform="rotate(-12 -52 88)"/>
        <ellipse cx="-4" cy="100" rx="26" ry="22" transform="rotate(8 -4 100)"/>
        <ellipse cx="48" cy="84" rx="24" ry="21" transform="rotate(-6 48 84)"/>
        <ellipse cx="-34" cy="50" rx="23" ry="20" transform="rotate(14 -34 50)"/>
        <ellipse cx="36" cy="52" rx="23" ry="20" transform="rotate(-10 36 52)"/>
        <ellipse cx="0" cy="62" rx="25" ry="22" transform="rotate(-5 0 62)"/>
        <ellipse cx="-56" cy="12" rx="21" ry="18" transform="rotate(6 -56 12)"/>
        <ellipse cx="54" cy="14" rx="21" ry="18" transform="rotate(-8 54 14)"/>
        <ellipse cx="-22" cy="20" rx="23" ry="20" transform="rotate(10 -22 20)"/>
        <ellipse cx="24" cy="22" rx="23" ry="20" transform="rotate(-4 24 22)"/>
      </g>
      <g fill="#e24b4a" stroke="#a32d2d" stroke-width="2.5">
        <rect x="-30" y="-44" width="44" height="26" rx="9" transform="rotate(-8 -8 -31)"/>
        <rect x="20" y="-38" width="40" height="24" rx="9" transform="rotate(14 40 -26)"/>
      </g>
      <g style="animation:riseFast 1.2s ease-out infinite">
        <circle cx="-56" cy="60" r="5.5" fill="#fff" opacity=".85"/>
        <circle cx="-18" cy="82" r="4.5" fill="#fff" opacity=".85"/>
        <circle cx="22" cy="74" r="5" fill="#fff" opacity=".85"/>
        <circle cx="54" cy="86" r="4" fill="#fff" opacity=".85"/>
      </g>
      <g style="animation:riseFast 1.2s ease-out .4s infinite">
        <circle cx="-38" cy="96" r="4.5" fill="#fff" opacity=".75"/>
        <circle cx="4" cy="106" r="5.5" fill="#fff" opacity=".75"/>
        <circle cx="42" cy="98" r="3.8" fill="#fff" opacity=".75"/>
      </g>
      <g style="animation:riseFast 1.2s ease-out .8s infinite">
        <circle cx="-12" cy="112" r="4" fill="#fff" opacity=".6"/>
        <circle cx="30" cy="114" r="4.6" fill="#fff" opacity=".6"/>
      </g>
    </g>
    <g transform="translate(202,566)">
      <text x="0" y="0" text-anchor="middle" font-size="16" font-weight="800" fill="#3f5220" font-family="system-ui">air in the florets - weigh them down</text>
    </g>
  </svg>'''


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()

    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('fim de linha: %d CRLF / %d LF' % (crlf, lf))
    eol = '\r\n' if crlf else '\n'

    m = re.search(r'(?ms)^([ \t]*)<svg class="scene[^"]*"[^>]*id="s4".*?</svg>', d)
    if not m:
        print('ABORTADO — nao achei a cena s4.')
        return 1
    indent = m.group(1)
    linhas = S4.replace('\n', eol).split(eol)
    linhas[0] = indent + linhas[0]
    d = d[:m.start()] + eol.join(linhas) + d[m.end():]
    print('cena s4 trocada por um jarro 156x224')

    with io.open(ARQ + '.antes-do-pote2', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: %s (backup .antes-do-pote2)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())
