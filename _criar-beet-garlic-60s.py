# -*- coding: utf-8 -*-
"""
_criar-beet-garlic-60s.py — corte de 60 s+ do #19 (beterraba + alho).

PEDIDO: "mesmo assunto, formato novo". O guia de dinheiro marca o TikTok Creator
Rewards (US$ 500-1.500 por 1M de views) e ele EXIGE video de 60 s ou mais; os
videos da serie tem 30-45 s. O #19 tem 54,0 s — e' o mais perto, e e' o
"beterraba + alho" que o usuario pediu.

NAO E' ESTICAR: as duas cenas novas sao SUBSTANCIA que o corte de 54 s nao tinha
espaco para ter. As duas saem da mesma fonte do #19 e nenhum video da serie toca:

  s8 — NADA FORA DA SALMOURA. O que fica para fora do liquido e' exatamente onde
       comeca o problema. Peso: um saquinho de salmoura serve.
  s9 — A PELICULA BRANCA NAO E' MOFO. Kahm yeast e' chata, plana e inofensiva:
       tira e segue. Mofo e' felpudo/colorido: esse sim, joga fora. (A serie manda
       jogar coisa boa fora por causa dessa confusao; nenhum video desfaz ela.)

DESENHO: as cenas novas falam a MESMA lingua visual do #19 (rotulo no topo em y=56,
titulo em y=552, legenda em y=578, caixa de nota em y=590-642, tinta #3d1f33,
beterraba #a01e52, mudo #8a7284). Nada de token: e' um patch de arquivo validado,
com ancoras contadas.

Uso:  python _criar-beet-garlic-60s.py            # dry-run
      python _criar-beet-garlic-60s.py --apply
"""
import io
import re
import sys

ORIGEM = 'beterraba/shorts-beet-garlic-en-1080x1920.html'
DESTINO = 'beterraba/shorts-beet-garlic-en-1080x1920-60s.html'

