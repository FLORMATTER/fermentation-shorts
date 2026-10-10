# -*- coding: utf-8 -*-
"""
Registra o video #15 (brocolis + laranja) na memoria do projeto.

- .workbuddy-ai/memory/2026-09-17.md  -> append (log do dia, so acrescenta)
- .workbuddy-ai/memory/MEMORY.md      -> insercao ancorada antes de "Ajustes nas ferramentas"
"""
import io, os, shutil, sys

LOG = '.workbuddy-ai/memory/2026-09-17.md'
MEM = '.workbuddy-ai/memory/MEMORY.md'

# ── 1) log do dia (append) ───────────────────────────────────────────────────
NOTA_LOG = """

---

## 🥦 Vídeo #15 — brócolis + laranja (`brocolis/shorts-broccoli-orange-en.html`)

Pedido do usuário: *"faz um video de fermentacao em ingles ...debrocolis e laranja"*.
8 cenas, 53 s, 405×720 com o bloco `?rec`. Fechado e validado.

### O ângulo — pesquisado ANTES de escrever

Não inventei ciência. Quatro buscas primeiro:

- **Brócolis é o primeiro legume da série que NÃO faz a própria salmoura.** Repolho,
  beterraba e rabanete soltam água e o sal sozinho resolve. Brócolis quase não solta —
  então **tem que acrescentar água**. É esse o gancho do vídeo.
- Salmoura **2–3%** na literatura; escolhi **2,5%** (mesma regra da couve-flor, e sal
  baixo demais convida kahm). 1 L de água + 25 g de sal **sem iodo**.
- Pedaços de **1–2 polegadas** — **não ralar**. **5–10 dias** (pico 7–14), guarda
  **4–6 meses** na geladeira.
- **Cheiro de enxofre/couve é NORMAL** — é o motivo nº1 de jogarem um pote bom fora.
  Película branca fina = **levedura kahm** (tira e segue); peludo verde/preto/rosa = fora.
  **Nunca começar de congelado** — o gelo quebra as células e vira papa.

### A laranja — a distinção que virou o vídeo

**A casca é tempero. O suco é açúcar.** Não são a mesma coisa:

- há trabalho publicado fermentando **casca** de laranja com bactérias láticas → a casca
  não inibe a fermentação;
- a conserva de cítricos usa **6,7–10%** de sal, ou seja, sal demais **para** a
  fermentação — o que confirma que o problema nunca foi a casca;
- o risco real é o **açúcar do suco** alimentando levedura → gás/álcool. Mesmo mecanismo
  do vídeo da melancia, só que aqui o açúcar é você que põe.
- Dose: **raspa de ½ laranja + 2 gomos**.

### 🔴 O defeito que o validador aprovou

A cena 6 dizia **"TASTE IT ON DAY 2"** e a cena 8 dizia **"Start tasting on day 3"** —
**contradição dentro do mesmo vídeo**, a 12 segundos de distância. O `_validar-short.py`
deu **0 problemas** (ele mede coordenada, largura, keyframe órfã — **nunca o texto**).
Corrigido para DAY 3 nas duas.

**Lição:** o validador aprova contradição de conteúdo. **Ler o texto das cenas**, não só
rodar o validador.

### O render comum é INCONSISTENTE (achado desta vez)

Na rodada `--cols 2` as cenas 2 e 3 saíram **sem texto nenhum**; na rodada `--cols 4`, o
**mesmo arquivo** saiu com todo o texto. Nada mudou no arquivo — é corrida do
`--virtual-time-budget`. A skill dizia "sai sempre no estado 0%"; corrigido para
"**inconsistente — nunca concluir nada do render comum, nem 'quebrou' nem 'está ok'**".
O modo determinístico é `--no-anim` (`animation:none` → o elemento cai no estilo base,
visível) ou `--final`.

### Limpeza

Duas `@keyframes` mortas (`floatUpDown`, `pulseRing`) removidas — o validador acusava
"nunca usado". Mesma decisão do vídeo #14 (`barFill`, `drawLine`).

### Metadados

Entrada **#15** no pacote (título, 3 alternativas, descrição completa com os 5 blocos,
hashtags), linha na QUICK CHART (`2.5% | 5-10 d | IT WILL SMELL LIKE SULFUR`), linha em
"WHICH FILE TO RECORD", nota nas variantes (ângulo novo, postar depois do #5 e do #4),
**Semana 8 dia 1** no plano de postagem. Contagens **14 → 15 vídeos** em `README.md`
(`14 Shorts + 1 longo`) e em `plano-de-postagem.md` (título da seção + "As 8 semanas").
Mapa de pastas do README ganhou `cores/` e `brocolis/`.

### Ferramentas

- **`_gerar-galeria.py`**: a galeria varria uma lista fixa de pastas e **não tinha
  `cores` nem `brocolis`** — os dois últimos vídeos ficavam fora do índice visual.
  Acrescentados a `ROTULO` e `ORDEM`. Galeria regerada: **39 shorts, 0 com o bug do
  `transform=`**.
- **Skill `shorts-svg-animado`** — 2 correções:
  1. o render comum é **inconsistente**, não "sempre 0%";
  2. ⚠️ **a folha do `_revisar-cenas.py` NÃO mostra o `.tag`** (nem `.wm`, nem `.cap`,
     nem a capa) — ela extrai **só** os `<svg class="scene">`. A faixa vermelha só marca
     onde a legenda entra. Ou seja: **"renderize e olhe" não cobre o `tag:`**, que é
     justamente o texto visível mais esquecido da tradução. Para conferir: ler o array
     `scenes` no `<script>`.
"""

