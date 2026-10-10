# -*- coding: utf-8 -*-
"""_inverter-dicionario.py — o dicionario PT->EN serve para voltar?

    python _inverter-dicionario.py

Por que: o #18, #19 e #20 nasceram em INGLES e precisam do original PT. Reescrever
617 frases a mao seria refazer um trabalho que ja' existe — mas inverter o
dicionario so' e' seguro onde o par e' 1:1.

O problema: 'Couve' -> 'Cabbage' e 'Repolho' -> 'Cabbage'. Invertendo, 'Cabbage'
volta como UMA das duas, e escolher errado poe "Couve" onde era "Repolho".

Este script NAO traduz nada. Ele so' MEDE:
  1. quantos pares sao 1:1 (seguros);
  2. quais EN colidem com 2+ PT (ambiguos, precisam de decisao);
  3. quais PT colidem com 2+ EN (o mesmo PT traduzido de duas formas — na volta
     nao ha' como saber qual usar).
Depois disso a traducao e' feita por ancora explicita, contada, abortando sem gravar.
"""
import io
import re
import sys
from collections import defaultdict

ARQ_DIC = '_dicionario-pt-en.py'


def carrega():
    ns = {}
    src = io.open(ARQ_DIC, encoding='utf-8', newline='').read()
    exec(compile(src, ARQ_DIC, 'exec'), ns)
    return ns['DIC']


def main():
    dic = carrega()
    print('pares no dicionario: %d' % len(dic))

    # --- 1. PT repetido (o mesmo PT com 2+ traducoes)
    por_pt = defaultdict(list)
    for pt, en in dic:
        por_pt[pt].append(en)
    dup_pt = {k: v for k, v in por_pt.items() if len(v) > 1}

    # --- 2. EN repetido (o mesmo EN vindo de 2+ PT) -> ambiguo na volta
    por_en = defaultdict(list)
    for pt, en in dic:
        por_en[en].append(pt)
    dup_en = {k: v for k, v in por_en.items() if len(v) > 1}

    print('\nPT com mais de uma traducao: %d' % len(dup_pt))
    for k, v in sorted(dup_pt.items()):
        print('   %-40s -> %s' % (k[:40], ' | '.join(v)))

    print('\nEN ambiguo na volta (2+ PT): %d' % len(dup_en))
    for k, v in sorted(dup_en.items(), key=lambda x: -len(x[1])):
        print('   %-40s <- %s' % (k[:40], ' | '.join(v)))

    seguros = len(dic) - sum(len(v) for v in dup_en.values())
    print('\n1:1 seguros: %d de %d' % (seguros, len(dic)))
    print('ambiguos   : %d' % sum(len(v) for v in dup_en.values()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
