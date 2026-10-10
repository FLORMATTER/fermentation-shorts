"""_pacote-mp4-2.py — o resto do lote canonico entra no pacote de publicacao.

Depois deste lote sobram so' o #13 (video longo, 16:9, fluxo proprio).

Nove ancoras contadas (8 entradas + o fecho). Aborta sem gravar se alguma nao casar
uma vez.
"""
import sys

ARQ = 'guias/pacote-legendas-descricoes-en.md'
d = open(ARQ, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in d else '\n'
print('%s: fim de linha %s' % (ARQ, 'CRLF' if nl == '\r\n' else 'LF'))
orig = d


def nota(caminho, seg, fps):
    return ('File: `%s.html`\n'
            '**The .mp4 is already rendered:** `%s.mp4`\n'
            '(1080x1920 vertical, H.264, %s s, constant %s fps) - no screen recording needed.\n'
            '\n' % (caminho, caminho, seg, fps))


ENTRADAS = [
    ('# 1. SAUERKRAUT — THE PILLAR VIDEO', 'repolho/shorts-chucrute-30s-en', '30.0', '30'),
    ('# 2. CABBAGE — THE TWO TRICKS', 'repolho/shorts-repolho-maos-canva-en', '52.0', '30'),
    ('# 3. BEETROOT', 'beterraba/shorts-beterraba-svg-puro-en', '44.0', '30'),
    ('# 5. CAULIFLOWER', 'couve-flor/shorts-couveflor-animado-en', '43.5', '30'),
    ('# 7. RADISH', 'rabanete/shorts-rabanete-animado-en', '40.5', '30'),
    ('# 8. BEETROOT + KALE', 'beterraba/shorts-beterraba-couve-en', '52.0', '30'),
    ('# 11. PILLAR VIDEO — GENERAL GUIDE', 'guia-geral/shorts-5-easiest-en', '49.0', '30'),
    ('# 14. 3 COLORS — GARLIC + ONION + BEETROOT', 'cores/shorts-3-colors-en', '53.5', '30'),
]

TROCAS = []
for cab, caminho, seg, fps in ENTRADAS:
    TROCAS.append((cab + '\n\n', cab + '\n\n' + nota(caminho, seg, fps)))

# --- a coluna da tabela
LINHAS = [
    ('| 1 | Sauerkraut (pillar) | `repolho/shorts-chucrute-30s-en.html` | - |',
     '| 1 | Sauerkraut (pillar) | `repolho/shorts-chucrute-30s-en.html` | ✅ |'),
    ('| 2 | Cabbage | `repolho/shorts-repolho-maos-canva-en.html` | - |',
     '| 2 | Cabbage | `repolho/shorts-repolho-maos-canva-en.html` | ✅ |'),
    ('| 3 | Beetroot | `beterraba/shorts-beterraba-svg-puro-en.html` | - |',
     '| 3 | Beetroot | `beterraba/shorts-beterraba-svg-puro-en.html` | ✅ |'),
    ('| 5 | Cauliflower | `couve-flor/shorts-couveflor-animado-en.html` | - |',
     '| 5 | Cauliflower | `couve-flor/shorts-couveflor-animado-en.html` | ✅ |'),
    ('| 7 | Radish | `rabanete/shorts-rabanete-animado-en.html` | - |',
     '| 7 | Radish | `rabanete/shorts-rabanete-animado-en.html` | ✅ |'),
    ('| 8 | Beetroot + kale | `beterraba/shorts-beterraba-couve-en.html` | - |',
     '| 8 | Beetroot + kale | `beterraba/shorts-beterraba-couve-en.html` | ✅ |'),
    ('| 11 | General guide (pillar) | `guia-geral/shorts-5-easiest-en.html` | - |',
     '| 11 | General guide (pillar) | `guia-geral/shorts-5-easiest-en.html` | ✅ |'),
    ('| 14 | 3 colors (garlic, onion, beetroot) | `cores/shorts-3-colors-en.html` | - |',
     '| 14 | 3 colors (garlic, onion, beetroot) | `cores/shorts-3-colors-en.html` | ✅ |'),
]
TROCAS.append((
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
""",
    """| # | Entry | File to open | .mp4 |
|---|---|---|---|
| 1 | Sauerkraut (pillar) | `repolho/shorts-chucrute-30s-en.html` | ✅ |
| 2 | Cabbage | `repolho/shorts-repolho-maos-canva-en.html` | ✅ |
| 3 | Beetroot | `beterraba/shorts-beterraba-svg-puro-en.html` | ✅ |
| 4 | Beetroot + watermelon ⚠️ | `beterraba/shorts-beterraba-melancia-en.html` | ✅ |
| 5 | Cauliflower | `couve-flor/shorts-couveflor-animado-en.html` | ✅ |
| 6 | Cucumber | `pepino/shorts-pepino-speed-en.html` | ✅ |
| 7 | Radish | `rabanete/shorts-rabanete-animado-en.html` | ✅ |
| 8 | Beetroot + kale | `beterraba/shorts-beterraba-couve-en.html` | ✅ |
| 9 | Garlic honey | `alho/shorts-garlic-honey-en.html` | ✅ |
| 10 | Red onion | `cebola/shorts-cebola-beterraba-en.html` | ✅ |
| 11 | General guide (pillar) | `guia-geral/shorts-5-easiest-en.html` | ✅ |
| 12 | Carrot | `cenoura/shorts-cenoura-animado-en.html` | ✅ |
| 13 | Long-form (7 veg) | `video-longo/player-video-longo-7-legumes-en.html` | - |
| 14 | 3 colors (garlic, onion, beetroot) | `cores/shorts-3-colors-en.html` | ✅ |
| 15 | Broccoli + orange | `brocolis/shorts-broccoli-orange-en.html` | ✅ |
| 16 | DIY mosquito trap (side track) | `mosquito/shorts-mosquito-trap-en.html` | ✅ |
| 17 | Cucumber + apple | `pepino/shorts-pepino-apple-en.html` | ✅ |

**16 of the 17 are already rendered.** On the `✅` rows you do not record anything: the
.mp4 sits in the same folder as the .html, 1080x1920, constant frame rate.

The only one left is **#13, the long-form 7-vegetable video**. It is 16:9, not a Short,
and it has its own review flow (`_revisar-videolongo.py`), so render it separately when
you get to it - do not put it in a batch with the Shorts.
"""))

for i, (velho, novo) in enumerate(TROCAS, 1):
    v = velho.replace('\n', nl)
    nv = novo.replace('\n', nl)
    n = d.count(v)
    rot = velho.split('\n')[0][:48]
    print('troca %2d: casou %d vez(es)  <- %s' % (i, n, rot))
    if n != 1:
        print('ABORTADO: ancora %d nao e unica. Nada foi gravado.' % i)
        sys.exit(1)
    d = d.replace(v, nv, 1)

assert d != orig
open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('gravado: %s (%d -> %d bytes)' % (ARQ, len(orig), len(d)))
