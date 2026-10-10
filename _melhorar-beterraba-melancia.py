# -*- coding: utf-8 -*-
"""_melhorar-beterraba-melancia.py — conserta no GERADOR o que o render mostrou.

O render (folha de contato `--final`) acusou 4 coisas que o validador nao ve:

 1. **cena 1 — COLISAO**: a garrafa estava em cima da escala de pH e cobria o
    rotulo `WATERMELON`, que aparecia cortado como "RMELON". A escala E' a
    mensagem da cena: ela nao pode ser coberta. A garrafa desce e encolhe.
 2. **cena 2 — a faca flutuava** longe da melancia. Desce e gira para a ponta
    pousar na fatia. As gotas sobem para junto da casca.
 3. **cena 3 — o "acucar" lia como copo vazio**: a forma clara sem nada dentro.
    Agora e' um copo INCLINADO com a palavra SUGAR e graos caindo na beterraba.
 4. **cena 6 — o fecho encostava na faixa da legenda** (y=634, e a faixa comeca
    em 647). Sobe para 604, com os cartoes reorganizados.
 5. **cena 4 — topo vazio**: entra um cabecalho curto para equilibrar.

REGRA DO PROJETO: conserto por script separado TEM de voltar para o gerador —
senao regerar o short desfaz o conserto.

    python _melhorar-beterraba-melancia.py            # dry-run
    python _melhorar-beterraba-melancia.py --apply
"""
import io
import re
import sys

GERADOR = '_criar-kombucha-beterraba-melancia.py'


def bloco(nome):
    """Padrao de bloco com o lookahead CERTO.

    ATENCAO: o `.*?\\n` ja' consome um `\\n`, entao no lookahead sobram DOIS, nao
    tres — `(?=\\n\\n\\ndef y)` NUNCA casa. Custou `casou 0 vez(es)` tres vezes
    (pepino `dente`, `bulbo_alho`, melao).
    """
    return re.compile(r'def %s\(t\):.*?\n(?=\n\n(?:#|TEXTOS))' % nome, re.S)


# --------------------------------------------------------------------- cena 2
S1 = """def s1(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <g transform="translate(202,196)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="@TEAL@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#0f6e56" font-family="system-ui">THE JAR MATCHES THE WINDOW</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#4a8a6e" font-family="system-ui">the first ferment ends inside the safe band</text>
    </g>
    @ESCALA@
    <g transform="translate(202,450)">
      <g style="animation:wobble 2.6s ease-in-out infinite">@GARRAFA@</g>
    </g>
    <g transform="translate(202,420)">@BOLHAS@</g>
    <g transform="translate(202,556)">
      <rect x="-172" y="-42" width="344" height="84" rx="12" fill="#eaf7f1" stroke="@TEAL@" stroke-width="3"/>
      <text x="0" y="-6" text-anchor="middle" font-size="16" font-weight="800" fill="#0f6e56" font-family="system-ui">2.5 TO 3.5 IS WHERE IT STOPS</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#4a8a6e" font-family="system-ui">beetroot survives that - it dies past it</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@TEAL@', TEAL) \\
     .replace('@ESCALA@', escala_ph_janela(
         202, 300, 312, 34, 3.0, 6.0,
         [(3.0, TEAL, 'KOMBUCHA'), (5.2, MELANCIA_ESC, 'WATERMELON')])) \\
     .replace('@GARRAFA@', garrafa(MAGENTA, 0.55)) \\
     .replace('@BOLHAS@', bolhas())"""


# --------------------------------------------------------------------- cena 3
S2 = """def s2(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <circle cx="188" cy="286" r="136" fill="@CREME@" opacity=".8"/>
    <g transform="translate(188,318)">
      <g style="animation:wobble 2.9s ease-in-out infinite">@MELANCIA@</g>
    </g>
    <g transform="translate(322,340)">@FACA@</g>
    @GOTAS@
    <g transform="translate(202,556)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="@MELANCIA_ESC@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@MELANCIA_ESC@" font-family="system-ui">MOSTLY WATER</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#c07a8a" font-family="system-ui">pH 5.2 and 92% water - it dilutes, not acidifies</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@CREME@', CREME) \\
     .replace('@MELANCIA_ESC@', MELANCIA_ESC).replace('@MELANCIA@', melancia(0, 0, 1.0)) \\
     .replace('@FACA@', faca(0, 0, 35)) \\
     .replace('@GOTAS@', '\\n    '.join([
         gota(152, 348, 1.0), gota(192, 364, 1.25), gota(230, 346, 0.85)]))"""


