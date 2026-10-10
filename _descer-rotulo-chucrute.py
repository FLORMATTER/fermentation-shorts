# -*- coding: utf-8 -*-
"""Desce os 3 rotulos de topo do chucrute (EN e PT) para nao baterem no @handle.

Medido: o .wm ocupa y=44..55 e x=311..389. Os rotulos estao em y=56 e chegam
ate x=346 -> invadem 22 a 34px. Descendo para y=72 o glifo comeca em y~65,
com ~10px de folga. As ilustracoes das 3 cenas comecam em y=96..120.
"""
import shutil, sys

APLICAR = '--apply' in sys.argv

ALVOS = [
    ('repolho/shorts-chucrute-30s-en.html', [
        ('>WASH · PULL THE LEAVES · CUT 2 mm<', 'y="56"'),
        ('>10 MINUTES · WITH NO WATER ADDED<', 'y="56"'),
        ('>2% OF THE WEIGHT · NON-IODIZED SALT<', 'y="56"'),
    ]),
    ('repolho/shorts-chucrute-30s.html', [
        ('>LAVA · TIRA AS FOLHAS · CORTA 2 mm<', 'y="56"'),
        ('>10 MINUTOS · SEM ADICIONAR ÁGUA<', 'y="56"'),
        ('>2% DO PESO · SAL SEM IODO<', 'y="56"'),
    ]),
]

for arq, itens in ALVOS:
    d = open(arq, encoding='utf-8').read()
    novo = d
    for ancora, velho in itens:
        # acha o <text ...> que termina nessa ancora
        i = novo.find(ancora)
        assert i > 0, '[%s] nao achei %r' % (arq, ancora)
        ini = novo.rfind('<text', 0, i)
        assert ini > 0, '[%s] nao achei o <text> de %r' % (arq, ancora)
        tag = novo[ini:i]
        assert tag.count(velho) == 1, \
            '[%s] %r tem %d ocorrencias de %s' % (arq, ancora, tag.count(velho), velho)
        novo = novo[:ini] + tag.replace(velho, 'y="72"') + novo[i:]

    # confere que sobrou 0 em y=56 e 3 em y=72
    sobrou = novo.count('y="56" text-anchor="middle" font-size="10"')
    novos = novo.count('y="72" text-anchor="middle" font-size="10"')
    print('%-42s y=56 restantes: %d | y=72: %d | %s'
          % (arq, sobrou, novos, 'GRAVANDO' if APLICAR else 'aplicaria'))
    assert sobrou == 0 and novos == 3, 'contagem inesperada em %s' % arq

    if APLICAR:
        shutil.copy2(arq, arq + '.antes-do-rotulo')
        open(arq, 'w', encoding='utf-8').write(novo)

print()
print('pronto' if APLICAR else 'dry-run — use --apply')
