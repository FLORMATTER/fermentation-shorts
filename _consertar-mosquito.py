# -*- coding: utf-8 -*-
"""Conserta 3 defeitos vistos no render do short do mosquito.
   Aborta SEM GRAVAR se qualquer ancora nao casar exatamente 1 vez."""
import io, sys

ARQ = 'mosquito/shorts-mosquito-trap-en.html'

# ---------------------------------------------------------------- 1) cena 2
S2_OLD = '''    <!-- copo (metade de baixo) -->
    <g transform="translate(202,300)">
      <g style="animation:floatSoft 3.4s ease-in-out infinite">
        <g clip-path="url(#s2Cup)">
          <rect x="-70" y="20" width="140" height="100" fill="#e8d5a4" opacity=".92"/>
          <rect x="-70" y="20" width="140" height="7" fill="#d6bd82"/>
        </g>
        <path d="M-66,-50 L-66,86 Q-66,110 -40,110 L40,110 Q66,110 66,86 L66,-50 Z" fill="#fbfdfc" stroke="#2f3a38" stroke-width="2.6" stroke-linejoin="round" opacity=".95"/>
        <!-- gargalo invertido -->
        <path d="M-58,-84 L-24,-28 L-15,12 L-18,26 L18,26 L15,12 L24,-28 L58,-84 Z" fill="#f4fbf9" stroke="#2f3a38" stroke-width="2.6" stroke-linejoin="round"/>
        <path d="M-58,-84 L58,-84" stroke="#2f3a38" stroke-width="2.6"/>
        <path d="M-18,26 L18,26" stroke="#c2551f" stroke-width="3"/>
        <path d="M-34,-40 L-24,-16" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity=".8"/>
      </g>
    </g>'''

S2_NEW = '''    <!-- copo (metade de baixo) com o gargalo invertido dentro -->
    <g transform="translate(202,300)">
      <g style="animation:floatSoft 3.4s ease-in-out infinite">
        <path d="M-66,-50 L-66,86 Q-66,110 -40,110 L40,110 Q66,110 66,86 L66,-50 Z" fill="#fbfdfc"/>
        <!-- funil: a metade de cima virada (borda larga em cima, gargalo embaixo) -->
        <path d="M-64,-56 C-60,-14 -26,2 -16,30 L-16,52 L16,52 L16,30 C26,2 60,-14 64,-56 Z" fill="#f4fbf9" stroke="#2f3a38" stroke-width="2.6" stroke-linejoin="round"/>
        <!-- liquido POR CIMA do gargalo: e o que le como "submerso" -->
        <g clip-path="url(#s2Cup)">
          <rect x="-70" y="18" width="140" height="102" fill="#e8d5a4" opacity=".55"/>
          <rect x="-70" y="18" width="140" height="6" fill="#d6bd82" opacity=".75"/>
        </g>
        <path d="M-64,-56 C-60,-14 -26,2 -16,30 L-16,52 L16,52 L16,30 C26,2 60,-14 64,-56 Z" fill="none" stroke="#2f3a38" stroke-width="2.6" stroke-linejoin="round"/>
        <path d="M-64,-56 L64,-56" stroke="#c2551f" stroke-width="3.2"/>
        <path d="M-66,-50 L-66,86 Q-66,110 -40,110 L40,110 Q66,110 66,86 L66,-50 Z" fill="none" stroke="#2f3a38" stroke-width="2.6" stroke-linejoin="round"/>
        <path d="M-46,-34 L-40,60" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity=".7"/>
      </g>
    </g>'''

# ---------------------------------------------------------------- 2) cena 5 (CO2)
CO2_OLD = '''    <g font-family="system-ui" font-weight="900" font-size="11" text-anchor="middle">
      <g style="animation:riseFast 3.6s ease-out infinite">
        <circle cx="108" cy="196" r="15" fill="#ffffff" stroke="#7fb8ac" stroke-width="2"/>
        <text x="108" y="200" fill="#1f7a6e">CO\u2082</text>
      </g>
      <g style="animation:riseFast 3.6s ease-out infinite; animation-delay:1.2s">
        <circle cx="196" cy="150" r="15" fill="#ffffff" stroke="#7fb8ac" stroke-width="2"/>
        <text x="196" y="154" fill="#1f7a6e">CO\u2082</text>
      </g>
    </g>'''

