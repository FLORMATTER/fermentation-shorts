# -*- coding: utf-8 -*-
"""_nota-pt-original.py — poe a nota do "original em portugues" nos #18, #19 e #20.

    python _nota-pt-original.py

Por que: quando os tres originais PT foram criados (`_criar-cenoura-maca-pt.py`,
`_criar-beterraba-alho-pt.py`, `_criar-couveflor-maca-pt.py`), o pacote continuou
dizendo "This one has **no Portuguese original**". Ficou mentindo. O #17 e o #21
ja' tem a nota certa — esta' aqui a mesma frase, palavra por palavra.

ARMADILHA: a string
    'This one has **no Portuguese original** - it was built in English.'
e' PREFIXO de DUAS entradas (#18 e #20). Ancorar so' nela casaria 2 vezes e o
`assert` derrubaria o script. Por isso a ancora do #20 leva o contexto de baixo.

Ancoras contadas, aborta SEM GRAVAR.
"""
import io
import sys

ALVO = 'guias/pacote-legendas-descricoes-en.md'

NOTA = ('There is also a **Portuguese original**, `%s`. The series\n'
        'convention is a PT original plus an `-en` sibling; this one was built EN-only, so\n'
        'the PT side was added later. It is not part of this package - it exists so the pair\n'
        'can be checked against each other.')

TROCAS = [
    # --------------------------------------------------------------- #18
    ('#18 carrot+apple',
     'This one has **no Portuguese original** - it was built in English. If the PT side is ever\n'
     'added, follow the `-en` convention: PT original plus the `-en` sibling.',
     NOTA % 'cenoura/shorts-carrot-apple.html', 1),

    # --------------------------------------------------------------- #19
    ('#19 beetroot+garlic',
     'This one has **no Portuguese original** - it was built in English, already in the upload\n'
     'format.',
     NOTA % 'beterraba/shorts-beet-garlic-1080x1920.html', 1),

    # --------------------------------------------------------------- #20
    # leva o contexto de baixo porque a 1a linha sozinha casa 2 vezes
    ('#20 cauliflower+apple',
     'This one has **no Portuguese original** - it was built in English.\n'
     '\n'
     '> This is the **second cauliflower entry**',
     NOTA % 'couve-flor/shorts-cauliflower-apple.html' + '\n\n> This is the **second cauliflower entry**', 1),
]


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    print('%s (%d bytes, %s)\n' % (ALVO, len(d.encode('utf-8')),
                                   'CRLF' if eol == '\r\n' else 'LF'))

    for i, (rotulo, velho, novo, esperado) in enumerate(TROCAS, 1):
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        c = d.count(v)
        if c != esperado:
            print('  %d. %-24s casou %d (esperado %d)  ERRO'
                  % (i, rotulo, c, esperado))
            print('\nABORTADO — nada foi gravado.')
            return 1
        d = d.replace(v, n)
        print('  %d. %-24s ok (%d)' % (i, rotulo, c))

    # prova: nao pode ter sobrado nenhuma negacao
    sobra = d.count('no Portuguese original')
    print('\n  "no Portuguese original" restantes: %d' % sobra)
    if sobra:
        print('ABORTADO — ainda sobrou negacao.')
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('  gravado: %d bytes' % len(d.encode('utf-8')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
