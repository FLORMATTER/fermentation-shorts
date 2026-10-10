# -*- coding: utf-8 -*-
"""Reescreve a secao do .mp4 no SKILL.md com o que a sessao de 18/09 mediu.
   Aborta SEM GRAVAR se a ancora nao casar exatamente 1 vez."""
import io, os, sys

ARQ = os.path.join(os.path.expanduser('~'), '.workbuddy-ai', 'skills',
                   'shorts-svg-animado', 'SKILL.md')

OLD = u'''## 🎬 Gerar o .mp4 de verdade (sem ffmpeg)

**Não existe ffmpeg nesta máquina — e não precisa.** O Chrome headless codifica
**H.264 dentro de MP4** nativamente
(`MediaRecorder.isTypeSupported('video/mp4;codecs=avc1.42E01E')` → `true`).
Quem desenha os quadros é o próprio navegador.

```bash
node _gerar-mp4.js mosquito/shorts-mosquito-trap-en.html   # um short
node _gerar-mp4.js --todos                                 # todos que ainda nao tem mp4
python _mp4/inspecionar.py <arquivo>.mp4                   # duracao / resolucao / codec
python _mp4/conferir-mp4.py <arquivo>.mp4                  # extrai 8 quadros -> PNG
node _mp4/rodar.js "file:///.../_mp4/bench.html?arq=../<pasta>/<short>.html" 90 --file-access
```

- `_mp4/render.js` é o motor — **injetado na página, nunca gravado dentro do short**;
  `_gerar-mp4.js` é o piloto; `_mp4/inspecionar.py` lê o box `mvhd` na mão.
- Saída: **1080×1920, H.264 (`avc1`), 30 fps, 8 Mbps**, mp4 fragmentado (YouTube aceita).
- **A marca d'água placeholder (`@yourchannel` / `@seucanal`) é omitida no mp4** — num
  arquivo gravado ela ficaria queimada para sempre. Só entra depois que o canal tiver nome.
- O piloto calcula a duração esperada somando os `ms:` do HTML.

### 🔴 Os 4 defeitos que custaram tempo — não repetir

1. **`requestAnimationFrame` no headless roda a ~11 Hz.** Não é o encoder nem o
   desenho: o rAF é servido pelo compositor, e sem tela ele tica devagar. O vídeo
   saía **32 s em vez de 53,5 s** porque o `MediaRecorder` carimbava 1/30 s por
   quadro entregue. **Usar `setTimeout(tick, 6)` com ritmo de relógio.**
2. **`captureStream(30)` amostra o canvas no tique do compositor.** Usar
   **`captureStream(0)` + `track.requestFrame()`**: cada chamada empurra exatamente
   um quadro, carimbado com a hora real. O ritmo deixa de depender do compositor.
3. **O blob não sai do navegador pelo CDP** — 3,4 MB em base64 travaram o
   `Runtime.evaluate` (o processo ficou pendurado). Solução: `_gerar-mp4.js` **serve a
   página por HTTP num servidor próprio** e o navegador **devolve o mp4 por POST**
   (mesma origem, sem CORS, sem limite de tamanho).
4. **`const scenes` é binding lexical, não é `window.scenes`.** Ao inspecionar o short
   de fora (iframe), ler as cenas pelo DOM: `querySelectorAll('svg.scene')`.

### ⚠️ Sempre conferir a duração

O piloto **recusa e apaga** o arquivo se `|duração real − duração esperada| > 0,6 s`.
Vídeo acelerado é o modo de falha silencioso desta técnica: o arquivo abre, tem
tamanho, parece certo — e está 1,6× mais rápido. **Nunca entregar sem essa checagem.**

E o `_mp4/conferir-mp4.py` é a segunda prova: abrir o mp4 e extrair quadros reais.
Tamanho de arquivo não prova que o vídeo decodifica.

### O que NÃO funcionou (para não tentar de novo)

- `--disable-gpu`: **piorou** (11,5 fps em vez de 18).
- Assar a cena a 405×720 e esticar: desnecessário. O custo real de assar + decodificar
  + desenhar é **~3,5 ms por quadro** (medido com `_mp4/bench.html`). **Medir antes de
  otimizar** — eu ia reescrever o pipeline por um gargalo que não existia.
- `--virtual-time-budget` **não** serve para medir tempo: ele virtualiza o relógio e
  destrói qualquer medição de `performance.now()`.'''

