# -*- coding: utf-8 -*-
"""
_criar-couveflor-maca.py — cria `couve-flor/shorts-cauliflower-apple-en.html`.

    python _criar-couveflor-maca.py

Template: `cenoura/shorts-carrot-apple-en.html` (#18) — o mais novo da serie, ja'
tem a maca desenhada, o sistema de selos e o validador passando limpo. Mesmo
conceito ("legume + maca"), entao a estrutura serve inteira.

O DESENHO DA COUVE-FLOR vem do #5 (`couve-flor/shorts-couveflor-animado-en.html`):
nuvem de circulos creme para os floretes, folhas verdes por baixo, talo palido.
Geometria conferida com `_extrair-cena.py`.

=== A SUBSTANCIA (pesquisada, nao inventada) ===

O #5 ja' ensina: floretes, quebrar com a mao, 2,5% de sal, massagem, prender
embaixo, 7-10 dias. **Este video nao repete nada disso** — ele e' sobre a MACA,
que nenhum video da serie toca.

  - couve-flor e' 90% agua, parede celular DENSA: a bacteria demora mais para
    pegar (5-7 dias, contra 3-5 do repolho). Comeco lento.
  - o comeco lento e' justamente a janela dos glucosinolatos -> mirosinase ->
    isotiocianatos/nitrilas. E' dai que vem o cheiro de ovo podre e o amargo.
  - **o pH regula a mirosinase.** Acido mais cedo = janela do enxofre mais curta.
  - a maca traz ACUCAR (comida da bacteria) e levedura na casca. Ela e' um
    **starter**, nao um sabor.
  - os floretes tem superficie irregular e prendem bolha de ar; ar = mais H2S.
    Por isso a couve-flor flutua E segura ar — pior que quase todo legume.
  - abrir o pote cheira pior do que come: e' H2S acumulado. Esperar 5 minutos.
  - pH alvo 3,6-4,0; 2,5% de sal (25 g/L); 18-20 C.

Fontes: fermenthive.com (glucosinolatos, H2S, submersao, 3% para brassicas) e
sourchad.com (mirosinase regulada por pH, 2,5%, pH 3,6-4,0, sucessao LAB).

=== CUIDADOS ===
  - so' usa keyframes que JA' existem no template (pulseBadge, chop2x, pour2x,
    riseFast, wobble, tick) — o validador reprova keyframe orfao.
  - contraste do liquido MEDIDO depois do render (licao do #18): jarro `#fdfcf7`,
    salmoura `#b9cd8c` (distancia 135), florete `#faf8ee` (130), maca `#e24b4a`
    (151). Tudo acima do limiar de ~130.
  - a barra de legenda NAO repete o texto que ja' esta' no SVG (licao do #19).
"""
import io
import re
import sys

ORIGEM = 'cenoura/shorts-carrot-apple-en.html'
DESTINO = 'couve-flor/shorts-cauliflower-apple-en.html'

