# -*- coding: utf-8 -*-
"""_registrar-pao.py — registra o video de PAO (#21) e conserta os cabecalhos 18-20.

    python _registrar-pao.py

Video novo entra em 3 lugares (regra do projeto): a pasta, `_gerar-galeria.py`
(dict ROTULO **e** lista ORDEM) e o pacote de publicacao.

Alem disso, conserta um defeito que eu mesmo introduzi antes: as entradas #18,
#19 e #20 foram para o pacote com Title/Description/Hashtags e estao nas tabelas,
mas **sem o cabecalho numerado** (`# 18. ...`) — entao o documento lia como se
fossem continuacao do #17. As entradas #1..#17 tem esse cabecalho; estas tres
nao tinham. Aqui ele entra.

Ancoras contadas, aborta SEM GRAVAR.
"""
import io
import re
import sys

PACOTE = 'guias/pacote-legendas-descricoes-en.md'
PLANO = 'guias/plano-de-postagem.md'
GALERIA = '_gerar-galeria.py'

# ---------------------------------------------------------------- cabecalhos que faltam
CABECALHOS = [
    ('#18',
     'checked against each other.\n\n---\n\n### Title',
     'checked against each other.\n\n---\n\n'
     '# 18. CARROT + APPLE — THE APPLE MAKES IT FIZZY\n\n### Title'),
    ('#19',
     '> #12 it is the obvious next question - what happens if you add sugar to a dense\n'
     '> vegetable.\n\n---\n\n### Title',
     '> #12 it is the obvious next question - what happens if you add sugar to a dense\n'
     '> vegetable.\n\n---\n\n'
     '# 19. BEETROOT + GARLIC — LAYER IT, DO NOT MIX\n\n### Title'),
    ('#20',
     '> mixing. Spread it out - do not post it next to #3 or #8.\n\n---\n\n### Title',
     '> mixing. Spread it out - do not post it next to #3 or #8.\n\n---\n\n'
     '# 20. CAULIFLOWER + APPLE — THE SMELL LIES\n\n### Title'),
]

# ---------------------------------------------------------------- entrada #21
ENTRADA_21 = """# 21. SOURDOUGH STARTER — FLOUR AND WATER

### Title
```
Sourdough starter: two microbes in one jar
```

**Alternatives:**
- `Flour and water is all it takes - here is what is happening inside`
- `Why your starter smells like vinegar (and how to change that)`
- `Warm or cold? That is what decides how sour your bread is`

### Description
```
A starter is not a recipe. It is a culture - and there are two organisms living in it.

Wild YEAST is what lifts the bread: it eats the sugars and gives off carbon dioxide, and
the gluten net traps that gas. LACTIC ACID BACTERIA are what make it sour, and they
outnumber the yeast by roughly 100 to one. The bacteria make two different acids:
lactic acid is mild and milky, acetic acid is sharp like vinegar. The ratio between the
two is the flavour of your bread.

You control that ratio with the thermometer, not with the recipe:

- 30-35 °C favours the bacteria -> milder, more lactic
- 20-24 °C favours the acetic side -> sharper, more sour

Feed it 1:1:1 - equal WEIGHT of starter, flour and water. Weight, not volume: a cup of
flour and a cup of water do not weigh the same, and the culture notices.

Ready in 5 to 10 days. The test is simple: drop a spoonful into water. If it floats, it
is holding enough gas and it is ready.

Two things that are not the same thing:

- Dark liquid on top is ALCOHOL. That is a hungry starter, not a dead one. Stir it back
  in and feed it.
- Pink or orange patches are MOULD. There is no way back from that one. Throw the whole
  jar out and start again.

Bread is the slowest thing on this channel and the only one you keep alive. Everything
else you make once and eat.
```

### Hashtags
```
#sourdough #starter #fermentation #bread #wildyeast #lactofermentation
```

File: `pao/shorts-sourdough-en.html`
**The .mp4 is already rendered:** `pao/shorts-sourdough-en.mp4`
(1080x1920 vertical, H.264, 44.4 s, constant 30 fps) - no screen recording needed.

There is also a **Portuguese original**, `pao/shorts-sourdough.html`, written at the same
time - not a later translation - so the pair can be checked against each other.

> This is the **first non-vegetable entry** in the series (#21). It is still fermentation:
> the same wild microbes, the same jar logic. Worth saying so in the description, or the
> channel reads as vegetables-only.

---

"""