# --------------------------------------------------------------------- cena 4
S3 = """def s3(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <circle cx="202" cy="292" r="140" fill="@CREME@" opacity=".8"/>
    <g transform="translate(202,292)">
      <g style="animation:wobble 3.0s ease-in-out infinite">@BETERRABA@</g>
    </g>
    <g transform="translate(202,130)">
      <g style="animation:pour2x 1.6s ease-out infinite">
        <g transform="rotate(28) scale(.88)">
          <path d="M-30,-32 L30,-32 L23,26 Q0,38 -23,26 Z" fill="#fbf7ea" stroke="#c9bfa4" stroke-width="3"/>
          <text x="0" y="6" text-anchor="middle" font-size="15" font-weight="800" fill="#8a7a5c" font-family="system-ui">SUGAR</text>
        </g>
      </g>
    </g>
    @GRAOS@
    <g transform="translate(202,468)">
      <rect x="-160" y="-34" width="320" height="68" rx="12" fill="#fff" stroke="@MAGENTA@" stroke-width="3"/>
      <text x="0" y="-2" text-anchor="middle" font-size="17" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">FUEL AND COLOUR AT ONCE</text>
      <text x="0" y="22" text-anchor="middle" font-size="13" font-weight="600" fill="#a8728c" font-family="system-ui">7 g of sugar per 100 g - more than the melon</text>
    </g>
    <g transform="translate(202,588)">
      <rect x="-176" y="-38" width="352" height="76" rx="12" fill="#fdf0f5" stroke="@MAGENTA_CLARO@" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="15" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">SUGAR FEEDS THE SECOND FERMENT</text>
      <text x="0" y="19" text-anchor="middle" font-size="13" font-weight="600" fill="#a8728c" font-family="system-ui">and the pigment comes along for free</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@CREME@', CREME) \\
     .replace('@MAGENTA@', MAGENTA).replace('@MAGENTA_ESC@', MAGENTA_ESC) \\
     .replace('@MAGENTA_CLARO@', MAGENTA_CLARO).replace('@BETERRABA@', beterraba(0, 0, 1.0)) \\
     .replace('@GRAOS@', '\\n    '.join(
         '<circle cx="%d" cy="%d" r="%s" fill="#fdfbf4" stroke="#c9bfa4"'
         ' stroke-width="1.6"/>' % (x, y, r)
         for x, y, r in ((184, 196, 3.4), (204, 208, 2.8), (194, 224, 3.2),
                         (212, 190, 2.6), (178, 212, 2.4))))"""


# --------------------------------------------------------------------- cena 5
S4 = """def s4(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <g transform="translate(202,116)">
      <text x="0" y="0" text-anchor="middle" font-size="17" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">SAME JUICE, TWO STATES</text>
    </g>
    <g transform="translate(118,268)">
      <g style="animation:wobble 2.8s ease-in-out infinite">@FATIA_BOA@</g>
    </g>
    <g transform="translate(290,268)">
      <g style="animation:wobble 3.1s ease-in-out infinite">@FATIA_RUIM@</g>
    </g>
    <g transform="translate(118,344)">
      <g style="animation:tick 2.2s ease-in-out infinite">
        <path d="M-14,-8 L-3,4 L15,-16" stroke="@VERDE_ESC@" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
    </g>
    <g transform="translate(290,344)">
      <path d="M-13,-13 L13,13 M13,-13 L-13,13" stroke="#c0392b" stroke-width="6" stroke-linecap="round"/>
    </g>
    <g transform="translate(118,424)">
      <rect x="-72" y="-26" width="144" height="52" rx="10" fill="#fdf0f5" stroke="@MAGENTA@" stroke-width="2.5"/>
      <text x="0" y="7" text-anchor="middle" font-size="19" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">MAGENTA</text>
    </g>
    <g transform="translate(290,424)">
      <rect x="-72" y="-26" width="144" height="52" rx="10" fill="#f2ece6" stroke="#a89488" stroke-width="2.5"/>
      <text x="0" y="7" text-anchor="middle" font-size="19" font-weight="800" fill="#7d6a5c" font-family="system-ui">BRICK</text>
    </g>
    <g transform="translate(202,548)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="@MAGENTA@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="@MAGENTA_ESC@" font-family="system-ui">THE JAR IS THE STATUS LIGHT</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#a8728c" font-family="system-ui">vivid means in, brick means you went past</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@MAGENTA@', MAGENTA) \\
     .replace('@MAGENTA_ESC@', MAGENTA_ESC).replace('@VERDE_ESC@', VERDE_ESC) \\
     .replace('@FATIA_BOA@', beterraba_fatia(0, 0, 1.05)) \\
     .replace('@FATIA_RUIM@', beterraba_fatia(0, 0, 1.05, cor='#b07a68'))"""


