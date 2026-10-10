# -*- coding: utf-8 -*-
"""_registrar-novos-videos.py — registra os 2 videos novos nos 3 lugares.

Os dois videos:
  #22 pepino + alho    -> pepino/shorts-cucumber-garlic-en.html
  #23 kombucha melancia+maca -> kombucha/shorts-watermelon-apple-en.html

Regra do projeto: video novo entra em **3 lugares** — a pasta (ja' feito), o
`_gerar-galeria.py` (dict ROTULO **e** lista ORDEM) e o pacote de publicacao
(`guias/pacote-legendas-descricoes-en.md` + `guias/plano-de-postagem.md`).

    python _registrar-novos-videos.py

Aborta SEM GRAVAR em qualquer arquivo cuja ancora nao casar exatamente 1 vez.
"""
import io
import sys

GALERIA = '_gerar-galeria.py'
PACOTE = 'guias/pacote-legendas-descricoes-en.md'
PLANO = 'guias/plano-de-postagem.md'


# ------------------------------------------------------------------ #22 e #23
ENTRADAS = '''# 22. CUCUMBER + GARLIC — THE CLOVE TURNS BLUE

### Title
```
Cucumber with garlic: the clove turns blue
```

**Alternatives:**
- `Blue garlic is not spoiled - here is what it actually is`
- `Garlic is not only flavour. It brings the bacteria.`
- `Cucumber needs more salt than cabbage - here is why`

### Description
```
Garlic is not only a flavour here. It is a source of the culture itself.

Leuconostoc and Weissella - two lactic acid bacteria - have been isolated from garlic,
and they are the ones that get the ferment started.

But raw garlic also carries ALLICIN, and allicin is antimicrobial. It attacks bacteria
in general, and the lactic ones are not immune. What saves the ferment is that allicin
degrades on its own in about two days - it cannot hold the line.

Then the clove turns BLUE or GREEN, and this is the part that makes people throw a good
jar away. It is not mould. The lactic acid reacts with the garlic's sulfur compounds and
forms POLYPYRROLES - a pigment. It is harmless, the taste barely changes, and it is proof
that the acid arrived.

In China that colour is the point: laba garlic (labasuan) is made jade green on purpose
and eaten at New Year.

Three things to get right:

- Cucumber needs MORE salt than cabbage: 3.5 to 5% by weight of water, against 2% for
  cabbage. A cucumber is about 96% water and it is soft - a weak brine gives you a soft
  pickle.
- TRIM THE BLOSSOM END. That is the end the flower was on, and it holds enzymes that
  soften the pickle. Cut a thin slice off before it goes in the jar.
- Do not peel it and do not blanch it. You would only lose what you are trying to keep.

One detail you will notice on day one: the cucumber floats and the garlic sinks. One jar,
two directions.
```

### Hashtags
```
#cucumber #garlic #fermentation #pickles #lactofermentation
```

File: `pepino/shorts-cucumber-garlic-en.html`
**The .mp4 is already rendered:** `pepino/shorts-cucumber-garlic-en.mp4`
(1080x1920 vertical, H.264, 45.0 s, constant 30 fps) - no screen recording needed.

> This one was **built in English** - there is no Portuguese original. The subject is the
> garlic, not the cucumber: cucumber already appears in #6 (the bay leaf) and #17 (the
> apple), so this entry deliberately does not repeat either of those tricks.

---

# 23. WATERMELON + APPLE KOMBUCHA — THE BOTTLE FIGHTS BACK

### Title
```
Watermelon and apple kombucha: the bottle fights back
```

**Alternatives:**
- `Why a sealed kombucha bottle can burst (and how to stop it)`
- `Watermelon kombucha: one part juice, three parts tea`
- `Two days is enough - then it goes in the fridge`

### Description
```
This is the SECOND fermentation. The kombucha is already made - now it goes into a sealed
bottle with fruit, and everything about it changes.

A sealed bottle with live yeast in it is a pressure vessel. The yeast keeps eating the
sugar from the fruit and giving off CO2, and the CO2 has nowhere to go. That is what
carbonates the drink, and that is also what bursts bottles.

Two fruits, two jobs:

- WATERMELON is about 92% water. It brings volume and very little sugar. Use it at equal
  parts and you dilute the tea until you are drinking pink water.
- APPLE brings FRUCTOSE, the sugar yeast ferments most easily. The apple is what gets you
  carbonation fast.

So the ratio is 1 part fruit juice to 3 parts kombucha - and no more.

Leave about one inch (2.5 cm) of headspace. Too much air and the CO2 has nothing to build
in, and the bottle stays flat.

Then:

- 1 to 3 days at room temperature, out of the sun. Two is usually enough.
- Open the bottle once a day, over the sink, to release the pressure. Then close it again.
- When the bottle feels FIRM, it goes in the fridge. Cold slows the yeast down - it does
  not kill it. A bottle that is firm and still warm is a bottle that keeps building.

The test is your hand, not a timer: firm means ready.
```

### Hashtags
```
#kombucha #watermelon #fermentation #fermenteddrinks #homebrew
```

File: `kombucha/shorts-watermelon-apple-en.html`
**The .mp4 is already rendered:** `kombucha/shorts-watermelon-apple-en.mp4`
(1080x1920 vertical, H.264, 45.4 s, constant 30 fps) - no screen recording needed.

> This is the **first drink** in the series, and the first entry that is not a jar of
> vegetables at all. The subject is the **second fermentation**, not the fruit: watermelon
> already appears in #4 and apple in #18 and #20. Post it far from those three.
>
> ⚠️ **Pressure warning.** Unlike every other entry, this one can make a mess. Keep the
> "open it once a day" line in the description - it is the safety note, not filler.

---

'''

