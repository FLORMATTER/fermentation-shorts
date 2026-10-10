# -*- coding: utf-8 -*-
"""_patch-kvass2.py — poe a faca de volta no painel dos cubos (o #28).

O gerador ABORTOU com `keyframe nunca usado: ['chop2x']`: ao reestruturar a cena 6
eu troquei a faca pelos cubos e o `chop2x` ficou orfao. O painel do jeito CERTO
tem de mostrar a faca cortando — e' ele que carrega o keyframe.

⚠️ A 2a troca emenda um `.replace()` numa linha que NAO tinha ` \\` no fim (a licao
do #27): por isso a ancora nova inclui o ` \\` explicitamente, em vez de so'
acrescentar a linha.

Uso:  python _patch-kvass2.py            # dry-run
      python _patch-kvass2.py --apply
"""
import io
import sys

ALVO = '_criar-beterraba-kvass.py'

PAINEL_VELHO = """      <g transform="translate(0,-6)">@CUBOS@</g>"""

PAINEL_NOVO = """      <g transform="translate(-2,-40) rotate(-8) scale(0.44)">@FACA@</g>
      <g transform="translate(0,20)">@CUBOS@</g>"""

CADEIA_VELHO = """     .replace('@RALADO@', ralado(0, 0, 0.6)).replace('@CUBOS@', cubos())"""

CADEIA_NOVO = """     .replace('@RALADO@', ralado(0, 0, 0.6)).replace('@CUBOS@', cubos()) \\
     .replace('@FACA@', faca(0, 0, 0))"""

TRABALHO = [(PAINEL_VELHO, PAINEL_NOVO, 1), (CADEIA_VELHO, CADEIA_NOVO, 1)]


def main():
    aplicar = '--apply' in sys.argv
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    antes = len(d)

    for velho, _, esperado in TRABALHO:
        n = d.count(velho)
        print('  %-58s %d vez(es) (esperava %d)'
              % (velho.strip().split('\n')[0][:58], n, esperado))
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

    if d.count("@FACA@") != 2:
        print('ABORTA: @FACA@ aparece %d vez(es), esperava 2 (desenho + replace).'
              % d.count('@FACA@'))
        return 1
    for trecho in ('rotate(-8) scale(0.44)', "faca(0, 0, 0)"):
        if trecho not in d:
            print('ABORTA: nao achei "%s" depois da troca.' % trecho)
            return 1

    print('  %s %d -> %d bytes' % (ALVO, antes, len(d)))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: a faca voltou ao painel dos cubos.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
