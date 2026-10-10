# -*- coding: utf-8 -*-
"""Contexto 2D sem alfa e dessincronizado.

   O canvas e opaco (todas as cenas tem fundo solido) e nao precisa de
   sincronizacao com a tela. `alpha:false` tira a composicao de alfa do caminho
   quente e `desynchronized:true` evita uma copia. Nenhum dos dois mexe na
   qualidade da imagem — e de graca, entao vale medir antes de baixar resolucao.
   Aborta SEM GRAVAR se a ancora nao casar exatamente 1 vez."""
import io, os, sys

ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render.js')

OLD = "  var cx = cv.getContext('2d');"
NEW = """  /* alpha:false -> o canvas e opaco (as cenas tem fundo solido); tirar o canal
     alfa do caminho quente acelera a rasterizacao e a copia para o codificador.
     desynchronized:true -> nao ha tela para sincronizar, a gravacao le o canvas
     direto. Nenhum dos dois muda um pixel do que sai. */
  var cx = cv.getContext('2d', { alpha: false, desynchronized: true });"""

d = io.open(ARQ, encoding='utf-8', newline='').read()
n = d.count(OLD)
print('ancora: %d ocorrencia(s) %s' % (n, 'OK' if n == 1 else '<-- FALHOU'))
if n != 1:
    print('ABORTADO: nada foi gravado.')
    sys.exit(1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d.replace(OLD, NEW, 1))
print('GRAVADO: %s' % ARQ)
print('  getContext com opcoes: %d' % d.count("getContext('2d', { alpha: false"))
