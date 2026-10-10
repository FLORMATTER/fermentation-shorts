# -*- coding: utf-8 -*-
"""_registrar-beterraba-kvass.py — registra o #28 nos 2 guias.

Video novo entra em 3 lugares: a pasta (ja' esta'), o PACOTE + o PLANO. Este script
faz os dois ultimos, com TODAS as ancoras conferidas ANTES de gravar.

    python _registrar-beterraba-kvass.py            # dry-run
    python _registrar-beterraba-kvass.py --apply
"""
import io
import re
import sys

PACOTE = 'guias/pacote-legendas-descricoes-en.md'
PLANO = 'guias/plano-de-postagem.md'

ENTRADA = """
---

# 28. BEET KVASS WITH GARLIC — THE WEAKEST BRINE HERE

### Title
```
Beet kvass with garlic: the weakest brine in the book
```

**Alternatives:**
- `One teaspoon of salt per litre - and why that changes everything`
- `Why beet kvass is salted by the water, not by the beet`
- `The brine that is a third of sauerkraut's`

### Description
```
Beet kvass is beet, water, salt and a clove of garlic - and it runs on the weakest brine
in this whole series.

ONE TEASPOON PER LITRE

That is about 6 g of salt in 1 litre of water: roughly 0.6% salt. Compare it to the rest of
the jars:

- sauerkraut runs at 2% - about three times more;
- a pickle brine runs at 3.5 to 5% - about eight times more.

And look at what the percentage is measured ON. In sauerkraut the salt is a percentage of
the WEIGHT OF THE CABBAGE, and the cabbage makes its own liquid. In kvass you add the water,
so the salt is a percentage of THE WATER. "2%" means nothing until you say 2% of what.

WHY THE WEAK BRINE CHANGES EVERYTHING

A weak brine cannot defend its own surface, and that is the whole reason this jar needs a
lid more than any other in the series: keep every piece under the liquid, seal it, and burp
it once a day.

Two ways to lose the batch:

- SHRED the beet and it gives up too much sugar too fast - you get alcoholic beet beer. Dice
  it into 2 cm cubes instead, and do not peel it: the bacteria you want are on the skin.
- Let it turn VISCOUS or SLIMY and it is gone. That is not a stage, it is a failure: throw
  it out and start again.

THEN

4 to 7 days at 18-21 C. Start tasting from day three - you are waiting for a clean lactic
tartness, not for a number of days. Strain it, chill it, and refill the same jar with fresh
brine for a second batch: it ferments faster and comes out lighter in colour and flavour.

Beet is the fuel here: about 7 g of sugar per 100 g, more than any other root in this
series. Kvass stays under 1% alcohol by volume, but it is not zero, and it keeps rising
while the jar sits. Drink it fresh and keep it cold.
```

### Hashtags
```
#beetkvass #beetroot #garlic #fermentation #lactofermentation
```

File: `beterraba/shorts-beet-kvass-garlic-en.html`
**The .mp4 is already rendered:** `beterraba/shorts-beet-kvass-garlic-en.mp4`
(1080x1920 vertical, H.264, 45.2 s, constant 30 fps) - no screen recording needed.

> This is the **eighth entry with beetroot** (#3, #4, #8, #14, #19, #25, #26) and the
> **sixth with garlic** (#9, #14, #19, #22, #27). What is new is the PRODUCT: #19 is a
> pickle of wedges salted at 2% of the VEGETABLE; this one is a DRINK, salted at 0.6% of
> the WATER. Same two vegetables, opposite lesson about salt - and that is the point.
>
> ⚠️ **Ordering note.** Do not post it next to #19. Same two vegetables back to back, and a
> viewer reads it as one video split in two.
>
> ⚠️ **The percentage has a base.** The video says "0.6% of the water" and never "0.6% of
> the jar": 6 g of salt in 1 litre of water is 0.6% of the water and about 0.4% of the whole
> jar once the beet is in. Keep the base attached to the number.
"""

