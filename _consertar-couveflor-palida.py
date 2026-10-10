# -*- coding: utf-8 -*-
"""
_consertar-couveflor-palida.py — os floretes nao se liam, e o pote ficou oco.

Dois defeitos vistos no render (`_revisar-cenas.py --final`):

1. **Floretes palidos.** Creme `#faf8ee` sobre o circulo `#d8e3bd` a .6 (composto
   `#e1e9cc`) da' distancia **45** — muito abaixo do limiar de ~130. A couve-flor
   saiu como uma mancha clara, sem forma. Conserto: florete BRANCO com CONTORNO
   verde-oliva `#93a663` (2,5 px). O contorno e' que define a forma: contra o
   circulo da' **147**. De quebra, os circulos sobrepostos com contorno leem como
   floretes individuais — que e' exatamente o que a couve-flor e'.

2. **Pote oco.** A salmoura do template ia de y=-30 a y=50 num jarro de -58 a 110:
   o terco de baixo ficava branco. Com os floretes grandes por cima, o pote virou
   tres faixas horizontais (verde/branco/verde). Conserto: salmoura ate' y=100 e
   floretes distribuidores pelo jarro inteiro.

Numeros medidos (alvo: >= ~130):
    florete #ffffff x circulo #e1e9cc ...... 172
    contorno #93a663 x circulo #e1e9cc ..... 147
    folha   #6f8f3c x circulo #e1e9cc ...... 205
    talo    #a9c078 x fundo  #eef3e2 ....... 131
    salmoura #b9cd8c x jarro #fdfcf7 ....... 135
"""
import io
import re
import sys

ARQ = 'couve-flor/shorts-cauliflower-apple-en.html'

# ---------------------------------------------------------------- s0
S0 = '''<svg class="scene on" id="s0" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#eef3e2"/>
    <circle cx="202" cy="300" r="142" fill="#d8e3bd" opacity=".6"/>
    <g transform="translate(118,300)">
      <g style="animation:wobble 3.2s ease-in-out infinite">
        <path d="M-76,28 Q-92,-6 -68,-26 Q-50,-10 -52,24Z" fill="#6f8f3c"/>
        <path d="M76,28 Q92,-6 68,-26 Q50,-10 52,24Z" fill="#6f8f3c"/>
        <path d="M-40,40 Q-46,6 -24,-10 Q-11,9 -15,40Z" fill="#82a44a"/>
        <path d="M40,40 Q46,6 24,-10 Q11,9 15,40Z" fill="#82a44a"/>
        <path d="M-14,56 L-11,94 Q0,100 11,94 L14,56Z" fill="#a9c078"/>
        <circle cx="-50" cy="30" r="26" fill="#f4f7ea" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="50" cy="30" r="26" fill="#f4f7ea" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="-62" cy="4" r="18" fill="#f4f7ea" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="62" cy="4" r="18" fill="#f4f7ea" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="-40" cy="0" r="28" fill="#fbfaf3" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="40" cy="0" r="28" fill="#fbfaf3" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="0" cy="-26" r="28" fill="#ffffff" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="-18" cy="14" r="30" fill="#ffffff" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="18" cy="18" r="28" fill="#ffffff" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="0" cy="42" r="26" fill="#fbfaf3" stroke="#93a663" stroke-width="2.5"/>
      </g>
    </g>
    <g transform="translate(280,344)">
      <g style="animation:wobble 2.4s ease-in-out infinite">
        <circle cx="0" cy="0" r="58" fill="#e24b4a" stroke="#a32d2d" stroke-width="3"/>
        <path d="M0,-54 Q4,-72 1,-84" stroke="#7a5c3e" stroke-width="6" fill="none" stroke-linecap="round"/>
        <ellipse cx="22" cy="-76" rx="20" ry="10" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(-20 22 -76)"/>
        <ellipse cx="-22" cy="-15" rx="11" ry="23" fill="#fff" opacity=".3" transform="rotate(-20 -22 -15)"/>
      </g>
    </g>
    <g transform="translate(332,148)">
      <rect x="-5" y="0" width="10" height="50" rx="4" fill="#5f5e5a" style="animation:chop2x .55s ease-in-out infinite"/>
      <path d="M-4,50 L4,50 L6,118 L-6,118Z" fill="#b4b2a9" style="animation:chop2x .55s ease-in-out infinite"/>
    </g>
  </svg>'''

