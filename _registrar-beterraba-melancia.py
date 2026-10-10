# -*- coding: utf-8 -*-
"""_registrar-beterraba-melancia.py — registra o #26 nos 2 guias.

Vídeo novo entra em 3 lugares: a pasta (ja' esta'), o PACOTE + o PLANO. Este script
faz os dois ultimos, com TODAS as ancoras conferidas ANTES de gravar.

    python _registrar-beterraba-melancia.py            # dry-run
    python _registrar-beterraba-melancia.py --apply
"""
import io
import re
import sys

PACOTE = 'guias/pacote-legendas-descricoes-en.md'
PLANO = 'guias/plano-de-postagem.md'

ENTRADA = """
---

# 26. BEETROOT + WATERMELON KOMBUCHA — THE COLOUR IS THE CLOCK

### Title
```
Beetroot and watermelon kombucha: the colour tells you when to stop
```

**Alternatives:**
- `Why beetroot keeps its red in kombucha - and loses it if you push too far`
- `The pH window where beetroot holds its colour: 3 to 6`
- `Beetroot and watermelon kombucha: read the jar, not the clock`

### Description
```
Beetroot's red is a pigment called betalain, and betalain is only stable between pH 3 and
6. Outside that window it breaks down - above 6 and below 3 the colour turns dull and
brick-brown.

That matters because kombucha finishes its first ferment at pH 2.5 to 3.5. The jar lands
INSIDE the window, so the red holds. Push the ferment further and the colour is the first
thing to go - which makes the jar itself a status light:

- vivid magenta = you are inside the window and the pigment is intact;
- dull brick = you went past it, and no amount of sugar brings the red back.

Betalain is also sensitive to LIGHT, HEAT and oxygen, so the second ferment belongs in a
cupboard, not on a windowsill.

The two fruits do different jobs:

- WATERMELON is about 92% water and sits at pH 5.2, so it dilutes the mix instead of
  acidifying it. It brings sugar and aroma - and it fades fast.
- BEETROOT brings about 7 g of sugar per 100 g (watermelon carries about 6.2 g) plus the
  pigment that makes the jar worth looking at. Cut it thin.

Then:

- 1 part fruit to 4 parts finished kombucha. More fruit is not more flavour - it is a
  faster, sweeter ferment you have to babysit.
- 3 days at room temperature, then the fridge. Cold slows the ferment and holds the colour.
- Do not heat it. Heat is the fastest way to lose the red.
- A second ferment is NOT alcohol-free. It makes a small amount, and it keeps growing while
  the bottle sits. Drink it fresh and keep it cold.
```

### Hashtags
```
#kombucha #beetroot #watermelon #fermentation #secondferment
```

File: `kombucha/shorts-beet-watermelon-en.html`
**The .mp4 is already rendered:** `kombucha/shorts-beet-watermelon-en.mp4`
(1080x1920 vertical, H.264, 44.4 s, constant 30 fps) - no screen recording needed.

> This is the **seventh beetroot** in the series (#3, #4, #8, #14, #19, #25), the **third
> kombucha** (#23, #24) and the **third watermelon** (#4, #23). What is new is the subject:
> the pigment has a pH window, and the kombucha lands inside it.
>
> ⚠️ **Ordering note.** Post it **alone in its week**, weeks away from the other beetroot
> videos and the other kombuchas. Seven beetroot videos read as a production line even when
> the science is different - which is exactly the pattern YouTube's "inauthentic content"
> rule is looking for.
>
> ⚠️ **Not a pH indicator.** Betalain is stable inside 3-6; it does not turn blue like the
> anthocyanin in red cabbage. What it does is FADE once you leave the window. The video
> says "the colour tells you where you are", not "the colour changes with pH".
"""

SEMANA_16 = """
### Semana 16 — a cor que diz onde você está
| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |
|---|---|---|---|---|
| 1 | Kombucha de beterraba com melancia 🆕 | `kombucha/shorts-beet-watermelon-en.html` | **#26** | `THE COLOUR IS THE CLOCK` |

**Esta semana tem UM vídeo só — de propósito.** É o **sétimo** vídeo com beterraba (#3,
#4, #8, #14, #19, #25) e o **terceiro** kombucha (#23, #24). Dois vídeos assim na mesma
semana é exatamente o padrão que a regra de "conteúdo inautêntico" procura: deixe esta
sozinha e afaste-a dos outros de beterraba e dos outros kombuchas.

O que este ensina e nenhum outro ensina: **a cor da beterraba tem uma JANELA de pH.** A
betalaina (betanina) só é estável **entre pH 3 e 6**; fora disso ela degrada e a cor vira
tijolo. E o kombucha termina a primeira fermentação em **pH 2,5 a 3,5** — ou seja, **cai
dentro da janela**, e é por isso que o vermelho segura. O jarro vira um **sinalizador**:
magenta vivo = dentro; tijolo = passou do ponto. A betalaina também é sensível a **luz,
calor e oxigênio** — a segunda fermentação vai no armário, não na janela.

⚠️ **Isto NÃO é dizer que a betalaina é indicador de pH** (como a antocianina do repolho
roxo, que vira azul). Dentro de 3–6 a cor fica estável; o que ela faz é **desbotar** quando
passa da janela.

Açúcar (USDA): beterraba **6,76 g/100 g**, melancia **6,2 g**, melão cantalupo **7,86 g** —
a beterraba ganha da melancia, mas **perde do melão do #24**. A comparação honesta é com a
melancia, que é a outra fruta deste vídeo.

"""