SEMANA_18 = """
### Semana 18 — a salmoura mais fraca do livro
| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |
|---|---|---|---|---|
| 1 | Kvass de beterraba com alho 🆕 ⚠️ | `beterraba/shorts-beet-kvass-garlic-en.html` | **#28** | `THE WEAKEST BRINE HERE` |

**Esta semana tem UM vídeo só.** As 17 semanas anteriores já estão ocupadas pelos 27 vídeos;
este abre a semana 18 sozinho. É o **oitavo** vídeo com beterraba (#3, #4, #8, #14, #19,
#25, #26) e o **sexto** com alho (#9, #14, #19, #22, #27).

O que este ensina e nenhum outro ensina: **a salmoura mais fraca da série — e que uma
porcentagem de sal não significa nada sem a BASE.** O kvass de beterraba leva **1 colher de
chá de sal por litro de água** (~6 g), ou seja **0,6% da ÁGUA**:

| Jarro | Sal | Medido em |
|---|---|---|
| Kvass (#28) | 0,6% | **na água** |
| Chucrute (#1) | 2% | no peso do repolho |
| Conserva | 3,5–5% | na água |

0,6% é **um terço** do chucrute e **um oitavo** de uma conserva a 5%. E é medido na água
porque aqui a água é **acrescentada** — no chucrute ela sai do próprio repolho.

⚠️ **A salmoura fraca é o que explica o resto.** A própria fonte diz: *"keeping oxygen out
is important since the brine is relatively low in salt"*. Traduzindo: **tampa e superfície
submersa importam mais neste jarro do que em qualquer outro da série.**

⚠️ **Os dois jeitos de perder o lote:** **ralar** a beterraba (o açúcar sai rápido demais e
vira cerveja de beterraba alcoólica) e deixar ficar **viscoso/limoso** — isso não é uma fase,
é falha: jogue fora e recomece. **Descascar também é erro:** as bactérias que você quer
estão na casca.

⚠️ **Álcool.** O kvass fica **abaixo de 1%**, mas não é zero, e continua subindo enquanto o
jarro fica parado. Beba fresco e mantenha na geladeira.

4 a 7 dias a 18–21 °C, provando do 3º dia. Depois coar, gelar e **reabastecer o mesmo
jarro** para um segundo lote — mais rápido e mais leve.

Fonte: American Homebrewers Association / *Zymurgy*, "How to Make Beet Kvass" (Amahl
Turczyn) — receita com alho e gengibre.

"""

TRABALHO = [
    # ---------------- PACOTE ----------------
    (PACOTE,
     '\n---\n\n# 📋 QUICK CHART — check before recording\n',
     ENTRADA + '\n---\n\n# 📋 QUICK CHART — check before recording\n'),
    (PACOTE,
     '| Apple + garlic + carrot ⚠️ | 2% | 6 d | `THE GARLIC COSTS 2 DAYS` |\n',
     '| Apple + garlic + carrot ⚠️ | 2% | 6 d | `THE GARLIC COSTS 2 DAYS` |\n'
     '| Beet kvass with garlic ⚠️ | 0.6% (of the water) | 4-7 d '
     '| `THE WEAKEST BRINE HERE` |\n'),
    (PACOTE,
     '| **17** | Apple + garlic + carrot |\n',
     '| **17** | Apple + garlic + carrot |\n'
     '| **18** | Beet kvass with garlic |\n'),
    (PACOTE,
     '| 27 | Apple + garlic + carrot 🆕 ⚠️ '
     '| `cenoura/shorts-apple-garlic-carrot-en.html` | ✅ |\n',
     '| 27 | Apple + garlic + carrot 🆕 ⚠️ '
     '| `cenoura/shorts-apple-garlic-carrot-en.html` | ✅ |\n'
     '| 28 | Beet kvass with garlic 🆕 ⚠️ '
     '| `beterraba/shorts-beet-kvass-garlic-en.html` | ✅ |\n'),
    (PACOTE,
     '**All 26 Shorts are already rendered',
     '**All 27 Shorts are already rendered'),
    # ---------------- PLANO ----------------
    (PLANO,
     '## ⚠️ Antes de tudo: você tem 27 vídeos, não 50 arquivos',
     '## ⚠️ Antes de tudo: você tem 28 vídeos, não 51 arquivos'),
    (PLANO,
     '## 📅 As 17 semanas',
     '## 📅 As 18 semanas'),
    (PLANO,
     '\n---\n\n## 🖊️ O `@yourchannel` — e por que ele NÃO sai no vídeo\n',
     SEMANA_18 + '---\n\n## 🖊️ O `@yourchannel` — e por que ele NÃO sai no vídeo\n'),
    # contagem de placeholders: medida no disco depois do arquivo novo existir
    (PLANO,
     'São **56 arquivos** com placeholder (30 `@yourchannel`, 20 `@seucanal`,\n'
     '6 `@yourhandle`).',
     'São **57 arquivos** com placeholder (31 `@yourchannel`, 20 `@seucanal`,\n'
     '6 `@yourhandle`).'),
]