NEW = u'''## 🎬 Gerar o .mp4 de verdade (sem ffmpeg)

**Não existe ffmpeg nesta máquina — e não precisa.** O Chrome headless codifica
**H.264 dentro de MP4** nativamente
(`MediaRecorder.isTypeSupported('video/mp4;codecs=avc1.42E01E')` → `true`).
Quem desenha os quadros é o próprio navegador.

```bash
node _gerar-mp4.js <arquivo>.html                    # padrao 1080x1920 a 30
node _gerar-mp4.js --w=720 --fps=20 <arquivo>.html   # mais fluido, menos resolucao
node _gerar-mp4.js --todos                           # todos que ainda nao tem mp4
python _mp4/inspecionar.py <arquivo>.mp4             # duracao / resolucao / codec
node _mp4/quadros-mp4.js <arquivo>.mp4 8             # extrai 8 quadros -> PNG
node _mp4/rodar.js "file:///.../_mp4/bench6.html?arq=../<pasta>/<short>.html" 240 --file-access
```

- `_mp4/render.js` é o motor — **injetado na página, nunca gravado dentro do short**;
  `_gerar-mp4.js` é o piloto; `_mp4/inspecionar.py` lê o box `mvhd` na mão.
- Saída: **H.264 (`avc1`)**, mp4 fragmentado (YouTube aceita).
- **A marca d'água placeholder (`@yourchannel` / `@seucanal`) é omitida no mp4** — num
  arquivo gravado ela ficaria queimada para sempre. Só entra depois que o canal tiver nome.
- O piloto calcula a duração esperada somando os `ms:` do HTML.

### 🔴 O gargalo real é o codificador H.264 — e ele manda na taxa

**Medido, não suposto.** O que limita a taxa de quadros é o **codificador H.264 do
`MediaRecorder`, rodando em software**, e o custo dele acompanha a **área do quadro**:

| resolução | teto medido | pedindo 30 sai | pedindo o teto sai |
|---|---|---|---|
| 1080×1920 | **~11 fps** | 10,8 | 11,1 (pedindo 12) |
| 720×1280 | **~20 fps** | 19,0 | **16,1** (pedindo 20) |
| 540×960 | ~21 fps | 20,9 | — |

Consequências práticas:

- **Pedir mais do que o teto não acelera nada** — só faz o motor pedir quadros que não
  consegue desenhar. Em 1080×1920, pedindo 15 saiu **10,8 fps**, *menos* que os 11,1 que
  saem pedindo 12, e o vídeo encheu de quadros repetidos.
- **A troca é resolução × fluidez.** Em 18/09 o short do mosquito saiu **720×1280 a
  16,1 fps** (24 quadros repetidos de 919). Para conteúdo de traço fino e muito texto,
  1080×1920 é mais nítido e 720×1280 é mais fluido — **dizer a troca ao usuário e
  deixar o flag à mão** em vez de decidir calado.
- **O `--fps` é honesto**: o vídeo sai com os quadros que o motor conseguiu desenhar,
  não com os que foram pedidos. Conferir sempre `ritmo real:` no log.

### 🛠 Para medir rápido: um short curto

```bash
python _mp4/_criar-teste-curto.py     # cria _mp4/teste-8s.html (8 cenas, 7 s)
```
O render de verdade leva ~60 s; o curto leva ~8 s. Mantém as 8 cenas (o peso de cada
uma é o que importa) e só encurta a duração. **Apagar o teste depois** — senão um
`--todos` futuro o pega como se fosse um short de verdade.

### 🔴 Os 4 defeitos que custaram tempo — não repetir

1. **`requestAnimationFrame` no headless roda a ~11 Hz.** Não é o encoder nem o
   desenho: o rAF é servido pelo compositor, e sem tela ele tica devagar. O vídeo
   saía **32 s em vez de 53,5 s** porque o `MediaRecorder` carimbava 1/30 s por
   quadro entregue. **Usar `setTimeout(tick, 6)` com ritmo de relógio.**
2. **`captureStream(30)` amostra o canvas no tique do compositor.** Usar
   **`captureStream(0)` + `track.requestFrame()`**: cada chamada empurra exatamente
   um quadro, carimbado com a hora real. O ritmo deixa de depender do compositor.
3. **O blob não sai do navegador pelo CDP** — 3,4 MB em base64 travaram o
   `Runtime.evaluate` (o processo ficou pendurado). Solução: `_gerar-mp4.js` **serve a
   página por HTTP num servidor próprio** e o navegador **devolve o mp4 por POST**
   (mesma origem, sem CORS, sem limite de tamanho).
4. **`const scenes` é binding lexical, não é `window.scenes`.** Ao inspecionar o short
   de fora (iframe), ler as cenas pelo DOM: `querySelectorAll('svg.scene')`.

E mais dois, do dia 18/09:

5. **As 7 cenas escondidas continuam animando.** O CSS esconde cena com
   `visibility:hidden`, não `display:none` — as 64 animações das 8 cenas rodam a
   gravação inteira. O motor agora **pausa todas no início** e guarda os objetos de
   animação por cena (`animsPorCena`), mexendo só na cena da vez.
6. **O último quadro não era carimbado.** Parar a gravação no mesmo instante do último
   desenho encurtava o arquivo em **~1%** (0,6 s em 57 s) e a trava de duração
   reprovava um vídeo certo. Solução: segurar o último quadro **150 ms** antes de
   `rec.stop()`, e tolerância de duração **proporcional** (`max(0,6 s, 2%)`) em vez de
   0,6 s fixos.

### ⚠️ Sempre conferir: duração E quadros

O piloto **recusa e apaga** o arquivo se a duração desviar mais que `max(0,6 s, 2%)`.
Vídeo acelerado é o modo de falha silencioso desta técnica: o arquivo abre, tem
tamanho, parece certo — e está 1,6× mais rápido.

A segunda prova é **abrir o mp4 e olhar quadros de verdade**:
`node _mp4/quadros-mp4.js <arquivo>.mp4 8` → `_revisao/<nome>-mp4.png`.
Tamanho de arquivo não prova que o vídeo decodifica.

> **O verificador antigo (`_mp4/conferir-mp4.py`) foi REMOVIDO em 18/09** porque dava
> **veredito falso** de "8 quadros idênticos". Dois defeitos somados: (1) disparar 8
> `v.currentTime = t` de uma vez faz o navegador coalescer num único seek; (2) a "rede
> de segurança" de 1200 ms desenhava de qualquer jeito, e com `--virtual-time-budget`
> esse timer dispara na hora — então o canvas pegava o quadro já decodificado, não o
> buscado. **Não voltar a conferir por seek.** O `quadros-mp4.js` não busca: ele
> **toca** o vídeo e fotografa quando `mediaTime` cruza cada alvo
> (`requestVideoFrameCallback`), servindo o mp4 por HTTP com suporte a Range.

### 🔬 Como medir sem se enganar — três armadilhas que já custaram horas

1. **Latência não é custo.** `new Image()` → `onload` mede **espera na fila**, não
   tempo de thread principal. Um `rasterizar 83 ms` no log era fila, não CPU. O que
   importa é **quanto o thread principal ficou travado** — medir com uma sonda de
   `setTimeout(2)` rodando junto e somando o atraso (`bench5.html` / `bench6.html`).
2. **Rasterização em cache.** Se o bench reusa a **mesma** data URL, o Chrome devolve
   o bitmap já rasterizado e o custo medido vira ~0. Foi assim que o `bench2` deu
   "12,7 ms em 1080×1920" e o render de verdade mostrou outra coisa. **Cada quadro
   medido tem que ser diferente** (variar o `currentTime`).
3. **Iframe fora da tela não anima.** Com `left:-3000px` o Chrome não compõe a cena, e
   a medição não vale. O palco tem que estar **na tela**.

**Corolário:** o custo de rasterizar um SVG **não depende do tamanho do bitmap**
(1080 e 540 custam igual) — depende do documento. Então "renderizar menor para
acelerar" **não funciona**; o que funciona é **rasterizar menos vezes por segundo**.

### O que NÃO funcionou (para não tentar de novo)

- `--disable-gpu`: **piorou** (11,5 fps em vez de 18).
- **`createImageBitmap(blob)` para tirar a rasterização do thread principal:**
  o Chrome **não decodifica SVG por essa via** (`The source image could not be
  decoded`). Não há como mover a rasterização de SVG para um worker — é por isso que
  o teto de taxa existe.
- **Rasterizar menor (405/540) para acelerar: não acelera** e ainda piora a nitidez.
- `--virtual-time-budget` **não** serve para medir tempo: ele virtualiza o relógio e
  destrói qualquer medição de `performance.now()`.'''

d = io.open(ARQ, encoding='utf-8', newline='').read()
n = d.count(OLD)
print('ancora: %d ocorrencia(s) %s' % (n, 'OK' if n == 1 else '<-- FALHOU'))
if n != 1:
    print('ABORTADO: nada foi gravado.')
    sys.exit(1)
d = d.replace(OLD, NEW, 1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('GRAVADO: %s (%d bytes)' % (ARQ, len(d.encode('utf-8'))))
for t in ['quadros-mp4.js', 'conferir-mp4.py', 'createImageBitmap', '--w=720',
          'animsPorCena', '_criar-teste-curto.py', 'Latência não é custo']:
    print('  %-24s %d' % (t, d.count(t)))
