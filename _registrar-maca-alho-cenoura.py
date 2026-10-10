# -*- coding: utf-8 -*-
"""_registrar-maca-alho-cenoura.py — registra o #27 nos 2 guias.

Video novo entra em 3 lugares: a pasta (ja' esta'), o PACOTE + o PLANO. Este script
faz os dois ultimos, com TODAS as ancoras conferidas ANTES de gravar.

    python _registrar-maca-alho-cenoura.py            # dry-run
    python _registrar-maca-alho-cenoura.py --apply
"""
import io
import re
import sys

PACOTE = 'guias/pacote-legendas-descricoes-en.md'
PLANO = 'guias/plano-de-postagem.md'

ENTRADA = """
---

# 27. APPLE + GARLIC + CARROT — THE GARLIC COSTS 2 DAYS

### Title
```
Apple, garlic and carrot: why the fizz arrives late
```

**Alternatives:**
- `The ingredient that fights the yeast in your jar`
- `Apple, garlic and carrot: the garlic costs you two days`
- `Why your jar sits still for two days - and then takes off`

### Description
```
Allicin is the compound that gives crushed garlic its smell, and it is not only
antibacterial. It is antifungal as well - and yeast is a fungus.

So when you put garlic into a ferment that runs on wild yeast, the garlic works against
the very thing that makes the bubbles. The apple brings sugar in the flesh and wild yeast
on its skin; the garlic slows that yeast down.

That is why this jar breaks the pattern:

- day 1 and day 2: nothing. No bubbles, no foam, no smell. The jar looks dead.
- from day 3: allicin breaks down on its own - it is unstable - the yeast recovers, and
  the ferment takes off.

The garlic does not kill the ferment, it delays it. Budget about 6 days instead of 4, and
do not throw the jar away on day 2.

THE SAFETY PART

Garlic in OIL is the classic botulism risk: no air, no acid, and Clostridium botulinum
thrives in exactly that. Garlic under BRINE is a different thing:

- 2% salt by weight, and the brine has to cover everything;
- the acid comes from the ferment itself;
- no oil in the jar.

Keep it under the brine, keep the oil out, and you are back to the risk you already
manage in every other jar.

THE CARROT

The carrot is the neutral one here. It brings sugar and its own surface yeasts and it
holds its crunch - it keeps the ferment fed without changing the story.
```

### Hashtags
```
#fermentation #garlic #apple #carrot #wildyeast
```

File: `cenoura/shorts-apple-garlic-carrot-en.html`
**The .mp4 is already rendered:** `cenoura/shorts-apple-garlic-carrot-en.mp4`
(1080x1920 vertical, H.264, 44.6 s, constant 30 fps) - no screen recording needed.

> This is the **third carrot** (#12, #18), the **fifth garlic** (#9, #14, #19, #22) and
> the **sixth apple** (#17, #18, #20, #23, #24). What is new is the subject: the
> **collision**. #18 taught that the apple makes the jar fizzy; #22 taught that allicin
> kills bacteria. This one is the two of them meeting - the same molecule that protects
> the jar is also working against its yeast.
>
> ⚠️ **Ordering note.** Post it **weeks away from #18 (carrot + apple)** and from #22
> (cucumber + garlic). The three share ingredients, and this is the only one that
> contradicts the other two on purpose.
>
> ⚠️ **It is not "garlic kills the ferment".** Allicin DELAYS the yeast, it does not
> sterilise the jar - which is why the video ends on "two more days" and not on "throw it
> away". Do not let the cover imply the jar failed.
"""

SEMANA_17 = """
### Semana 17 — o ingrediente que briga com o jarro
| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |
|---|---|---|---|---|
| 1 | Maçã com alho e cenoura 🆕 ⚠️ | `cenoura/shorts-apple-garlic-carrot-en.html` | **#27** | `THE GARLIC COSTS 2 DAYS` |

**Esta semana tem UM vídeo só.** As 16 semanas anteriores já estão ocupadas pelos 26
vídeos; este é o único que sobra, então ele abre a semana 17 sozinho. É o **terceiro**
vídeo com cenoura (#12, #18), o **quinto** com alho (#9, #14, #19, #22) e o **sexto**
com maçã (#17, #18, #20, #23, #24).

O que este ensina e nenhum outro ensina: **o alho briga com a própria levedura do jarro.**
A alicina — a molécula que dá o cheiro ao alho amassado — não é só antibacteriana, é
**antifúngica**, e **levedura é fungo**. A maçã traz açúcar na polpa e levedura na casca;
o alho **atrasa** essa levedura. Resultado: **dia 1 e dia 2 o jarro parece morto** (sem
bolha, sem espuma, sem cheiro) e **do dia 3 em diante a alicina se degrada sozinha** —
ela é instável — e a fermentação dispara.

⚠️ **Não é "o alho mata a fermentação"** — ele **atrasa**. Conte **6 dias, não 4**, e
**não jogue o jarro fora no dia 2**. É esse o gancho, e é por isso que a capa diz que o
alho *custa 2 dias* em vez de dizer que deu errado.

⚠️ **A parte de segurança.** Alho **no óleo** é o risco clássico de botulismo: sem ar,
sem ácido, e o *Clostridium botulinum* adora exatamente essa combinação. Alho **na
salmoura** é outra coisa: **2% de sal**, tudo submerso, **sem óleo** — e o ácido vem da
própria fermentação. O vídeo põe os dois lado a lado: o X vermelho no óleo, o certo na
salmoura.

"""

