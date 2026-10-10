# -*- coding: utf-8 -*-
"""_melhorar-beterraba-cenoura2.py — conserta a faca e a REPETICAO de texto.

Dois defeitos:

1. A FACA virou **tubo de ensaio**. Desenhada em pe' (lamina para cima, cabo para
   baixo), a lamina estreita e vertical nao diz "faca" — o render mostrou um tubo
   com rolha. -> desenhar de LADO (lamina longa + cabo curto) e girar.

2. A BARRA DE LEGENDA repetia o titulo que ja' esta na cena — o erro (k) da
   skill. Acontecia em **4 das 7 cenas**, e em duas delas a sublinha tambem era
   quase a mesma frase. A regra: os 4 campos de texto de uma cena
   (titulo do cartao / sublinha do cartao / cap / sub) tem de dizer coisas
   DIFERENTES.

O conserto vai no GERADOR. Se qualquer ancora nao casar 1 vez, aborta sem gravar.

    python _melhorar-beterraba-cenoura2.py
"""
import io
import re
import sys

ALVO = '_criar-beterraba-cenoura.py'

# ---------------------------------------------------------------- a faca
FACA = '''def faca(x, y, rot=0, s=1.0):
    """Faca de chef vista de LADO: lamina longa + cabo curto. Depois girada.

    Em pe' (lamina para cima, cabo para baixo) a lamina estreita e vertical le'
    como **tubo de ensaio** — foi o que o render mostrou. Deitada, com lamina
    longa e cabo curto, e' inconfundivel.
    """
    return (f'<g transform="translate({x:g},{y:g}) rotate({rot:g}) scale({s:g})">'
            '<g style="animation:chop2x 1.7s ease-in-out infinite">'
            # lamina
            '<path d="M-92,-13 L22,-13 L22,13 L-62,13 Q-92,13 -92,-1 Z"'
            ' fill="#cdd6dc" stroke="#7a8a92" stroke-width="2.5"'
            ' stroke-linejoin="round"/>'
            # fio (borda de corte), mais claro
            '<path d="M-92,2 L22,2 L22,13 L-62,13 Q-92,13 -92,2 Z"'
            ' fill="#eef3f6"/>'
            # bolster
            '<rect x="22" y="-16" width="12" height="32" rx="3" fill="#9aa8b0"'
            ' stroke="#6d7c85" stroke-width="2"/>'
            # cabo
            '<rect x="34" y="-14" width="62" height="28" rx="11" fill="#5e3a1f"'
            ' stroke="#40260f" stroke-width="2.5"/>'
            '<circle cx="52" cy="0" r="3.4" fill="#cdd6dc"/>'
            '<circle cx="72" cy="0" r="3.4" fill="#cdd6dc"/>'
            '</g></g>')'''

# ------------------------------------------------------- textos sem repeticao
TEXTOS = """TEXTOS = {
    'titulo': 'Shorts animado — Beetroot and carrot (fermented)',
    'badge': '🟣 + 🥕',
    'capdiv': ('Beetroot and carrot'
               '<small>one makes the acid, one saves the colour</small>'),
    # Cada cena tem 4 campos de texto e eles NAO podem repetir a mesma frase:
    # titulo do cartao (SVG) / sublinha do cartao (SVG) / cap (barra) / sub (barra)
    'cenas': [
        ('s0', 6400, '%s 1 / 7' % TAG, 'Beetroot and carrot',
         'one bleeds red, one stays orange', ROXO_ESC),
        ('s1', 6400, '%s 2 / 7' % TAG, 'Why it fades',
         'betanin is the pigment - and it is fragile', '#a8909c'),
        ('s2', 6200, '%s 3 / 7' % TAG, 'Use salt without iodine',
         'iodine stalls the bacteria you want', '#8a6a2f'),
        ('s3', 6400, '%s 4 / 7' % TAG, 'Beet thin, carrot thick',
         'surface area decides how fast the sugar comes out', LARANJA_ESC),
        ('s4', 7000, '%s 5 / 7' % TAG, 'Two jars, same beet',
         'only the one with carrot keeps its colour', LARANJA_ESC),
        ('s5', 6400, '%s 6 / 7' % TAG, 'Nothing here is acid',
         'the acid has to be made - that is what the sugar is for', '#8a6a2f'),
        ('s6', 6400, '%s 7 / 7' % TAG, 'Five days is a guide',
         'taste it - sour means ready, sweet means wait', '#2f5c0d'),
    ],
}"""

# (nome, texto novo, PADRAO COMPLETO — ATENCAO: o `.*?\n` ja' consome um \n,
#  entao no lookahead sobram DOIS \n, nao tres)
BLOCOS = (
    ('faca', FACA, r'def faca\(.*?\n(?=\n\ndef relogio\()'),
    ('TEXTOS', TEXTOS, r'TEXTOS = \{.*?\n(?=\n\ndef cena\()'),
)