# ---------------------------------------------------------------- s1
S1 = '''<svg class="scene" id="s1" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#eef3e2"/>
    <ellipse cx="202" cy="540" rx="170" ry="38" fill="#d8e3bd" opacity=".4"/>
    <g transform="translate(112,300)">
      <path d="M-10,50 L-8,88 Q0,94 8,88 L10,50Z" fill="#a9c078"/>
      <circle cx="-22" cy="24" r="22" fill="#f4f7ea" stroke="#93a663" stroke-width="2.5"/>
      <circle cx="22" cy="24" r="22" fill="#f4f7ea" stroke="#93a663" stroke-width="2.5"/>
      <circle cx="-15" cy="-2" r="24" fill="#fbfaf3" stroke="#93a663" stroke-width="2.5"/>
      <circle cx="15" cy="-2" r="24" fill="#fbfaf3" stroke="#93a663" stroke-width="2.5"/>
      <circle cx="0" cy="-26" r="24" fill="#ffffff" stroke="#93a663" stroke-width="2.5"/>
      <circle cx="0" cy="8" r="26" fill="#ffffff" stroke="#93a663" stroke-width="2.5"/>
      <text x="0" y="134" text-anchor="middle" font-size="16" font-weight="800" fill="#3f5220" font-family="system-ui">small</text>
    </g>
    <g transform="translate(202,300)">
      <path d="M-12,0 L12,0" stroke="#5f5e5a" stroke-width="6" stroke-linecap="round"/>
    </g>
    <g transform="translate(292,300)">
      <rect x="-38" y="-72" width="76" height="150" rx="18" fill="#e24b4a" stroke="#a32d2d" stroke-width="3"/>
      <rect x="-26" y="-58" width="52" height="122" rx="12" fill="#fbe9e7"/>
      <ellipse cx="-7" cy="-20" rx="4" ry="7" fill="#7a5c3e"/>
      <ellipse cx="8" cy="24" rx="4" ry="7" fill="#7a5c3e"/>
      <ellipse cx="-14" cy="-40" rx="7" ry="18" fill="#fff" opacity=".35"/>
      <text x="0" y="134" text-anchor="middle" font-size="16" font-weight="800" fill="#791f1f" font-family="system-ui">thick</text>
    </g>
  </svg>'''

# ---------------------------------------------------------------- s3
S3 = '''<svg class="scene" id="s3" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#fbe9e7"/>
    <ellipse cx="202" cy="516" rx="158" ry="34" fill="#e24b4a" opacity=".12"/>
    <g transform="translate(108,248)">
      <g style="animation:wobble 2.6s ease-in-out infinite">
        <circle cx="0" cy="0" r="56" fill="#e24b4a" stroke="#a32d2d" stroke-width="3"/>
        <path d="M0,-52 Q4,-68 1,-80" stroke="#7a5c3e" stroke-width="6" fill="none" stroke-linecap="round"/>
        <ellipse cx="22" cy="-72" rx="19" ry="10" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(-20 22 -72)"/>
        <ellipse cx="-21" cy="-14" rx="11" ry="22" fill="#fff" opacity=".3" transform="rotate(-20 -21 -14)"/>
      </g>
      <text x="0" y="98" text-anchor="middle" font-size="16" font-weight="800" fill="#791f1f" font-family="system-ui">sugar + yeast</text>
    </g>
    <g transform="translate(296,248)">
      <g style="animation:tick 2.2s ease-in-out infinite">
        <path d="M-9,46 L-7,80 Q0,86 7,80 L9,46Z" fill="#a9c078"/>
        <circle cx="-20" cy="22" r="20" fill="#f4f7ea" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="20" cy="22" r="20" fill="#f4f7ea" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="-13" cy="-2" r="22" fill="#fbfaf3" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="13" cy="-2" r="22" fill="#fbfaf3" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="0" cy="-24" r="22" fill="#ffffff" stroke="#93a663" stroke-width="2.5"/>
        <circle cx="0" cy="8" r="24" fill="#ffffff" stroke="#93a663" stroke-width="2.5"/>
      </g>
      <text x="0" y="98" text-anchor="middle" font-size="16" font-weight="800" fill="#3f5220" font-family="system-ui">dense + slow</text>
    </g>
    <g transform="translate(202,448)">
      <rect x="-150" y="-38" width="300" height="76" rx="12" fill="#fff" stroke="#e24b4a" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="19" font-weight="800" fill="#791f1f" font-family="system-ui">THE APPLE STARTS IT</text>
      <text x="0" y="24" text-anchor="middle" font-size="14" font-weight="600" fill="#a32d2d" font-family="system-ui">sugar feeds the bacteria - acid comes sooner</text>
    </g>
  </svg>'''

