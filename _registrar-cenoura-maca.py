# -*- coding: utf-8 -*-
"""
_registrar-cenoura-maca.py — poe o video novo no pacote de publicacao.

Entrada nova: `cenoura/shorts-carrot-apple-en.html` (cenoura + maca, 7 cenas,
42,8 s). E' o 18o do pacote.

ATENCAO ao ponto delicado: o pacote proibe postar o MESMO legume duas vezes
(risco de "conteudo inautentico"), e ja' existe a entrada #12 = cenoura pura.
Por isso o texto de entrada explica que o #18 nao e' re-render: ele responde
outra pergunta (o que a maca faz num legume DENSO). Sem isso a regra do pacote
fica contradizendo a si mesma.

Mexe em 6 lugares do arquivo, cada um com contagem exata — aborta sem gravar.
"""
import io
import sys

ARQ = 'guias/pacote-legendas-descricoes-en.md'

ENTRADA = """### Title
```
Carrot and apple: the jar that fizzes in 4 days
```

**Alternatives:**
- `The apple makes the carrot ferment in 4 days`
- `Why this jar fizzes and the plain carrot one does not`
- `Carrot and apple - and yes, it makes alcohol`

### Description
```
Carrot on its own is dense and slow. It has very little sugar, so the jar takes 5 to 7
days and barely fizzes. Put one apple in and the same jar is done in 4 to 5 days - and
it is fizzy.

The apple is doing two jobs at once. It brings SUGAR, which the bacteria eat. And the
skin carries WILD YEAST, which is what actually makes the bubbles. That is why the fizz
turns up so much earlier than it does with carrot alone.

Two things that go wrong:

- Cut the carrot THIN and the apple THICK. Carrot is dense - it needs the surface area.
  Apple goes soft fast, so keep it in chunks if you want it to still have a bite on day 4.
- The apple FLOATS. Anything sitting above the brine is where mould grows. Push it down,
  or hold it under with a small bag of brine.

Carrot to fill the jar + 1 apple, in chunks.
2% brine = 1 litre of water + 20 g of salt.
Everything under the brine. 4 to 5 days, then the fridge.

One honest note: a fruit ferment makes more alcohol than a plain vegetable one - roughly
0.5% to 2% by the time it is properly fizzy. A low-sugar sauerkraut is close to zero. If
the jar fizzes hard, it is not only CO2. Keep it cold to slow it down.

#carrot #apple #fermentation #pickles
```

### Hashtags
```
#carrot #apple #fermentation #pickles #fermentedcarrots #lactofermentation
```

File: `cenoura/shorts-carrot-apple-en.html`
**The .mp4 is already rendered:** `cenoura/shorts-carrot-apple-en.mp4`
(1080x1920 vertical, H.264, 42.8 s, constant 29.4 fps) - no screen recording needed.

This one has **no Portuguese original** - it was built in English. If the PT side is ever
added, follow the `-en` convention: PT original plus the `-en` sibling.

> Post it **after #12 (carrot)**. On its own it looks like the same video twice; after
> #12 it is the obvious next question - what happens if you add sugar to a dense
> vegetable.
"""

# --------------------------------------------------------------- ancoras
ANCORAS = [
    # 1) entrada nova, logo antes do QUICK CHART
    (
        'entrada #18',
        'checked against each other.\n\n---\n\n# 📋 QUICK CHART — check before recording',
        'checked against each other.\n\n---\n\n' + ENTRADA + '\n---\n\n# 📋 QUICK CHART — check before recording',
    ),
    # 2) linha no quadro rapido
    (
        'quadro rapido',
        '| Cucumber + apple | 3% | 4-6 d | `SUGAR IS NOT TANNIN` |',
        '| Cucumber + apple | 3% | 4-6 d | `SUGAR IS NOT TANNIN` |\n'
        '| Carrot + apple | 2% | 4-5 d ⚠️ | `THE APPLE MAKES IT FIZZY` |',
    ),
    # 3) ordem de postagem
    (
        'ordem de postagem',
        '| **9** | Cucumber + apple |',
        '| **9** | Cucumber + apple |\n| **10** | Carrot + apple |',
    ),
    # 4) tabela "qual arquivo gravar"
    (
        'tabela de arquivos',
        '| 17 | Cucumber + apple | `pepino/shorts-pepino-apple-en.html` | ✅ |',
        '| 17 | Cucumber + apple | `pepino/shorts-pepino-apple-en.html` | ✅ |\n'
        '| 18 | Carrot + apple ⚠️ | `cenoura/shorts-carrot-apple-en.html` | ✅ |',
    ),
    # 5) a contagem
    (
        'contagem de renderizados',
        '**16 of the 17 are already rendered.**',
        '**17 of the 18 are already rendered.**',
    ),
    # 6) a regra dos variantes — o #18 e' legume repetido, tem de se explicar
    (
        'nota do #18 na secao VARIANTS',
        'Só poste **depois** do #5 (couve-flor, a regra dos 2,5%) e do #4 (beterraba com\nmelancia, o aviso do álcool) — é deles que ela continua.',
        'Só poste **depois** do #5 (couve-flor, a regra dos 2,5%) e do #4 (beterraba com\n'
        'melancia, o aviso do álcool) — é deles que ela continua.\n\n'
        '**Entrada #18 (`cenoura/shorts-carrot-apple-en.html`) é legume REPETIDO — e mesmo\n'
        'assim pode postar.** A cenoura já existe no #12, então a regra "um por legume" se\n'
        'aplica. O que salva o #18 é que ele **não é o mesmo vídeo**: o #12 ensina a cenoura\n'
        'sozinha (5 a 7 dias, crocante, sem gás); o #18 responde o que muda quando entra\n'
        'açúcar — 4 a 5 dias, jarro com gás, e o aviso honesto de que fermentação de fruta\n'
        'chega a 0,5–2% de álcool. Substância diferente, não verniz novo. **Ordem obrigatória:\n'
        'poste o #12 primeiro**, senão o #18 cai sem comparação e vira "a mesma cenoura duas\n'
        'vezes".',
    ),
]


def main():
    with io.open(ARQ, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()

    crlf = d.count('\r\n')
    lf = d.count('\n') - crlf
    print('fim de linha: %d CRLF / %d LF' % (crlf, lf))
    eol = '\r\n' if crlf else '\n'

    falhou = False
    for rotulo, velho, novo in ANCORAS:
        v = velho.replace('\n', eol)
        n = novo.replace('\n', eol)
        quantos = d.count(v)
        print('%-34s casou %d vez(es)' % (rotulo, quantos))
        if quantos != 1:
            falhou = True
            continue
        d = d.replace(v, n, 1)

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1

    with io.open(ARQ + '.antes-do-18', 'w', encoding='utf-8', newline='') as fh:
        with io.open(ARQ, 'r', encoding='utf-8', newline='') as g:
            fh.write(g.read())

    with io.open(ARQ, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)

    print('\ngravado: %s (backup .antes-do-18)' % ARQ)
    return 0


if __name__ == '__main__':
    sys.exit(main())
