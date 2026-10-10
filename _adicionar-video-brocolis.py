# -*- coding: utf-8 -*-
"""
Adiciona o video #15 (brocolis + laranja) em todos os indices do projeto.

Padrao do projeto: cada troca precisa casar exatamente N vezes ou o script
ABORTA sem gravar nada. Nunca duas edicoes no mesmo arquivo em paralelo.
"""
import io, os, shutil, sys

PACOTE  = 'guias/pacote-legendas-descricoes-en.md'
PLANO   = 'guias/plano-de-postagem.md'
README  = 'README.md'

# ─────────────────────────────────────────────────────────────────────────────
# A) guias/pacote-legendas-descricoes-en.md
# ─────────────────────────────────────────────────────────────────────────────

ENTRADA_15 = """---

# 15. BROCCOLI + ORANGE — THE SULFUR ONE

Broccoli is the **first vegetable in this series that does not make its own
brine**. Cabbage does. Beetroot does. Broccoli barely releases anything — so
here you have to add water, and salt alone will not do it.

> Post it **after** #5 (cauliflower — the 2.5% rule) and #4 (beetroot +
> watermelon — the alcohol warning). Without those two it lands without context.

### Title
```
Broccoli and orange - the one that smells like sulfur
```

**Alternatives:**
- `Fermented broccoli smells like sulfur. That is normal`
- `The only vegetable here that needs a brine`
- `Broccoli + orange: zest yes, juice no`

### Description
```
Broccoli is the one vegetable here that does NOT make its own brine.
Cabbage does. Beetroot does. Broccoli barely releases anything - so you have to
add water, and salt alone will not do it.

THE BRINE - 2.5%, not 2%
1 liter of water + 25 g of non-iodized salt. Broccoli is a brassica, like
cauliflower, and brassicas need a little more salt. Stir until it disappears.

THE CUT - 1-inch pieces, never shredded
Cut small and it turns to mush in two days. And mushy broccoli never comes back.
Keep the stems - they are the part that stays crunchy.

THE ORANGE - zest yes, juice only a little
The peel adds aroma and does not stop the ferment. The juice is sugar, and sugar
is food for yeast. Half an orange is the whole orange: the zest of half plus two
segments. More than that and the jar turns fizzy and boozy - still safe, it just
stops being a ferment.

IT WILL SMELL LIKE SULFUR - AND THAT IS NORMAL
Broccoli is a sulfur vegetable. The smell is the number one reason people throw
out a perfectly good jar. The smell fades. The crunch does not.

WHITE FILM vs FUZZ
A thin white film on top is kahm yeast. Skim it off and keep going.
Fuzzy green, black or pink - throw the jar out.

NEVER START FROM FROZEN
Freezing breaks the cells. Frozen broccoli turns to mush before the ferment
even starts.

Ready in 5 to 10 days. Start tasting on day 3. When you like it, it goes in the
fridge - that is what stops the clock. Keeps 4 to 6 months.

#fermentation #fermentedfoods #broccoli #orange #lactofermentation
```

### Hashtags
```
#fermentation #fermentedfoods #broccoli #orange #lactofermentation
```

---

# 📋 QUICK CHART — check before recording"""

NOTA_15 = """
**Entrada #15 (`brocolis/shorts-broccoli-orange-en.html`) também é ângulo NOVO.**
Brócolis não existia na série, e a laranja entra por um motivo que nenhum outro
vídeo toca: **a casca é tempero, o suco é açúcar.** Não repete receita nenhuma.
Só poste **depois** do #5 (couve-flor, a regra dos 2,5%) e do #4 (beterraba com
melancia, o aviso do álcool) — é deles que ela continua."""

