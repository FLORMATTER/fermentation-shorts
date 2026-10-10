# -*- coding: utf-8 -*-
"""Conserta o _mp4/render.js: ritmo e legenda.
   Aborta SEM GRAVAR se qualquer ancora nao casar exatamente 1 vez."""
import io, sys

ARQ = '_mp4/render.js'

# 1) fila menor: cada bake() forca recalc de estilo na pagina inteira
A1_OLD = "  var W = 1080, H = 1920, FPS = 30, LOOK = 48;"
A1_NEW = ("  var W = 1080, H = 1920, FPS = 30, LOOK = 6;\n"
          "  /* LOOK era 48. Cada bake() mexe em classList e em animation.currentTime, e\n"
          "     isso forca um recalculo de estilo na pagina TODA (8 cenas, ~800 nos).\n"
          "     Com 48 quadros assados por tique o navegador gastava ~100 ms por quadro\n"
          "     desenhado: o short saia a 10 quadros/s. Com fila curta sobra tempo. */")

# 2) nao mexer nas classes se a cena nao mudou
A2_OLD = """    var id = scenes[idx].id;
    for (var n = 0; n < scenes.length; n++) {
      var el = document.getElementById(scenes[n].id);
      if (n === idx) el.classList.add('on'); else el.classList.remove('on');
    }"""
A2_NEW = """    var id = scenes[idx].id;
    /* so troca as classes quando a cena MUDA — trocar a cada quadro invalidava o
       estilo das 8 cenas e era metade do custo de assar */
    if (cenaLigada !== idx) {
      for (var n = 0; n < scenes.length; n++) {
        var el = document.getElementById(scenes[n].id);
        if (n === idx) el.classList.add('on'); else el.classList.remove('on');
      }
      cenaLigada = idx;
    }"""
A2_ANCHOR2 = "  var animados = indexarAnimados();"
A2_ANCHOR2_NEW = "  var animados = indexarAnimados();\n  var cenaLigada = -1;"

# 3) a legenda tem que ser redesenhada TODO quadro: a imagem da cena cobre o canvas inteiro
A3_OLD = """    /* O overlay so muda quando a cena muda — redesenhar 1080x1920 a cada quadro
       e trabalho jogado fora; a legenda fica no canvas entre as trocas de cena. */
    if (info.idx !== ultimoIdx) {
      if (ovImg[info.idx]) cx.drawImage(ovImg[info.idx], 0, 0, W, H);
      ultimoIdx = info.idx;
    } else {
      cx.fillStyle = 'rgba(0,0,0,.12)';
      cx.fillRect(0, 0, W, 4 * S);
    }"""
A3_NEW = """    /* O overlay TEM que ser redesenhado a cada quadro. A imagem da cena cobre o
       canvas inteiro (405x720 com fundo solido), entao "desenhar so quando a cena
       muda" apagava a barra de legenda: o video saiu sem legenda nenhuma. */
    if (ovImg[info.idx]) cx.drawImage(ovImg[info.idx], 0, 0, W, H);"""

SUBS = [('fila LOOK=6', A1_OLD, A1_NEW),
        ('var cenaLigada', A2_ANCHOR2, A2_ANCHOR2_NEW),
        ('nao trocar classes', A2_OLD, A2_NEW),
        ('legenda todo quadro', A3_OLD, A3_NEW)]

d = io.open(ARQ, encoding='utf-8', newline='').read()
falhou = False
for nome, old, new in SUBS:
    n = d.count(old)
    print('%-22s ocorrencias: %d %s' % (nome, n, 'OK' if n == 1 else '<-- FALHOU'))
    if n != 1:
        falhou = True
if falhou:
    print('\nABORTADO: nada foi gravado.')
    sys.exit(1)
for nome, old, new in SUBS:
    d = d.replace(old, new, 1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('\nGRAVADO: %s' % ARQ)
