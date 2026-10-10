# -*- coding: utf-8 -*-
"""
_patch-maca2.py — tira as 4 repeticoes entre o CARTAO e a BARRA DE LEGENDA.

O `acha_repeticoes()` do gerador acusou:
  s1 cap="The apple is the engine"
  s3 sub="your jar is not dead - it is waiting"
  s4 cap="Two days of silence"
  s6 cap="Six days, not four"

Ou seja: o texto grande da cena dizia exatamente o que a barra de legenda do mp4
ja' ia dizer — o espectador leria a mesma frase duas vezes na tela. O conserto e'
sempre no CARTAO (a legenda e' a narracao; o cartao tem de ACRESCENTAR).

Ancora com contagem esperada: ABORTA SEM GRAVAR se alguma nao casar.
"""
import io
import os
import sys

ALVO = '_criar-maca-alho-cenoura.py'

# (ancora, substituto, quantas vezes tem de casar)
EDICOES = [
    # s1 — o cartao de cima
    (r'>THE APPLE IS THE ENGINE</text>', r'>WHAT THE APPLE BRINGS</text>', 1),
    (r'>sugar for the bacteria, yeast on the skin</text>',
     r'>sugar in the flesh, yeast on the skin</text>', 1),

    # s3 — a linha de baixo do cartao de cima
    (r'>your jar is not dead - it is waiting</text>',
     r'>the allicin has to fade first</text>', 1),

    # s4 — o cartao de cima
    (r'>TWO DAYS OF SILENCE</text>', r'>THE JAR GOES QUIET</text>', 1),

    # s6 — o selo
    (r'>SIX DAYS, NOT FOUR</text>', r'>TWO MORE DAYS</text>', 1),
]


def main():
    if not os.path.exists(ALVO):
        print('ABORTA: nao achei %s' % ALVO)
        return 1
    with io.open(ALVO, encoding='utf-8', newline='') as f:
        d = f.read()
    antes = len(d.encode('utf-8'))

    for old, new, esperado in EDICOES:
        n = d.count(old)
        if n != esperado:
            print('ABORTA: ancora casou %d vez(es), esperava %d:' % (n, esperado))
            print('   %r' % old)
            return 1
        d = d.replace(old, new, esperado)
        print('  ok  %d vez(es)  %-52s -> %s'
              % (n, old[:52], new[1:new.find('</text>')]))

    compile(d, ALVO, 'exec')
    tmp = ALVO + '.tmp'
    with io.open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write(d)
    os.replace(tmp, ALVO)
    print()
    print('gravado: %s  %d -> %d bytes' % (ALVO, antes, len(d.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
