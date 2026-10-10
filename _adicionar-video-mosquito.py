# -*- coding: utf-8 -*-
"""Adiciona a entrada #16 (armadilha de mosquito) ao pacote de publicacao.
   Aborta SEM GRAVAR se qualquer ancora nao casar exatamente 1 vez."""
import io, sys

ARQ = 'guias/pacote-legendas-descricoes-en.md'

ENTRADA = '''---

# 16. DIY MOSQUITO TRAP \u2014 SIDE TRACK (not fermentation)

**This is the first video outside the fermentation series.** Same visual
language, same channel, different job: it is a **seasonal, high-demand search**
("how to get rid of mosquitoes") that brings in an audience the fermentation
videos never touch \u2014 and can point them back at the series.

File: `mosquito/shorts-mosquito-trap-en.html`

### Title
```
DIY mosquito trap - bottle, water, sugar and yeast
```

**Alternatives:**
- `The 5-minute mosquito trap you already have the parts for`
- `Why yeast traps mosquitoes (it is the CO2)`
- `Stop buying mosquito traps. Use a soda bottle.`

### Description
```
A 2-liter soda bottle, a cup of warm water, 3 tablespoons of sugar and 1
teaspoon of yeast. That is the whole trap.

WHY IT WORKS
Mosquitoes do not hunt you by sight. They follow carbon dioxide - the gas you
breathe out. Yeast eating sugar makes exactly the same gas. The bottle is not
the trick. The gas is. The bottle is only the cage.

HOW TO BUILD IT
1. Cut the bottle just below the shoulder, about a third of the way down.
2. Keep both halves. Flip the top over and drop it into the bottom - the neck
   becomes a funnel. Tape the rim if it wobbles.
3. Mix 3 tbsp of sugar and 1 tsp of yeast with about a cup of warm water.
   Warm, never hot - hot water kills the yeast before it starts. Stir until
   the sugar disappears, then pour it in.
4. Paint it black, or wrap it in black tape. Dark containers catch more.

WHERE TO PUT IT
Low, in the shade, out of the rain - and near the breeding spot, which is where
the mosquitoes actually are. Not right next to where you sit.

REPLACE IT EVERY 2 WEEKS
The yeast eats all the sugar, the CO2 stops and the trap goes quiet. Bubbles =
working. Flat = dead. Rinse it, mix a fresh batch, set it back out.

THE HONEST PART
This trap catches a few. Standing water breeds hundreds. Dump the buckets, the
plant saucers, the old tires and the clogged gutters first - that is the real
fix. The bottle helps. It is not magic.

#mosquito #mosquitotrap #diy #garden #summer
```

### Hashtags
```
#mosquito #mosquitotrap #diy #garden #summer
```

'''

ANC_ENTRADA = '''### Hashtags
```
#fermentation #fermentedfoods #broccoli #orange #lactofermentation
```

---

# \U0001F4CB QUICK CHART \u2014 check before recording'''

ANC_ENTRADA_NOVO = '''### Hashtags
```
#fermentation #fermentedfoods #broccoli #orange #lactofermentation
```

''' + ENTRADA + '''---

# \U0001F4CB QUICK CHART \u2014 check before recording'''

ANC_TABELA = '''| 14 | 3 colors (garlic, onion, beetroot) | `cores/shorts-3-colors-en.html` |
| 15 | Broccoli + orange | `brocolis/shorts-broccoli-orange-en.html` |'''

ANC_TABELA_NOVO = ANC_TABELA + '''
| 16 | DIY mosquito trap (side track) | `mosquito/shorts-mosquito-trap-en.html` |'''

SUBS = [
    ('entrada #16', ANC_ENTRADA, ANC_ENTRADA_NOVO),
    ('tabela de gravacao', ANC_TABELA, ANC_TABELA_NOVO),
]

d = io.open(ARQ, encoding='utf-8', newline='').read()
crlf = '\r\n' in d
print('fim de linha: %s' % ('CRLF' if crlf else 'LF'))

falhou = False
for nome, old, new in SUBS:
    a, b = (old, new)
    if crlf:
        a, b = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
    n = d.count(a)
    print('%-22s ocorrencias: %d %s' % (nome, n, 'OK' if n == 1 else '<-- FALHOU'))
    if n != 1:
        falhou = True

if falhou:
    print('\nABORTADO: nada foi gravado.')
    sys.exit(1)

for nome, old, new in SUBS:
    a, b = (old, new)
    if crlf:
        a, b = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
    d = d.replace(a, b, 1)

io.open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('\nGRAVADO: %s' % ARQ)
