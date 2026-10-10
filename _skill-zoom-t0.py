# -*- coding: utf-8 -*-
"""
Insere no SKILL.md a licao do _zoom-cena.py mostrar t=0.
Edicao com contagem: se a ancora nao casar exatamente 1 vez, ABORTA SEM GRAVAR.
"""
import io, os, shutil, sys

S = os.path.expanduser('~/.workbuddy-ai/skills/shorts-svg-animado/SKILL.md')

with io.open(S, 'r', encoding='utf-8') as f:
    d = f.read()

ANTES = len(d)

ANCORA = (
    "python _zoom-cena.py <arquivo>.html 0,3,5            # v\u00e1rias, uma por PNG\n"
    "```\n"
)

NOVO = ANCORA + """
> \U0001f441\ufe0f **O `_zoom-cena.py` mostra o t=0 \u2014 e no t=0 quase nada existe.** O zoom
> congela a cena no **primeiro quadro**, e todo elemento que entra por `fadeSlide`,
> `popInSeq` ou `popInSeq ... both` **come\u00e7a com `opacity:0`**. Ou seja: no PNG do zoom
> aparece **s\u00f3 o desenho est\u00e1tico sempre-vis\u00edvel** \u2014 r\u00f3tulo, t\u00edtulo, legenda e caixa de
> nota **n\u00e3o aparecem**, e concluir "faltou o texto" \u00e9 falso positivo.
>
> Aconteceu em 23/09 no #28 (`beterraba/shorts-beet-kvass-garlic-en.html`): o zoom da cena 2
> veio **sem r\u00f3tulo e sem as tr\u00eas barras de salmoura** \u2014 o `fadeSlide` do grupo ainda n\u00e3o
> tinha come\u00e7ado. O `--final` mostrou tudo no lugar.
>
> **Regra:** o zoom serve para julgar **forma do desenho est\u00e1tico** (o frasco, o dente de
> alho, a faca). Para **texto e anota\u00e7\u00e3o**, quem manda \u00e9 o `--final` \u2014 e presen\u00e7a/contraste,
> o `--no-anim`.

"""

n = d.count(ANCORA)
if n != 1:
    print('ERRO: ancora casou %d vez(es), esperado 1. Nada gravado.' % n)
    sys.exit(1)

d = d.replace(ANCORA, NOVO)

# guarda de token sobrevivente: nada de placeholder novo pode ter ficado
import re
sobrou = sorted(set(re.findall(r'@[A-Z_]{3,}@', d)))

if len(d) <= ANTES:
    print('ERRO: arquivo nao cresceu (%d -> %d). Nada gravado.' % (ANTES, len(d)))
    sys.exit(1)

# conferir que os trechos novos estao la, um por um
for t in ['O `_zoom-cena.py` mostra o t=0', 'fadeSlide` do grupo ainda n', 'quem manda \u00e9 o `--final`']:
    if t not in d:
        print('ERRO: nao achei o trecho novo: %r. Nada gravado.' % t)
        sys.exit(1)

shutil.copy2(S, S + '.antes-do-zoom-t0')
with io.open(S, 'w', encoding='utf-8') as f:
    f.write(d)

print('OK: %d -> %d bytes (+%d)' % (ANTES, len(d), len(d) - ANTES))
print('tokens @...@ sobreviventes: %s' % (sobrou if sobrou else 'nenhum'))