# --------------------------------------------------------------- cena 9 (nova)
S8 = '''  <svg class="scene" id="s8" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="bGlass8" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#ffffff" stop-opacity=".55"/>
        <stop offset="22%" stop-color="#ffffff" stop-opacity=".06"/>
        <stop offset="78%" stop-color="#ffffff" stop-opacity=".04"/>
        <stop offset="100%" stop-color="#ffffff" stop-opacity=".38"/>
      </linearGradient>
      <clipPath id="bJar8"><path d="M134,96 Q134,82 148,82 L256,82 Q270,82 270,96 L270,318 Q270,340 248,340 L156,340 Q134,340 134,318Z"/></clipPath>
    </defs>
    <rect width="405" height="720" fill="#f7f0f4"/>
    <text x="202" y="56" text-anchor="middle" font-size="10" font-weight="800" fill="#a8899a" font-family="system-ui" letter-spacing="2">STEP 6 \u00b7 KEEP IT UNDER</text>

    <!-- o jarro, cheio ate a linha -->
    <g transform="translate(202,258)"><g style="animation:holdSteady 3.6s ease-in-out infinite">
      <g transform="translate(-202,-232)">
        <path d="M134,96 Q134,82 148,82 L256,82 Q270,82 270,96 L270,318 Q270,340 248,340 L156,340 Q134,340 134,318Z" fill="#faf2f7" opacity=".8"/>
        <g clip-path="url(#bJar8)">
          <rect x="134" y="150" width="136" height="190" fill="#8f1a45"/>
          <path d="M134,152 Q202,143 270,152 L270,162 L134,162Z" fill="#c94d78"/>
          <g transform="translate(170,196) rotate(-9)"><rect x="-9" y="-25" width="18" height="50" rx="7" fill="#a52a5a"/></g>
          <g transform="translate(234,202) rotate(8)"><ellipse rx="12" ry="19" fill="#e8dcc2"/><ellipse cy="-12" rx="9" ry="13" fill="#f5eeda"/></g>
          <g transform="translate(176,246) rotate(-9)"><rect x="-9" y="-25" width="18" height="50" rx="7" fill="#96284f"/></g>
          <g transform="translate(234,258) rotate(8)"><ellipse rx="12" ry="19" fill="#e8dcc2"/><ellipse cy="-12" rx="9" ry="13" fill="#f5eeda"/></g>
          <g transform="translate(170,296) rotate(-9)"><rect x="-9" y="-25" width="18" height="50" rx="7" fill="#b3255c"/></g>
          <g transform="translate(234,308) rotate(8)"><ellipse rx="12" ry="19" fill="#e8dcc2"/><ellipse cy="-12" rx="9" ry="13" fill="#f5eeda"/></g>
          <g fill="#f6c6da" opacity=".9">
            <circle cx="156" cy="186" r="4.2" style="animation:bubbleRise 3.2s ease-out infinite"/>
            <circle cx="252" cy="240" r="3.6" style="animation:bubbleRise 3.2s ease-out .8s infinite"/>
            <circle cx="194" cy="300" r="4" style="animation:bubbleRise 3.2s ease-out 1.6s infinite"/>
          </g>
          <!-- a cunha que ficou PARA FORA: logo acima da linha, nao la' em cima -->
          <g transform="translate(238,132) rotate(12)"><rect x="-10" y="-30" width="20" height="56" rx="7" fill="#b3255c"/></g>
          <rect x="134" y="82" width="136" height="258" fill="url(#bGlass8)"/>
        </g>
        <path d="M134,96 Q134,82 148,82 L256,82 Q270,82 270,96 L270,318 Q270,340 248,340 L156,340 Q134,340 134,318Z" fill="none" stroke="#d8c6d2" stroke-width="2.4"/>
        <rect x="142" y="62" width="120" height="24" rx="7" fill="#f2e8ee" stroke="#d8c6d2" stroke-width="2.2"/>
        <rect x="184" y="44" width="36" height="20" rx="6" fill="#eadce4" stroke="#d8c6d2" stroke-width="2"/>
      </g>
    </g></g>

    <!-- a linha do liquido -->
    <g style="animation:fadeSlide .6s ease both; animation-delay:.5s">
      <line x1="126" y1="176" x2="278" y2="176" stroke="#c0392b" stroke-width="2.4" stroke-dasharray="7 6"/>
      <text x="290" y="180" font-size="10" font-weight="800" fill="#c0392b" font-family="system-ui" letter-spacing="1">THE LINE</text>
    </g>

    <!-- o X na cunha que ficou fora -->
    <g style="animation:fadeSlide .5s ease both; animation-delay:.9s">
      <line x1="222" y1="122" x2="254" y2="154" stroke="#c0392b" stroke-width="5" stroke-linecap="round"/>
      <line x1="254" y1="122" x2="222" y2="154" stroke="#c0392b" stroke-width="5" stroke-linecap="round"/>
    </g>

    <!-- o peso -->
    <g style="animation:pressDown 2.6s ease-in-out infinite">
      <ellipse cx="202" cy="200" rx="60" ry="12" fill="#e8dcc2" stroke="#c9b89a" stroke-width="2.4"/>
      <ellipse cx="202" cy="194" rx="60" ry="12" fill="#f5eeda" stroke="#c9b89a" stroke-width="2.4"/>
      <text x="202" y="198" text-anchor="middle" font-size="10" font-weight="800" fill="#8a7284" font-family="system-ui" letter-spacing="1">WEIGHT</text>
    </g>

    <text x="202" y="552" text-anchor="middle" font-size="20" font-weight="900" fill="#3d1f33" font-family="system-ui" style="animation:popInSeq .6s cubic-bezier(.3,1.5,.5,1) both; animation-delay:.2s">KEEP IT UNDER THE BRINE</text>
    <text x="202" y="578" text-anchor="middle" font-size="11.5" font-weight="600" fill="#a01e52" font-family="system-ui" style="animation:fadeSlide .6s ease both; animation-delay:.45s">What sticks out is what goes wrong</text>

    <g style="animation:fadeSlide .7s ease both; animation-delay:.8s">
      <rect x="34" y="590" width="337" height="52" rx="13" fill="#f6ecf1" stroke="#e4d2de" stroke-width="2"/>
      <text x="202" y="612" text-anchor="middle" font-size="12.5" font-weight="900" fill="#3d1f33" font-family="system-ui">A zip bag of brine works as a weight</text>
      <text x="202" y="630" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7284" font-family="system-ui">Fill it, seal it, press it down on the beet</text>
    </g>
  </svg>
'''

