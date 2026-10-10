# -*- coding: utf-8 -*-
"""Conserta a entrada #2 (nao e repolho roxo) e alinha o texto ao arquivo real."""
P = 'guias/pacote-legendas-descricoes-en.md'
d = open(P, encoding='utf-8').read()
orig = d


def troca(d, velho, novo, n=1):
    c = d.count(velho)
    assert c == n, 'ANCORA nao casou %d vez(es) (achei %d): %r' % (n, c, velho[:70])
    return d.replace(velho, novo)


# --------------------------------------------- 1) TROCA A SECAO #2 INTEIRA
ini = d.find('# 2. RED CABBAGE')
fim = d.find('# 3. BEETROOT')
assert ini > 0, 'nao achei o inicio da secao 2'
assert fim > ini, 'nao achei o fim da secao 2'
print('secao 2 antiga: %d bytes' % (fim - ini))

NOVA = """# 2. CABBAGE — THE TWO TRICKS

Same vegetable as video #1, different job. #1 is the recipe in 30 seconds.
This one is the two small techniques that decide whether the batch works or
turns to mush.

### Title
```
The 2 sauerkraut tricks nobody tells you
```

**Alternatives:**
- `Sauerkraut: the step almost everyone gets wrong`
- `Why your sauerkraut goes soft (2 fixes)`
- `Flip the jar. That is the trick.`

### Description
```
Two small things decide whether your sauerkraut works or goes soft.

TRICK 1 — CUT IT THIN (2 to 3 mm)
Cut too thick and the salt never reaches the middle. It stays hard on the
outside and ferments unevenly. 2 to 3 mm, every leaf.

TRICK 2 — FLIP THE JAR EVERY DAY
The brine sinks and the salt ends up sitting at the bottom. If you never flip
it, the cabbage at the top never gets the same salt as the cabbage at the
bottom. One flip a day, for the 7 days.

The base, in case you missed video #1:
2% salt · 10 minutes of massaging · press it under the liquid · 7 days

⚠️ Cabbage above the liquid = mold. Keep it all down.
⚠️ Bubbles and a sour smell = normal. That is it working.

#sauerkraut #fermentation #cabbage
```

### Hashtags
```
#sauerkraut #fermentation #cabbage #homemade #fermentedfoods
```

---

"""
d = d[:ini] + NOVA + d[fim:]

# ---------------------------------------------- 2) TABELA RAPIDA
d = troca(d, "| Red cabbage | 2% | 7 d | `THE MISTAKE THAT RUINS IT` |",
             "| Cabbage | 2% | 7 d | `FLIP THE JAR EVERY DAY` |")

# ---------------------------------------------- 3) ORDEM DE POSTAGEM
d = troca(d, "| **5** | Beetroot+kale + Red cabbage |",
             "| **5** | Beetroot+kale + Cabbage |")

# ---------------------------------------------- 4) TABELA DE VARIANTES
d = troca(d,
          "| Cabbage | `shorts-chucrute-30s`, `shorts-repolho-animado`, `shorts-repolho-maos-canva` |\n"
          "| Beetroot | `shorts-beterraba-animado`, `shorts-beterraba-svg-puro`, `shorts-beterraba-camadas` |\n"
          "| Beetroot + kale | `shorts-beterraba-camadas` (the \"inside\" view) |",
          "| Cabbage | `shorts-repolho-animado` (a 15-second version of video #1) |\n"
          "| Beetroot | `shorts-beterraba-animado`, `shorts-beterraba-camadas` |")

# ---------------------------------------------- 5) PT: o #repolhox que originou o erro
P2 = 'guias/pacote-legendas-descricoes.md'
p = open(P2, encoding='utf-8').read()
p = troca(p, "#repolhox #fermentação #chucrute", "#repolho #fermentação #chucrute")

open(P, 'w', encoding='utf-8').write(d)
open(P2, 'w', encoding='utf-8').write(p)
print('EN %d -> %d bytes' % (len(orig), len(d)))
print('PT corrigido: #repolhox -> #repolho')