# =================================================================== s0
S0_NOVO = '''<svg class="scene on" id="s0" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#eef3e2"/>
    <circle cx="202" cy="300" r="142" fill="#d8e3bd" opacity=".6"/>
    <g transform="translate(124,300)">
      <g style="animation:wobble 3.2s ease-in-out infinite">
        <path d="M-70,26 Q-84,-6 -62,-24 Q-46,-10 -48,22Z" fill="#6f8f3c"/>
        <path d="M70,26 Q84,-6 62,-24 Q46,-10 48,22Z" fill="#6f8f3c"/>
        <path d="M-36,36 Q-42,4 -22,-10 Q-10,8 -14,36Z" fill="#82a44a"/>
        <path d="M36,36 Q42,4 22,-10 Q10,8 14,36Z" fill="#82a44a"/>
        <circle cx="-46" cy="28" r="28" fill="#f2efe0"/>
        <circle cx="46" cy="28" r="28" fill="#f2efe0"/>
        <circle cx="-38" cy="-2" r="30" fill="#faf8ee"/>
        <circle cx="38" cy="-2" r="30" fill="#faf8ee"/>
        <circle cx="0" cy="-24" r="30" fill="#fdfbf4"/>
        <circle cx="0" cy="12" r="32" fill="#faf8ee"/>
        <circle cx="-58" cy="4" r="18" fill="#efeadd"/>
        <circle cx="58" cy="4" r="18" fill="#efeadd"/>
        <g fill="none" stroke="#ded8c4" stroke-width="1.6" opacity=".9">
          <path d="M-24,-6 Q-12,8 0,-2"/>
          <path d="M24,-6 Q12,8 0,-2"/>
          <path d="M-14,22 Q0,30 14,22"/>
        </g>
        <path d="M-13,54 L-10,88 Q0,94 10,88 L13,54Z" fill="#cfe0a8"/>
      </g>
    </g>
    <g transform="translate(276,344)">
      <g style="animation:wobble 2.4s ease-in-out infinite">
        <circle cx="0" cy="0" r="58" fill="#e24b4a" stroke="#a32d2d" stroke-width="3"/>
        <path d="M0,-54 Q4,-72 1,-84" stroke="#7a5c3e" stroke-width="6" fill="none" stroke-linecap="round"/>
        <ellipse cx="22" cy="-76" rx="20" ry="10" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(-20 22 -76)"/>
        <ellipse cx="-22" cy="-15" rx="11" ry="23" fill="#fff" opacity=".3" transform="rotate(-20 -22 -15)"/>
      </g>
    </g>
    <g transform="translate(330,148)">
      <rect x="-5" y="0" width="10" height="50" rx="4" fill="#5f5e5a" style="animation:chop2x .55s ease-in-out infinite"/>
      <path d="M-4,50 L4,50 L6,118 L-6,118Z" fill="#b4b2a9" style="animation:chop2x .55s ease-in-out infinite"/>
    </g>
  </svg>'''