TROCAS = (
    # a faca: sai do canto em pe', entra deitada e girada
    ('<g transform="translate(318,196)">@FACA@</g>',
     '<g transform="translate(310,168)">@FACA@</g>', 1),
    ('faca(0, 0, 20)', 'faca(0, 0, -34, 0.68)', 1),
    # sublinha do cartao do sal (a antiga virava eco da barra)
    ('never guessed, always weighed',
     'that is 2% of the vegetable weight', 1),
    # sublinha do cartao do corte (a antiga foi para a barra)
    ('surface area decides how fast the sugar comes out</text>',
     'one releases sugar, one keeps the crunch</text>', 1),
)


def acha_repeticoes(txt):
    """Devolve as cenas em que o `cap` repete algum <text> da propria cena.

    Comparar com o texto do cartao por `font-size` era fragil: a cena 2 titula
    com 46 px ("2%") e a 4 com 17 px. Varrer TODOS os <text> da cena e' o certo.
    """
    blocos = re.findall(
        r'def s(\d)\(t\):(.*?)(?=\ndef s\d\(t\):|\n# -{3,} montagem)', txt, re.S)
    caps = re.findall(r"TAG, '([^']*)',", txt)
    achados = []
    for (idx, corpo), cap in zip(blocos, caps):
        textos = [t.strip().lower() for t in
                  re.findall(r'<text[^>]*>([^<]*)</text>', corpo)]
        if cap.strip().lower() in textos:
            achados.append('s%s "%s"' % (idx, cap))
    return achados, len(blocos), len(caps)


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'

    # --- 0) PROVA de que o verificador funciona: no arquivo ANTES do conserto
    #        ele TEM de achar as repeticoes. Verificador que nunca falha nao
    #        prova nada.
    antes, ncen, ncap = acha_repeticoes(d)
    if ncen != 7 or ncap != 7:
        print('ERRO: achei %d cenas e %d caps (esperava 7 e 7)' % (ncen, ncap))
        return 1
    if not antes:
        print('ERRO: o verificador NAO achou repeticao no arquivo antes do')
        print('      conserto — entao ele nao prova nada. Conferir a mao.')
        return 1
    print('  verificador testado: %d repeticao(oes) antes -> %s'
          % (len(antes), antes))

    # --- 1) confere TUDO antes de gravar
    for nome, novo, pat_str in BLOCOS:
        n = len(re.findall(pat_str, d, re.S))
        if n != 1:
            print('ERRO: bloco %s casou %d vez(es)' % (nome, n))
            return 1
    for velho, _, n in TROCAS:
        achou = d.count(velho)
        if achou != n:
            print('ERRO: ancora casou %d vez(es), esperava %d: %s'
                  % (achou, n, velho[:60]))
            return 1

    # --- 2) aplica
    for nome, novo, pat_str in BLOCOS:
        d = re.sub(pat_str, lambda m: novo.replace('\n', eol) + eol, d,
                   count=1, flags=re.S)
        print('  bloco trocado: %s' % nome)
    for velho, novo, n in TROCAS:
        d = d.replace(velho, novo, n)
        print('  troca: %s' % velho[:48])

    # --- 3) sanidade estrutural
    for nome in ('beterraba', 'beterraba_fatia', 'cenoura', 'cenoura_palito',
                 'escudo', 'jarra_dois', 'bolhas', 'colher_sal', 'faca',
                 'relogio', 'escala_ph'):
        if len(re.findall(r'^def %s\(' % nome, d, re.M)) != 1:
            print('ERRO: `def %s` sumiu ou duplicou' % nome)
            return 1
    if len(re.findall(r'^TEXTOS = \{', d, re.M)) != 1:
        print('ERRO: TEXTOS sumiu ou duplicou')
        return 1
    if d.count("'cenas': [") != 1:
        print('ERRO: a lista `cenas` nao esta sozinha')
        return 1
    for resto in ('never guessed', 'faca(0, 0, 20)', 'translate(318,196)'):
        if resto in d:
            print('ERRO: sobrou "%s"' % resto)
            return 1

    # --- 4) a REGRA do erro (k), agora no texto NOVO
    depois, ncen2, ncap2 = acha_repeticoes(d)
    if ncen2 != 7 or ncap2 != 7:
        print('ERRO: achei %d cenas e %d caps (esperava 7 e 7)' % (ncen2, ncap2))
        return 1
    if depois:
        print('ERRO: cap repetindo texto da propria cena:')
        for c in depois:
            print('    %s' % c)
        return 1
    print('  conferido: 7 cenas, %d caps, 0 repetidos' % ncap2)

    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as exc:
        print('ERRO: nao compila: linha %s: %s' % (exc.lineno, exc.msg))
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: 2 blocos + 4 trocas | %d bytes' % len(d.encode('utf-8')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
