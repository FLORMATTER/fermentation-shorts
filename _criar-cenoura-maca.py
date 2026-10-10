"""_criar-cenoura-maca.py — cria o short CENOURA + MACA (carrot with apple).

    python _criar-cenoura-maca.py

Por que este arquivo e' um script e nao um "salve como": o short novo tem que sair
IDENTICO ao da serie no CSS, no motor JS e no modo ?rec. Copiando o template e trocando
so' o conteudo, com contagem exata em cada ancora, o que nao e' conteudo fica provado
igual. Se qualquer ancora casar 0 ou 2+ vezes, o script ABORTA sem gravar.

Template: pepino/shorts-pepino-apple-en.html — e' o irmao mais proximo (mesmo conceito
"legume + maca", a maca JA' esta desenhada, e o validador ja' passa limpo nele). O
template da cenoura (`shorts-cenoura-animado-en`) e' do estilo antigo, mais pobre —
nao usar.

A substancia vem da pesquisa, nao do chute:
  - CENOURA: raiz densa, 2% de sal, 4 a 6 dias. Segura bem a crocancia.
  - MACA: entra por ACUCAR **e por levedura selvagem na casca** — e' por isso que um
    fermentado com maca fica ESPUMANTE tao rapido.
  - O AVISO HONESTO: fermentado com fruta pode chegar a **0,5% a 2% de alcool**,
    enquanto o chucrute (so' legume, pouco acucar) fica perto de zero. A fonte diz
    ainda que **se esta' espumante, pode ter mais alcool**, e que recipiente fechado
    prende o alcool enquanto o aberto deixa virar vinagre.
  - A REGRA DE CORTE: a cenoura e' densa e demora a amaciar; a maca amacia rapido.
    Entao **cenoura fina, maca grossa**, para as duas ficarem prontas juntas.
  - A MACA FLUTUA — e' o pedaco mais rico em acucar e o mais leve, entao e' o primeiro
    a criar mofo se ficar fora da salmoura.
"""
import sys

ORIGEM = 'pepino/shorts-pepino-apple-en.html'
DESTINO = 'cenoura/shorts-carrot-apple-en.html'

# ------------------------------------------------------------------ cena 1
S0_VELHO = '''  <svg class="scene on" id="s0" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#e1f5ee"/>
    <circle cx="202" cy="300" r="142" fill="#9fe1cb" opacity=".55"/>
    <g transform="translate(120,296) rotate(-16)">
      <rect x="-32" y="-96" width="64" height="192" rx="30" fill="#5dcaa5"/>
      <rect x="-32" y="-96" width="64" height="192" rx="30" fill="none" stroke="#1d9e75" stroke-width="3"/>
      <g fill="#0f6e56" opacity=".55">
        <circle cx="-10" cy="-50" r="2.6"/><circle cx="9" cy="-34" r="2.6"/>
        <circle cx="-4" cy="-12" r="2.6"/><circle cx="12" cy="6" r="2.6"/>
        <circle cx="-12" cy="26" r="2.6"/><circle cx="6" cy="46" r="2.6"/>
        <circle cx="-6" cy="64" r="2.6"/><circle cx="13" cy="76" r="2.6"/>
      </g>
      <path d="M-5,-96 Q0,-110 5,-96" stroke="#3b6d11" stroke-width="5" fill="none" stroke-linecap="round"/>
      <ellipse cx="-14" cy="-52" rx="9" ry="30" fill="#fff" opacity=".3"/>
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

S0_NOVO = '''  <svg class="scene on" id="s0" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#faeeda"/>
    <circle cx="202" cy="300" r="142" fill="#fac775" opacity=".55"/>
    <g transform="translate(118,296) rotate(-14)">
      <path d="M-26,-92 L26,-92 L10,102 L-10,102 Z" fill="#f0a03c" stroke="#c2701a" stroke-width="3" stroke-linejoin="round"/>
      <g stroke="#c2701a" stroke-width="2" opacity=".5">
        <path d="M-22,-64 L22,-64 M-19,-34 L19,-34 M-16,-4 L16,-4 M-13,26 L13,26 M-11,56 L11,56"/>
      </g>
      <ellipse cx="-15" cy="-120" rx="7" ry="21" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(-24 -15 -120)"/>
      <ellipse cx="0" cy="-130" rx="7" ry="23" fill="#97c459" stroke="#639922" stroke-width="2.5"/>
      <ellipse cx="15" cy="-120" rx="7" ry="21" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(24 15 -120)"/>
      <ellipse cx="-13" cy="-44" rx="7" ry="32" fill="#fff" opacity=".3"/>
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

