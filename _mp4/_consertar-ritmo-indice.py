# -*- coding: utf-8 -*-
"""Troca o limite de TEMPO do desenho pelo INDICE do quadro.

   O defeito: a versao anterior desenhava so quando
       t - ultimoDesenho >= 1/FPS - 1
   Mas o tique roda MAIS RAPIDO que o intervalo do quadro, entao a condicao ficava
   falsa em tiques inteiros e o motor pulava quadros:

       540x960@30   tique 26,3 ms | limite 32,3 ms -> desenhava 1 a cada 2 tiques
       1080x1920@12 tique 11,5 ms | limite 82,3 ms -> desenhava 1 a cada 8 tiques

   Isso explica os 20,9 e os 11,1 quadros/s medidos — o teto NAO era o codificador
   H.264, como eu tinha concluido. Comparando o INDICE do quadro, todo tique que
   avanca o quadro desenha, e a taxa passa a ser a que o motor aguenta de verdade.

   Cada ancora tem que casar EXATAMENTE uma vez, senao aborta sem gravar."""
import io, os, sys

ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render.js')

A1_OLD = '''  var ultimoIdx = -1, desenhados = 0, ultimoDesenho = -1;
  var INTERVALO = 1000 / FPS;
  var t0 = null;'''

A1_NEW = '''  var ultimoIdx = -1, desenhados = 0, ultimoDesenho = -1;
  var INTERVALO = 1000 / FPS;
  var ultimoFrame = -1;
  var t0 = null;'''

A2_OLD = '''    /* 1. DESENHAR PRIMEIRO. O relogio da gravacao manda: o quadro tem que sair
       na hora certa mesmo que assar esteja atrasado. */
    if (t - ultimoDesenho >= INTERVALO - 1) {
      ultimoDesenho = t;
      desenha(Math.floor(t / 1000 * FPS), t);
      track.requestFrame();
    }'''

A2_NEW = '''    /* 1. DESENHAR PRIMEIRO, guiado pelo INDICE do quadro — nao por um limite de
       tempo. A versao anterior desenhava so quando t - ultimoDesenho >= 1/FPS - 1,
       e como o tique roda MAIS RAPIDO que o intervalo do quadro ela ficava falsa em
       tiques inteiros: com tique a 26 ms e limite de 32 ms, desenhava 1 a cada 2
       tiques. Era isso que segurava o video em 11-21 quadros/s — nao o codificador.
       Comparando indices, todo tique que avanca o quadro desenha, e quando o motor
       nao acompanha ele entrega o quadro ATUAL (nao acumula atraso). */
    var f = Math.floor(t / 1000 * FPS);
    if (f > ultimoFrame) {
      ultimoFrame = f;
      desenha(f, t);
      track.requestFrame();
    }'''

A3_OLD = '''    var f = Math.floor(t / 1000 * FPS);
    var limite = performance.now() + ORCAMENTO;'''

A3_NEW = '''    var limite = performance.now() + ORCAMENTO;'''

d = io.open(ARQ, encoding='utf-8', newline='').read()
falhou = False
for nome, old in [('ultimoFrame', A1_OLD), ('bloco de desenho', A2_OLD), ('f duplicado', A3_OLD)]:
    n = d.count(old)
    print('%-18s ocorrencias: %d %s' % (nome, n, 'OK' if n == 1 else '<-- FALHOU'))
    if n != 1:
        falhou = True
if falhou:
    print('\nABORTADO: nada foi gravado.')
    sys.exit(1)

d = d.replace(A1_OLD, A1_NEW, 1).replace(A2_OLD, A2_NEW, 1).replace(A3_OLD, A3_NEW, 1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('\nGRAVADO: %s' % ARQ)
for t in ['ultimoFrame', 'if (f > ultimoFrame)', 'var f = Math.floor(t / 1000 * FPS);']:
    print('  %-38s %d' % (t, d.count(t)))
