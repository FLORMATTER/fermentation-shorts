# -*- coding: utf-8 -*-
"""_corrigir-melao-acido.py — conserta o MULTIPLO DE ACIDEZ do short maca+melao.

O cartao da cena 3 dizia "ABOUT 1800 TIMES MORE ACID", mas os dois numeros
mostrados no proprio cartao sao **3.0** (maca) e **6.4** (melao):

    diferenca 3.4 pontos -> 10^3.4 = 2512 -> "about 2500", nao 1800.

E o subtitulo explicava a escala com "3 points is a thousand", que tambem nao
bate com 3.4 pontos. Trocado por uma frase que explica a escala sem se
comprometer com um numero que o cartao nao mostra.

O conserto vai no GERADOR (fonte da verdade), com contagem conferida: se
qualquer ancora nao casar exatamente 1 vez, aborta SEM GRAVAR.

    python _corrigir-melao-acido.py
"""
import io
import re
import sys

ALVO = '_criar-kombucha-melao.py'

TROCAS = (
    # (ancora, substituto, quantas vezes)
    ('>ABOUT 1800 TIMES MORE ACID<',
     '>ABOUT 2500 TIMES MORE ACID<', 1),
    ('>pH is a scale of ten, so 3 points is a thousand<',
     '>each pH point is ten times more acid<', 1),
)


def main():
    with io.open(ALVO, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'

    # --- 1) confere TUDO antes de escrever qualquer coisa
    for velho, novo, n in TROCAS:
        achou = d.count(velho)
        if achou != n:
            print('ERRO: ancora casou %d vez(es), esperava %d:\n  %s'
                  % (achou, n, velho[:70]))
            return 1

    # --- 2) aplica
    for velho, novo, n in TROCAS:
        d = d.replace(velho, novo, n)
        print('  ok: %s  ->  %s' % (velho[1:-1], novo[1:-1]))

    # --- 3) sanidade: os numeros que o cartao MOSTRA nao podem ter mudado
    for numero in ('>3.0<', '>6.4<'):
        if d.count(numero) < 1:
            print('ERRO: o numero %s sumiu do cartao' % numero)
            return 1
    if '1800' in d:
        print('ERRO: sobrou "1800" no gerador')
        return 1
    if eol not in d:
        print('ERRO: fim de linha sumiu')
        return 1

    try:
        compile(d, ALVO, 'exec')
    except SyntaxError as exc:
        print('ERRO: nao compila: linha %s: %s' % (exc.lineno, exc.msg))
        return 1

    with io.open(ALVO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('OK: 2 trocas | %d bytes' % len(d.encode('utf-8')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
