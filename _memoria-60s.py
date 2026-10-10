# -*- coding: utf-8 -*-
"""Anexa ao log do dia. Append puro: nunca sobrescreve."""
import io, os, sys

LOG = 'C:/Users/Saxa/Desktop/youtube-work/.workbuddy-ai/memory/2026-09-26.md'

TEXTO = """

---

## #19 em 60 s (corte para TikTok) + 2 defeitos reais na galeria

### O corte de 60 s

`_criar-beet-garlic-60s.py` gerou `beterraba/shorts-beet-garlic-en-1080x1920-60s.html`:
**10 cenas, 67,5 s, 18/18 keyframes, 66.102 bytes**, `_validar-short.py` = 0 problemas.

Duas cenas de **substância nova** (não esticadas, pela regra "o formato pode repetir, a
substância não"): **s8** `STEP 6 · KEEP IT UNDER` / `KEEP IT UNDER THE BRINE` — o que fica
fora da salmoura é o que dá errado, e um zip bag de salmoura serve de peso; **s9**
`STEP 7 · THE WHITE FILM` / `FLAT IS FINE, FUZZY IS NOT` — película branca é kahm yeast e é
inofensiva, peludo/colorido é mofo.

**Defeito pego:** a inserção em `m.end()` foi calculada **antes** de um replace que mudou o
comprimento (rótulo `1 / 8` → `1 / 10`, +1 char) → o offset andou e a inserção comeu um
caractere: **10 cenas e 9 `</svg>`** (cena aberta). O `_validar-short.py` **não pega** — ele
conta `<svg class="scene`, não pares. **Guarda nova:** `d.count('</svg>') != len(ids)` →
aborta. **Provada** com `_provar-guarda-60s.py` (arquivo quebrado acusa; regerado silencia).

### mp4

`node _gerar-mp4.js --w=1080 --fps=30 --kbps=3000 --cfr=1 --passo=150` →
**21.065.051 bytes (20,1 MB), 67,50 s, 1080x1920, 2025 quadros a ~30,0 fps** — 67,5 × 30 =
**2025 exato**. Conferido **tocando** (`_mp4/quadros-mp4.js ... 13`): as **10 cenas cobertas**,
rótulo fecha em **"1 / 10"**, e a marca d'água sai **omitida por desenho** — o
`_mp4/render.js:100` injeta `#cover,.ui,.bar,.tag,.wm,.cap{display:none!important}` e as
linhas 118-120 pulam o placeholder. O rótulo e a legenda do mp4 **não** vêm do DOM: são
redesenhados no canvas a partir do dado da cena. (Leitura errada no PNG de contato:
"FERMENTED TO FISTER" era **FERMENTED TOGETHER** — o texto está certo.)

### 2 defeitos reais na galeria — conserto no GERADOR (regra 12)

1. **Os números do topo vinham de uma tupla `%` e eu inverti dois argumentos.** O alerta
   passou a dizer *"66 dos shorts já têm .mp4"* (era a contagem de **arquivos**) e o lead
   *"27 arquivos HTML+SVG"* (era a de **mp4**). Cada frase ficou com o número da outra, e
   "parece plausível" passa. **Conserto:** autochecagem antes de gravar — confere a frase do
   alerta, confere `html.count('class="b mp4"') == com_mp4` e a frase do lead; `SystemExit`
   **antes** de escrever. **Provada** com `_provar-guarda-galeria.py`.
2. **`cap:`/`sub:` vêm do JS com `\\uXXXX` cru.** A galeria imprimia `2% salt \\u00b7 ready`
   em vez de `2% salt · ready` — **3 de 55** subs. **Conserto:** `_unesc()` decodifica ao
   extrair.
3. **Bônus:** o alerta dizia *"não existem arquivos `.mp4` neste projeto"* e mandava gravar
   com OBS, quando o `_gerar-mp4.js` já gera os `.mp4`. Agora ele **conta** os mp4 (28) e cada
   cartão ganha o selo **`.mp4 pronto`**.

### Lição de método

**Para provar uma guarda da galeria, a cópia defeituosa tem de rodar na RAIZ.**
`RAIZ = os.path.dirname(os.path.abspath(__file__))` — uma cópia em `_revisao/` varre **0
shorts**, os dois números empatam em **0** e a guarda **parece cega**. Foi um falso "guarda
NÃO provada" na 1ª tentativa. A copia defeituosa vai na raiz e só a `SAIDA` é redirecionada.

### O contador "27 dos 28" está CERTO (não "consertar")

Desconfiei ao ver 28 `.mp4` no disco e fui medir na fonte: a tabela **WHICH FILE TO RECORD**
marca ✅ em **27** linhas e `-` no **#13** (o vídeo longo 16:9, que não é Short e tem fluxo
próprio). Um dos 28 arquivos é a **variante 60s**, que não é entrada de catálogo. Logo
27 de 28. **Número conferido contra a fonte, não "arrumado" no olho.**

### Galeria

`python _gerar-galeria.py` → **57 shorts, 0 bugs, 3 avisos, 47:08**. Números do topo
**28 dos shorts já têm .mp4** e **66 arquivos HTML+SVG** (57 + 9 fora) — os dois fecham com a
contagem de selos e de cartões.

### Skill

+ seção **"🖼️ A galeria (`_gerar-galeria.py`) — o 3º lugar do registro"** com as 3 armadilhas
e a nota do RAIZ. 111.279 → **113.042 chars**. Antes disso, + a lição do `_zoom-cena.py`
mostrar **t=0** (elemento com `fadeSlide`/`popInSeq` é invisível no zoom; texto e anotação se
julgam no `--final`).
"""

if not os.path.exists(LOG):
    print('ERRO: log do dia nao existe: %s' % LOG)
    sys.exit(1)

antes = os.path.getsize(LOG)
with io.open(LOG, 'a', encoding='utf-8', newline='') as f:
    f.write(TEXTO)

depois = os.path.getsize(LOG)
d = io.open(LOG, encoding='utf-8').read()
for t in ['#19 em 60 s', '27 dos 28" está CERTO', 'A galeria (`_gerar-galeria.py`)']:
    if t not in d:
        print('ERRO: trecho nao entrou: %r' % t)
        sys.exit(1)
print('OK: log %d -> %d bytes (+%d)' % (antes, depois, depois - antes))
