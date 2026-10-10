# -*- coding: utf-8 -*-
"""_rewrap-notas.py — re-embrulha as duas notas PT que ficaram com a 1a linha longa.

    python _rewrap-notas.py

O #19 e o #20 tem nome de arquivo comprido, entao a 1a linha da nota saiu com
100 e 97 colunas, enquanto o #17, o #18 e o #21 embrulham em ~85. So' estetica,
mas o arquivo e' entregavel. Nada de conteudo muda — so' onde a linha quebra.

Ancoras contadas, aborta SEM GRAVAR.
"""
import io
import sys

ALVO = 'guias/pacote-legendas-descricoes-en.md'

TROCAS = [
    ('#19 beterraba',
     'There is also a **Portuguese original**, `beterraba/shorts-beet-garlic-1080x1920.html`. The series\n'
     'convention is a PT original plus an `-en` sibling;',
     'There is also a **Portuguese original**,\n'
     '`beterraba/shorts-beet-garlic-1080x1920.html`. The series convention is a PT original\n'
     'plus an `-en` sibling;', 1),

    ('#20 couve-flor',
     'There is also a **Portuguese original**, `couve-flor/shorts-cauliflower-apple.html`. The series\n'
     'convention is a PT original plus an `-en` sibling;',
     'There is also a **Portuguese original**,\n'
     '`couve-flor/shorts-cauliflower-apple.html`. The series convention is a PT original\n'
     'plus an `-en` sibling;', 1),
]


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    print('%s\n' % ALVO)

    for i, (rotulo, velho, novo, esperado) in enumerate(TROCAS, 1):
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        c = d.count(v)
        if c != esperado:
            print('  %d. %-16s casou %d (esperado %d)  ERRO' % (i, rotulo, c, esperado))
            print('\nABORTADO — nada foi gravado.')
            return 1
        d = d.replace(v, n)
        print('  %d. %-16s ok (%d)' % (i, rotulo, c))

    # prova: nenhuma linha pode passar de 90 colunas nas notas novas
    longas = [(n, len(l)) for n, l in enumerate(d.split(eol), 1)
              if 'Portuguese original' in l and len(l) > 90]
    print('\n  linhas de nota > 90 colunas: %d' % len(longas))
    if longas:
        print('ABORTADO — ainda ha linha longa: %s' % longas)
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('  gravado: %d bytes' % len(d.encode('utf-8')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
