"""_criar-pepino-maca-pt.py — cria o ORIGINAL PT do short PEPINO + MACA.

    python _criar-pepino-maca-pt.py

Por que: a convencao da serie e' **original PT + irmao `-en`**. O #17
(`pepino/shorts-pepino-apple-en.html`) nasceu so' em ingles porque foi feito a
partir do `-en`. Isto aqui devolve o original que faltava, para o par ficar
completo e o `_sobras-vs-original.py` poder conferir os dois.

Mesma receita do `_criar-pepino-maca.py`: template da serie + 10 ancoras
contadas, abortando SEM GRAVAR se alguma casar 0 ou 2+ vezes. O que nao e'
conteudo (CSS, motor JS, modo ?rec, geometria do desenho) sai provado igual ao
template; so' o idioma muda.

Template: pepino/shorts-pepino-speed.html (o original PT — mesma geometria do
`-en` de que o #17 saiu; conferido com `_extrair-cena.py`).

Duas coisas que o #17 ja' tinha e este tambem tem, de proposito:
  - o selo vira vermelho e diz "🍎 + MAÇÃ" (era "⚡ SPEED" verde);
  - os keyframes `zoomIn` e `blink` saem — ninguem usa, e o `_validar-short.py`
    reprova com "[X] @keyframes nunca usado".
"""
import sys

ORIGEM = 'pepino/shorts-pepino-speed.html'
DESTINO = 'pepino/shorts-pepino-apple.html'

# ------------------------------------------------------------------ s0 (novo)
# Geometria identica a do #17 (nao tem texto dentro, so' desenho).
S0_NOVO = '''  <svg class="scene on" id="s0" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
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

# ------------------------------------------------------------------ s3 (novo)
# Mesma geometria do #17: a maca a esquerda (ACUCAR), o louro a direita (TANINO),
# e a caixa que desfaz a confusao. So' os rotulos viram PT.
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
      <text x="0" y="98" text-anchor="middle" font-size="17" font-weight="800" fill="#791f1f" font-family="system-ui">açúcar</text>
    </g>
    <g transform="translate(296,248)">
      <g style="animation:tick 2.2s ease-in-out infinite">
        <ellipse cx="-26" cy="18" rx="30" ry="19" fill="#97c459" stroke="#639922" stroke-width="3" transform="rotate(-24 -26 18)"/>
        <path d="M-26,18 L-26,44" stroke="#3b6d11" stroke-width="3"/>
        <ellipse cx="24" cy="24" rx="32" ry="20" fill="#97c459" stroke="#639922" stroke-width="3" transform="rotate(12 24 24)"/>
        <path d="M24,24 L24,52" stroke="#3b6d11" stroke-width="3"/>
      </g>
      <text x="0" y="98" text-anchor="middle" font-size="17" font-weight="800" fill="#27500a" font-family="system-ui">tanino</text>
    </g>
    <g transform="translate(202,448)">
      <rect x="-150" y="-38" width="300" height="76" rx="12" fill="#fff" stroke="#e24b4a" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="21" font-weight="800" fill="#791f1f" font-family="system-ui">AÇÚCAR NÃO É TANINO</text>
      <text x="0" y="24" text-anchor="middle" font-size="14" font-weight="600" fill="#a32d2d" font-family="system-ui">é a folha que segura a crocância</text>
    </g>
  </svg>'''

