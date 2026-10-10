# -*- coding: utf-8 -*-
"""Atualiza o MEMORY.md do projeto: estado do mp4 + a licao do teto do codificador.
   Duas trocas, cada ancora com contagem exata. Aborta SEM GRAVAR se falhar."""
import io, os, sys

ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                   '.workbuddy-ai', 'memory', 'MEMORY.md')

A1_OLD = u'''**#16 `mosquito/shorts-mosquito-trap-en.html`** (armadilha de mosquito — **side track,
não é fermentação**).
Plano em `guias/plano-de-postagem.md`; upload em `guias/guia-de-upload.md`.'''

A1_NEW = u'''**#16 `mosquito/shorts-mosquito-trap-en.html`** (armadilha de mosquito — **side track,
não é fermentação**).
Plano em `guias/plano-de-postagem.md`; upload em `guias/guia-de-upload.md`.

- **#16 é o único com .mp4 pronto:** `mosquito/shorts-mosquito-trap-en.mp4`
  (720×1280, H.264, 57 s, ~16 fps). Os outros 15 ainda dependem de gravação de tela.'''

A2_OLD = u'## 🚧 Pendências'

A2_NEW = u'''## 🎬 O .mp4 (18/09) — o teto é do codificador, não do desenho

`node _gerar-mp4.js [--w=720] [--fps=20] <arq>.html` grava **H.264/MP4 sem ffmpeg**
(Chrome headless + `MediaRecorder`). O detalhe técnico está na skill
(`shorts-svg-animado` → "Gerar o .mp4 de verdade"). O que vale lembrar aqui:

- **O teto de taxa é o codificador H.264 em software, e acompanha a ÁREA do quadro:**
  **~11 fps em 1080×1920**, **~20 fps em 720×1280**. Pedir mais que o teto **piora** —
  em 1080, pedir 15 deu 10,8 fps e pedir 12 deu 11,1.
- **A troca é resolução × fluidez, e quem decide é o usuário.** O #16 saiu
  **720×1280 a 16 fps**; `--w=1080 --fps=12` é a versão nítida e mais travada.
- **O `--fps` é um pedido, não uma promessa.** Conferir `ritmo real:` no log.
- **Conferir o vídeo é TOCAR, não buscar:** `node _mp4/quadros-mp4.js <arq>.mp4 8`.
  O verificador antigo por seek (`conferir-mp4.py`) foi **removido** — dava veredito
  falso de "quadros idênticos" e já me fez achar que um vídeo bom estava travado.
- **Para medir, duas armadilhas:** latência não é custo (usar sonda de travamento), e
  rasterização em cache mede ~0 (cada quadro medido tem que ser único).

## 🚧 Pendências'''

d = io.open(ARQ, encoding='utf-8', newline='').read()
falhou = False
for nome, old in [('catalogo', A1_OLD), ('pendencias', A2_OLD)]:
    n = d.count(old)
    print('%-12s ocorrencias: %d %s' % (nome, n, 'OK' if n == 1 else '<-- FALHOU'))
    if n != 1:
        falhou = True
if falhou:
    print('\nABORTADO: nada foi gravado.')
    sys.exit(1)

d = d.replace(A1_OLD, A1_NEW, 1).replace(A2_OLD, A2_NEW, 1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('\nGRAVADO: %s (%d bytes)' % (ARQ, len(d.encode('utf-8'))))
for t in ['shorts-mosquito-trap-en.mp4', '~11 fps em 1080×1920', 'quadros-mp4.js',
          'O .mp4 (18/09)']:
    print('  %-28s %d' % (t, d.count(t)))