# -------------------------------------------------------------- cena 10 (nova)
S9 = '''  <svg class="scene" id="s9" viewBox="0 0 405 720" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="bGlass9" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#ffffff" stop-opacity=".55"/>
        <stop offset="22%" stop-color="#ffffff" stop-opacity=".06"/>
        <stop offset="78%" stop-color="#ffffff" stop-opacity=".04"/>
        <stop offset="100%" stop-color="#ffffff" stop-opacity=".38"/>
      </linearGradient>
      <clipPath id="bJar9"><path d="M134,96 Q134,82 148,82 L256,82 Q270,82 270,96 L270,318 Q270,340 248,340 L156,340 Q134,340 134,318Z"/></clipPath>
    </defs>
    <rect width="405" height="720" fill="#f7f0f4"/>
    <text x="202" y="56" text-anchor="middle" font-size="10" font-weight="800" fill="#a8899a" font-family="system-ui" letter-spacing="2">STEP 7 \u00b7 THE WHITE FILM</text>

    <!-- o jarro com a pelicula PLANA -->
    <g transform="translate(202,258)"><g style="animation:holdSteady 3.6s ease-in-out infinite">
      <g transform="translate(-202,-232)">
        <path d="M134,96 Q134,82 148,82 L256,82 Q270,82 270,96 L270,318 Q270,340 248,340 L156,340 Q134,340 134,318Z" fill="#faf2f7" opacity=".8"/>
        <g clip-path="url(#bJar9)">
          <rect x="134" y="150" width="136" height="190" fill="#8f1a45"/>
          <path d="M134,152 Q202,143 270,152 L270,162 L134,162Z" fill="#c94d78"/>
          <g transform="translate(170,196) rotate(-9)"><rect x="-9" y="-25" width="18" height="50" rx="7" fill="#a52a5a"/></g>
          <g transform="translate(234,202) rotate(8)"><ellipse rx="12" ry="19" fill="#e8dcc2"/><ellipse cy="-12" rx="9" ry="13" fill="#f5eeda"/></g>
          <g transform="translate(176,248) rotate(-9)"><rect x="-9" y="-25" width="18" height="50" rx="7" fill="#96284f"/></g>
          <g transform="translate(234,262) rotate(8)"><ellipse rx="12" ry="19" fill="#e8dcc2"/><ellipse cy="-12" rx="9" ry="13" fill="#f5eeda"/></g>
          <g fill="#f6c6da" opacity=".9">
            <circle cx="158" cy="212" r="4.2" style="animation:bubbleRise 3.2s ease-out infinite"/>
            <circle cx="250" cy="270" r="3.6" style="animation:bubbleRise 3.2s ease-out .8s infinite"/>
          </g>
          <!-- a pelicula: PLANA, colada na superficie -->
          <path d="M134,148 Q170,143 202,148 Q234,153 270,148 L270,158 L134,158Z" fill="#fdfaf5" opacity=".92"/>
          <rect x="134" y="82" width="136" height="258" fill="url(#bGlass9)"/>
        </g>
        <path d="M134,96 Q134,82 148,82 L256,82 Q270,82 270,96 L270,318 Q270,340 248,340 L156,340 Q134,340 134,318Z" fill="none" stroke="#d8c6d2" stroke-width="2.4"/>
        <rect x="142" y="62" width="120" height="24" rx="7" fill="#f2e8ee" stroke="#d8c6d2" stroke-width="2.2"/>
        <rect x="184" y="44" width="36" height="20" rx="6" fill="#eadce4" stroke="#d8c6d2" stroke-width="2"/>
      </g>
    </g></g>

    <g style="animation:fadeSlide .6s ease both; animation-delay:.5s">
      <line x1="276" y1="178" x2="316" y2="178" stroke="#8a7284" stroke-width="1.6"/>
      <text x="320" y="182" font-size="10" font-weight="800" fill="#8a7284" font-family="system-ui" letter-spacing="1">KAHM</text>
    </g>

    <!-- a outra coisa: felpudo, e riscado -->
    <g style="animation:fadeSlide .6s ease both; animation-delay:1s">
      <rect x="150" y="398" width="104" height="76" rx="12" fill="#fff" stroke="#e6d4de" stroke-width="2"/>
      <circle cx="190" cy="430" r="13" fill="#9bb87a"/>
      <circle cx="214" cy="440" r="15" fill="#8aa868"/>
      <circle cx="204" cy="418" r="10" fill="#a8c48a"/>
      <circle cx="218" cy="422" r="7" fill="#7d9c5c"/>
      <line x1="140" y1="388" x2="264" y2="484" stroke="#c0392b" stroke-width="5" stroke-linecap="round"/>
      <line x1="264" y1="388" x2="140" y2="484" stroke="#c0392b" stroke-width="5" stroke-linecap="round"/>
      <text x="202" y="494" text-anchor="middle" font-size="11" font-weight="900" fill="#c0392b" font-family="system-ui" letter-spacing="1">FUZZY \u00b7 THROW IT OUT</text>
    </g>

    <text x="202" y="552" text-anchor="middle" font-size="20" font-weight="900" fill="#3d1f33" font-family="system-ui" style="animation:popInSeq .6s cubic-bezier(.3,1.5,.5,1) both; animation-delay:.2s">FLAT IS FINE, FUZZY IS NOT</text>
    <text x="202" y="578" text-anchor="middle" font-size="11.5" font-weight="600" fill="#a01e52" font-family="system-ui" style="animation:fadeSlide .6s ease both; animation-delay:.45s">A thin white film is kahm yeast, and it is harmless</text>

    <g style="animation:fadeSlide .7s ease both; animation-delay:1.3s">
      <rect x="34" y="590" width="337" height="52" rx="13" fill="#f6ecf1" stroke="#e4d2de" stroke-width="2"/>
      <text x="202" y="612" text-anchor="middle" font-size="12.5" font-weight="900" fill="#3d1f33" font-family="system-ui">Skim it off and carry on</text>
      <text x="202" y="630" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7284" font-family="system-ui">Hairy, coloured or spotted? That one is mould</text>
    </g>
  </svg>
'''