CO2_NEW = '''    <g font-family="system-ui" font-weight="900" font-size="11" text-anchor="middle">
      <g style="animation:riseCo2 3.6s ease-out infinite">
        <circle cx="226" cy="300" r="15" fill="#ffffff" stroke="#7fb8ac" stroke-width="2"/>
        <text x="226" y="304" fill="#1f7a6e">CO\u2082</text>
      </g>
      <g style="animation:riseCo2 3.6s ease-out infinite; animation-delay:1.2s">
        <circle cx="256" cy="272" r="15" fill="#ffffff" stroke="#7fb8ac" stroke-width="2"/>
        <text x="256" y="276" fill="#1f7a6e">CO\u2082</text>
      </g>
    </g>'''

# ---------------------------------------------------------------- 3) cena 6 (defs)
S5_DEFS_OLD = '''    <defs>
      <clipPath id="s5Clip">
        <path d="M-48,-16 L-48,100 Q-48,118 -30,118 L30,118 Q48,118 48,100 L48,-16 Q48,-46 15,-64 L15,-104 L-15,-104 L-15,-64 Q-48,-46 -48,-16 Z"/>
      </clipPath>
    </defs>'''

S5_DEFS_NEW = '''    <defs>
      <clipPath id="s5Clip">
        <path d="M-48,-16 L-48,100 Q-48,118 -30,118 L30,118 Q48,118 48,100 L48,-16 Q48,-46 15,-64 L15,-104 L-15,-104 L-15,-64 Q-48,-46 -48,-16 Z"/>
      </clipPath>
      <linearGradient id="s5Shade" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="40%" stop-color="#2f3a38" stop-opacity="0"/>
        <stop offset="100%" stop-color="#2f3a38" stop-opacity=".17"/>
      </linearGradient>
      <linearGradient id="s5Floor" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#2f3a38" stop-opacity="0"/>
        <stop offset="100%" stop-color="#2f3a38" stop-opacity=".12"/>
      </linearGradient>
    </defs>'''

S5_SHADE_OLD = '''    <!-- canto escuro -->
    <g opacity=".9">
      <path d="M40,116 L40,424 L368,424 L368,116" fill="none" stroke="#c9c2b2" stroke-width="2.2" stroke-dasharray="7 7"/>
      <rect x="252" y="118" width="114" height="304" fill="#2f3a38" opacity=".08"/>
      <rect x="42" y="300" width="324" height="122" fill="#2f3a38" opacity=".05"/>
    </g>'''

S5_SHADE_NEW = '''    <!-- canto escuro (sombra em degrade, sem borda dura) -->
    <rect x="40" y="116" width="328" height="308" fill="url(#s5Shade)"/>
    <rect x="40" y="300" width="328" height="124" fill="url(#s5Floor)"/>
    <path d="M40,116 L40,424 L368,424 L368,116" fill="none" stroke="#c9c2b2" stroke-width="2.2" stroke-dasharray="7 7"/>'''

# ---------------------------------------------------------------- 4) keyframe novo
KF_OLD = '''  @keyframes wingFlap {
    0%,100% { transform: rotate(-18deg) }'''

KF_NEW = '''  @keyframes riseCo2 {
    0%   { transform: translateY(0) scale(.7); opacity: 0 }
    22%  { opacity: 1 }
    100% { transform: translateY(-110px) scale(1.15); opacity: 0 }
  }
  @keyframes wingFlap {
    0%,100% { transform: rotate(-18deg) }'''

SUBS = [
    ('cena 2 (copo + funil)', S2_OLD, S2_NEW),
    ('cena 5 (chips CO2)',    CO2_OLD, CO2_NEW),
    ('cena 6 (defs sombra)',  S5_DEFS_OLD, S5_DEFS_NEW),
    ('cena 6 (sombra)',       S5_SHADE_OLD, S5_SHADE_NEW),
    ('keyframe riseCo2',      KF_OLD, KF_NEW),
]

d = io.open(ARQ, encoding='utf-8', newline='').read()
falhou = False
for nome, old, new in SUBS:
    n = d.count(old)
    print('%-24s ocorrencias: %d %s' % (nome, n, 'OK' if n == 1 else '<-- FALHOU'))
    if n != 1:
        falhou = True
if falhou:
    print('\nABORTADO: nada foi gravado.')
    sys.exit(1)

for nome, old, new in SUBS:
    d = d.replace(old, new, 1)

io.open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('\nGRAVADO: %s' % ARQ)
