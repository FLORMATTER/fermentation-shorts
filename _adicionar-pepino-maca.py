"""_adicionar-pepino-maca.py — poe o video #17 (pepino + maca) nos indices.

    python _adicionar-pepino-maca.py

Padrao do projeto: cada troca precisa casar exatamente 1 vez ou o script ABORTA
sem gravar. Fim de linha detectado (os .md e .html deste projeto sao CRLF).
"""
import sys

PACOTE = 'guias/pacote-legendas-descricoes-en.md'

ENTRADA_17 = """---

# 17. CUCUMBER + APPLE — SUGAR IS NOT TANNIN

Cucumber already has its own video (#6, the 4-day one). This one does **not**
repeat it: it answers the question that video leaves open.

**Everyone drops apple into the pickle jar "to keep it crunchy". Apple is not a
tannin source.** The tannin sources that actually work are grape, oak, bay,
horseradish and cherry leaves, plus a pinch of black tea. The apple is there for
**sugar** — it makes the jar go faster and taste fruitier — and the bay leaf is
still the thing holding the crunch. Apple is a *sugar*, not a *tannin*.

> Post it **after #6 (cucumber)**. Without that one the tannin rule lands with no
> context and this video looks like it contradicts itself.

### Title
```
Apple does not keep pickles crunchy - the leaf does
```

**Alternatives:**
- `Cucumber and apple: sugar is not tannin`
- `I put apple in the pickle jar. It did not do what I expected`
- `Why your pickles still go soft (it is not the apple)`

### Description
```
Everyone says to drop apple into the pickle jar to keep it crunchy. That is not how it works.

The apple brings SUGAR. Sugar feeds the bacteria, so the jar moves faster and tastes
fruitier. That is a real job - it is just not the job people think it is.

Crunch comes from TANNIN, and tannin comes from a leaf: bay, grape, oak, horseradish,
cherry - or a pinch of black tea. No tannin, no crunch. The pectinase enzyme eats the
pectin and the cucumber turns to mush.

Cucumber to fill the jar + 1 apple, in wedges.
3% brine = 1 litre of water + 30 g of salt.
Bay leaf in. Everything under the brine.
4 to 6 days - the apple makes it go faster, so start tasting on day 3.
Then the fridge. The apple goes soft before the cucumber does.

#cucumber #apple #fermentation #pickles
```

### Hashtags
```
#cucumber #apple #fermentation #pickles #fermentedfoods #lactofermentation
```

File: `pepino/shorts-pepino-apple-en.html`
**The .mp4 is already rendered:** `pepino/shorts-pepino-apple-en.mp4`
(1080x1920 vertical, H.264, 41.8 s, constant 30 fps) - no screen recording needed.

"""

TROCAS = [
    # entrada nova, antes do QUICK CHART
    ("---\n\n# 📋 QUICK CHART — check before recording",
     ENTRADA_17 + "---\n\n# 📋 QUICK CHART — check before recording"),

    # linha no QUICK CHART
    ("| Broccoli + orange | 2.5% | 5-10 d | `IT WILL SMELL LIKE SULFUR` |",
     "| Broccoli + orange | 2.5% | 5-10 d | `IT WILL SMELL LIKE SULFUR` |\n"
     "| Cucumber + apple | 3% | 4-6 d | `SUGAR IS NOT TANNIN` |"),

    # semana 9 na ordem de postagem
    ("| **8** | Broccoli + orange |",
     "| **8** | Broccoli + orange |\n| **9** | Cucumber + apple |"),

    # tabela de qual arquivo gravar
    ("| 16 | DIY mosquito trap (side track) | `mosquito/shorts-mosquito-trap-en.html` |",
     "| 16 | DIY mosquito trap (side track) | `mosquito/shorts-mosquito-trap-en.html` |\n"
     "| 17 | Cucumber + apple | `pepino/shorts-pepino-apple-en.html` |"),
]


def main():
    d = open(PACOTE, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in d else '\n'
    print('%s: fim de linha %s' % (PACOTE, 'CRLF' if nl == '\r\n' else 'LF'))
    orig = d
    for i, (velho, novo) in enumerate(TROCAS, 1):
        v = velho.replace('\n', nl)
        nv = novo.replace('\n', nl)
        n = d.count(v)
        print('troca %d: casou %d vez(es)' % (i, n))
        if n != 1:
            print('ABORTADO: ancora %d nao e unica. Nada foi gravado.' % i)
            return 1
        d = d.replace(v, nv, 1)
    assert d != orig
    open(PACOTE, 'w', encoding='utf-8', newline='').write(d)
    print('gravado: %s (%d -> %d bytes)' % (PACOTE, len(orig), len(d)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