LINHA_CHART = ('| Cucumber + garlic | 3.5-5% | 5 d | `THE GARLIC TURNS BLUE` |\n'
               '| Watermelon + apple kombucha ⚠️ | none | 1-3 d | `SEAL IT AND IT CAN BLOW` |')

LINHA_ORDEM = ('| **13** | Cucumber + garlic |\n'
               '| **14** | Watermelon + apple kombucha ⚠️ |')

LINHA_TABELA = ('| 22 | Cucumber + garlic 🆕 | `pepino/shorts-cucumber-garlic-en.html` | ✅ |\n'
                '| 23 | Watermelon + apple kombucha 🆕 ⚠️ '
                '| `kombucha/shorts-watermelon-apple-en.html` | ✅ |')

SEMANAS = '''### Semana 14 — o alho que fica azul
| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |
|---|---|---|---|---|
| 1 | Pepino com alho 🆕 | `pepino/shorts-cucumber-garlic-en.html` | **#22** | `THE GARLIC TURNS BLUE` |
| 2 | Kombucha de melancia e maçã 🆕 ⚠️ | `kombucha/shorts-watermelon-apple-en.html` | **#23** | `SEAL IT AND IT CAN BLOW` |

**O pepino volta pela terceira vez** (#6 e #17) — e por isso o assunto aqui **não é o
pepino, é o alho**. O que o vídeo ensina e nenhum outro ensina: o alho **não é só sabor,
ele é fonte de bactéria lática** (Leuconostoc e Weissella foram isoladas dele), mas o
alho cru traz **alicina**, que é antimicrobiana e mata as láticas também. O que salva a
fermentação é que a **alicina se degrada sozinha em ~2 dias**. E aí o dente fica **azul
ou verde** — não é mofo, é **polipirrol** (ácido + enxofre), e é **prova de que o ácido
chegou**. Na China isso é procurado: o *laba garlic* é verde de propósito.

**O kombucha é o primeiro NÃO-legume e a primeira bebida da série.** O assunto não é a
melancia (#4) nem a maçã (#18, #20) — é a **segunda fermentação**: garrafa fechada com
levedura viva é **vaso de pressão**. Melancia é 92% água (dilui), maçã traz **frutose**
(fermenta fácil) → **1 parte de suco para 3 de kombucha**, ~2,5 cm de espaço vazio, 1 a
3 dias, **abrir todo dia sobre a pia**, e para a geladeira quando estiver **firme** —
o frio **desacelera**, não mata.

⚠️ **É a única entrada que pode fazer sujeira.** A linha "abra todo dia" é aviso de
segurança, não enfeite — **não tire**.

'''