# =================================================================== s1
S1_NOVO = '''<svg class="scene" id="s1" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#eef3e2"/>
    <ellipse cx="202" cy="540" rx="170" ry="38" fill="#d8e3bd" opacity=".4"/>
    <g transform="translate(112,300)">
      <path d="M-9,52 L-7,86 Q0,92 7,86 L9,52Z" fill="#cfe0a8"/>
      <circle cx="-20" cy="22" r="24" fill="#f2efe0"/>
      <circle cx="20" cy="22" r="24" fill="#f2efe0"/>
      <circle cx="-14" cy="-4" r="26" fill="#faf8ee"/>
      <circle cx="14" cy="-4" r="26" fill="#faf8ee"/>
      <circle cx="0" cy="-26" r="26" fill="#fdfbf4"/>
      <circle cx="0" cy="6" r="28" fill="#faf8ee"/>
      <g fill="none" stroke="#ded8c4" stroke-width="1.5" opacity=".9">
        <path d="M-14,-6 Q-6,6 0,-2"/>
        <path d="M14,-6 Q6,6 0,-2"/>
      </g>
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

# =================================================================== s2
S2_NOVO = '''<svg class="scene" id="s2" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#e6f1fb"/>
    <g transform="translate(202,250)">
      <path d="M-56,-70 L56,-70 L50,-46 L-50,-46Z" fill="#b5d4f4" stroke="#378add" stroke-width="3"/>
      <rect x="-50" y="-46" width="100" height="82" rx="10" fill="#e6f1fb" stroke="#378add" stroke-width="3"/>
      <text x="0" y="14" text-anchor="middle" font-size="26" font-weight="800" fill="#0c447c" font-family="system-ui">1 L</text>
      <text x="0" y="66" text-anchor="middle" font-size="13" font-weight="700" fill="#185fa5" font-family="system-ui">of water</text>
    </g>
    <text x="318" y="258" text-anchor="middle" font-size="40" font-weight="800" fill="#378add" font-family="system-ui">+</text>
    <g transform="translate(202,420)">
      <path d="M-56,-44 L56,-44 L50,66 Q0,80 -50,66Z" fill="#fff" stroke="#378add" stroke-width="3.5"/>
      <rect x="-50" y="-34" width="100" height="13" rx="4" fill="#b5d4f4"/>
      <text x="0" y="20" text-anchor="middle" font-size="28" font-weight="800" fill="#0c447c" font-family="system-ui">25 g</text>
      <text x="0" y="46" text-anchor="middle" font-size="14" font-weight="700" fill="#185fa5" font-family="system-ui">of salt</text>
    </g>
    <g style="animation:pour2x 1.1s ease-out infinite">
      <rect x="196" y="316" width="12" height="54" rx="6" fill="#378add" opacity=".8"/>
    </g>
    <text x="202" y="600" text-anchor="middle" font-size="22" font-weight="800" fill="#0c447c" font-family="system-ui">2.5% brine</text>
  </svg>'''

# =================================================================== s3
S3_NOVO = '''<svg class="scene" id="s3" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
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
        <path d="M-9,48 L-7,80 Q0,86 7,80 L9,48Z" fill="#cfe0a8"/>
        <circle cx="-19" cy="20" r="22" fill="#f2efe0"/>
        <circle cx="19" cy="20" r="22" fill="#f2efe0"/>
        <circle cx="-13" cy="-4" r="24" fill="#faf8ee"/>
        <circle cx="13" cy="-4" r="24" fill="#faf8ee"/>
        <circle cx="0" cy="-24" r="24" fill="#fdfbf4"/>
        <circle cx="0" cy="6" r="26" fill="#faf8ee"/>
        <g fill="none" stroke="#ded8c4" stroke-width="1.5" opacity=".9">
          <path d="M-13,-6 Q-6,5 0,-2"/>
          <path d="M13,-6 Q6,5 0,-2"/>
        </g>
      </g>
      <text x="0" y="98" text-anchor="middle" font-size="16" font-weight="800" fill="#3f5220" font-family="system-ui">dense + slow</text>
    </g>
    <g transform="translate(202,448)">
      <rect x="-150" y="-38" width="300" height="76" rx="12" fill="#fff" stroke="#e24b4a" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="19" font-weight="800" fill="#791f1f" font-family="system-ui">THE APPLE STARTS IT</text>
      <text x="0" y="24" text-anchor="middle" font-size="14" font-weight="600" fill="#a32d2d" font-family="system-ui">sugar feeds the bacteria - acid comes sooner</text>
    </g>
  </svg>'''

# =================================================================== s4
S4_NOVO = '''<svg class="scene" id="s4" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#eef3e2"/>
    <g transform="translate(202,286)">
      <path d="M-104,110 L-104,-40 Q-104,-58 -86,-58 L86,-58 Q104,-58 104,-40 L104,110 Z"
            fill="#fdfcf7" stroke="#5c7a29" stroke-width="4"/>
      <rect x="-104" y="-58" width="208" height="24" rx="6" fill="#c9d9a4" stroke="#5c7a29" stroke-width="4"/>
      <path d="M-104,50 L-104,-14 Q-104,-30 -86,-30 L86,-30 Q104,-30 104,-14 L104,50 Z" fill="#b9cd8c"/>
      <g fill="#faf8ee" stroke="#ded8c4" stroke-width="2">
        <ellipse cx="-62" cy="14" rx="30" ry="26" transform="rotate(-12 -62 14)"/>
        <ellipse cx="-6" cy="26" rx="32" ry="28" transform="rotate(8 -6 26)"/>
        <ellipse cx="56" cy="10" rx="30" ry="26" transform="rotate(-6 56 10)"/>
        <ellipse cx="-34" cy="-8" rx="28" ry="24" transform="rotate(14 -34 -8)"/>
        <ellipse cx="30" cy="-6" rx="28" ry="24" transform="rotate(-10 30 -6)"/>
      </g>
      <g fill="#e24b4a" stroke="#a32d2d" stroke-width="2.5">
        <rect x="-30" y="-34" width="44" height="26" rx="9" transform="rotate(-8 -8 -21)"/>
        <rect x="22" y="-28" width="40" height="24" rx="9" transform="rotate(14 42 -16)"/>
      </g>
      <g style="animation:riseFast 1.2s ease-out infinite">
        <circle cx="-62" cy="30" r="5.5" fill="#fff" opacity=".85"/>
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