# ------------------------------------------------------------------ cena 2
S1_VELHO = '''  <svg class="scene" id="s1" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#faeeda"/>
    <ellipse cx="202" cy="540" rx="170" ry="38" fill="#fac775" opacity=".35"/>
    <g transform="translate(130,300)">
      <rect x="-34" y="-100" width="68" height="200" rx="32" fill="#5dcaa5" stroke="#1d9e75" stroke-width="3"/>
      <line x1="-34" y1="-84" x2="34" y2="-84" stroke="#e24b4a" stroke-width="6" stroke-linecap="round"/>
      <line x1="-34" y1="80" x2="34" y2="80" stroke="#e24b4a" stroke-width="6" stroke-linecap="round"/>
      <g fill="#0f6e56" opacity=".5">
        <circle cx="-8" cy="-30" r="2.6"/><circle cx="10" cy="0" r="2.6"/><circle cx="-10" cy="34" r="2.6"/>
      </g>
      <text x="0" y="128" text-anchor="middle" font-size="15" font-weight="800" fill="#993c1d" font-family="system-ui">cut the ends</text>
    </g>
    <g transform="translate(202,300)">
      <path d="M-12,0 L12,0" stroke="#5f5e5a" stroke-width="6" stroke-linecap="round"/>
    </g>
    <g transform="translate(286,300)">
      <rect x="-30" y="-96" width="60" height="192" rx="28" fill="#97c459" stroke="#639922" stroke-width="3"/>
      <g stroke="#3b6d11" stroke-width="2.5" opacity=".75">
        <path d="M-20,-60 L20,-60 M-22,-34 L22,-34 M-22,-8 L22,-8 M-22,18 L22,18 M-22,44 L22,44 M-20,68 L20,68"/>
      </g>
      <path d="M-4,-96 Q0,-108 4,-96" stroke="#639922" stroke-width="5" fill="none" stroke-linecap="round"/>
      <text x="0" y="128" text-anchor="middle" font-size="15" font-weight="800" fill="#3b6d11" font-family="system-ui">pierce it with a fork</text>
    </g>
  </svg>'''

