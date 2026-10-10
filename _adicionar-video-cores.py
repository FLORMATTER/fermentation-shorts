# -*- coding: utf-8 -*-
"""
_adicionar-video-cores.py — registra o video novo (3 cores) no pacote e no plano.

Video: `cores/shorts-3-colors-en.html` — alho + cebola + beterraba.
Angulo NOVO: por que cada um muda de cor, e por que o azul do alho nao e mofo.
Nao repete receita de nenhum dos tres individuais (#3, #9, #10).

8 edicoes em 3 arquivos, cada uma com contagem exata (aborta se nao casar).

Uso:
    python _adicionar-video-cores.py            # dry-run
    python _adicionar-video-cores.py --apply
"""
import io
import os
import shutil
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))

ENTRADA_14 = """# 14. 3 COLORS — GARLIC + ONION + BEETROOT

Not a re-render of anything. This is the **only video that explains the colors** —
why each of these three changes, and why the blue garlic is not mold.

> Post it **after** the three individual videos (#3 beetroot, #9 garlic honey,
> #10 red onion), or it lands without context.

### Title
```
3 ferments that change color — and why
```

**Alternatives:**
- `Why your garlic turns blue (and it is fine)`
- `Beetroot, onion, garlic: 3 colors, 3 reasons`
- `Blue garlic is not spoiled. Here is why`

### Description
```
Three ferments. Three colors. Three completely different reasons.

BEETROOT — turns deep magenta
Betalain. A pigment that dissolves in the water and dyes everything it touches:
the brine, the onion next to it, and your hands. It fades in about 2 days.

RED ONION — turns shocking pink
Anthocyanin. A pigment that reacts to acid. The more acid the ferment makes,
the brighter it gets. One slice of beet in the jar turns soft pink into magenta.

GARLIC IN HONEY — turns blue or green
This one is NOT a pigment. It is a chemical reaction: sulfur compounds from the
garlic meeting amino acids in the honey. Blue or green garlic is normal.
It is not mold. Do not throw it out.

⚠️ THE ONE COLOR THAT IS BAD
Color inside the liquid = the ferment is working.
Fuzz sitting ON TOP of the surface (green, black or orange) = throw it out.
Colored liquid is fine. Colored fluff is not.

Full recipes for all three are on the channel.

#fermentation #fermentedfoods #garlic #beetroot #redonion
```

### Hashtags
```
#fermentation #fermentedfoods #garlic #beetroot #redonion
```

---

"""

NOTA_VARIANTES = """Different substance. Not a different coat of paint.

**Entrada #14 (`cores/shorts-3-colors-en.html`) é um caso diferente: ângulo NOVO.**
Não é re-render de nada. Ela não repete receita nenhuma — pega os três vídeos que
já existem (beterraba #3, alho no mel #9, cebola roxa #10) e responde uma pergunta
que nenhum deles responde: **por que cada um muda de cor, e por que o azul do alho
não é mofo.** Pode postar sem medo de duplicar. Só poste **depois** dos três
individuais, senão o vídeo cai sem contexto."""

PLANO = [
    ('guias/pacote-legendas-descricoes-en.md', [
        # 1. a entrada nova, antes da tabela rapida
        ('# 📋 QUICK CHART — check before recording',
         ENTRADA_14 + '# 📋 QUICK CHART — check before recording'),
        # 2. linha na tabela rapida
        ('| Long-form (7 veg) | — | — | `7 VEGETABLES, 1 METHOD` |',
         '| Long-form (7 veg) | — | — | `7 VEGETABLES, 1 METHOD` |\n'
         '| 3 colors (garlic+onion+beet) | — | — | `THESE 3 TURN COLOR` |'),
        # 3. qual arquivo gravar
        ('| 13 | Long-form (7 veg) | `video-longo/player-video-longo-7-legumes-en.html` |',
         '| 13 | Long-form (7 veg) | `video-longo/player-video-longo-7-legumes-en.html` |\n'
         '| 14 | 3 colors (garlic, onion, beetroot) | `cores/shorts-3-colors-en.html` |'),
        # 4. ordem de postagem
        ('| **7** | Long-form video (7 vegetables) |',
         '| **7** | Long-form video (7 vegetables) + 3 colors (garlic, onion, beetroot) |'),
        # 5. nota nas variantes
        ('Different substance. Not a different coat of paint.', NOTA_VARIANTES),
    ]),
    ('guias/plano-de-postagem.md', [
        # 6. contagem
        ('## ⚠️ Antes de tudo: você tem 13 vídeos, não 37',
         '## ⚠️ Antes de tudo: você tem 14 vídeos, não 37'),
        # 7. semana 7, segundo video
        ('| 1 | **Vídeo longo** (7 legumes) — poste como vídeo **normal**, não Short | '
         '`video-longo/player-video-longo-7-legumes-en.html` | **#13** |',
         '| 1 | **Vídeo longo** (7 legumes) — poste como vídeo **normal**, não Short | '
         '`video-longo/player-video-longo-7-legumes-en.html` | **#13** |\n'
         '| 2 | **3 cores** (alho + cebola + beterraba) | '
         '`cores/shorts-3-colors-en.html` | **#14** |'),
    ]),
    ('README.md', [
        # 8. contagem no README
        ('| `guias/pacote-legendas-descricoes-en.md` | Títulos, descrições e hashtags '
         'dos **13 vídeos** (12 Shorts + 1 vídeo longo) |',
         '| `guias/pacote-legendas-descricoes-en.md` | Títulos, descrições e hashtags '
         'dos **14 vídeos** (13 Shorts + 1 vídeo longo) |'),
    ]),
]


def ler(p):
    bruto = io.open(p, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in bruto else '\n'
    return bruto.replace('\r\n', '\n'), nl


def gravar(p, d, nl):
    saida = d if nl == '\n' else d.replace('\n', nl)
    io.open(p, 'w', encoding='utf-8', newline='').write(saida)


def main():
    aplicar = '--apply' in sys.argv
    total = 0
    for rel, edicoes in PLANO:
        p = os.path.join(RAIZ, rel.replace('/', os.sep))
        if not os.path.exists(p):
            print('FALTA  %s' % rel)
            return 1
        d, nl = ler(p)
        antes = len(d)
        for velho, novo in edicoes:
            c = d.count(velho)
            if c != 1:
                print('ABORTOU %s\n  ancora com %d ocorrencia(s):\n  %s' % (
                    rel, c, velho[:110]))
                return 1
            d = d.replace(velho, novo, 1)
        print('%-42s %d -> %d bytes  (%d edicoes)' % (
            rel, antes, len(d), len(edicoes)))
        total += len(edicoes)
        if aplicar:
            bk = p + '.antes-do-video14'
            if not os.path.exists(bk):
                shutil.copy2(p, bk)
            gravar(p, d, nl)

    if aplicar:
        print('\nOK — %d edicoes aplicadas' % total)
    else:
        print('\nDRY-RUN — %d edicoes prontas. Rode com --apply.' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
