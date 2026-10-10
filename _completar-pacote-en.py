# -*- coding: utf-8 -*-
"""Completa o pacote EN: cenoura, video longo, mapa de arquivos e aviso de variantes.
Cada ancora tem que casar EXATAMENTE o numero de vezes esperado, senao nao grava nada.
"""
P = 'guias/pacote-legendas-descricoes-en.md'
d = open(P, encoding='utf-8').read()
orig = d
n_edits = 0


def troca(d, velho, novo, n=1):
    c = d.count(velho)
    assert c == n, 'ANCORA nao casou %d vez(es) (achei %d): %r' % (n, c, velho[:70])
    return d.replace(velho, novo)


# ---------------------------------------------------------------- 1) NOVAS SECOES
NOVOS = """# 12. CARROT

Carrot is the fastest of the root vegetables — and the reason is sugar.

### Title
```
Fermented carrot sticks — crunchy in 5 days 🥕
```

**Alternatives:**
- `Carrots ferment faster than cabbage. Here's why`
- `The carrot sticks that keep for months`
- `5 days, 2 ingredients, no cooking`

### Description
```
Fermented carrots. Ready in 5 to 7 days — and they stay CRUNCHY.

Carrots are full of natural sugar. Sugar is exactly what the bacteria eat.
More sugar = faster ferment. That is the whole reason carrot beats cabbage
on speed, and why it does not need the full 7 days.

📌 RECIPE
200 g carrots
4 g non-iodized salt (2% of the weight)
Cut into sticks, all the same size → massage → press down → 5 days

🚫 NO WATER. The carrot releases its own brine.
If the liquid does not cover everything, press harder — do not add water.

⚠️ Sticks poking out of the liquid = mold. Everything stays submerged.
⚠️ Bubbles + sour smell = normal. That is the ferment working.

Taste it on day 5. Then it goes in the fridge and keeps for weeks.

#fermentedcarrots #carrots #fermentation
```

### Hashtags
```
#fermentedcarrots #carrots #fermentation #pickles #guthealth
```

---

# 13. LONG-FORM VIDEO — 7 VEGETABLES

The only horizontal video. Post it as a normal upload, **not** as a Short.
It is the video that explains the whole method in one sitting — the one people
save and come back to. Pin it to your profile.

### Title
```
7 vegetables, 1 method — the complete fermentation guide
```

**Alternatives:**
- `I fermented 7 vegetables with the same 4 steps`
- `The only fermentation guide you need (7 vegetables)`
- `Fermenting 101: 7 vegetables, one method`

### Description
```
One method. Seven vegetables. Everything I learned fermenting at home,
in a single video.

THE METHOD — the same 4 steps for all 7
1. Cut thin and even
2. Weigh the salt — 2% of the vegetable's weight
3. Massage until it releases its own water
4. Press it down and keep it submerged

SALT & TIME — vegetable by vegetable
Cabbage .......... 2% ....... 7 days
Carrot ........... 2% ....... 5-7 days
Radish ........... 2% ....... 5 days
Cauliflower ...... 2.5% ..... 7-10 days
Beetroot ......... 2% ....... 9 days
Beetroot + kale .. 2% ....... 10-14 days
Garlic + honey ... none ..... 3-4 weeks

THE 3 THINGS THAT RUIN A FERMENT
❌ Vegetable above the liquid → mold
❌ Iodized salt → kills the bacteria
❌ Adding water when the vegetable makes its own

HOW TO KNOW IT IS WORKING
✅ Bubbles rising
✅ Sour, pickle-like smell
✅ Cloudy brine
❌ Fuzz, green / black / orange spots → throw it out

#fermentation #fermentedfoods #vegetables
```

### Hashtags
```
#fermentation #fermentedfoods #vegetables #pickles #homemade
```

---

"""
d = troca(d, "# 📋 QUICK CHART — check before recording",
          NOVOS + "# 📋 QUICK CHART — check before recording")
n_edits += 1

