# -*- coding: utf-8 -*-
"""
_registrar-beterraba-alho.py — poe o video de beterraba + alho no pacote.

Entrada nova: `beterraba/shorts-beet-garlic-en-1080x1920.html` (8 cenas, 54 s).
E' a 19a entrada do pacote.

PONTO DELICADO: esta e' a QUARTA entrada de beterraba (#3 pura, #4 com melancia,
#8 com couve). O pacote proibe repetir legume (risco de "conteudo inautentico"),
entao a nota da secao VARIANTS tem de dizer por que esta passa — e o que ela tem
de diferente (o ALHO: alicina que amarga e depois adoça, camadas em vez de
mistura). Sem isso o pacote se contradiz.
"""
import io
import sys

ARQ = 'guias/pacote-legendas-descricoes-en.md'

ENTRADA = """### Title
```
Beetroot and garlic in one jar - layer them, do not mix
```

**Alternatives:**
- `Beetroot and garlic: the jar that dyes itself purple`
- `Why you layer beetroot and garlic instead of mixing them`
- `Raw garlic burns. Two weeks in a beet jar fixes that`

### Description
```
Beetroot and garlic go in the same jar, and they change each other.

Raw garlic is harsh - the allicin burns. Two weeks in a brine and it turns sweet and
mellow. The beetroot does the other half: its colour comes from BETALAIN, that pigment
leaks out and dyes everything in the jar, garlic included. That is why a jar of beet and
garlic looks like it was painted.

The four things that matter:

- Cut the beet into WEDGES, about 2 cm, skin off. Never grate it. Grated beet turns to
  mush and the ferment goes sloppy; wedges stay crunchy.
- Peel the garlic and CRUSH each clove once, with the flat blade. A crushed clove gives
  up its oil, and that oil is the flavour. Whole cloves stay shy.
- LAYER it, do not mix it: beet, garlic, beet, garlic. Press each layer down as you go.
  Mixed, you lose the layers; layered, you can pull out exactly what you want.
- 2% salt by weight - 20 g for every 1 kg of beet and garlic. Coarse salt, NOT iodized:
  iodine slows the ferment down.

Week 1 on the counter at 18-22 C, everything under the liquid, burp the jar daily.
Week 2 in the fridge. Longer wait means deeper colour and softer garlic. It keeps for
months.

Use it on salads, burgers, eggs, soups - or straight out of the jar.

#beetroot #beets #garlic #fermentation #pickles
```

### Hashtags
```
#beetroot #beets #garlic #fermentation #pickles #lactofermentation
```

File: `beterraba/shorts-beet-garlic-en-1080x1920.html`
**The .mp4 is already rendered:** `beterraba/shorts-beet-garlic-en-1080x1920.mp4`
(1080x1920 vertical, H.264, 54.0 s, constant 29.8 fps) - no screen recording needed.

This one has **no Portuguese original** - it was built in English, already in the upload
format.

> This is the **fourth beetroot entry** (#3, #4, #8). It is here because the substance is
> the **garlic**, not the beet: garlic softening over two weeks, and layering instead of
> mixing. Spread it out - do not post it next to #3 or #8.
"""

ANCORAS = [
    (
        'entrada #19',
        '> #12 it is the obvious next question - what happens if you add sugar to a dense\n'
        '> vegetable.\n\n---\n\n# 📋 QUICK CHART — check before recording',
        '> #12 it is the obvious next question - what happens if you add sugar to a dense\n'
        '> vegetable.\n\n---\n\n' + ENTRADA + '\n---\n\n# 📋 QUICK CHART — check before recording',
    ),
    (
        'quadro rapido',
        '| Carrot + apple | 2% | 4-5 d ⚠️ | `THE APPLE MAKES IT FIZZY` |',
        '| Carrot + apple | 2% | 4-5 d ⚠️ | `THE APPLE MAKES IT FIZZY` |\n'
        '| Beetroot + garlic | 2% | 1-2 wk | `LAYER IT, DO NOT MIX IT` |',
    ),
    (
        'ordem de postagem',
        '| **10** | Carrot + apple |',
        '| **10** | Carrot + apple |\n| **11** | Beetroot + garlic |',
    ),
    (
        'tabela de arquivos',
        '| 18 | Carrot + apple ⚠️ | `cenoura/shorts-carrot-apple-en.html` | ✅ |',
        '| 18 | Carrot + apple ⚠️ | `cenoura/shorts-carrot-apple-en.html` | ✅ |\n'
        '| 19 | Beetroot + garlic ⚠️ | `beterraba/shorts-beet-garlic-en-1080x1920.html` | ✅ |',
    ),
    (
        'contagem de renderizados',
        '**17 of the 18 are already rendered.**',
        '**18 of the 19 are already rendered.**',
    ),
    (
        'nota do #19 na secao VARIANTS',
        'poste o #12 primeiro**, senão o #18 cai sem comparação e vira "a mesma cenoura duas\nvezes".',
        'poste o #12 primeiro**, senão o #18 cai sem comparação e vira "a mesma cenoura duas\n'
        'vezes".\n\n'
        '**Entrada #19 (`beterraba/shorts-beet-garlic-en-1080x1920.html`) é beterraba pela\n'
        'QUARTA vez** (#3 pura, #4 com melancia, #8 com couve). Passa porque o assunto não é\n'
        'a beterraba — é o **alho**: a alicina que arde crua e vira doce em duas semanas, e a\n'
        'regra de **camadas em vez de mistura** (beterraba, alho, beterraba, alho), que nenhum\n'
        'dos outros três toca. O que a beterraba faz aqui é tingir: a **betalaina** sai dela e\n'
        'pinta o alho de roxo. **Espalhe na grade** — não poste colado no #3 nem no #8, senão\n'
        'o feed mostra três potes de beterraba na mesma semana e o padrão fica evidente.',
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

    with io.open(ARQ + '.antes-do-19', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())
    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('\ngravado: %s (backup .antes-do-19)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())
