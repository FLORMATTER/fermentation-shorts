# -*- coding: utf-8 -*-
"""_patch-kvass.py — 2 correcoes no gerador do #28, com contagem.

1) O `@SAL@` estava solto, sem `<g transform>`: os graos de sal seriam desenhados
   na ORIGEM (canto superior esquerdo do cartao), nao entre a colher e o jarro.
2) Os cubos de 2 cm passavam da borda do painel verde (y ia ate 72, o painel
   acaba em 64): virou 2x2 dentro de +-36.

Uso:  python _patch-kvass.py            # dry-run
      python _patch-kvass.py --apply
"""
import io
import sys

ALVO = '_criar-beterraba-kvass.py'

SAL_VELHO = """    <g transform="translate(140,378)">@COLHER@</g>
    @SAL@
    <g transform="translate(300,392)">@JARRA@</g>"""

SAL_NOVO = """    <g transform="translate(136,376)">@COLHER@</g>
    <g transform="translate(212,344)">@SAL@</g>
    <g transform="translate(304,394)">@JARRA@</g>"""

CUBOS_VELHO = """            f'<rect x="-40" y="-34" width="34" height="34" rx="7" fill="{BETERRABA}"/>'
            f'<rect x="2" y="-34" width="34" height="34" rx="7" fill="{BETERRABA_CLARO}"/>'
            f'<rect x="-19" y="4" width="34" height="34" rx="7" fill="{BETERRABA}"/>'
            f'<rect x="-40" y="38" width="34" height="34" rx="7" fill="{BETERRABA_CLARO}"/>'
            f'<rect x="2" y="38" width="34" height="34" rx="7" fill="{BETERRABA}"/>'"""

CUBOS_NOVO = """            f'<rect x="-36" y="-36" width="32" height="32" rx="7" fill="{BETERRABA}"/>'
            f'<rect x="4" y="-36" width="32" height="32" rx="7" fill="{BETERRABA_CLARO}"/>'
            f'<rect x="-36" y="4" width="32" height="32" rx="7" fill="{BETERRABA_CLARO}"/>'
            f'<rect x="4" y="4" width="32" height="32" rx="7" fill="{BETERRABA}"/>'"""

TRABALHO = [(SAL_VELHO, SAL_NOVO, 1), (CUBOS_VELHO, CUBOS_NOVO, 1)]


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

    # o codigo tem de continuar compilavel ANTES de gravar
    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as e:
        print('ABORTA: SyntaxError linha %s: %s' % (e.lineno, e.msg))
        return 1

    for trecho in ('translate(212,344)', 'x="-36" y="-36"', 'x="4" y="4"',
                   'x="4" y="-36"', 'x="-36" y="4"'):
        if trecho not in d:
            print('ABORTA: nao achei "%s" depois da troca.' % trecho)
            return 1
    if '@SAL@\n    <g transform="translate(304,394)"' in d:
        print('ABORTA: o sal continua solto.')
        return 1

    print('  %s %d -> %d bytes' % (ALVO, antes, len(d)))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: 2 correcoes no gerador do #28.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
