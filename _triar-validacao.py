# -*- coding: utf-8 -*-
"""Lista quais shorts o validador acusa e por que — separa bug real de falso positivo."""
import io, re

d = io.open('_validacao.txt', encoding='utf-8', errors='replace').read().splitlines()

atual, prob = None, []
res = []
for ln in d:
    s = ln.strip()
    if s.endswith('.html') and '\\' in s or s.endswith('.html') and '/' in s:
        if atual and prob:
            res.append((atual, prob))
        atual, prob = s, []
    elif '[X]' in s:
        prob.append(s.replace('[X]', '').strip())
if atual and prob:
    res.append((atual, prob))

LEVES = ('nunca usado', 'hex suspeito')
reais = []
print('arquivos com acusacao: %d\n' % len(res))
for arq, ps in res:
    pesados = [p for p in ps if not any(k in p for k in LEVES)]
    marca = 'BUG REAL' if pesados else 'so aviso'
    print('%-58s %s' % (arq, marca))
    for p in ps:
        print('      %s' % p)
    if pesados:
        reais.append((arq, pesados))

print('\n=== resumo ===')
print('bugs reais : %d' % len(reais))
for arq, ps in reais:
    print('  %s -> %s' % (arq, ps))