# =================================================================== s5
S5_NOVO = '''<svg class="scene" id="s5" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#f1efe8"/>
    <circle cx="202" cy="300" r="132" fill="#d3d1c7" opacity=".4"/>
    <g transform="translate(202,300)">
      <g style="animation:tick 1.2s ease-in-out infinite">
        <circle cx="0" cy="0" r="96" fill="#f4faf3" stroke="#5f5e5a" stroke-width="4"/>
        <path d="M0,-96 L0,0 L62,74" stroke="#5f5e5a" stroke-width="5.5" stroke-linecap="round" fill="none"/>
        <path d="M0,0 L-54,-64" stroke="#888780" stroke-width="5" stroke-linecap="round" fill="none"/>
        <circle cx="0" cy="0" r="7" fill="#5f5e5a"/>
      </g>
    </g>
    <g transform="translate(202,466)">
      <rect x="-116" y="-32" width="232" height="64" rx="12" fill="#eef3e2" stroke="#5c7a29" stroke-width="3"/>
      <text x="0" y="9" text-anchor="middle" font-size="22" font-weight="800" fill="#3f5220" font-family="system-ui">5 TO 7 DAYS</text>
    </g>
  </svg>'''

# =================================================================== s6
S6_NOVO = '''<svg class="scene" id="s6" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#eef3e2"/>
    <circle cx="202" cy="278" r="130" fill="#d8e3bd" opacity=".6"/>
    <g transform="translate(202,278)">
      <circle cx="0" cy="0" r="82" fill="#fdfcf7" stroke="#5c7a29" stroke-width="4"/>
      <path d="M-32,4 L-8,30 L34,-24" stroke="#3f5220" stroke-width="11" fill="none"
            stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g transform="translate(202,444)">
      <text x="0" y="0" text-anchor="middle" font-size="25" font-weight="800" fill="#3f5220" font-family="system-ui">Crisp and a little sweet</text>
      <text x="0" y="32" text-anchor="middle" font-size="15" font-weight="600" fill="#5c7a29" font-family="system-ui">the jar smells worse than it tastes</text>
    </g>
  </svg>'''

# =================================================================== array
SCENES_NOVO = """const scenes = [
  { id:'s0', ms:5600, tag:'CAULI+APPLE 1 / 7', cap:'Cauliflower and apple',       sub:'the apple is a starter, not a flavour',              color:'#5c7a29' },
  { id:'s1', ms:6200, tag:'CAULI+APPLE 2 / 7', cap:'Cauliflower small, apple thick', sub:'even florets ferment evenly - the apple softens first', color:'#5c7a29' },
  { id:'s2', ms:5800, tag:'CAULI+APPLE 3 / 7', cap:'25 g of salt per litre',      sub:'2.5% brine - the apple does not change the salt',    color:'#378add' },
  { id:'s3', ms:7000, tag:'CAULI+APPLE 4 / 7', cap:'The apple starts it',         sub:'sugar feeds the bacteria - acid on day 1, not day 3', color:'#a32d2d' },
  { id:'s4', ms:6600, tag:'CAULI+APPLE 5 / 7', cap:'Air in the florets',          sub:'that is where the sulfur smell comes from',          color:'#1d9e75' },
  { id:'s5', ms:6000, tag:'CAULI+APPLE 6 / 7', cap:'5 to 7 days, taste on day 4', sub:'the fridge stops the sulfur',                        color:'#5f5e5a' },
  { id:'s6', ms:6600, tag:'CAULI+APPLE 7 / 7', cap:'The smell lies',              sub:'open it, wait 5 minutes - hydrogen sulfide leaves',  color:'#3b6d11' }
];"""

