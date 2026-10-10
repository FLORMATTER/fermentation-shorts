# -*- coding: utf-8 -*-
"""_consertar-numeros-melancia.py — conserta 3 textos do #26 no GERADOR.

1. **"more than the melon" estava FALSO.** O cartao comparava com o melao (do #24)
   e o melao cantalupo tem MAIS acucar que a beterraba. Numeros (USDA):
     beterraba (raw) 6,76 g / 100 g | melancia 6,2 g | melao cantalupo 7,86 g
   A comparacao honesta e' com a MELANCIA — que e' a outra fruta DESTE video.
   (Regra do projeto: numero no cartao tem de fechar com a conta.)

2. **"beetroot survives that - it dies past it"**: o "it" ficava ambiguo (a
   beterraba morre? o pigmento?). Quem degrada e' o PIGMENTO.

3. **"1 PART FRUIT TO 4 OF KOMBUCHA"** repetia a proporcao que e' o assunto da
   cena 7 do #24. Aqui o fecho e' o frio — que tambem e' o que segura a cor.

    python _consertar-numeros-melancia.py            # dry-run
    python _consertar-numeros-melancia.py --apply
"""
import io
import sys

GERADOR = '_criar-kombucha-beterraba-melancia.py'

TRABALHO = [
    # 1. a comparacao de acucar
    ('>7 g of sugar per 100 g - more than the melon<',
     '>7 g of sugar per 100 g - more than the watermelon<'),
    # 2. o "it" ambiguo
    ('>beetroot survives that - it dies past it<',
     '>the pigment holds inside the band<'),
    # 3. o fecho: frio em vez da proporcao do #24
    ('>1 PART FRUIT TO 4 OF KOMBUCHA</text>\n'
     '      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600"'
     ' fill="#b08f4e" font-family="system-ui">then three days in the fridge</text>',
     '>THREE DAYS, THEN THE FRIDGE</text>\n'
     '      <text x="0" y="20" text-anchor="middle" font-size="13" font-weight="600"'
     ' fill="#b08f4e" font-family="system-ui">cold slows it down and holds the colour</text>'),
    # 4. registrar os numeros certos na docstring (a fonte da verdade)
    ('  - **beterraba: ~7 g de acucar / 100 g**; melancia: **~6 g / 100 g** (USDA);',
     '  - acucar (USDA): **beterraba 6,76 g / 100 g**, **melancia 6,2 g**, **melao\n'
     '    cantalupo 7,86 g** — a beterraba ganha da MELANCIA mas PERDE do melao do\n'
     '    #24. Comparar com o melao seria falso; o cartao diz "more than the watermelon";'),
]


def main():
    aplicar = '--apply' in sys.argv
    with io.open(GERADOR, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    antes = len(d)

    for velho, _ in TRABALHO:
        n = d.count(velho)
        print('  ancora %-52s %d vez(es)' % (velho.split('\n')[0][:52], n))
        if n != 1:
            print('ABORTA: ancora casou %d vez(es), esperava 1.' % n)
            return 1
    for velho, novo in TRABALHO:
        d = d.replace(velho, novo, 1)

    for trecho in ('more than the watermelon', 'the pigment holds inside the band',
                   'THREE DAYS, THEN THE FRIDGE', 'cantalupo 7,86 g'):
        if trecho not in d:
            print('ABORTA: nao achei "%s" depois da troca.' % trecho)
            return 1
    for velho in ('more than the melon', 'it dies past it',
                  '1 PART FRUIT TO 4 OF KOMBUCHA'):
        if velho in d:
            print('ABORTA: sobrou o texto velho "%s".' % velho)
            return 1
    try:
        compile(d, GERADOR, 'exec')
    except SyntaxError as e:
        print('ABORTA: sintaxe invalida — %s' % e)
        return 1

    print('%s: %d -> %d bytes' % (GERADOR, antes, len(d)))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    with io.open(GERADOR, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