# ---------------------------------------------------------------- s4
S4 = '''<svg class="scene" id="s4" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#eef3e2"/>
    <g transform="translate(202,286)">
      <path d="M-104,110 L-104,-40 Q-104,-58 -86,-58 L86,-58 Q104,-58 104,-40 L104,110 Z"
            fill="#fdfcf7" stroke="#5c7a29" stroke-width="4"/>
      <rect x="-104" y="-58" width="208" height="24" rx="6" fill="#c9d9a4" stroke="#5c7a29" stroke-width="4"/>
      <path d="M-104,100 L-104,-14 Q-104,-30 -86,-30 L86,-30 Q104,-30 104,-14 L104,100 Z" fill="#b9cd8c"/>
      <g fill="#fbfaf3" stroke="#93a663" stroke-width="2.5">
        <ellipse cx="-64" cy="62" rx="26" ry="23" transform="rotate(-12 -64 62)"/>
        <ellipse cx="-12" cy="74" rx="28" ry="24" transform="rotate(8 -12 74)"/>
        <ellipse cx="52" cy="58" rx="26" ry="23" transform="rotate(-6 52 58)"/>
        <ellipse cx="-42" cy="26" rx="24" ry="21" transform="rotate(14 -42 26)"/>
        <ellipse cx="34" cy="28" rx="24" ry="21" transform="rotate(-10 34 28)"/>
        <ellipse cx="-64" cy="-6" rx="22" ry="19" transform="rotate(6 -64 -6)"/>
        <ellipse cx="58" cy="-4" rx="22" ry="19" transform="rotate(-8 58 -4)"/>
        <ellipse cx="-4" cy="30" rx="26" ry="23" transform="rotate(-5 -4 30)"/>
      </g>
      <g fill="#e24b4a" stroke="#a32d2d" stroke-width="2.5">
        <rect x="-30" y="-34" width="44" height="26" rx="9" transform="rotate(-8 -8 -21)"/>
        <rect x="22" y="-28" width="40" height="24" rx="9" transform="rotate(14 42 -16)"/>
      </g>
      <g style="animation:riseFast 1.2s ease-out infinite">
        <circle cx="-62" cy="20" r="5.5" fill="#fff" opacity=".85"/>
        <circle cx="-22" cy="42" r="4.5" fill="#fff" opacity=".85"/>
        <circle cx="20" cy="34" r="5" fill="#fff" opacity=".85"/>
        <circle cx="60" cy="44" r="4" fill="#fff" opacity=".85"/>
      </g>
      <g style="animation:riseFast 1.2s ease-out .4s infinite">
        <circle cx="-42" cy="46" r="4.5" fill="#fff" opacity=".75"/>
        <circle cx="2" cy="52" r="5.5" fill="#fff" opacity=".75"/>
        <circle cx="44" cy="46" r="3.8" fill="#fff" opacity=".75"/>
      </g>
      <g style="animation:riseFast 1.2s ease-out .8s infinite">
        <circle cx="-12" cy="58" r="4" fill="#fff" opacity=".6"/>
        <circle cx="30" cy="60" r="4.6" fill="#fff" opacity=".6"/>
      </g>
    </g>
    <g transform="translate(202,560)">
      <text x="0" y="0" text-anchor="middle" font-size="16" font-weight="800" fill="#3f5220" font-family="system-ui">air in the florets - weigh them down</text>
    </g>
  </svg>'''

NOVAS = [('s0', S0), ('s1', S1), ('s3', S3), ('s4', S4)]


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()

    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('fim de linha: %d CRLF / %d LF' % (crlf, lf))
    eol = '\r\n' if crlf else '\n'

    falhou = False
    for cid, novo in NOVAS:
        m = re.search(r'(?ms)^([ \t]*)<svg class="scene[^"]*"[^>]*id="%s".*?</svg>' % cid, d)
        if not m:
            print('cena %-4s NAO ACHEI' % cid)
            falhou = True
            continue
        indent = m.group(1)
        linhas = novo.replace('\n', eol).split(eol)
        linhas[0] = indent + linhas[0]
        bloco = eol.join(linhas)
        d = d[:m.start()] + bloco + d[m.end():]
        print('cena %-4s trocada (%d car)' % (cid, len(bloco)))

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    with io.open(ARQ + '.antes-da-palida', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('\ngravado: %s (backup .antes-da-palida)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())