TROCAS_GALERIA = [
    ("    'pao': 'Pão / Levain',\n",
     "    'pao': 'Pão / Levain',\n    'kombucha': 'Kombucha',\n", 1),
    ("'cores', 'brocolis', 'pao', 'mosquito',\n",
     "'cores', 'brocolis', 'pao', 'kombucha', 'mosquito',\n", 1),
]

TROCAS_PACOTE = [
    ('---\n\n# 📋 QUICK CHART — check before recording',
     '---\n\n' + ENTRADAS + '# 📋 QUICK CHART — check before recording', 1),
    ('| Cauliflower + apple | 2.5% | 5-7 d | `IT WILL NOT SMELL` |\n',
     '| Cauliflower + apple | 2.5% | 5-7 d | `IT WILL NOT SMELL` |\n'
     + LINHA_CHART + '\n', 1),
    ('| **12** | Cauliflower + apple |\n',
     '| **12** | Cauliflower + apple |\n' + LINHA_ORDEM + '\n', 1),
    ('| 21 | Sourdough starter 🆕 | `pao/shorts-sourdough-en.html` | ✅ |\n',
     '| 21 | Sourdough starter 🆕 | `pao/shorts-sourdough-en.html` | ✅ |\n'
     + LINHA_TABELA + '\n', 1),
    ('**20 of the 21 are already rendered.**',
     '**All 23 are already rendered.**', 1),
]

TROCAS_PLANO = [
    ('**Os vídeos já estão prontos E gravados.** 20 dos 21 têm `.mp4` renderizado',
     '**Os vídeos já estão prontos E gravados.** 23 dos 23 têm `.mp4` renderizado', 1),
    ('## ⚠️ Antes de tudo: você tem 21 vídeos, não 43 arquivos',
     '## ⚠️ Antes de tudo: você tem 23 vídeos, não 45 arquivos', 1),
    ('## 📅 As 13 semanas', '## 📅 As 15 semanas', 1),
    ('⚠️ **A beterraba com melancia é a mais perigosa da série.**',
     SEMANAS + '⚠️ **A beterraba com melancia é a mais perigosa da série.**', 1),
]


def prepara(caminho, trocas):
    """Le, confere TODAS as ancoras e devolve o texto novo (ou None se falhar).

    NAO grava: a gravacao acontece so' depois que os TRES arquivos passarem. Se
    gravasse aqui, uma falha no pacote deixaria a galeria ja' alterada — metade
    do registro feito.
    """
    with io.open(caminho, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    antes = len(d.encode('utf-8'))
    d2 = d
    for velho, novo, esperado in trocas:
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        c = d2.count(v)
        if c != esperado:
            print('ERRO em %s: ancora casou %d (esperado %d): %r'
                  % (caminho, c, esperado, velho[:60]))
            return None
        d2 = d2.replace(v, n)
    return caminho, d2, antes, eol


def main():
    prontos = []
    for caminho, trocas in ((GALERIA, TROCAS_GALERIA),
                            (PACOTE, TROCAS_PACOTE),
                            (PLANO, TROCAS_PLANO)):
        p = prepara(caminho, trocas)
        if p is None:
            print('NADA FOI GRAVADO.')
            return 1
        prontos.append(p)

    for caminho, d2, antes, eol in prontos:
        with io.open(caminho, 'w', encoding='utf-8', newline='') as fh:
            fh.write(d2)
        print('  ok: %s  %d -> %d bytes' % (caminho, antes, len(d2.encode('utf-8'))))
    print('OK: os 3 lugares registrados.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
