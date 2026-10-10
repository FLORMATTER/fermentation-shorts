# -*- coding: utf-8 -*-
"""_registrar-melao.py — registra o #24 (kombucha maca+melao) nos 3 lugares.

Videos novos entram em 3 lugares:
  1. a pasta                      -> ja' feito (kombucha/shorts-apple-melon-en.html)
  2. _gerar-galeria.py            -> NADA A FAZER: a galeria varre as pastas de
                                     ORDEM, entao o cartao aparece sozinho
  3. pacote + plano de postagem   -> este script

Padrao do projeto: confere TODAS as ancoras primeiro e so' escreve se todas
casarem. Assim um erro num arquivo nao deixa os outros meio-registrados.

    python _registrar-melao.py
"""
import io
import sys

PACOTE = 'guias/pacote-legendas-descricoes-en.md'
PLANO = 'guias/plano-de-postagem.md'

# ----------------------------------------------------------------- entrada #24
ENTRADA = '''# 24. APPLE + MELON KOMBUCHA — THE MELON IS NOT ACID

### Title
```
Apple and melon kombucha: the one fruit that is not acid
```

**Alternatives:**
- `Why a melon will not preserve itself (and what does it instead)`
- `Melon kombucha: 1 part melon, 4 parts kombucha`
- `The melon sits above the line - the kombucha drags it under`

### Description
```
Every fruit you have put in a jar so far was acid on its own. Apple, beetroot, cucumber -
all of them sit below pH 4.6. That number is the line: above it, the bacteria that spoil
food grow; below it, they do not.

A MELON IS NOT ACID. A melon sits at pH 6.0 to 6.7 - the same range as raw meat. On its
own it is a low-acid food, and low-acid is exactly where the wrong things grow.

So why does this work at all? Because the kombucha is already acid. Finished kombucha is
pH 2.5 to 3.5. Put the melon into that and the whole jar is pulled back under the line -
the melon never gets a chance to sit above it.

Two fruits, two jobs:

- MELON brings the flavour and almost no acid. It is the one ingredient here that is not
  protecting itself. That is why the ratio is strict: 1 part melon to 4 parts kombucha.
  Add more melon and you are back above the line.
- APPLE is the insurance. At pH 3.0 the apple is about 2,500 times more acid than the
  melon. pH is a ten-fold scale - every point is ten times more acid than the one before.

And one step you cannot skip: WASH THE RIND. The net on a melon is a set of deep grooves,
and that is where Salmonella and Listeria sit. Wash it, and use the flesh only - cut the
rind away.

Then:

- 1 to 3 days at room temperature, out of the sun.
- Melon fades fast. Drink it before the fizz goes, not after.
- Once it is ready, it goes in the fridge.
```

### Hashtags
```
#kombucha #melon #fermentation #fermenteddrinks #foodsafety
```

File: `kombucha/shorts-apple-melon-en.html`
**The .mp4 is already rendered:** `kombucha/shorts-apple-melon-en.mp4`
(1080x1920 vertical, H.264, 44.6 s, constant 30 fps) - no screen recording needed.

> This is the **second drink** and the second kombucha. What makes it new is not the fruit
> but the **pH**: melon is the only fruit in the whole series that is *not* acid on its own,
> and the only one where the **kombucha**, not the fruit, is what keeps the jar safe.
>
> ⚠️ **Food-safety note.** The "wash the rind" line is the point of the video, not filler.
> A netted melon rind is a known carrier of Salmonella and Listeria. Do not cut it.

**Spread it out.** Watermelon already appears in #4 and #23 - this is the first **cantaloupe**
in the series, and it is the **second kombucha**. Post it **weeks away from #23**, and never
in the same week: two kombuchas back to back read as the same video, even though the science
is different. The hook here is the pH, not the fruit.

---
'''

# ------------------------------------------------------------------ semana 15
SEMANA = '''### Semana 15 — o melão que não é ácido
| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |
|---|---|---|---|---|
| 1 | Kombucha de maçã com melão 🆕 | `kombucha/shorts-apple-melon-en.html` | **#24** | `THE MELON IS NOT ACID` |

**Esta semana tem um vídeo só.** O #24 é o último que está pronto — o dia 2 fica livre para
o próximo que você fizer (ou para o #13, o vídeo longo, se você já tiver gravado).

**O melão de verdade entra pela primeira vez na série** — o #4 e o #23 usam **melancia**, que
é outra coisa. E este é o **segundo kombucha**: poste **longe do #23 e em outra semana**, porque
dois kombuchas seguidos leem como o mesmo vídeo, mesmo a ciência sendo outra.

O que este ensina e nenhum outro ensina: **o melão é a única fruta da série que NÃO é ácida.**
Ele fica em **pH 6,0 a 6,7** — a mesma faixa da carne crua — ou seja, **acima da linha de 4,6**,
que é onde as bactérias ruins crescem. Quem salva o pote é o **kombucha** (pH 2,5–3,5), com a
**maçã** (pH 3,0, ~2.500× mais ácida) de reforço. E a **casca rendada** do melão é carregador
conhecido de *Salmonella* e *Listeria*: **lave a casca** — é o ponto do vídeo, não enfeite.

---
'''

