"""_mp4/_atualizar-skill-cfr.py — reescreve a secao do .mp4 na SKILL.md.

A secao antiga afirmava que "o gargalo real e' o codificador H.264 e ele manda na
taxa" e trazia uma tabela de teto (~11 q/s em 1080, ~20 em 720). A sessao de 18/09
mostrou que o teto nao e' o problema: o problema e' o MediaRecorder DESCARTA
quadro, e em CFR o relogio deixa de importar. A secao inteira e' substituida.

Troca por marcadores: tudo entre o titulo da secao e o proximo "## " de topo.
"""
import sys

ARQ = 'C:/Users/Saxa/.workbuddy-ai/skills/shorts-svg-animado/SKILL.md'
INICIO = '## 🎬 Gerar o .mp4 de verdade (sem ffmpeg)'
FIM = '## 🗂 Organizar as pastas do projeto (quando a raiz estiver cheia)'

NOVO = """## 🎬 Gerar o .mp4 de verdade (sem ffmpeg)

**Não existe ffmpeg nesta máquina — e não precisa.** O Chrome headless codifica
**H.264 dentro de MP4** nativamente
(`MediaRecorder.isTypeSupported('video/mp4;codecs=avc1.42E01E')` → `true`).
Quem desenha os quadros é o próprio navegador.

```bash
# 1. GRAVAR em taxa constante, alimentando devagar para nao perder quadro
node _gerar-mp4.js --w=1080 --fps=30 --kbps=3000 --cfr=1 --passo=150 <arq>.html
# 2. RETIMAR: poe todas as amostras em 1/30 s
python _mp4/retimar.py <arq>.mp4 --fps=30 --quadros=<N> --bruto

python _mp4/inspecionar.py <arq>.mp4                    # duracao / resolucao / codec
python _mp4/dump-mp4.py <arq>.mp4                       # ARVORE de boxes + campos
python _mp4/diagnosticar.py <arq>.mp4 --desenhou=<N>    # quantos quadros SOBREVIVERAM
node _mp4/quadros-mp4.js <arq>.mp4 8                    # extrai 8 quadros -> PNG
node _mp4/quadros-mp4.js <arq>.mp4 8 --tempos=0.5,30,56.5
node _mp4/rodar.js "file:///.../_mp4/bench6.html?arq=../<pasta>/<short>.html" 240 --file-access
```

- `_mp4/render.js` é o motor — **injetado na página, nunca gravado dentro do short**;
  `_gerar-mp4.js` é o piloto; os `_mp4/*.py` leem os boxes na mão.
- Saída: **H.264 (`avc1`)**, mp4 fragmentado (YouTube aceita).
- **A marca d'água placeholder (`@yourchannel` / `@seucanal`) é omitida no mp4** — num
  arquivo gravado ela ficaria queimada para sempre.
- O piloto calcula a duração esperada somando os `ms:` do HTML.

### 🔴 O inimigo é quadro DESCARTADO, não quadro repetido (18/09 — a virada)

O sintoma era "a animação trava entre quadros". O diagnóstico óbvio — quadro
repetido — estava **errado**, e persegui-lo custou uma sessão inteira.

**O `MediaRecorder` DESCARTA quadro sem avisar quando a fila do codificador enche.**
Medido com `_mp4/diagnosticar.py`:

| gravação | desenhados | no arquivo | sobreviveu |
|---|---|---|---|
| 720p em tempo real, 8 Mbps | 89 | 66 | **74%** |
| 720p CFR a 19 q/s, 2 Mbps | 214 | 163 | **76%** |
| 1080p CFR com `--passo=150` | 214 | 211 | **99%** |

Quadro descartado é **pior que quadro repetido**: o anterior fica o **dobro** do tempo
na tela. E o contador `repetidos por atraso` marcava **0** enquanto 24% sumia — por
isso o defeito atravessou uma sessão de medições sem ser visto.

> **Medir o que SOBREVIVEU no arquivo, não o que foi desenhado.** O contador interno
> do motor não enxerga descarte; só `diagnosticar.py` enxerga.

### ✅ A cura: CFR + passo + retimagem

1. **CFR (`--cfr=1`)** — o motor desenha **um índice de quadro por vez, em ordem, sem
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

### 📐 Em CFR o gargalo é a RASTERIZAÇÃO, não o codificador

O teto de taxa em tempo real (a tabela antiga: ~11 q/s em 1080, ~20 em 720) **deixou
de ser o limite**, porque em CFR o relógio não manda. O que sobra é o custo por quadro:

| etapa | por quadro |
|---|---|
| assar (`getComputedStyle` + serializar) | ~4 ms |
| desenhar no canvas | ~3,4 ms |
| **rasterizar o SVG** (`img.onload`) | **~20 ms em 1080, ~45 ms em 720** |
| **total** | **~6 q/s em 1080, ~19 q/s em 720** |

- **Renderizar 57 s em 1080×1920 leva ~4,5 min** (1710 quadros). Em 720 leva ~1,5 min.
  Vale a pena: o relógio de parede é o preço da taxa constante.
- **O bitrate é alavanca de verdade** — e o `--kbps` era **no-op** até 18/09: o driver
  mandava `?mp4kbps=` na URL e o `render.js` ignorava, ficando fixo em 8 Mbps. Consertado.
- **Apagar o perfil do Chrome antes de cada gravação.** Reusar o mesmo
  `--user-data-dir` degrada o render: a mesma configuração caiu de 16,1 para 11,5 q/s,
  e apagar o perfil devolveu o desempenho.
- **Não há H.264 por hardware nesta máquina** (Intel HD Graphics 520 — o WebCodecs
  recusa **toda** configuração H.264). `--enable-accelerated-video-encode` **piorou**.
- **Em CFR não vale a pena otimizar o codificador**: baixar resolução, baixar bitrate e
  mexer no contexto do canvas compram pouco, porque quem manda é a rasterização.

### 🛠 Para medir rápido: um short curto

```bash
python _mp4/_criar-teste-curto.py     # cria _mp4/teste-8s.html (8 cenas, 7 s)
```
O render de verdade leva ~4,5 min; o curto leva ~35 s. Mantém as 8 cenas (o peso de
cada uma é o que importa) e só encurta a duração. **Apagar o teste depois** — senão um
`--todos` futuro o pega como se fosse um short de verdade.

### 🔴 Os defeitos que custaram tempo — não repetir

1. **`requestAnimationFrame` no headless roda a ~11 Hz.** Não é o encoder nem o
   desenho: o rAF é servido pelo compositor, e sem tela ele tica devagar. O vídeo
   saía **32 s em vez de 53,5 s** porque o `MediaRecorder` carimbava 1/30 s por
   quadro entregue. **Usar `setTimeout` com ritmo de relógio.**
2. **`captureStream(30)` amostra o canvas no tique do compositor.** Usar
   **`captureStream(0)` + `track.requestFrame()`**: cada chamada empurra exatamente
   um quadro, carimbado com a hora real.
3. **O blob não sai do navegador pelo CDP** — 3,4 MB em base64 travaram o
   `Runtime.evaluate` (o processo ficou pendurado). Solução: `_gerar-mp4.js` **serve a
   página por HTTP num servidor próprio** e o navegador **devolve o mp4 por POST**.
4. **`const scenes` é binding lexical, não é `window.scenes`.** Ao inspecionar o short
   de fora (iframe), ler as cenas pelo DOM: `querySelectorAll('svg.scene')`.
5. **As 7 cenas escondidas continuam animando.** O CSS esconde cena com
   `visibility:hidden`, não `display:none` — as 64 animações das 8 cenas rodam a
   gravação inteira. O motor agora **pausa todas no início** e guarda os objetos de
   animação por cena (`animsPorCena`), mexendo só na cena da vez.
6. **O último quadro não era carimbado.** Parar a gravação no mesmo instante do último
   desenho encurtava o arquivo em **~1%** (0,6 s em 57 s). Solução: segurar o último
   quadro **150 ms** antes de `rec.stop()`.
7. **A barra de legenda apagava.** A imagem da cena cobre o canvas inteiro (405×720
   com fundo sólido), então "desenhar o overlay só quando a cena muda" produzia vídeo
   **sem legenda nenhuma**. O overlay é redesenhado **todo quadro**.
8. **A tolerância de duração fixa de 0,6 s reprovava vídeo certo.** Tem que ser
   **proporcional**: `max(0,6 s, 2%)`.

### ⚠️ Sempre conferir: duração E quadros

Em **CFR** o piloto **não** confere a duração (o arquivo cru é mais longo de
propósito) — quem confere é o `retimar.py`, e ele nunca erra a duração. Em **tempo
real** o piloto **recusa e apaga** o arquivo se a duração desviar mais que
`max(0,6 s, 2%)`: vídeo acelerado é o modo de falha silencioso desta técnica.

A segunda prova é **abrir o mp4 e olhar quadros de verdade**:
`node _mp4/quadros-mp4.js <arquivo>.mp4 8` → `_revisao/<nome>-mp4.png`.
Tamanho de arquivo não prova que o vídeo decodifica.

> **O verificador antigo (`_mp4/conferir-mp4.py`) foi REMOVIDO em 18/09** porque dava
> **veredito falso** de "8 quadros idênticos". Dois defeitos somados: (1) disparar 8
> `v.currentTime = t` de uma vez faz o navegador coalescer num único seek; (2) a "rede
> de segurança" de 1200 ms desenhava de qualquer jeito, e com `--virtual-time-budget`
> esse timer dispara na hora. **Não voltar a conferir por seek.** O `quadros-mp4.js`
> não busca: ele **toca** o vídeo e fotografa quando `mediaTime` cruza cada alvo
> (`requestVideoFrameCallback`), servindo o mp4 por HTTP com suporte a Range.

### 🔬 Como medir sem se enganar — três armadilhas que já custaram horas

1. **Latência não é custo.** `new Image()` → `onload` mede **espera na fila**, não
   tempo de thread principal. Um `rasterizar 83 ms` no log era fila, não CPU. O que
   importa é **quanto o thread principal ficou travado** — medir com uma sonda de
   `setTimeout(2)` rodando junto e somando o atraso (`bench5.html` / `bench6.html`).
2. **Rasterização em cache.** Se o bench reusa a **mesma** data URL, o Chrome devolve
   o bitmap já rasterizado e o custo medido vira ~0. **Cada quadro medido tem que ser
   diferente** (variar o `currentTime`).
3. **Iframe fora da tela não anima.** Com `left:-3000px` o Chrome não compõe a cena, e
   a medição não vale. O palco tem que estar **na tela**.

### O que NÃO funcionou (para não tentar de novo)

- `--disable-gpu`: **piorou** (11,5 fps em vez de 18).
- **`createImageBitmap(blob)` para tirar a rasterização do thread principal:** o Chrome
  **não decodifica SVG por essa via** (`The source image could not be decoded`). Não há
  como mover a rasterização de SVG para um worker.
- **Rasterizar menor (405/540) para acelerar: não acelera** e ainda piora a nitidez.
- `--virtual-time-budget` **não** serve para medir tempo: ele virtualiza o relógio.
- **As "otimizações" de 18/09 que foram medidas e REVERTIDAS** — não repetir:
  ritmo por índice em tempo real, `ORCAMENTO = 12`, `AQUECER = 24`, leitura antecipada
  a partir de `f+1`, `RAS = 1080` (supersampling), `{alpha:false, desynchronized:true}`
  no contexto do canvas, e `--enable-accelerated-video-encode`. Todas pioraram ou não
  mudaram nada. **A config boa é a que está no arquivo.**

"""

d = open(ARQ, encoding='utf-8').read()
i = d.find(INICIO)
j = d.find(FIM)
if i < 0 or j < 0 or j <= i:
    print('ABORTADO: nao achei os marcadores (i=%d j=%d)' % (i, j))
    sys.exit(1)
if d.count(INICIO) != 1 or d.count(FIM) != 1:
    print('ABORTADO: marcador nao e unico')
    sys.exit(1)
novo = d[:i] + NOVO + d[j:]
open(ARQ, 'w', encoding='utf-8', newline='').write(novo)
print('SKILL.md: %d -> %d bytes' % (len(d), len(novo)))
print('secao substituida (%d chars -> %d chars)' % (j - i, len(NOVO)))
