# _mp4/_consertar-fim.py
# 1. render.js: segura o ultimo quadro antes de parar a gravacao.
# 2. _gerar-mp4.js: tolerancia de duracao PROPORCIONAL.
#
# Por que: o arquivo sai ~1% mais curto que a conta do HTML (o codificador nao
# carimba direito o ultimo quadro se a gravacao parar na mesma hora). Em 7 s isso
# da 0,1 s e passa; em 57 s da 0,6 s e a trava de 0,6 s FIXOS rejeitava um video
# que estava certo. Tolerancia proporcional aceita o 1% sem aceitar erro de
# verdade (2x acelerado continua sendo recusado).
import io, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

problemas = []
def aplicar(caminho, trocas, nome):
    with io.open(caminho, encoding='utf-8') as f:
        d = f.read()
    crlf = '\r\n' in d
    def N(s):
        return s.replace('\n', '\r\n') if crlf else s
    for i, (velho, novo) in enumerate(trocas, 1):
        c = d.count(N(velho))
        if c != 1:
            problemas.append('%s troca %d: casou %d vez(es), esperava 1' % (nome, i, c))
            return None
    for velho, novo in trocas:
        d = d.replace(N(velho), N(novo))
    return d

RENDER = os.path.join(RAIZ, '_mp4', 'render.js')
DRIVER = os.path.join(RAIZ, '_gerar-mp4.js')

t_render = [(
    '''        ' | atraso do timer ' + (perfLagN ? (perfLag / perfLagN).toFixed(1) : '-') + ' ms');
      rec.stop();
      return;''',
    '''        ' | atraso do timer ' + (perfLagN ? (perfLag / perfLagN).toFixed(1) : '-') + ' ms');
      /* segura o ultimo quadro antes de parar. Se parar na mesma hora, o
         codificador nao carimba o quadro final e o arquivo sai ~1% mais curto
         que a conta do HTML — em 57 s isso da 0,6 s. */
      setTimeout(function () { rec.stop(); }, 150);
      return;'''
)]

t_driver = [(
    '''    if (Math.abs(real - dur) > 0.6) {''',
    '''    /* tolerancia PROPORCIONAL: o codificador sempre perde ~1% no fim (o ultimo
       quadro nao e carimbado). 0,6 s fixos reprovavam um video de 57 s que estava
       certo e aprovavam 0,6 s de erro num video de 5 s. */
    const tol = Math.max(0.6, dur * 0.02);
    if (Math.abs(real - dur) > tol) {'''
)]

r = aplicar(RENDER, t_render, 'render.js')
d2 = aplicar(DRIVER, t_driver, '_gerar-mp4.js')

if problemas:
    print('ABORTADO, nada foi gravado:')
    for p in problemas:
        print('  ' + p)
    sys.exit(1)

with io.open(RENDER, 'w', encoding='utf-8', newline='') as f:
    f.write(r)
with io.open(DRIVER, 'w', encoding='utf-8', newline='') as f:
    f.write(d2)

print('ok')
with io.open(RENDER, encoding='utf-8') as f:
    d = f.read()
print('  render.js  segura-ultimo-quadro: %d | rec.stop(): %d' %
      (d.count('setTimeout(function () { rec.stop(); }, 150)'), d.count('rec.stop();')))
with io.open(DRIVER, encoding='utf-8') as f:
    d = f.read()
print('  _gerar-mp4.js  const tol: %d' % d.count('const tol = Math.max(0.6, dur * 0.02);'))