TROCAS_PACOTE = [
    ('entrada #21 antes do QUICK CHART',
     '# 📋 QUICK CHART — check before recording',
     ENTRADA_21 + '# 📋 QUICK CHART — check before recording'),
    ('linha do #21 na tabela de arquivos',
     '| 20 | Cauliflower + apple ⚠️ | `couve-flor/shorts-cauliflower-apple-en.html` | ✅ |\n',
     '| 20 | Cauliflower + apple ⚠️ | `couve-flor/shorts-cauliflower-apple-en.html` | ✅ |\n'
     '| 21 | Sourdough starter 🆕 | `pao/shorts-sourdough-en.html` | ✅ |\n'),
    ('contagem de renderizados',
     '**19 of the 20 are already rendered.**',
     '**20 of the 21 are already rendered.**'),
    ('linha do pao no quick chart',
     '| Cauliflower | 2.5% | 7-10 d | `IT\'S NOT 2%. IT\'S 2.5%` |',
     '| Cauliflower | 2.5% | 7-10 d | `IT\'S NOT 2%. IT\'S 2.5%` |\n'
     '| Sourdough starter | none | 5-10 d | `FLOUR AND WATER` |'),
]

TROCAS_PLANO = [
    ('contagem de videos',
     '## ⚠️ Antes de tudo: você tem 20 vídeos, não 42 arquivos',
     '## ⚠️ Antes de tudo: você tem 21 vídeos, não 43 arquivos'),
    ('titulo das semanas',
     '## 📅 As 12 semanas',
     '## 📅 As 13 semanas'),
    ('semana 13 depois da semana 12',
     'A partir daqui o ritmo é o mesmo: **um vídeo por post**, sempre nos mesmos dois dias da\n'
     'semana. O 20º é a couve-flor com maçã — o primeiro da série que explica o CHEIRO, e não a\n'
     'receita.\n',
     'A partir daqui o ritmo é o mesmo: **um vídeo por post**, sempre nos mesmos dois dias da\n'
     'semana. O 20º é a couve-flor com maçã — o primeiro da série que explica o CHEIRO, e não a\n'
     'receita.\n'
     '\n'
     '### Semana 13 — o primeiro pão\n'
     '| Dia | Vídeo | Arquivo para abrir | Entrada no pacote | Gancho da capa |\n'
     '|---|---|---|---|---|\n'
     '| 1 | Levain (pão) 🆕 | `pao/shorts-sourdough-en.html` | **#21** | `FLOUR AND WATER` |\n'
     '\n'
     '**O primeiro vídeo da série que não é legume.** Continua sendo fermentação — os mesmos\n'
     'micróbios selvagens, o mesmo pote — mas o assunto é pão. Vale dizer isso na descrição,\n'
     'para o canal não parecer "só legumes".\n'
     '\n'
     'A substância: o levain são **duas vidas** (levedura selvagem + bactérias láticas, umas\n'
     '100 bactérias por levedura), e o que separa um pão suave de um pão ácido **não é a\n'
     'receita, é o termômetro** — 30–35 °C puxa o lático (suave), 20–24 °C puxa o acético\n'
     '(agudo). Alimentação 1:1:1 por **peso**, não por volume. Pronto em 5 a 10 dias, e o\n'
     'teste é a colher que boia.\n'
     '\n'
     '**E o único erro sem volta:** mancha rosa ou laranja é mofo — joga o pote inteiro fora.\n'
     'Líquido escuro em cima é só álcool: mistura e alimenta.\n'),
]

TROCAS_GALERIA = [
    ('rotulo da pasta pao',
     "    'rabanete': 'Rabanete',\n",
     "    'rabanete': 'Rabanete',\n    'pao': 'Pão / Levain',\n"),
    ('pao entra na ORDEM',
     "'cores', 'brocolis', 'mosquito',\n",
     "'cores', 'brocolis', 'pao', 'mosquito',\n"),
]


def aplica(arq, trocas, rotulo):
    with io.open(arq, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    eol = '\r\n' if d.count('\r\n') else '\n'
    print('\n%s (%d bytes, %s)' % (arq, len(d), 'CRLF' if eol == '\r\n' else 'LF'))
    falhou = False
    for nome, velho, novo in trocas:
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        c = d.count(v)
        if c != 1:
            print('  %-42s casou %d (esperado 1) ERRO' % (nome, c))
            falhou = True
            continue
        d = d.replace(v, n, 1)
        print('  %-42s ok' % nome)
    if falhou:
        print('  ABORTADO — %s nao foi gravado.' % rotulo)
        return None
    with io.open(arq, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('  gravado: %d bytes' % len(d))
    return d


def main():
    ok = True
    for arq, trocas, rotulo in ((PACOTE, CABECALHOS + TROCAS_PACOTE, 'pacote'),
                                (PLANO, TROCAS_PLANO, 'plano'),
                                (GALERIA, TROCAS_GALERIA, 'galeria')):
        if aplica(arq, trocas, rotulo) is None:
            ok = False
    if not ok:
        return 1

    # ---- prova: os 21 cabecalhos existem
    d = io.open(PACOTE, encoding='utf-8', newline='').read()
    nums = [int(m) for m in re.findall(r'^# (\d+)\.', d, re.M)]
    print('\ncabecalhos no pacote: %s' % nums)
    faltam = [n for n in range(1, 22) if n not in nums]
    if faltam:
        print('FALTAM: %s' % faltam)
        return 1
    print('1..21 completos')
    return 0


if __name__ == '__main__':
    sys.exit(main())
