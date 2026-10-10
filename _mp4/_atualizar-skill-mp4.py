# -*- coding: utf-8 -*-
"""Atualiza a skill shorts-svg-animado: agora existe export .mp4 de verdade.
   Aborta SEM GRAVAR se qualquer ancora nao casar exatamente 1 vez."""
import io, sys

ARQ = r'C:\Users\Saxa\.workbuddy-ai\skills\shorts-svg-animado\SKILL.md'

A1_OLD = """  autocontidos que o usuário grava a tela para virar .mp4. Formato padrão da série:"""
A1_NEW = """  autocontidos. Também entrega o .mp4 de verdade, gerado pelo próprio Chrome headless
  (sem ffmpeg) — ver a seção "Gerar o .mp4 de verdade". Formato padrão da série:"""

A2_OLD = """Isso deve ser explicado em UMA frase, sem drama, e a entrega deve vir em seguida.
Nunca prometer gerar .mp4."""
A2_NEW = """Isso deve ser explicado em UMA frase, sem drama, e a entrega deve vir em seguida.

**Mas o .mp4 existe e é para entregar.** O produto não gera vídeo por IA — quem
codifica é o **Chrome headless desta máquina**, em H.264/MP4, sem ffmpeg. Se o usuário
pedir "um mp4", **não recuse**: rode `node _gerar-mp4.js <short>.html` (ver a seção
"🎬 Gerar o .mp4 de verdade"). Gravar a tela virou o plano B."""

A3_OLD = """## 🗂 Organizar as pastas do projeto (quando a raiz estiver cheia)"""

A3_NEW = """## 🎬 Gerar o .mp4 de verdade (sem ffmpeg)

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
  destrói qualquer medição de `performance.now()`.

## 🗂 Organizar as pastas do projeto (quando a raiz estiver cheia)"""

SUBS = [('descricao da skill', A1_OLD, A1_NEW),
        ('secao "Por que existe"', A2_OLD, A2_NEW),
        ('nova secao do mp4', A3_OLD, A3_NEW)]

d = io.open(ARQ, encoding='utf-8', newline='').read()
falhou = False
for nome, old, new in SUBS:
    n = d.count(old)
    print('%-24s ocorrencias: %d %s' % (nome, n, 'OK' if n == 1 else '<-- FALHOU'))
    if n != 1:
        falhou = True
if falhou:
    print('\nABORTADO: nada foi gravado.')
    sys.exit(1)

io.open(ARQ + '.antes-do-mp4', 'w', encoding='utf-8', newline='').write(d)
for nome, old, new in SUBS:
    d = d.replace(old, new, 1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('\nGRAVADO: %s (%d -> %d bytes)' % (ARQ, len(io.open(ARQ + '.antes-do-mp4', encoding='utf-8', newline='').read()), len(d)))