# ------------------------------------------------------------- array de cenas
ARRAY_NOVO = """const scenes = [
  { id:'s0', ms:6000, tag:'BEETS+GARLIC 1 / 10', cap:'One beet, one garlic head',   sub:'2% salt \\u00b7 ready in 1 to 2 weeks',          color:'#a01e52' },
  { id:'s1', ms:6500, tag:'BEETS+GARLIC 2 / 10', cap:'Skin off, 2 cm wedges',       sub:'grated beet goes to mush \\u2014 wedges stay crunchy', color:'#8f2450' },
  { id:'s2', ms:6500, tag:'BEETS+GARLIC 3 / 10', cap:'One smash per clove',         sub:'that is what releases the oil',             color:'#c2551f' },
  { id:'s3', ms:7500, tag:'BEETS+GARLIC 4 / 10', cap:'Beet, garlic, beet, garlic',   sub:'layered, so you can pull out what you want', color:'#a01e52' },
  { id:'s4', ms:7000, tag:'BEETS+GARLIC 5 / 10', cap:'20 g of salt per 1 kg',       sub:'coarse salt \\u2014 iodine stalls the ferment', color:'#ba7517' },
  { id:'s5', ms:7000, tag:'BEETS+GARLIC 6 / 10', cap:'Day 1 sharp, week 2 sweet',   sub:'betalain from the beet dyes the garlic',    color:'#0f6e56' },
  { id:'s6', ms:7000, tag:'BEETS+GARLIC 7 / 10', cap:'One week out, one week cold', sub:'18-22 \\u00b0C \\u00b7 burp the jar daily',        color:'#0f6e56' },
  { id:'s7', ms:6500, tag:'BEETS+GARLIC 8 / 10', cap:'Salads, burgers, eggs',       sub:'keeps for months in the fridge',            color:'#3d1f33' },
  { id:'s8', ms:6500, tag:'BEETS+GARLIC 9 / 10', cap:'Nothing above the line',      sub:'anything out of the brine is where mould starts', color:'#0f6e56' },
  { id:'s9', ms:7000, tag:'BEETS+GARLIC 10 / 10', cap:'The white film is not mould', sub:'flat and harmless \\u2014 fuzzy means throw it out', color:'#c0392b' }
];"""

CENAS_NOVAS = [
    ('s8', 6500, 'Nothing above the line',
     'anything out of the brine is where mould starts'),
    ('s9', 7000, 'The white film is not mould',
     'flat and harmless \\u2014 fuzzy means throw it out'),
]


