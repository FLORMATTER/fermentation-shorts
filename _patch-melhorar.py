# -*- coding: utf-8 -*-
"""_patch-melhorar.py — conserta a ANCORA do _melhorar-beterraba-melancia.py.

O 1o dry-run deu `ancora de s1 casou 0 vez(es)`: entre as cenas NAO ha' so'
linhas em branco — ha' uma linha de COMENTARIO (`\\n\\n# ---- cena 3: ...`). Entao
`(?=\\n\\ndef s2\\()` nunca casa.

Licao (4a vez que esse lookahead morde): nao ancorar no `def` seguinte, ancorar
no SEPARADOR — que aqui e' sempre `\\n\\n#` ou `\\n\\nTEXTOS`. Assim a mesma
ancora serve para todas as cenas, sem saber o nome da proxima.

    python _patch-melhorar.py            # dry-run
    python _patch-melhorar.py --apply
"""
import io
import re
import sys

ALVO = '_melhorar-beterraba-melancia.py'

TRABALHO = [
    # a ancora generica: vale para todas as cenas
    ("    return re.compile(r'def %s\\(t\\):.*?\\n(?=\\n\\ndef %s\\()' % (nome, proximo), re.S)",
     "    return re.compile(r'def %s\\(t\\):.*?\\n(?=\\n\\n(?:#|TEXTOS))' % nome, re.S)"),
    # uso 1 (conferencia das ancoras)
    ('        n = len(bloco(nome, prox).findall(d))',
     '        n = len(bloco(nome).findall(d))'),
    # uso 2 (a troca) — repoe o `\\n` que o padrao consumiu
    ('        d = bloco(nome, prox).sub(lambda m: novo_txt, d, count=1)',
     '        d = bloco(nome).sub(lambda m: novo_txt + eol, d, count=1)'),
]


def main():
    aplicar = '--apply' in sys.argv
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    antes = len(d)

    for velho, _ in TRABALHO:
        n = d.count(velho)
        print('  ancora %-56s %d vez(es)' % (velho.strip()[:56], n))
        if n != 1:
            print('ABORTA: ancora casou %d vez(es), esperava 1.' % n)
            return 1
    for velho, novo in TRABALHO:
        d = d.replace(velho, novo, 1)

    for trecho in ('(?=\\n\\n(?:#|TEXTOS))', 'bloco(nome).findall(d)',
                   'novo_txt + eol, d, count=1'):
        if trecho not in d:
            print('ABORTA: nao achei "%s" depois da troca.' % trecho)
            return 1
    if 'bloco(nome, prox)' in d:
        print('ABORTA: sobrou chamada com `prox`.')
        return 1
    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as e:
        print('ABORTA: sintaxe invalida — %s' % e)
        return 1

    print('%s: %d -> %d bytes' % (ALVO, antes, len(d)))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
