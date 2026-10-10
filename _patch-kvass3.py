# -*- coding: utf-8 -*-
"""_patch-kvass3.py — 3 correcoes no gerador do #28 (achadas OLHANDO o render).

1) CENA 4: a tampa+airlock estava em `translate(300,344)`, SOLTA ao lado do jarro,
   e lia como cogumelo/embolo. Agora ela vai DENTRO do grupo que balanca, no lugar
   exato da boca do jarro (local -75 = -104 * 0.72) e com escala 0.93 para casar a
   largura da boca (48 * 0.93 = 44.6 = 62 * 0.72).
   ⚠️ Tem de ficar dentro do grupo do `wobble`: o keyframe e' `rotate(+-2.5deg)`,
   entao fora dele a tampa descola do jarro a cada ciclo.

2) CENA 1: o endro saiu. No zoom 3x ele le' como GRAVETO/pinha, nao como erva — e
   nenhum texto do video depende dele. Ficam os dois objetos que o pedido pediu:
   beterraba e alho.

3) Reenquadramento da cena 1 depois de tirar o endro (o conteudo estava 14 px
   a' esquerda do centro).

O que NAO foi mexido, de proposito: as bolhas "sumidas" da cena 7. O `riseFast`
comeca e termina em `opacity:0`, e o `--final` congela em -1s (71% do ciclo):
o `--no-anim` mostra as bolhas dentro do jarro. Artefato do modo de revisao,
nao defeito — a licao que ja' esta' na skill.

Uso:  python _patch-kvass3.py            # dry-run
      python _patch-kvass3.py --apply
"""
import io
import sys

ALVO = '_criar-beterraba-kvass.py'

CENA4_VELHO = """    <g transform="translate(140,404)">
      <g style="animation:wobble 2.8s ease-in-out infinite">@JARRA@</g>
    </g>
    <g transform="translate(300,344)">@TAMPA@</g>"""

CENA4_NOVO = """    <g transform="translate(202,404)">
      <g style="animation:wobble 2.8s ease-in-out infinite">@JARRA@<g transform="translate(0,-75) scale(0.93)">@TAMPA@</g></g>
    </g>"""

CENA0_VELHO = """    <g transform="translate(118,272)">@BETERRABA@</g>
    <g transform="translate(262,262)">@ALHO@</g>
    <g transform="translate(324,306)">@ENDRO@</g>"""

CENA0_NOVO = """    <g transform="translate(132,272)">@BETERRABA@</g>
    <g transform="translate(276,262)">@ALHO@</g>"""

CADEIA_VELHO = """     .replace('@BETERRABA@', beterraba(0, 0, 0.72)).replace('@ALHO@', alho(0, 0, 0.72)) \\
     .replace('@ENDRO@', endro(0, 0, 0.85))"""

CADEIA_NOVO = """     .replace('@BETERRABA@', beterraba(0, 0, 0.72)).replace('@ALHO@', alho(0, 0, 0.72))"""

TRABALHO = [(CENA4_VELHO, CENA4_NOVO, 1),
            (CENA0_VELHO, CENA0_NOVO, 1),
            (CADEIA_VELHO, CADEIA_NOVO, 1)]


def main():
    aplicar = '--apply' in sys.argv
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    antes = len(d)

    for velho, _, esperado in TRABALHO:
        n = d.count(velho)
        print('  %-56s %d vez(es) (esperava %d)'
              % (velho.strip().split('\n')[0][:56], n, esperado))
        if n != esperado:
            print('ABORTA: nada foi gravado.')
            return 1

    for velho, novo, _ in TRABALHO:
        d = d.replace(velho, novo, 1)

    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as e:
        print('ABORTA: SyntaxError linha %s: %s' % (e.lineno, e.msg))
        return 1

    for trecho in ('translate(0,-75) scale(0.93)', 'translate(132,272)',
                   'translate(276,262)'):
        if trecho not in d:
            print('ABORTA: nao achei "%s" depois da troca.' % trecho)
            return 1
    if '@ENDRO@' in d:
        print('ABORTA: @ENDRO@ sobrou no gerador (o desenho saiu, o replace tinha de sair).')
        return 1
    if 'translate(300,344)' in d:
        print('ABORTA: a tampa solta continua la.')
        return 1

    print('  %s %d -> %d bytes' % (ALVO, antes, len(d)))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: 3 correcoes no gerador do #28.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
