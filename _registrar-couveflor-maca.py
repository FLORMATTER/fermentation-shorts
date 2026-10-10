# -*- coding: utf-8 -*-
"""
_registrar-couveflor-maca.py — poe a couve-flor + maca no pacote (entrada #20).

PONTO DELICADO: ja' existe a couve-flor no #5 ("IT'S NOT 2%. IT'S 2.5%"), que
ensina floretes, quebrar com a mao, 2,5% de sal, massagem e 7-10 dias. Esta
entrada NAO repete nada disso — o assunto e' a MACA como STARTER e o enxofre
(glucosinolatos -> mirosinase -> H2S, regulado por pH). A nota da secao VARIANTS
tem de dizer isso, senao o pacote se contradiz.
"""
import io
import sys

ARQ = 'guias/pacote-legendas-descricoes-en.md'

ENTRADA = """### Title
```
Cauliflower and apple: no more sulfur smell
```

**Alternatives:**
- `Why fermented cauliflower smells like rotten eggs`
- `Cauliflower starts slow. The apple makes it start`
- `The apple is not for flavour - it is a starter`

### Description
```
Fermented cauliflower has a reputation: it smells like rotten eggs. That is not spoilage.
Cauliflower is a Brassica, and it carries glucosinolates - sulfur compounds that turn into
hydrogen sulfide once the cells are broken and the enzymes get to work. The smell is normal.
It is also avoidable.

It happens because cauliflower starts SLOW. It is 90% water, with dense cell walls and almost
no sugar, so the lactic acid bacteria take days to get a hold. That slow window is exactly
when the sulfur compounds get their chance.

That is the job of the apple. It is not there for flavour - it is a STARTER. The sugar feeds
the bacteria, so the acid arrives sooner. And acid is what switches the enzyme off: pH is the
main regulator of myrosinase, the enzyme behind the smell. Faster acid, shorter smell.

The two things people get wrong:

- Both of them FLOAT. Cauliflower florets have an irregular surface that traps little pockets
  of air, and air pockets are where the hydrogen sulfide forms. Pack it tight and weigh it
  down - with cauliflower this matters more than with almost any other vegetable.
- The jar smells worse than it tastes. That is hydrogen sulfide built up inside a sealed jar.
  Open it, let it stand for five minutes, and it leaves. What is underneath is clean and
  bright.

Cauliflower small and even, apple in thick wedges.
2.5% brine = 25 g of salt per litre. Non-iodized.
Everything under the liquid. 5 to 7 days at 18-20 C - start tasting on day 4.
Then the fridge: the cold stops the sulfur.

#cauliflower #apple #fermentation #pickles
```

### Hashtags
```
#cauliflower #apple #fermentation #pickles #fermentedvegetables #lactofermentation
```

File: `couve-flor/shorts-cauliflower-apple-en.html`
**The .mp4 is already rendered:** `couve-flor/shorts-cauliflower-apple-en.mp4`
(1080x1920 vertical, H.264, 43.8 s, constant 30 fps) - no screen recording needed.

This one has **no Portuguese original** - it was built in English.

> This is the **second cauliflower entry** (#5). It is here because the subject is the
> **apple** and the sulfur chemistry, not the 2.5% method that #5 already teaches. Post it
> **after #5**, and not in the same week - on its own it looks like the same vegetable twice.
"""

ANCORAS = [
    (
        'entrada #20',
        '> mixing. Spread it out - do not post it next to #3 or #8.\n\n---\n\n# 📋 QUICK CHART',
        '> mixing. Spread it out - do not post it next to #3 or #8.\n\n---\n\n'
        + ENTRADA + '\n---\n\n# 📋 QUICK CHART',
    ),
    (
        'quadro rapido',
        '| Beetroot + garlic | 2% | 1-2 wk | `LAYER IT, DO NOT MIX IT` |',
        '| Beetroot + garlic | 2% | 1-2 wk | `LAYER IT, DO NOT MIX IT` |\n'
        '| Cauliflower + apple | 2.5% | 5-7 d | `IT WILL NOT SMELL` |',
    ),
    (
        'ordem de postagem',
        '| **11** | Beetroot + garlic |',
        '| **11** | Beetroot + garlic |\n| **12** | Cauliflower + apple |',
    ),
    (
        'tabela de arquivos',
        '| 19 | Beetroot + garlic ⚠️ | `beterraba/shorts-beet-garlic-en-1080x1920.html` | ✅ |',
        '| 19 | Beetroot + garlic ⚠️ | `beterraba/shorts-beet-garlic-en-1080x1920.html` | ✅ |\n'
        '| 20 | Cauliflower + apple ⚠️ | `couve-flor/shorts-cauliflower-apple-en.html` | ✅ |',
    ),
    (
        'contagem de renderizados',
        '**18 of the 19 are already rendered.**',
        '**19 of the 20 are already rendered.**',
    ),
    (
        'nota do #20 na secao VARIANTS',
        'o feed mostra três potes de beterraba na mesma semana e o padrão fica evidente.',
        'o feed mostra três potes de beterraba na mesma semana e o padrão fica evidente.\n\n'
        '**Entrada #20 (`couve-flor/shorts-cauliflower-apple-en.html`) é couve-flor pela\n'
        'SEGUNDA vez** (#5). Passa porque **não repete nenhum ensinamento do #5**: lá é floretes,\n'
        'quebrar com a mão, 2,5% de sal, massagem e 7-10 dias; aqui é **a maçã como starter** e a\n'
        'química do enxofre — glucosinolatos → mirosinase → H₂S, com o **pH regulando a enzima**.\n'
        'A couve-flor só entra porque é o legume que **começa devagar**, e é esse atraso que dá a\n'
        'janela para o cheiro. **Poste depois do #5**, e em outra semana: sozinha, parece o mesmo\n'
        'legume duas vezes.',
    ),
]


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()

    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('fim de linha: %d CRLF / %d LF' % (crlf, lf))
    eol = '\r\n' if crlf else '\n'

    falhou = False
    for rotulo, velho, novo in ANCORAS:
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        q = d.count(v)
        print('%-32s casou %d vez(es)' % (rotulo, q))
        if q != 1:
            falhou = True
            continue
        d = d.replace(v, n, 1)

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    with io.open(ARQ + '.antes-do-20', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('\ngravado: %s (backup .antes-do-20)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())