S1_NOVO = '''  <svg class="scene" id="s1" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#faeeda"/>
    <ellipse cx="202" cy="540" rx="170" ry="38" fill="#fac775" opacity=".35"/>
    <g transform="translate(112,300)">
      <path d="M-24,-88 L24,-88 L9,98 L-9,98 Z" fill="#f0a03c" stroke="#c2701a" stroke-width="3" stroke-linejoin="round"/>
      <g stroke="#c2701a" stroke-width="2" opacity=".5">
        <path d="M-20,-62 L20,-62 M-17,-32 L17,-32 M-14,-2 L14,-2 M-12,28 L12,28 M-10,58 L10,58"/>
      </g>
      <ellipse cx="-14" cy="-114" rx="6.5" ry="19" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(-24 -14 -114)"/>
      <ellipse cx="0" cy="-123" rx="6.5" ry="21" fill="#97c459" stroke="#639922" stroke-width="2.5"/>
      <ellipse cx="14" cy="-114" rx="6.5" ry="19" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(24 14 -114)"/>
      <text x="0" y="134" text-anchor="middle" font-size="16" font-weight="800" fill="#8a4b12" font-family="system-ui">thin</text>
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

# ------------------------------------------------------------------ cena 4
S3_VELHO = '''  <svg class="scene" id="s3" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#fbe9e7"/>
    <ellipse cx="202" cy="516" rx="158" ry="34" fill="#e24b4a" opacity=".12"/>
    <g transform="translate(108,248)">
      <g style="animation:wobble 2.6s ease-in-out infinite">
        <circle cx="0" cy="0" r="56" fill="#e24b4a" stroke="#a32d2d" stroke-width="3"/>
        <path d="M0,-52 Q4,-68 1,-80" stroke="#7a5c3e" stroke-width="6" fill="none" stroke-linecap="round"/>
        <ellipse cx="22" cy="-72" rx="19" ry="10" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(-20 22 -72)"/>
        <ellipse cx="-21" cy="-14" rx="11" ry="22" fill="#fff" opacity=".3" transform="rotate(-20 -21 -14)"/>
      </g>
      <text x="0" y="98" text-anchor="middle" font-size="17" font-weight="800" fill="#791f1f" font-family="system-ui">sugar</text>
    </g>
    <g transform="translate(296,248)">
      <g style="animation:tick 2.2s ease-in-out infinite">
        <ellipse cx="-26" cy="18" rx="30" ry="19" fill="#97c459" stroke="#639922" stroke-width="3" transform="rotate(-24 -26 18)"/>
        <path d="M-26,18 L-26,44" stroke="#3b6d11" stroke-width="3"/>
        <ellipse cx="24" cy="24" rx="32" ry="20" fill="#97c459" stroke="#639922" stroke-width="3" transform="rotate(12 24 24)"/>
        <path d="M24,24 L24,52" stroke="#3b6d11" stroke-width="3"/>
      </g>
      <text x="0" y="98" text-anchor="middle" font-size="17" font-weight="800" fill="#27500a" font-family="system-ui">tannin</text>
    </g>
    <g transform="translate(202,448)">
      <rect x="-150" y="-38" width="300" height="76" rx="12" fill="#fff" stroke="#e24b4a" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="21" font-weight="800" fill="#791f1f" font-family="system-ui">SUGAR IS NOT TANNIN</text>
      <text x="0" y="24" text-anchor="middle" font-size="14" font-weight="600" fill="#a32d2d" font-family="system-ui">the leaf is what keeps it firm</text>
    </g>
  </svg>'''

S3_NOVO = '''  <svg class="scene" id="s3" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
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
        <path d="M-30,-58 L30,-58 L13,58 L-13,58 Z" fill="#f0a03c" stroke="#c2701a" stroke-width="3" stroke-linejoin="round"/>
        <g stroke="#c2701a" stroke-width="2" opacity=".5">
          <path d="M-24,-34 L24,-34 M-20,-8 L20,-8 M-16,18 L16,18 M-14,42 L14,42"/>
        </g>
        <ellipse cx="-16" cy="-84" rx="6.5" ry="18" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(-24 -16 -84)"/>
        <ellipse cx="0" cy="-93" rx="6.5" ry="20" fill="#97c459" stroke="#639922" stroke-width="2.5"/>
        <ellipse cx="16" cy="-84" rx="6.5" ry="18" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(24 16 -84)"/>
      </g>
      <text x="0" y="98" text-anchor="middle" font-size="16" font-weight="800" fill="#27500a" font-family="system-ui">dense + slow</text>
    </g>
    <g transform="translate(202,448)">
      <rect x="-150" y="-38" width="300" height="76" rx="12" fill="#fff" stroke="#e24b4a" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="19" font-weight="800" fill="#791f1f" font-family="system-ui">THE APPLE MAKES IT FIZZY</text>
      <text x="0" y="24" text-anchor="middle" font-size="14" font-weight="600" fill="#a32d2d" font-family="system-ui">sugar plus the yeast on the skin</text>
    </g>
  </svg>'''

# ------------------------------------------------------------------ cena 5
S4_VELHO = '''  <svg class="scene" id="s4" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#e1f5ee"/>
    <g transform="translate(202,300)">
      <path d="M-104,110 L-104,-40 Q-104,-58 -86,-58 L86,-58 Q104,-58 104,-40 L104,110 Z"
            fill="#f4faf3" stroke="#1d9e75" stroke-width="4"/>
      <rect x="-104" y="-58" width="208" height="24" rx="6" fill="#9fe1cb" stroke="#1d9e75" stroke-width="4"/>
      <path d="M-104,50 L-104,-14 Q-104,-30 -86,-30 L86,-30 Q104,-30 104,-14 L104,50 Z" fill="#5dcaa5" opacity=".75"/>
      <g fill="#3b6d11">
        <rect x="-94" y="-16" width="24" height="76" rx="11" transform="rotate(-10 -82 22)"/>
        <rect x="-58" y="-26" width="24" height="88" rx="11" transform="rotate(7 -46 18)"/>
        <rect x="-18" y="-14" width="24" height="80" rx="11" transform="rotate(-4 -6 26)"/>
        <rect x="22" y="-28" width="24" height="92" rx="11" transform="rotate(9 34 18)"/>
        <rect x="62" y="-8" width="24" height="74" rx="11" transform="rotate(-7 74 29)"/>
      </g>
      <ellipse cx="0" cy="-20" rx="30" ry="14" fill="#97c459" stroke="#639922" stroke-width="2.5"/>
      <ellipse cx="60" cy="-8" rx="24" ry="12" fill="#97c459" stroke="#639922" stroke-width="2.5" transform="rotate(20 60 -8)"/>
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
  </svg>'''

S4_NOVO = '''  <svg class="scene" id="s4" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#faeeda"/>
    <g transform="translate(202,286)">
      <path d="M-104,110 L-104,-40 Q-104,-58 -86,-58 L86,-58 Q104,-58 104,-40 L104,110 Z"
            fill="#fdf9f2" stroke="#ba7517" stroke-width="4"/>
      <rect x="-104" y="-58" width="208" height="24" rx="6" fill="#fac775" stroke="#ba7517" stroke-width="4"/>
      <path d="M-104,50 L-104,-14 Q-104,-30 -86,-30 L86,-30 Q104,-30 104,-14 L104,50 Z" fill="#fac775" opacity=".7"/>
      <g fill="#f0a03c" stroke="#c2701a" stroke-width="2">
        <rect x="-94" y="-16" width="24" height="76" rx="11" transform="rotate(-10 -82 22)"/>
        <rect x="-58" y="-26" width="24" height="88" rx="11" transform="rotate(7 -46 18)"/>
        <rect x="-18" y="-14" width="24" height="80" rx="11" transform="rotate(-4 -6 26)"/>
        <rect x="22" y="-28" width="24" height="92" rx="11" transform="rotate(9 34 18)"/>
        <rect x="62" y="-8" width="24" height="74" rx="11" transform="rotate(-7 74 29)"/>
      </g>
      <g fill="#e24b4a" stroke="#a32d2d" stroke-width="2.5">
        <rect x="-34" y="-30" width="44" height="28" rx="9" transform="rotate(-8 -12 -16)"/>
        <rect x="26" y="-22" width="40" height="26" rx="9" transform="rotate(14 46 -9)"/>
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
      <text x="0" y="0" text-anchor="middle" font-size="16" font-weight="800" fill="#8a4b12" font-family="system-ui">the apple floats - keep it down</text>
    </g>
  </svg>'''

# ------------------------------------------------------------------ cena 7
S6_VELHO = '''  <svg class="scene" id="s6" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#e1f5ee"/>
    <circle cx="202" cy="278" r="130" fill="#9fe1cb" opacity=".55"/>
    <g transform="translate(202,278)">
      <circle cx="0" cy="0" r="82" fill="#f4faf3" stroke="#1d9e75" stroke-width="4"/>
      <path d="M-32,4 L-8,30 L34,-24" stroke="#0f6e56" stroke-width="11" fill="none"
            stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g transform="translate(202,444)">
      <text x="0" y="0" text-anchor="middle" font-size="25" font-weight="800" fill="#04342c" font-family="system-ui">Fruity and a little sour</text>
      <text x="0" y="32" text-anchor="middle" font-size="15" font-weight="600" fill="#0f6e56" font-family="system-ui">fridge on day 4</text>
    </g>
  </svg>'''

S6_NOVO = '''  <svg class="scene" id="s6" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#faeeda"/>
    <circle cx="202" cy="278" r="130" fill="#fac775" opacity=".55"/>
    <g transform="translate(202,278)">
      <circle cx="0" cy="0" r="82" fill="#fdf9f2" stroke="#ba7517" stroke-width="4"/>
      <path d="M-32,4 L-8,30 L34,-24" stroke="#8a4b12" stroke-width="11" fill="none"
            stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    <g transform="translate(202,444)">
      <text x="0" y="0" text-anchor="middle" font-size="25" font-weight="800" fill="#4a2606" font-family="system-ui">Fizzy and a little sweet</text>
      <text x="0" y="32" text-anchor="middle" font-size="15" font-weight="600" fill="#8a4b12" font-family="system-ui">0.5% to 2% alcohol - keep it cold</text>
    </g>
  </svg>'''

TROCAS = [
    # --- cabecalho
    ('<title>Shorts animado — Cucumber with apple (fermented)</title>',
     '<title>Shorts animado — Carrot with apple (fermented)</title>'),

    # --- selo: vermelho da maca -> laranja da cenoura
    ('''  .speed-badge {
    position:absolute; top:52px; left:18px; z-index:36;
    background:#e24b4a; color:#fff;''',
     '''  .speed-badge {
    position:absolute; top:52px; left:18px; z-index:36;
    background:#d97706; color:#fff;'''),
    ('<div class="speed-badge">🍎 + APPLE</div>',
     '<div class="speed-badge">🥕 + APPLE</div>'),

    # --- as 5 cenas que mudam de desenho
    (S0_VELHO, S0_NOVO),
    (S1_VELHO, S1_NOVO),
    (S3_VELHO, S3_NOVO),
    (S4_VELHO, S4_NOVO),
    (S6_VELHO, S6_NOVO),

    # --- cena 3: 3% de salmoura (pepino) -> 2% (cenoura)
    ('>30 g</text>', '>20 g</text>'),
    ('>3% brine</text>', '>2% brine</text>'),

    # --- cena 6: 4 a 5 dias
    ('>ONLY 4 TO 6 DAYS</text>', '>ONLY 4 TO 5 DAYS</text>'),

    # --- barra de legenda
    ('''const scenes = [
  { id:'s0', ms:5200, tag:'SCENE 1 / 7', cap:'Cucumber with apple', sub:'the fruity one', color:'#e24b4a' },
  { id:'s1', ms:5800, tag:'SCENE 2 / 7', cap:'Cut the ends and prick it', sub:'otherwise it goes hollow inside', color:'#993c1d' },
  { id:'s2', ms:6000, tag:'SCENE 3 / 7', cap:'3% brine', sub:'1 litre of water + 30 g of salt', color:'#378add' },
  { id:'s3', ms:6600, tag:'SCENE 4 / 7', cap:'Sugar, not tannin', sub:'the apple speeds it up - the leaf keeps it firm', color:'#a32d2d' },
  { id:'s4', ms:6000, tag:'SCENE 5 / 7', cap:'Cucumber under the brine', sub:'everything under the liquid', color:'#1d9e75' },
  { id:'s5', ms:5800, tag:'SCENE 6 / 7', cap:'Only 4 to 6 days', sub:'the apple makes it go faster', color:'#5f5e5a' },
  { id:'s6', ms:6400, tag:'SCENE 7 / 7', cap:'Fruity and a little sour', sub:'straight into the fridge', color:'#0f6e56' }
];''',
     '''const scenes = [
  { id:'s0', ms:5400, tag:'CARROT 1 / 7', cap:'Carrot with apple', sub:'the sweet one - and it fizzes', color:'#d97706' },
  { id:'s1', ms:6200, tag:'CARROT 2 / 7', cap:'Cut the carrot thin, the apple thick', sub:'the carrot is dense, the apple is not', color:'#ba7517' },
  { id:'s2', ms:5800, tag:'CARROT 3 / 7', cap:'2% brine', sub:'1 litre of water + 20 g of salt', color:'#378add' },
  { id:'s3', ms:6800, tag:'CARROT 4 / 7', cap:'The apple is sugar and wild yeast', sub:'that is what makes it fizz so fast', color:'#a32d2d' },
  { id:'s4', ms:6200, tag:'CARROT 5 / 7', cap:'Everything under the brine', sub:'apple floats - keep it down', color:'#1d9e75' },
  { id:'s5', ms:5800, tag:'CARROT 6 / 7', cap:'Only 4 to 5 days', sub:'the apple makes it faster than carrot', color:'#5f5e5a' },
  { id:'s6', ms:6600, tag:'CARROT 7 / 7', cap:'Fizzy and a little sweet', sub:'0.5% to 2% alcohol - keep it cold', color:'#3b6d11' }
];'''),

    # --- legenda estatica (fallback sem JS)
    ('<div class="cap" id="cap">Cucumber with apple<small>the fruity one</small></div>',
     '<div class="cap" id="cap">Carrot with apple<small>the sweet one - and it fizzes</small></div>'),
]


def main():
    d = open(ORIGEM, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in d else '\n'
    print('fim de linha do template: %s' % ('CRLF' if nl == '\r\n' else 'LF'))
    orig = d
    for i, (velho, novo) in enumerate(TROCAS, 1):
        velho = velho.replace('\n', nl)
        novo = novo.replace('\n', nl)
        n = d.count(velho)
        rotulo = velho.split('\n')[0].strip()[:46]
        print('troca %2d: casou %d vez(es)  <- %s' % (i, n, rotulo))
        if n != 1:
            print('ABORTADO: ancora %d nao e unica. Nada foi gravado.' % i)
            return 1
        d = d.replace(velho, novo, 1)
    assert d != orig
    open(DESTINO, 'w', encoding='utf-8', newline='').write(d)
    print('gravado: %s (%d -> %d bytes)' % (DESTINO, len(orig), len(d)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