TROCAS = [
    # --- cabecalho
    ('<title>Shorts animado — Pepino fermentado (speed)</title>',
     '<title>Shorts animado — Pepino com maçã (fermentado)</title>'),

    # --- selo: verde "SPEED" vira vermelho "+ MAÇÃ"
    ('''  .speed-badge {
    position:absolute; top:52px; left:18px; z-index:36;
    background:#1d9e75; color:#fff;''',
     '''  .speed-badge {
    position:absolute; top:52px; left:18px; z-index:36;
    background:#e24b4a; color:#fff;'''),
    ('<div class="speed-badge">⚡ SPEED</div>',
     '<div class="speed-badge">🍎 + MAÇÃ</div>'),

    # --- keyframes que ninguem usa (o validador reprova por isso)
    ('''  @keyframes zoomIn { 0%{transform:scale(.85);opacity:0} 100%{transform:scale(1);opacity:1} }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.25} }
''', ''),

    # --- cena 1: entra a maca
    ('''  <svg class="scene on" id="s0" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#e1f5ee"/>
    <circle cx="202" cy="300" r="140" fill="#9fe1cb" opacity=".55"/>
    <g transform="translate(202,300) rotate(-14)">
      <rect x="-38" y="-108" width="76" height="216" rx="36" fill="#5dcaa5"/>
      <rect x="-38" y="-108" width="76" height="216" rx="36" fill="none" stroke="#1d9e75" stroke-width="3"/>
      <g fill="#0f6e56" opacity=".55">
        <circle cx="-12" cy="-56" r="2.8"/><circle cx="10" cy="-40" r="2.8"/>
        <circle cx="-4" cy="-16" r="2.8"/><circle cx="14" cy="4" r="2.8"/>
        <circle cx="-14" cy="24" r="2.8"/><circle cx="6" cy="48" r="2.8"/>
        <circle cx="-8" cy="68" r="2.8"/><circle cx="16" cy="82" r="2.8"/>
      </g>
      <path d="M-6,-108 Q0,-122 6,-108" stroke="#3b6d11" stroke-width="6" fill="none" stroke-linecap="round"/>
      <ellipse cx="-16" cy="-60" rx="10" ry="34" fill="#fff" opacity=".3"/>
    </g>
    <g transform="translate(300,180)">
      <rect x="-5" y="0" width="10" height="50" rx="4" fill="#5f5e5a" style="animation:chop2x .55s ease-in-out infinite"/>
      <path d="M-4,50 L4,50 L6,118 L-6,118Z" fill="#b4b2a9" style="animation:chop2x .55s ease-in-out infinite"/>
    </g>
  </svg>''', S0_NOVO),

    # --- cena 4: o que a maca faz e o que ela NAO faz
    ('''  <svg class="scene" id="s3" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <rect width="405" height="720" fill="#eaf3de"/>
    <ellipse cx="202" cy="530" rx="150" ry="34" fill="#c0dd97" opacity=".5"/>
    <g transform="translate(202,290)">
      <ellipse cx="-72" cy="26" rx="34" ry="22" fill="#97c459" stroke="#639922" stroke-width="3" transform="rotate(-24 -72 26)"/>
      <path d="M-72,26 L-72,56" stroke="#3b6d11" stroke-width="3"/>
      <ellipse cx="0" cy="34" rx="38" ry="24" fill="#97c459" stroke="#639922" stroke-width="3" transform="rotate(8 0 34)"/>
      <path d="M0,34 L0,66" stroke="#3b6d11" stroke-width="3"/>
      <ellipse cx="74" cy="24" rx="33" ry="22" fill="#97c459" stroke="#639922" stroke-width="3" transform="rotate(22 74 24)"/>
      <path d="M74,24 L74,54" stroke="#3b6d11" stroke-width="3"/>
      <path d="M-72,26 L-6,34" stroke="#3b6d11" stroke-width="2" opacity=".6"/>
      <path d="M0,34 L74,24" stroke="#3b6d11" stroke-width="2" opacity=".6"/>
      <text x="0" y="-52" text-anchor="middle" font-size="19" font-weight="800" fill="#27500a" font-family="system-ui">folha de louro</text>
      <text x="0" y="-24" text-anchor="middle" font-size="14" font-weight="600" fill="#3b6d11" font-family="system-ui">mantém crocante</text>
    </g>
    <g transform="translate(202,470)">
      <rect x="-132" y="-30" width="264" height="60" rx="12" fill="#fff" stroke="#639922" stroke-width="3"/>
      <text x="0" y="8" text-anchor="middle" font-size="19" font-weight="800" fill="#27500a" font-family="system-ui">SEM TANINO = MOLE</text>
    </g>
  </svg>''', S3_NOVO),

    # --- cena 7: o resultado muda de "crocante" para "frutado"
    ('>Crocante e azedinho</text>', '>Frutado e azedinho</text>'),
    ('>pronto em 4 dias, não em 7</text>', '>geladeira no 4º dia</text>'),

    # --- barra de legenda (mesmas duracoes do #17: 41,8 s)
    ('''const scenes = [
  { id:'s0', ms:2600, tag:'CENA 1 / 7', cap:'Pepino fermentado em 4 dias', sub:'modo rápido', color:'#1d9e75' },
  { id:'s1', ms:2800, tag:'CENA 2 / 7', cap:'Corta as pontas e fura', sub:'senão ele fica oco por dentro', color:'#993c1d' },
  { id:'s2', ms:2800, tag:'CENA 3 / 7', cap:'Salmoura de 3%', sub:'1 litro de água + 30 g de sal', color:'#378add' },
  { id:'s3', ms:3200, tag:'CENA 4 / 7', cap:'Louro dentro do pote', sub:'é o tanino que mantém crocante', color:'#3b6d11' },
  { id:'s4', ms:3400, tag:'CENA 5 / 7', cap:'Pepino submerso na salmoura', sub:'tudo embaixo do líquido', color:'#1d9e75' },
  { id:'s5', ms:2800, tag:'CENA 6 / 7', cap:'Só 4 dias', sub:'pepino é o mais rápido de todos', color:'#5f5e5a' },
  { id:'s6', ms:3200, tag:'CENA 7 / 7', cap:'Crocante e azedinho', sub:'guarda na geladeira', color:'#0f6e56' }
];''',
     '''const scenes = [
  { id:'s0', ms:5200, tag:'CENA 1 / 7', cap:'Pepino com maçã', sub:'o frutado', color:'#e24b4a' },
  { id:'s1', ms:5800, tag:'CENA 2 / 7', cap:'Corta as pontas e fura', sub:'senão ele fica oco por dentro', color:'#993c1d' },
  { id:'s2', ms:6000, tag:'CENA 3 / 7', cap:'Salmoura de 3%', sub:'1 litro de água + 30 g de sal', color:'#378add' },
  { id:'s3', ms:6600, tag:'CENA 4 / 7', cap:'Açúcar, não tanino', sub:'a maçã acelera - a folha segura firme', color:'#a32d2d' },
  { id:'s4', ms:6000, tag:'CENA 5 / 7', cap:'Pepino submerso na salmoura', sub:'tudo embaixo do líquido', color:'#1d9e75' },
  { id:'s5', ms:5800, tag:'CENA 6 / 7', cap:'Só 4 a 6 dias', sub:'a maçã faz ir mais rápido', color:'#5f5e5a' },
  { id:'s6', ms:6400, tag:'CENA 7 / 7', cap:'Frutado e azedinho', sub:'direto pra geladeira', color:'#0f6e56' }
];'''),

    # --- legenda estatica (fallback sem JS)
    ('<div class="cap" id="cap">Pepino fermentado em 4 dias<small>modo rápido</small></div>',
     '<div class="cap" id="cap">Pepino com maçã<small>o frutado</small></div>'),
]


def main():
    d = open(ORIGEM, encoding='utf-8', newline='').read()
    # Os .html da serie sao CRLF puro. Ancora de uma linha casa de qualquer jeito;
    # a de varias linhas com \n casa 0 vezes. Normalizar aqui evita o
    # "casou 0 vez(es)" que ja' custou uma rodada no _criar-pepino-maca.py.
    nl = '\r\n' if '\r\n' in d else '\n'
    print('fim de linha do template: %s' % ('CRLF' if nl == '\r\n' else 'LF'))
    orig = d
    for i, (velho, novo) in enumerate(TROCAS, 1):
        velho = velho.replace('\n', nl)
        novo = novo.replace('\n', nl)
        n = d.count(velho)
        print('troca %2d: casou %d vez(es)' % (i, n))
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