TRABALHO = [
    # ---------------- PACOTE ----------------
    (PACOTE,
     '\n---\n\n# 📋 QUICK CHART — check before recording\n',
     ENTRADA + '\n---\n\n# 📋 QUICK CHART — check before recording\n'),
    (PACOTE,
     '| Beetroot + carrot | 2% | 5-7 d | `THE CARROT SAVES THE RED` |\n',
     '| Beetroot + carrot | 2% | 5-7 d | `THE CARROT SAVES THE RED` |\n'
     '| Beetroot + watermelon kombucha ⚠️ | none | 1-3 d | `THE COLOUR IS THE CLOCK` |\n'),
    (PACOTE,
     '| **15** | Apple + melon kombucha + Beetroot and carrot |\n',
     '| **15** | Apple + melon kombucha + Beetroot and carrot |\n'
     '| **16** | Beetroot and watermelon kombucha |\n'),
    (PACOTE,
     '| 25 | Beetroot + carrot 🆕 | `beterraba/shorts-beet-carrot-en.html` | ✅ |\n',
     '| 25 | Beetroot + carrot 🆕 | `beterraba/shorts-beet-carrot-en.html` | ✅ |\n'
     '| 26 | Beetroot + watermelon kombucha 🆕 ⚠️ '
     '| `kombucha/shorts-beet-watermelon-en.html` | ✅ |\n'),
    (PACOTE,
     '**All 24 Shorts are already rendered — every entry except #13.**',
     '**All 25 Shorts are already rendered — every entry except #13.**'),
    # ---------------- PLANO ----------------
    (PLANO,
     '## ⚠️ Antes de tudo: você tem 25 vídeos, não 48 arquivos',
     '## ⚠️ Antes de tudo: você tem 26 vídeos, não 49 arquivos'),
    (PLANO,
     '## 📅 As 15 semanas',
     '## 📅 As 16 semanas'),
    (PLANO,
     '\n---\n\n## 🖊️ O `@yourchannel` — e por que ele NÃO sai no vídeo\n',
     SEMANA_16 + '---\n\n## 🖊️ O `@yourchannel` — e por que ele NÃO sai no vídeo\n'),
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
    if entradas != [str(i) for i in range(1, 27)]:
        print('ABORTA: as entradas do pacote nao sao 1..26: %s' % entradas)
        return 1
    if [int(x) for x in semanas_pac] != list(range(1, 17)):
        print('ABORTA: as semanas do pacote nao sao 1..16: %s' % semanas_pac)
        return 1
    if [int(x) for x in semanas_pla] != list(range(1, 17)):
        print('ABORTA: as semanas do plano nao sao 1..16: %s' % semanas_pla)
        return 1
    for trecho, alvo in (('Title', pac), ('Description', pac), ('Hashtags', pac),
                         ('shorts-beet-watermelon-en.html', pac),
                         ('shorts-beet-watermelon-en.mp4', pac),
                         ('THE COLOUR IS THE CLOCK', pac),
                         ('shorts-beet-watermelon-en.html', pla)):
        if trecho not in alvo:
            print('ABORTA: nao achei "%s".' % trecho)
            return 1
    # a entrada #26 tem de ter os 4 blocos
    bloco26 = pac.split('# 26. ')[1].split('\n---\n')[0]
    for campo in ('### Title', '### Description', '### Hashtags', 'File: '):
        if campo not in bloco26:
            print('ABORTA: a entrada #26 nao tem "%s".' % campo)
            return 1

    for arq in (PACOTE, PLANO):
        print('  %-42s %d -> %d bytes' % (arq.split('/')[-1], antes[arq], len(dados[arq])))
    if not aplicar:
        print('(dry-run — use --apply)')
        return 0
    for arq, d in dados.items():
        with io.open(arq, 'w', encoding='utf-8', newline='') as fh:
            fh.write(d)
    print('gravado: #26 nos 2 guias.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