EDICOES_PACOTE = [
    # A1 — a entrada nova, antes do QUICK CHART
    ("---\n\n# 📋 QUICK CHART — check before recording",
     ENTRADA_15, 1),

    # A2 — linha no QUICK CHART
    ("| 3 colors (garlic+onion+beet) | — | — | `THESE 3 TURN COLOR` |",
     "| 3 colors (garlic+onion+beet) | — | — | `THESE 3 TURN COLOR` |\n"
     "| Broccoli + orange | 2.5% | 5-10 d | `IT WILL SMELL LIKE SULFUR` |", 1),

    # A3 — ordem de postagem, semana 8
    ("| **7** | Long-form video (7 vegetables) + 3 colors (garlic, onion, beetroot) |",
     "| **7** | Long-form video (7 vegetables) + 3 colors (garlic, onion, beetroot) |\n"
     "| **8** | Broccoli + orange |", 1),

    # A4 — tabela "WHICH FILE TO RECORD"
    ("| 14 | 3 colors (garlic, onion, beetroot) | `cores/shorts-3-colors-en.html` |",
     "| 14 | 3 colors (garlic, onion, beetroot) | `cores/shorts-3-colors-en.html` |\n"
     "| 15 | Broccoli + orange | `brocolis/shorts-broccoli-orange-en.html` |", 1),

    # A5 — nota de variantes
    ("individuais, senão o vídeo cai sem contexto.",
     "individuais, senão o vídeo cai sem contexto.\n" + NOTA_15, 1),
]

# ─────────────────────────────────────────────────────────────────────────────
# B) guias/plano-de-postagem.md
# ─────────────────────────────────────────────────────────────────────────────

SEMANA_8 = """### Semana 8 — a série continua
| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |
|---|---|---|---|---|
| 1 | Brócolis + laranja | `brocolis/shorts-broccoli-orange-en.html` | **#15** | `IT WILL SMELL LIKE SULFUR` |

A partir daqui o ritmo é o mesmo: **um legume novo por post**, sempre nos mesmos
dois dias da semana. O 15º é o brócolis com laranja.

"""

EDICOES_PLANO = [
    ("## ⚠️ Antes de tudo: você tem 14 vídeos, não 37",
     "## ⚠️ Antes de tudo: você tem 15 vídeos, não 37", 1),

    ("## 📅 As 7 semanas",
     "## 📅 As 8 semanas", 1),

    ("quantidade — 2 por semana durante 7 semanas ganha de 10 numa semana e nada depois.",
     "quantidade — 2 por semana, toda semana, ganha de 10 numa semana e nada depois.", 1),

    ("| 2 | **3 cores** (alho + cebola + beterraba) | `cores/shorts-3-colors-en.html` | **#14** |\n\n"
     "⚠️ **A beterraba com melancia é a mais perigosa da série.**",
     "| 2 | **3 cores** (alho + cebola + beterraba) | `cores/shorts-3-colors-en.html` | **#14** |\n\n"
     + SEMANA_8 +
     "⚠️ **A beterraba com melancia é a mais perigosa da série.**", 1),
]

# ─────────────────────────────────────────────────────────────────────────────
# C) README.md
# ─────────────────────────────────────────────────────────────────────────────

EDICOES_README = [
    ("dos **14 vídeos** (13 Shorts + 1 vídeo longo)",
     "dos **15 vídeos** (14 Shorts + 1 vídeo longo)", 1),

    ("| `pepino/` | 1 short | |",
     "| `pepino/` | 1 short | |\n"
     "| `cores/` | 1 short | Os 3 que mudam de cor (alho + cebola + beterraba) — nº 14 |\n"
     "| `brocolis/` | 1 short | Brócolis + laranja — nº 15. O único que precisa de salmoura |", 1),
]

# ─────────────────────────────────────────────────────────────────────────────

PLANO_DE_TRABALHO = [
    (PACOTE, EDICOES_PACOTE),
    (PLANO,  EDICOES_PLANO),
    (README, EDICOES_README),
]

total = 0
for arq, edicoes in PLANO_DE_TRABALHO:
    with io.open(arq, 'r', encoding='utf-8') as f:
        d = f.read()

    antes = len(d)
    for ancora, novo, n in edicoes:
        c = d.count(ancora)
        if c != n:
            print('ABORTADO em %s — a ancora casou %d vez(es), esperava %d:' % (arq, c, n))
            print('   ' + repr(ancora[:90]))
            sys.exit(1)

    # so grava depois de TODAS as ancoras do arquivo conferirem
    for ancora, novo, n in edicoes:
        d = d.replace(ancora, novo, n)

    bk = arq + '.antes-do-video15'
    if not os.path.exists(bk):
        shutil.copy2(arq, bk)
        print('backup  ->', bk)

    with io.open(arq, 'w', encoding='utf-8', newline='') as f:
        f.write(d)

    total += len(edicoes)
    print('OK  %-42s %d trocas  (%d -> %d bytes)' % (arq, len(edicoes), antes, len(d)))

print('\nOK — %d trocas aplicadas em %d arquivos.' % (total, len(PLANO_DE_TRABALHO)))