# ------------------------------------------------------------------- trocas
# (arquivo, ancora, substituto, quantas vezes)
TROCAS = (
    # --- pacote: entrada nova antes do QUICK CHART
    (PACOTE,
     '# 📋 QUICK CHART — check before recording',
     ENTRADA + '\n# 📋 QUICK CHART — check before recording', 1),

    # --- pacote: linha do QUICK CHART
    (PACOTE,
     '| Watermelon + apple kombucha ⚠️ | none | 1-3 d | `SEAL IT AND IT CAN BLOW` |',
     '| Watermelon + apple kombucha ⚠️ | none | 1-3 d | `SEAL IT AND IT CAN BLOW` |\n'
     '| Apple + melon kombucha | none | 1-3 d | `THE MELON IS NOT ACID` |', 1),

    # --- pacote: ordem de postagem
    (PACOTE,
     '| **14** | Watermelon + apple kombucha ⚠️ |',
     '| **14** | Watermelon + apple kombucha ⚠️ |\n'
     '| **15** | Apple + melon kombucha |', 1),

    # --- pacote: tabela "WHICH FILE TO RECORD"
    (PACOTE,
     '| 23 | Watermelon + apple kombucha 🆕 ⚠️ | `kombucha/shorts-watermelon-apple-en.html` | ✅ |',
     '| 23 | Watermelon + apple kombucha 🆕 ⚠️ | `kombucha/shorts-watermelon-apple-en.html` | ✅ |\n'
     '| 24 | Apple + melon kombucha 🆕 ⚠️ | `kombucha/shorts-apple-melon-en.html` | ✅ |', 1),

    # --- pacote: a contagem (24 entradas - o #13, video longo = 23 Shorts)
    (PACOTE,
     '**All 23 are already rendered.**',
     '**All 23 Shorts are already rendered — every entry except #13.**', 1),

    # --- plano: a contagem do topo
    (PLANO,
     '**Os vídeos já estão prontos E gravados.** 23 dos 23 têm',
     '**Os vídeos já estão prontos E gravados.** Todos os 23 Shorts têm', 1),

    # --- plano: o aviso de "nao sao 45 arquivos" (agora sao 47)
    (PLANO,
     '## ⚠️ Antes de tudo: você tem 23 vídeos, não 45 arquivos',
     '## ⚠️ Antes de tudo: você tem 24 vídeos, não 47 arquivos', 1),

    # --- plano: numero de semanas
    (PLANO,
     '## 📅 As 14 semanas',
     '## 📅 As 15 semanas', 1),

    # --- plano: semana nova antes do @yourchannel
    (PLANO,
     '## 🖊️ O `@yourchannel` — e por que ele NÃO sai no vídeo',
     SEMANA + '\n## 🖊️ O `@yourchannel` — e por que ele NÃO sai no vídeo', 1),
)


def le(nome):
    with io.open(nome, 'r', encoding='utf-8', newline='') as fh:
        return fh.read()


def main():
    conteudo = {}
    for nome in (PACOTE, PLANO):
        conteudo[nome] = le(nome)

    # --- 1) confere TODAS as ancoras antes de escrever qualquer coisa
    problemas = []
    for nome, velho, novo, n in TROCAS:
        achou = conteudo[nome].count(velho)
        if achou != n:
            problemas.append('%s: ancora casou %d vez(es), esperava %d:\n    %s'
                             % (nome, achou, n, velho.split('\n')[0][:70]))
    if problemas:
        print('ERRO — nada foi gravado:')
        for p in problemas:
            print('  ' + p)
        return 1

    # --- 2) aplica
    for nome, velho, novo, n in TROCAS:
        conteudo[nome] = conteudo[nome].replace(velho, novo, n)

    # --- 3) sanidade: os numeros antigos nao podem sobrar
    for nome, proibido in ((PACOTE, 'All 23 are already rendered'),
                           (PLANO, '23 dos 23'),
                           (PLANO, 'você tem 23 vídeos'),
                           (PLANO, 'As 14 semanas')):
        if proibido in conteudo[nome]:
            print('ERRO: sobrou "%s" em %s' % (proibido, nome))
            return 1

    # --- 4) o pacote tem de terminar com 24 entradas, numeradas 1..24
    import re
    nums = [int(m) for m in re.findall(r'^# (\d+)\. ', conteudo[PACOTE], re.M)]
    if nums != list(range(1, 25)):
        print('ERRO: entradas do pacote = %s' % (nums or 'nenhuma'))
        return 1

    # --- 5) o plano tem de terminar com 15 semanas, numeradas 1..15
    sem = [int(m) for m in re.findall(r'^### Semana (\d+)', conteudo[PLANO], re.M)]
    if sem != list(range(1, 16)):
        print('ERRO: semanas do plano = %s' % (sem or 'nenhuma'))
        return 1

    # --- 6) grava
    for nome in (PACOTE, PLANO):
        with io.open(nome, 'w', encoding='utf-8', newline='') as fh:
            fh.write(conteudo[nome])
        print('  gravado: %s | %d bytes' % (nome, len(conteudo[nome].encode('utf-8'))))

    print('OK: #24 registrado | %d trocas | pacote 24 entradas | plano 15 semanas'
          % len(TROCAS))
    return 0


if __name__ == '__main__':
    sys.exit(main())