# ------------------------------------------------- 2) TABELA RAPIDA: 2 LINHAS NOVAS
d = troca(d,
          "| General guide (pillar) | — | — | `THE 5 EASIEST` |",
          "| General guide (pillar) | — | — | `THE 5 EASIEST` |\n"
          "| Carrot | 2% | 5-7 d | `CRUNCHY IN 5 DAYS` |\n"
          "| Long-form (7 veg) | — | — | `7 VEGETABLES, 1 METHOD` |")
n_edits += 1

# ------------------------------------------------------ 3) ORDEM DE POSTAGEM
d = troca(d,
          "| **6** | Beetroot+watermelon ⚠️ + Carrots |",
          "| **6** | Beetroot+watermelon ⚠️ + Carrots |\n"
          "| **7** | Long-form video (7 vegetables) |")
n_edits += 1

# ---------------------------- 4) MAPA DE ARQUIVOS + AVISO DE VARIANTES
MAPA = """# 🗂️ WHICH FILE TO RECORD — entry by entry

The titles above are the *content*. This is the *file* you open and record.
Every one of these already has an English version (the `-en` file).

| # | Entry | File to open |
|---|---|---|
| 1 | Sauerkraut (pillar) | `repolho/shorts-chucrute-30s-en.html` |
| 2 | Cabbage | `repolho/shorts-repolho-maos-canva-en.html` |
| 3 | Beetroot | `beterraba/shorts-beterraba-svg-puro-en.html` |
| 4 | Beetroot + watermelon ⚠️ | `beterraba/shorts-beterraba-melancia-en.html` |
| 5 | Cauliflower | `couve-flor/shorts-couveflor-animado-en.html` |
| 6 | Cucumber | `pepino/shorts-pepino-speed-en.html` |
| 7 | Radish | `rabanete/shorts-rabanete-animado-en.html` |
| 8 | Beetroot + kale | `beterraba/shorts-beterraba-couve-en.html` |
| 9 | Garlic honey | `alho/shorts-garlic-honey-en.html` |
| 10 | Red onion | `cebola/shorts-cebola-beterraba-en.html` |
| 11 | General guide (pillar) | `guia-geral/shorts-5-easiest-en.html` |
| 12 | Carrot | `cenoura/shorts-cenoura-animado-en.html` |
| 13 | Long-form (7 veg) | `video-longo/player-video-longo-7-legumes-en.html` |

Open it in the browser, press **▶**, let it play through once, then record.

---

# ⚠️ VARIANTS — do NOT post the same vegetable twice

You have more than one render of a few vegetables. They are the **same video
in a different visual style** — same facts, same numbers, same script.

| Vegetable | Extra renders you also have |
|---|---|
| Cabbage | `shorts-chucrute-30s`, `shorts-repolho-animado`, `shorts-repolho-maos-canva` |
| Beetroot | `shorts-beterraba-animado`, `shorts-beterraba-svg-puro`, `shorts-beterraba-camadas` |
| Beetroot + kale | `shorts-beterraba-camadas` (the "inside" view) |

**Post only ONE per vegetable in the first round.** Use the file listed in the
table above and leave the others alone for now.

**Why this matters.** YouTube's rule against *mass-produced / inauthentic
content* asks one question: does the substance actually change from one video
to the next? Three cabbage videos with the same recipe and the same numbers is
exactly the pattern that gets a channel flagged. Format may repeat — substance
may not.

**When you do use the extras later, give each one a different JOB**, not just a
different look:

- `shorts-beterraba-camadas` = "what happens inside those 7 days" → a science
  follow-up, a genuinely different angle.
- `shorts-repolho-animado` = a 15-second teaser → use it to point at the pillar
  video, not as a standalone duplicate.

Different substance. Not a different coat of paint.

---

"""
d = troca(d, "# ⚠️ BEFORE POSTING — 5-SECOND CHECKLIST",
          MAPA + "# ⚠️ BEFORE POSTING — 5-SECOND CHECKLIST")
n_edits += 1

open(P, 'w', encoding='utf-8').write(d)
print('OK — %d edicoes aplicadas' % n_edits)
print('%d -> %d bytes' % (len(orig), len(d)))