TRABALHO = [
    # ---------------- PACOTE ----------------
    (PACOTE,
     '\n---\n\n# 📋 QUICK CHART — check before recording\n',
     ENTRADA + '\n---\n\n# 📋 QUICK CHART — check before recording\n'),
    (PACOTE,
     '| Beetroot + watermelon kombucha ⚠️ | none | 1-3 d | `THE COLOUR IS THE CLOCK` |\n',
     '| Beetroot + watermelon kombucha ⚠️ | none | 1-3 d | `THE COLOUR IS THE CLOCK` |\n'
     '| Apple + garlic + carrot ⚠️ | 2% | 6 d | `THE GARLIC COSTS 2 DAYS` |\n'),
    (PACOTE,
     '| **16** | Beetroot and watermelon kombucha |\n',
     '| **16** | Beetroot and watermelon kombucha |\n'
     '| **17** | Apple + garlic + carrot |\n'),
    (PACOTE,
     '| 26 | Beetroot + watermelon kombucha 🆕 ⚠️ '
     '| `kombucha/shorts-beet-watermelon-en.html` | ✅ |\n',
     '| 26 | Beetroot + watermelon kombucha 🆕 ⚠️ '
     '| `kombucha/shorts-beet-watermelon-en.html` | ✅ |\n'
     '| 27 | Apple + garlic + carrot 🆕 ⚠️ '
     '| `cenoura/shorts-apple-garlic-carrot-en.html` | ✅ |\n'),
    (PACOTE,
     '**All 25 Shorts are already rendered',
     '**All 26 Shorts are already rendered'),
    # ---------------- PLANO ----------------
    (PLANO,
     '## ⚠️ Antes de tudo: você tem 26 vídeos, não 49 arquivos',
     '## ⚠️ Antes de tudo: você tem 27 vídeos, não 50 arquivos'),
    (PLANO,
     '## 📅 As 16 semanas',
     '## 📅 As 17 semanas'),
    (PLANO,
     '\n---\n\n## 🖊️ O `@yourchannel` — e por que ele NÃO sai no vídeo\n',
     SEMANA_17 + '---\n\n## 🖊️ O `@yourchannel` — e por que ele NÃO sai no vídeo\n'),
    # contagem de placeholders estava VELHA: medido no disco, nao chutado
    (PLANO,
     'São **50 arquivos** com placeholder (24 `@yourchannel`, 20 `@seucanal`,\n'
     '6 `@yourhandle`).',
     'São **56 arquivos** com placeholder (30 `@yourchannel`, 20 `@seucanal`,\n'
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
    if entradas != [str(i) for i in range(1, 28)]:
        print('ABORTA: as entradas do pacote nao sao 1..27: %s' % entradas)
        return 1
    if [int(x) for x in semanas_pac] != list(range(1, 18)):
        print('ABORTA: as semanas do pacote nao sao 1..17: %s' % semanas_pac)
        return 1
    if [int(x) for x in semanas_pla] != list(range(1, 18)):
        print('ABORTA: as semanas do plano nao sao 1..17: %s' % semanas_pla)
        return 1
    for trecho, alvo in (('Title', pac), ('Description', pac), ('Hashtags', pac),
                         ('shorts-apple-garlic-carrot-en.html', pac),
                         ('shorts-apple-garlic-carrot-en.mp4', pac),
                         ('THE GARLIC COSTS 2 DAYS', pac),
                         ('shorts-apple-garlic-carrot-en.html', pla),
                         ('THE GARLIC COSTS 2 DAYS', pla),
                         ('**56 arquivos**', pla)):
        if trecho not in alvo:
            print('ABORTA: nao achei "%s".' % trecho)
            return 1
    # a entrada #27 tem de ter os 4 blocos
    bloco27 = pac.split('# 27. ')[1].split('\n---\n')[0]
    for campo in ('### Title', '### Description', '### Hashtags', 'File: '):
        if campo not in bloco27:
            print('ABORTA: a entrada #27 nao tem "%s".' % campo)
            return 1
    # o #27 nao pode repetir o numero do #26
    if '27' in re.findall(r'^# (\d+)\. ', pac, re.M)[:-1]:
        print('ABORTA: numero 27 apareceu antes da ultima entrada.')
        return 1

    for arq in (PACOTE, PLANO):
        print('  %-42s %d -> %d bytes' % (arq.split('/')[-1], antes[arq], len(dados[arq])))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    for arq, d in dados.items():
        with io.open(arq, 'w', encoding='utf-8', newline='') as fh:
            fh.write(d)
    print('gravado: #27 nos 2 guias.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
