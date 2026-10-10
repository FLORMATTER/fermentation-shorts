# -*- coding: utf-8 -*-
"""Atualiza a entrada #16 do pacote de publicacao para o conteudo dos 6 passos
   (1,5 L / 200 ml / 50 g / 1 g) e registra que o .mp4 ja existe.
   Aborta SEM GRAVAR se qualquer ancora nao casar exatamente 1 vez."""
import io, sys

ARQ = 'guias/pacote-legendas-descricoes-en.md'

A1_OLD = "File: `mosquito/shorts-mosquito-trap-en.html`"
A1_NEW = ("File: `mosquito/shorts-mosquito-trap-en.html`\n"
          "**The .mp4 is already rendered:** `mosquito/shorts-mosquito-trap-en.mp4`\n"
          "(720x1280 vertical, H.264, 57 s, ~16 fps) - no screen recording needed for\n"
          "this one. 720p is a deliberate trade: this machine's software H.264 encoder\n"
          "tops out near 11 fps at 1080x1920, and 16 fps of real motion reads better\n"
          "than 11. Re-render at `--w=1080 --fps=12` if you want the extra sharpness\n"
          "more than the smoothness.")

A2_OLD = '''A 2-liter soda bottle, a cup of warm water, 3 tablespoons of sugar and 1
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

#mosquito #mosquitotrap #diy #garden #summer'''

A2_NEW = '''A 1.5-liter soda bottle, 200 ml of warm water, 50 g of sugar and 1 g of yeast.
That is the whole trap. Five minutes, and it costs you nothing.

WHY IT WORKS
Mosquitoes do not hunt you by sight. They follow carbon dioxide - the gas you
breathe out. Yeast eating sugar makes exactly the same gas. The bottle is not
the trick. The gas is. The bottle is only the cage.

STEP 1 - CUT THE TOP OFF
Cut about a third of the way down, right at the shoulder. A 1.5 L bottle is the
classic size. Keep both halves - nothing is thrown away, the top becomes the
funnel.

STEP 2 - 200 ml WARM WATER + 50 g SUGAR
Warm water from the tap. Mix until the sugar is gone. 50 g is about three
heaped tablespoons.

STEP 3 - COOL IT, THEN 1 g YEAST
Hot water kills the yeast, so wait until it is lukewarm. 1 g is about a quarter
of a teaspoon. Do not stir - it dissolves on its own, and stirring changes
nothing.

STEP 4 - FLIP THE TOP OVER
Push it in neck-first. The neck becomes a funnel: they fly in and cannot find
the way back out. Press it down firmly so the rim sits just under the edge of
the bottle.

STEP 5 - WRAP IT IN PAPER
A sheet of newspaper or a plastic bag. They look for dark places. Leave the top
open - dark, but never sealed. Seal it and nothing can get in.

STEP 6 - DARK CORNER, THEN WAIT
Low, in the shade, out of the rain, near where they breed. Bubbles mean it is
working. Replace it every 2 weeks: when the bubbles stop, the trap is dead.

THE PART NOBODY TELLS YOU
This trap catches a few. Standing water breeds hundreds. Dump the buckets, the
plant saucers, the old tires and the clogged gutters first - that is the real
fix. The bottle helps. It is not magic.

#mosquito #mosquitotrap #diy #garden #summer'''

SUBS = [('aviso do mp4 pronto', A1_OLD, A1_NEW),
        ('descricao dos 6 passos', A2_OLD, A2_NEW)]

d = io.open(ARQ, encoding='utf-8', newline='').read()
falhou = False
for nome, old, new in SUBS:
    n = d.count(old)
    print('%-24s ocorrencias: %d %s' % (nome, n, 'OK' if n == 1 else '<-- FALHOU'))
    if n != 1:
        falhou = True
if falhou:
    print('\nABORTADO: nada foi gravado.')
    sys.exit(1)
for nome, old, new in SUBS:
    d = d.replace(old, new, 1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('\nGRAVADO: %s' % ARQ)