def acha_cena(d, cid):
    return re.search(r'(?ms)^([ \t]*)<svg class="scene[^"]*"[^>]*id="%s".*?</svg>' % cid, d)


def acha_repeticoes(d, cenas):
    achados = []
    for cid, ms, cap, sub in cenas:
        m = acha_cena(d, cid)
        if not m:
            continue
        textos = [x.strip().lower()
                  for x in re.findall(r'<text[^>]*>([^<]*)</text>', m.group(0))]
        for campo, valor in (('cap', cap), ('sub', sub)):
            if valor.strip().lower() in textos:
                achados.append('%s %s="%s"' % (cid, campo, valor))
    return achados


def main():
    aplicar = '--apply' in sys.argv
    with io.open(ORIGEM, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    antes = len(d)
    print('origem   : %s (%d bytes, %s)' % (ORIGEM, antes,
                                            'CRLF' if eol == '\r\n' else 'LF'))

    m = acha_cena(d, 's7')
    if not m:
        print('ERRO: nao achei a cena s7')
        return 1

    # 2) as 2 cenas novas entram DEPOIS do </svg> da s7.
    #    ⚠️ ISTO VEM PRIMEIRO. `m.end()` foi medido NESTE `d`: mexer no texto antes
    #    invalida o offset e a insercao corta caractere. Aconteceu aqui — a troca do
    #    rotulo ("1 / 8" -> "1 / 10", +1 char) deixou `</svg` sem o `>` e o arquivo
    #    saiu com 10 cenas e 9 `</svg>` (uma cena nao fechada). O validador passou:
    #    ele conta `<svg class="scene`, nao pares.
    novo = eol + eol + (S8 + S9).replace('\n', eol).rstrip('\n')
    d = d[:m.end()] + novo + d[m.end():]

    # 1) o rotulo estatico do topo (o resto vem do motor)
    rotulo = '>BEETS+GARLIC 1 / 8</div>'
    if d.count(rotulo) != 1:
        print('ERRO: o rotulo estatico casou %d vez(es)' % d.count(rotulo))
        return 1
    d = d.replace(rotulo, '>BEETS+GARLIC 1 / 10</div>', 1)

    # 3) o array de cenas
    arr = re.search(r'const scenes = \[.*?\n\];', d, re.S)
    if not arr:
        print('ERRO: nao achei `const scenes`')
        return 1
    d = d.replace(arr.group(0), ARRAY_NOVO.replace('\n', eol), 1)

    # ------------------------------------------------------------ conferencias
    ids = re.findall(r'<svg class="scene[^"]*" id="(s\d+)"', d)
    print('  cenas no HTML: %d -> %s' % (len(ids), ' '.join(ids)))
    if ids != ['s%d' % i for i in range(10)]:
        print('ERRO: as cenas nao sao s0..s9')
        return 1
    # a guarda que teria pego o bug do offset: cena aberta sem fechar passa por tudo
    if d.count('</svg>') != len(ids):
        print('ERRO: %d cenas mas %d `</svg>` — alguma cena ficou aberta.'
              % (len(ids), d.count('</svg>')))
        return 1
    total = sum(int(x) for x in re.findall(r'ms:(\d+)', d))
    print('  duracao: %.1f s' % (total / 1000.0))
    if total < 60000:
        print('ERRO: %.1f s nao passa dos 60 s que o TikTok exige.' % (total / 1000.0))
        return 1
    for t in ('bGlass8', 'bJar8', 'bGlass9', 'bJar9'):
        if d.count('id="%s"' % t) != 1:
            print('ERRO: id de defs duplicado ou ausente: %s' % t)
            return 1
    if 'BEETS+GARLIC 1 / 8' in d or ' / 8' in d:
        print('ERRO: sobrou rotulo "/ 8"')
        return 1
    rep = acha_repeticoes(d, CENAS_NOVAS)
    if rep:
        print('ERRO: a legenda do mp4 repete o texto da cena: %s' % rep)
        return 1
    for trecho in ('KEEP IT UNDER THE BRINE', 'FLAT IS FINE, FUZZY IS NOT',
                   'THROW IT OUT', 'KAHM'):
        if trecho not in d:
            print('ERRO: nao achei "%s"' % trecho)
            return 1

    print('  %s %d -> %d bytes' % (DESTINO, antes, len(d.encode('utf-8'))))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(DESTINO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: corte de 60 s do #19.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