def main():
    aplicar = '--apply' in sys.argv
    dados = {}
    for arq in (PACOTE, PLANO):
        with io.open(arq, 'r', encoding='utf-8', newline='') as fh:
            dados[arq] = fh.read()
    antes = {a: len(d) for a, d in dados.items()}

    for arq, velho, _ in TRABALHO:
        n = dados[arq].count(velho)
        print('  %-42s %-46s %d vez(es)'
              % (arq.split('/')[-1], velho.strip().split('\n')[0][:46], n))
        if n != 1:
            print('ABORTA: ancora casou %d vez(es), esperava 1.' % n)
            return 1
    for arq, velho, novo in TRABALHO:
        dados[arq] = dados[arq].replace(velho, novo, 1)

    # ---------------- conferencias ----------------
    pac, pla = dados[PACOTE], dados[PLANO]
    entradas = re.findall(r'^# (\d+)\. ', pac, re.M)
    semanas_pac = re.findall(r'^\| \*\*(\d+)\*\* \|', pac, re.M)
    semanas_pla = re.findall(r'^### Semana (\d+)', pla, re.M)
    print('  pacote: %d entradas (%s..%s) | %d semanas na tabela'
          % (len(entradas), entradas[0], entradas[-1], len(semanas_pac)))
    print('  plano : %d semanas (%s..%s)' % (len(semanas_pla),
                                              semanas_pla[0], semanas_pla[-1]))
    if entradas != [str(i) for i in range(1, 29)]:
        print('ABORTA: as entradas do pacote nao sao 1..28: %s' % entradas)
        return 1
    if [int(x) for x in semanas_pac] != list(range(1, 19)):
        print('ABORTA: as semanas do pacote nao sao 1..18: %s' % semanas_pac)
        return 1
    if [int(x) for x in semanas_pla] != list(range(1, 19)):
        print('ABORTA: as semanas do plano nao sao 1..18: %s' % semanas_pla)
        return 1
    for trecho, alvo in (('Title', pac), ('Description', pac), ('Hashtags', pac),
                         ('shorts-beet-kvass-garlic-en.html', pac),
                         ('shorts-beet-kvass-garlic-en.mp4', pac),
                         ('THE WEAKEST BRINE HERE', pac),
                         ('0.6% (of the water)', pac),
                         ('shorts-beet-kvass-garlic-en.html', pla),
                         ('THE WEAKEST BRINE HERE', pla),
                         ('**57 arquivos**', pla)):
        if trecho not in alvo:
            print('ABORTA: nao achei "%s".' % trecho)
            return 1
    bloco28 = pac.split('# 28. ')[1].split('\n---\n')[0]
    for campo in ('### Title', '### Description', '### Hashtags', 'File: '):
        if campo not in bloco28:
            print('ABORTA: a entrada #28 nao tem "%s".' % campo)
            return 1
    # a conta do video tem de fechar com o texto do pacote
    if '0.6% of the water' not in bloco28:
        print('ABORTA: a entrada #28 nao diz a BASE da porcentagem.')
        return 1

    for arq in (PACOTE, PLANO):
        print('  %-42s %d -> %d bytes' % (arq.split('/')[-1], antes[arq], len(dados[arq])))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    for arq, d in dados.items():
        with io.open(arq, 'w', encoding='utf-8', newline='') as fh:
            fh.write(d)
    print('gravado: #28 nos 2 guias.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