# --------------------------------------------------------------------- cena 7
S6 = """def s6(t):
    return '''    <rect width="405" height="720" fill="@FUNDO@"/>
    <circle cx="202" cy="250" r="136" fill="@CREME@" opacity=".8"/>
    <g transform="translate(202,250)">
      <g style="animation:wobble 2.7s ease-in-out infinite">@GARRAFA@</g>
    </g>
    <g transform="translate(202,250)">@BOLHAS@</g>
    <g transform="translate(202,412)">
      <rect x="-176" y="-46" width="352" height="92" rx="12" fill="#fff" stroke="@AMBAR@" stroke-width="3"/>
      <text x="0" y="-12" text-anchor="middle" font-size="18" font-weight="800" fill="#8a6a2f" font-family="system-ui">DRINK IT FRESH</text>
      <text x="0" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">the longer it sits, the more alcohol it makes</text>
    </g>
    <g transform="translate(202,508)">
      <rect x="-172" y="-40" width="344" height="80" rx="12" fill="#fff8e6" stroke="@AMBAR@" stroke-width="3"/>
      <text x="0" y="-4" text-anchor="middle" font-size="15" font-weight="800" fill="#8a6a2f" font-family="system-ui">1 PART FRUIT TO 4 OF KOMBUCHA</text>
      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600" fill="#b08f4e" font-family="system-ui">then three days in the fridge</text>
    </g>
    <g transform="translate(202,604)">
      <text x="0" y="0" text-anchor="middle" font-size="15" font-weight="800" fill="#0f6e56" font-family="system-ui">which one should I ferment next?</text>
    </g>'''.replace('@FUNDO@', FUNDO).replace('@CREME@', CREME) \\
     .replace('@AMBAR@', AMBAR).replace('@GARRAFA@', garrafa(MAGENTA, 0.78)) \\
     .replace('@BOLHAS@', bolhas())"""


TRABALHO = (('s1', 's2', S1), ('s2', 's3', S2), ('s3', 's4', S3),
            ('s4', 's5', S4), ('s6', 'monta_cenas', S6))


def main():
    aplicar = '--apply' in sys.argv
    with io.open(GERADOR, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    antes = len(d)
    print('gerador: %s (%d bytes, %s)' % (GERADOR, antes,
                                          'CRLF' if eol == '\r\n' else 'LF'))

    # ---------- 1) conferir TODAS as ancoras antes de tocar em nada
    for nome, prox, _ in TRABALHO:
        n = len(bloco(nome).findall(d))
        print('  ancora %-4s -> %-12s %d vez(es)' % (nome, prox, n))
        if n != 1:
            print('ABORTA: a ancora de %s casou %d vez(es).' % (nome, n))
            return 1

    # ---------- 2) trocar
    for nome, prox, novo in TRABALHO:
        novo_txt = novo.replace('\n', eol)
        d = bloco(nome).sub(lambda m: novo_txt + eol, d, count=1)

    # ---------- 3) conferencias
    for nome, _, _ in TRABALHO:
        if len(re.findall(r'^def %s\(t\):' % nome, d, re.M)) != 1:
            print('ABORTA: `def %s` nao ficou 1 vez.' % nome)
            return 1
    # a ancora `\n\n#` engole as funcoes seguintes: contar TODAS
    for nome in ('s0', 's1', 's2', 's3', 's4', 's5', 's6'):
        if len(re.findall(r'^def %s\(t\):' % nome, d, re.M)) != 1:
            print('ABORTA: perdi a funcao s%s.' % nome)
            return 1
    for trecho in ('SAME JUICE, TWO STATES', 'SUGAR</text>', '@GRAOS@',
                   'faca(0, 0, 35)', 'translate(202,604)', 'garrafa(MAGENTA, 0.55)'):
        if trecho not in d:
            print('ABORTA: nao achei "%s" no texto novo.' % trecho)
            return 1
    for velho in ('translate(322,214)', 'translate(202,634)',
                  'd="M-13,-34 L13,-34 L17,10 Q0,24 -17,10 Z"'):
        if velho in d:
            print('ABORTA: o trecho velho "%s" ainda esta no arquivo.' % velho)
            return 1
    try:
        compile(d, GERADOR, 'exec')
    except SyntaxError as e:
        print('ABORTA: sintaxe invalida — %s' % e)
        return 1

    print('gerador: %d -> %d bytes (+%d)' % (antes, len(d), len(d) - antes))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(GERADOR, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado. Agora: python %s && python _revisar-cenas.py <saida> --final'
          % GERADOR)
    return 0


if __name__ == '__main__':
    sys.exit(main())
