# -*- coding: utf-8 -*-
"""Deixa o _mp4/quadros-mp4.js aceitar tempos explicitos:
       node _mp4/quadros-mp4.js <arq>.mp4 8 --tempos=0.5,4.4,30,56.5
   Sem isso a amostragem e sempre uniforme, e as pontas (0 s e o fim) nunca eram
   conferidas — justo onde o MediaRecorder costuma deixar quadro em branco.
   Duas trocas, cada ancora com contagem exata. Aborta SEM GRAVAR se falhar."""
import io, os, sys

ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quadros-mp4.js')

A1_OLD = "const N = parseInt(process.argv[3] || '8', 10);"
A1_NEW = """const N = parseInt(process.argv[3] || '8', 10);
/* --tempos=0.5,4.4,30,56.5 : amostra estes instantes em vez de dividir por igual.
   Serve para conferir as PONTAS (0 s e o fim), onde o MediaRecorder costuma
   deixar quadro em branco. */
const TEMPOS = (function () {
  const a = process.argv.find(x => x.indexOf('--tempos=') === 0);
  return a ? a.slice(9).split(',').map(Number).filter(n => !isNaN(n)) : [];
})();"""

A2_OLD = """  var passo = DUR / (N + 1);
  for (var j = 1; j <= N; j++){
    alvos.push(passo * j);
    var cv = document.createElement('canvas');
    cv.width = 540; cv.height = 960;
    var fig = document.createElement('figure');
    var cp = document.createElement('figcaption');
    cp.textContent = 't = ' + (passo * j).toFixed(1) + 's';
    fig.appendChild(cv); fig.appendChild(cp); g.appendChild(fig);
    cvs.push({ cv: cv, ok: false });
  }"""

A2_NEW = """  var pedidos = ${JSON.stringify(TEMPOS)};
  if (pedidos.length) { alvos = pedidos.slice(); N = alvos.length; }
  else { var passo = DUR / (N + 1); for (var q = 1; q <= N; q++) alvos.push(passo * q); }
  for (var j = 0; j < alvos.length; j++){
    var cv = document.createElement('canvas');
    cv.width = 540; cv.height = 960;
    var fig = document.createElement('figure');
    var cp = document.createElement('figcaption');
    cp.textContent = 't = ' + alvos[j].toFixed(1) + 's';
    fig.appendChild(cv); fig.appendChild(cp); g.appendChild(fig);
    cvs.push({ cv: cv, ok: false });
  }"""

d = io.open(ARQ, encoding='utf-8', newline='').read()
falhou = False
for nome, old in [('argv', A1_OLD), ('pagina', A2_OLD)]:
    n = d.count(old)
    print('%-8s ocorrencias: %d %s' % (nome, n, 'OK' if n == 1 else '<-- FALHOU'))
    if n != 1:
        falhou = True
if falhou:
    print('\nABORTADO: nada foi gravado.')
    sys.exit(1)

d = d.replace(A1_OLD, A1_NEW, 1).replace(A2_OLD, A2_NEW, 1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('\nGRAVADO: %s' % ARQ)
for t in ['--tempos=', 'var pedidos = ', 'if (pedidos.length)']:
    print('  %-24s %d' % (t, d.count(t)))