with io.open(LOG, 'a', encoding='utf-8', newline='') as f:
    f.write(NOTA_LOG)
print('OK  log do dia      -> %s (+%d bytes)' % (LOG, len(NOTA_LOG.encode('utf-8'))))

# ── 2) MEMORY.md (ancorado) ──────────────────────────────────────────────────
ENTRADA = """## 📊 Vídeo #15 — brócolis + laranja (17/09)

`brocolis/shorts-broccoli-orange-en.html` — 8 cenas, 53 s, `?rec`. **Ângulo pesquisado,
não inventado:** brócolis é o **primeiro legume da série que não faz a própria salmoura**
(repolho/beterraba/rabanete soltam água; brócolis quase não) → tem que **acrescentar
água**. Salmoura **2,5%**, pedaços de **1 polegada** (nunca ralado), **5–10 dias**,
**4–6 meses** na geladeira. **Cheiro de enxofre é NORMAL.** Película branca = kahm (tira
e segue); peludo verde/preto/rosa = fora. Nunca começar de congelado.

**A laranja: casca é tempero, suco é açúcar.** Raspa de ½ + 2 gomos. O risco não é a
casca (há trabalho publicado fermentando casca de laranja com láticas; a conserva de
cítricos usa 6,7–10% de sal, ou seja, sal demais **para** a fermentação) — é o **açúcar
do suco** virando gás/álcool, igual à melancia.

**O validador aprovou uma contradição:** a cena 6 dizia "TASTE IT ON DAY 2" e a cena 8
"Start tasting on day 3". Ele mede coordenada, **nunca texto**. Corrigido. Lição: **ler o
texto das cenas**, não só rodar o validador.

Postar depois do #5 (couve-flor) e do #4 (melancia). Semana 8, dia 1. Entrada #15.

"""

with io.open(MEM, 'r', encoding='utf-8') as f:
    d = f.read()

ancora = '## 🧰 Ajustes nas ferramentas (17/09)'
if d.count(ancora) != 1:
    print('ABORTADO — a ancora casou %d vez(es), esperava 1.' % d.count(ancora))
    sys.exit(1)

d = d.replace(ancora, ENTRADA + ancora, 1)

bk = MEM + '.antes-do-video15'
if not os.path.exists(bk):
    shutil.copy2(MEM, bk)
    print('backup  ->', bk)

with io.open(MEM, 'w', encoding='utf-8', newline='') as f:
    f.write(d)

print('OK  MEMORY.md       -> %s (%d bytes, NUL=%d)' % (MEM, len(d.encode('utf-8')), d.count('\x00')))
