# -*- coding: utf-8 -*-
"""Diagnostico: aplica as edicoes em memoria e mostra o que quebrou. Nao grava nada."""
import io
import sys

sys.path.insert(0, '.')
import importlib.util

spec = importlib.util.spec_from_file_location('pm', '_patch-maca.py')
pm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pm)

with io.open(pm.ALVO, encoding='utf-8', newline='') as f:
    d = f.read()

for i, (old, new, esperado) in enumerate(pm.EDICOES, 1):
    n = d.count(old)
    if n != esperado:
        print('edicao %d: NAO CASOU (%d)' % (i, n))
        break
    d = d.replace(old, new, esperado)
    print('edicao %d aplicada' % i)

linhas = d.split('\n')
print()
print('total de linhas: %d' % len(linhas))
print('--- 225 a 250 ---')
for n in range(224, min(250, len(linhas))):
    print('%4d | %s' % (n + 1, linhas[n]))
