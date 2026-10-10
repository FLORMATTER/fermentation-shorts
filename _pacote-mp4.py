"""_pacote-mp4.py — o pacote de publicacao passa a dizer quais videos JA' tem .mp4.

Antes so' 3 entradas (#4, #16, #17) tinham a nota. Agora sao 9. E a tabela de
arquivos ganhou a coluna do .mp4, para nao ter que ler 17 secoes para descobrir
o que falta gravar.

Oito ancoras contadas. Aborta sem gravar se alguma nao casar uma vez.
"""
import sys

ARQ = 'guias/pacote-legendas-descricoes-en.md'
d = open(ARQ, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in d else '\n'
print('%s: fim de linha %s' % (ARQ, 'CRLF' if nl == '\r\n' else 'LF'))
orig = d


def nota(caminho, seg, fps, minutos=None):
    return ('File: `%s.html`\n'
            '**The .mp4 is already rendered:** `%s.mp4`\n'
            '(1080x1920 vertical, H.264, %s s, constant %s fps) - no screen recording needed.\n'
            '\n' % (caminho, caminho, seg, fps))


TROCAS = [
    ('# 6. CUCUMBER\n\n',
     '# 6. CUCUMBER\n\n' + nota('pepino/shorts-pepino-speed-en', '20.8', '30')),
    ('# 9. GARLIC HONEY\n\n',
     '# 9. GARLIC HONEY\n\n' + nota('alho/shorts-garlic-honey-en', '52.5', '29.5')),
    ('# 10. RED ONION\n\n',
     '# 10. RED ONION\n\n' + nota('cebola/shorts-cebola-beterraba-en', '53.5', '29.9')),
    ('# 12. CARROT\n\n',
     '# 12. CARROT\n\n' + nota('cenoura/shorts-cenoura-animado-en', '32.6', '29.8')),
    ('# 15. BROCCOLI + ORANGE — THE SULFUR ONE\n\n',
     '# 15. BROCCOLI + ORANGE — THE SULFUR ONE\n\n'
     + nota('brocolis/shorts-broccoli-orange-en', '53.0', '29.8')),

    # --- o comando do #16 era o antigo (dois passos)
    ("""```
node _gerar-mp4.js --w=1080 --fps=30 --kbps=3000 --cfr=1 --passo=150 mosquito/shorts-mosquito-trap-en.html
python _mp4/retimar.py mosquito/shorts-mosquito-trap-en.mp4 --fps=30 --quadros=<frames> --bruto
```

The `--cfr=1 --passo=150` pair is what keeps the motion continuous. Without
the pacing, MediaRecorder silently discards about a quarter of the frames
and the animation stutters.
""",
     """```
node _gerar-mp4.js --w=1080 --fps=30 --kbps=3000 --cfr=1 mosquito/shorts-mosquito-trap-en.html
```

One command only: the driver retimes the file and checks the duration itself
(it refuses to keep the file if the duration is off by more than 0.05 s).

`--cfr=1` plus the built-in pacing is what keeps the motion continuous. Without
the pacing, MediaRecorder silently discards about a quarter of the frames and
the animation stutters.
"""),

    # --- a nota do #17 ganha o irmao PT
    ("""File: `pepino/shorts-pepino-apple-en.html`
**The .mp4 is already rendered:** `pepino/shorts-pepino-apple-en.mp4`
(1080x1920 vertical, H.264, 41.8 s, constant 30 fps) - no screen recording needed.
""",
     """File: `pepino/shorts-pepino-apple-en.html`
**The .mp4 is already rendered:** `pepino/shorts-pepino-apple-en.mp4`
(1080x1920 vertical, H.264, 41.8 s, constant 30 fps) - no screen recording needed.

There is also a **Portuguese original**, `pepino/shorts-pepino-apple.html`. The series
convention is a PT original plus an `-en` sibling; this one was built EN-only, so the
PT side was added later. It is not part of this package - it exists so the pair can be
checked against each other.
"""),

    # --- tabela de arquivos com a coluna do mp4
    ("""| # | Entry | File to open |
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
| 14 | 3 colors (garlic, onion, beetroot) | `cores/shorts-3-colors-en.html` |
| 15 | Broccoli + orange | `brocolis/shorts-broccoli-orange-en.html` |
| 16 | DIY mosquito trap (side track) | `mosquito/shorts-mosquito-trap-en.html` |
| 17 | Cucumber + apple | `pepino/shorts-pepino-apple-en.html` |

Open it in the browser, press **▶**, let it play through once, then record.
""",
     """| # | Entry | File to open | .mp4 |
|---|---|---|---|
| 1 | Sauerkraut (pillar) | `repolho/shorts-chucrute-30s-en.html` | - |
| 2 | Cabbage | `repolho/shorts-repolho-maos-canva-en.html` | - |
| 3 | Beetroot | `beterraba/shorts-beterraba-svg-puro-en.html` | - |
| 4 | Beetroot + watermelon ⚠️ | `beterraba/shorts-beterraba-melancia-en.html` | ✅ |
| 5 | Cauliflower | `couve-flor/shorts-couveflor-animado-en.html` | - |
| 6 | Cucumber | `pepino/shorts-pepino-speed-en.html` | ✅ |
| 7 | Radish | `rabanete/shorts-rabanete-animado-en.html` | - |
| 8 | Beetroot + kale | `beterraba/shorts-beterraba-couve-en.html` | - |
| 9 | Garlic honey | `alho/shorts-garlic-honey-en.html` | ✅ |
| 10 | Red onion | `cebola/shorts-cebola-beterraba-en.html` | ✅ |
| 11 | General guide (pillar) | `guia-geral/shorts-5-easiest-en.html` | - |
| 12 | Carrot | `cenoura/shorts-cenoura-animado-en.html` | ✅ |
| 13 | Long-form (7 veg) | `video-longo/player-video-longo-7-legumes-en.html` | - |
| 14 | 3 colors (garlic, onion, beetroot) | `cores/shorts-3-colors-en.html` | - |
| 15 | Broccoli + orange | `brocolis/shorts-broccoli-orange-en.html` | ✅ |
| 16 | DIY mosquito trap (side track) | `mosquito/shorts-mosquito-trap-en.html` | ✅ |
| 17 | Cucumber + apple | `pepino/shorts-pepino-apple-en.html` | ✅ |

**9 of the 17 are already rendered.** On the `✅` rows you do not record anything:
the .mp4 sits in the same folder as the .html, 1080x1920, constant frame rate.
On the others, open the file in the browser, press **▶**, let it play through
once, then record.

To render any of them (or the whole remaining batch):

```
node _gerar-mp4.js --w=1080 --fps=30 --kbps=3000 --cfr=1 <file>.html
node _gerar-mp4.js --todos --lista     # what is still missing, plus the estimate
node _gerar-mp4.js --todos             # render everything that is missing
```

One command per video: the driver retimes the file and checks the duration
itself. Budget about 2x the video length. The batch command skips the PT
originals and the `-1080x1920` style variants on purpose - those are the same
video in another language or another look, and posting both is the "inauthentic
content" risk.
"""),
]

for i, (velho, novo) in enumerate(TROCAS, 1):
    v = velho.replace('\n', nl)
    nv = novo.replace('\n', nl)
    n = d.count(v)
    print('troca %d: casou %d vez(es)' % (i, n))
    if n != 1:
        print('ABORTADO: ancora %d nao e unica. Nada foi gravado.' % i)
        sys.exit(1)
    d = d.replace(v, nv, 1)

assert d != orig
open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('gravado: %s (%d -> %d bytes)' % (ARQ, len(orig), len(d)))