# ================================================================== simples
ANCORAS_SIMPLES = [
    ('<title>', '<title>Shorts animado — Carrot with apple (fermented)</title>',
     '<title>Shorts animado — Cauliflower with apple (fermented)</title>'),
    ('cor do selo', 'background:#d97706; color:#fff;', 'background:#5c7a29; color:#fff;'),
    ('texto do selo', '<div class="speed-badge">🥕 + APPLE</div>',
     '<div class="speed-badge">🥦 + APPLE</div>'),
    ('barra de legenda',
     '<div class="cap" id="cap">Carrot with apple<small>the sweet one - and it fizzes</small></div>',
     '<div class="cap" id="cap">Cauliflower and apple<small>the apple is a starter, not a flavour</small></div>'),
]

CENAS = [('s0', S0_NOVO), ('s1', S1_NOVO), ('s2', S2_NOVO),
         ('s3', S3_NOVO), ('s4', S4_NOVO), ('s5', S5_NOVO), ('s6', S6_NOVO)]


def acha_cena(d, cid):
    return re.search(r'(?ms)^([ \t]*)<svg class="scene[^"]*"[^>]*id="%s".*?</svg>' % cid, d)


def main():
    with io.open(ORIGEM, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()

    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('fim de linha do template: %s' % ('CRLF' if crlf else 'LF'))
    eol = '\r\n' if crlf else '\n'

    # --- provar que a origem e' o arquivo certo -------------------------
    if 'Carrot with apple' not in d:
        print('ABORTADO — o template nao parece ser o do #18.')
        return 1

    falhou = False

    # --- 1. as 7 cenas -------------------------------------------------
    for cid, novo in CENAS:
        m = acha_cena(d, cid)
        if not m:
            print('%-34s NAO ACHEI a cena' % cid)
            falhou = True
            continue
        indent = m.group(1)
        linhas = novo.replace('\n', eol).split(eol)
        # So' a PRIMEIRA linha leva o recuo da cena: os filhos do bloco ja' estao
        # com 4 espacos no fonte, que e' o que o template usa.
        linhas[0] = indent + linhas[0]
        bloco = eol.join(linhas)
        d = d[:m.start()] + bloco + d[m.end():]
        print('%-34s substituida (%d car)' % ('cena ' + cid, len(bloco)))

    # --- 2. o array scenes ---------------------------------------------
    m = re.search(r'(?ms)^const scenes = \[.*?\n\];', d)
    if not m:
        print('array scenes                    NAO ACHEI')
        falhou = True
    else:
        d = d[:m.start()] + SCENES_NOVO.replace('\n', eol) + d[m.end():]
        print('%-34s substituido' % 'array scenes')

    # --- 3. as ancoras simples -----------------------------------------
    for rotulo, velho, novo in ANCORAS_SIMPLES:
        v = velho.replace('\n', eol)
        q = d.count(v)
        print('%-34s casou %d vez(es)' % (rotulo, q))
        if q != 1:
            falhou = True
            continue
        d = d.replace(v, n := novo.replace('\n', eol), 1)

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    # --- 4. conferencias finais ----------------------------------------
    dur = sum(int(x) for x in re.findall(r'ms:(\d+)', SCENES_NOVO))
    print('\nduracao total: %.1f s' % (dur / 1000.0))
    kf_usados = set(re.findall(r'animation:(\w+)', d))
    kf_defs = set(re.findall(r'@keyframes (\w+)', d))
    orfaos = kf_usados - kf_defs
    print('keyframes usados: %s' % ', '.join(sorted(kf_usados)))
    print('keyframes orfaos: %s' % (', '.join(sorted(orfaos)) if orfaos else 'nenhum'))
    if orfaos:
        print('ABORTADO — keyframe sem definicao.')
        return 1

    with io.open(DESTINO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('\ngravado: %s (%d bytes)' % (DESTINO, len(d.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
