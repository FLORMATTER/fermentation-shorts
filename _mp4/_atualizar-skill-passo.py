"""Atualiza a secao do .mp4 na skill com a curva do --passo medida hoje (19/09).

O que mudou:
  - o --passo passou a ter padrao 60 (a skill recomendava 150, que custa 2,4x mais);
  - o driver retima sozinho desde hoje (a skill ainda mandava rodar o retimar.py a mao);
  - a tabela "em CFR o gargalo e' a rasterizacao" tinha 1080 e 720 TROCADOS
    (dizia ~45 ms em 720 e ~20 ms em 1080) e taxas que nao batem com o medido;
  - a causa da perda nao e' so' a fila do codificador: o requestFrame() do
    captureStream(0) sobrescreve o quadro ainda nao consumido.

Quatro ancoras contadas. Aborta sem gravar se alguma nao casar uma vez.
"""
import sys

ARQ = r'C:\Users\Saxa\.workbuddy-ai\skills\shorts-svg-animado\SKILL.md'
d = open(ARQ, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in d else '\n'
print('%s: fim de linha %s | %d bytes' % (ARQ.split('\\')[-1], 'CRLF' if nl == '\r\n' else 'LF', len(d)))
orig = d

TROCAS = [
    # ---------- A) bloco de uso ----------
    ("""# 1. GRAVAR em taxa constante, alimentando devagar para nao perder quadro
node _gerar-mp4.js --w=1080 --fps=30 --kbps=3000 --cfr=1 --passo=150 <arq>.html
# 2. RETIMAR: poe todas as amostras em 1/30 s
python _mp4/retimar.py <arq>.mp4 --fps=30 --quadros=<N> --bruto
""",
     """node _gerar-mp4.js --w=1080 --fps=30 --kbps=3000 --cfr=1 <arq>.html
# O driver RETIMA e CONFERE a duracao sozinho no fim (desde 19/09).
# --sem-retimar desliga, para depurar o arquivo cru.

node _gerar-mp4.js --todos --lista     # ve o lote e estimativa, SEM gravar
node _gerar-mp4.js --todos             # grava o lote (so' short publicavel)
"""),

    # ---------- B) tabela do diagnostico ----------
    ("""| 720p em tempo real, 8 Mbps | 89 | 66 | **74%** |
| 720p CFR a 19 q/s, 2 Mbps | 214 | 163 | **76%** |
| 1080p CFR com `--passo=150` | 214 | 211 | **99%** |
""",
     """| 720p em tempo real, 8 Mbps | 89 | 66 | **74%** |
| 720p CFR a 19 q/s, 2 Mbps | 214 | 163 | **76%** |
| 1080p CFR com `--passo=150` | 214 | 211 | **99%** |
| 1080p CFR **sem** `--passo` | 624 | 431 | **69%** |
"""),

    # ---------- C) a cura ----------
    ("""1. **CFR (`--cfr=1`)** — o motor desenha **um índice de quadro por vez, em ordem, sem
   olhar o relógio**. Repetição fica impossível por construção. O arquivo cru sai com
   a duração do *render*, não do vídeo — e isso deixa de importar.
2. **`--passo=NN`** — intervalo **mínimo** entre quadros, em ms. Como em CFR o relógio
   não importa, dá para **esperar de propósito** e a fila do codificador nunca enche.
   Foi de 76% para **99%**.
3. **`python _mp4/retimar.py <arq>.mp4 --fps=30 --quadros=<N>`** — reescreve **no
   lugar** a duração de cada amostra para `1/30 s` e conserta `mvhd` / `tkhd` / `mdhd`
   / `tfdt`. **Não recodifica nada**: o `mdat` fica intacto, o tamanho do arquivo não
   muda.
   - `--quadros=N` é a **rede de segurança**: se algum quadro ainda cair, o retimer
     **preserva a duração** e distribui as amostras que sobraram (sai 29,6 q/s em vez
     de 30). O vídeo **nunca sai curto nem acelerado**.
   - Estrutura que ele assume (conferida com `dump-mp4.py`): `mvhd`/`tkhd` v1 em escala
     **1000**, `mdhd` v1 em escala **30000**, `trun` flags `0x000305` (duração **por
     amostra**), `tfdt` v1, `stts`/`stsz` zerados (fragmentado), sem `mehd` nem `elst`.
   - **O Chrome grava lixo no `mdhd`**: o `duration` sai em ms embora a escala seja
     30000 (dá 1,894 s num vídeo de 56,8 s). O retimer conserta.

Resultado do #16: **1080×1920, H.264, 57,0 s, 30 q/s constante, nenhum quadro
repetido, 99% dos quadros presentes.**
""",
     """1. **CFR (`--cfr=1`)** — o motor desenha **um índice de quadro por vez, em ordem, sem
   olhar o relógio**. Repetição fica impossível por construção. O arquivo cru sai com
   a duração do *render*, não do vídeo — e isso deixa de importar.
2. **`--passo=NN`** — intervalo **mínimo** entre quadros, em ms. Como em CFR o relógio
   não importa, dá para **esperar de propósito**.
   O que se perde sem ele **não é só a fila do codificador**: o `requestFrame()` do
   `captureStream(0)` **sobrescreve o quadro que ainda não foi consumido**. É por isso
   que há perda mesmo **abaixo** do teto do codificador (a 29 q/s submetidos em 1080p
   ainda caíam 5%).
3. **O driver retima sozinho** (desde 19/09). O `_gerar-mp4.js` chama o `retimar.py` no
   fim e **confere a duração** — recusa o arquivo se a diferença passar de 0,05 s.
   Antes o retimar era um passo manual que o driver só *lembrava* de imprimir; num lote
   de 13 vídeos isso entregava um vídeo de 280 s como se fosse de 57 s.
   O retimar reescreve **no lugar** a duração de cada amostra para `1/30 s` e conserta
   `mvhd` / `tkhd` / `mdhd` / `tfdt`. **Não recodifica nada**: o `mdat` fica intacto, o
   tamanho do arquivo não muda.
   - `--quadros=N` é a **rede de segurança**: se algum quadro ainda cair, o retimer
     **preserva a duração** e distribui as amostras que sobraram. O vídeo **nunca sai
     curto nem acelerado**.
   - Estrutura que ele assume (conferida com `dump-mp4.py`): `mvhd`/`tkhd` v1 em escala
     **1000**, `mdhd` v1 em escala **30000**, `trun` flags `0x000305` (duração **por
     amostra**), `tfdt` v1, `stts`/`stsz` zerados (fragmentado), sem `mehd` nem `elst`.
   - **O Chrome grava lixo no `mdhd`**: o `duration` sai em ms embora a escala seja
     30000 (dá 1,894 s num vídeo de 56,8 s). O retimer conserta.

#### 📐 Quanto esperar: a curva do `--passo` (medida em 19/09)

624 quadros = 20,8 s, `pepino/shorts-pepino-speed-en.html`:

| `--passo` | render | sobreviveu | taxa efetiva | render/vídeo |
|---|---|---|---|---|
| 0 ms | 18,5 s | **69%** | 20,7 q/s | 0,9× |
| 40 ms | 31,1 s | 95% | 28,5 q/s | 1,5× |
| **60 ms** | ~41 s | **~97%** | ~29 q/s | **~2×** |
| 80 ms | 53,3 s | 97% | 29,1 q/s | 2,6× |
| 120 ms | 82,3 s | 99% | 29,7 q/s | 4,0× |
| 150 ms | 99,1 s | 100% | 30,0 q/s | 4,8× |

**O padrão agora é 60 ms.** 97% = 29 q/s na prática — indistinguível de 30, e **menos da
metade do tempo** do `--passo=150`. Num lote de 32 min de vídeo: **~1 h** em vez de ~2 h 36.

- `--passo=150` **não está errado, é caro**. Para uma peça só, tudo bem; para lote, não.
- **A perda não trava a animação quando se retima.** Cada amostra sobrevivente recebe a
  mesma duração: o movimento fica um pouco mais grosseiro, **nunca parado**. É por isso
  que 97% serve — o defeito que o usuário viu era *outro* (quadro repetido, no modo
  tempo real).

Resultado do #16: **1080×1920, H.264, 57,0 s, 30 q/s constante, nenhum quadro
repetido, 99% dos quadros presentes.**
"""),

    # ---------- D) o custo por quadro ----------
    ("""O teto de taxa em tempo real (a tabela antiga: ~11 q/s em 1080, ~20 em 720) **deixou
de ser o limite**, porque em CFR o relógio não manda. O que sobra é o custo por quadro:

| etapa | por quadro |
|---|---|
| assar (`getComputedStyle` + serializar) | ~4 ms |
| desenhar no canvas | ~3,4 ms |
| **rasterizar o SVG** (`img.onload`) | **~20 ms em 1080, ~45 ms em 720** |
| **total** | **~6 q/s em 1080, ~19 q/s em 720** |

- **Renderizar 57 s em 1080×1920 leva ~4,5 min** (1710 quadros). Em 720 leva ~1,5 min.
  Vale a pena: o relógio de parede é o preço da taxa constante.
""",
     """O teto de taxa em tempo real (a tabela antiga: ~11 q/s em 1080, ~20 em 720) **deixou
de ser o limite**, porque em CFR o relógio não manda. O que sobra é o custo por quadro —
e, medido em 19/09, ele é **bem menor** do que a tabela antiga dizia (e ela tinha 720 e
1080 **trocados**):

| etapa | 720p | 1080p |
|---|---|---|
| assar + desenhar + rasterizar | ~13 ms | ~30 ms |
| teto de submissão, **sem** espera | ~77 q/s | ~34 q/s |

- **Renderizar 57 s em 1080×1920 leva ~2 min com `--passo=60`** (1710 quadros) — não 4,5.
  O relógio de parede é o preço da taxa constante, mas o preço é menor do que se pensava.
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
print('gravado: %d -> %d bytes' % (len(orig), len(d)))
