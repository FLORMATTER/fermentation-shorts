# _mp4/_tamanho-configuravel.py
# Deixa o tamanho do quadro e a taxa de quadros virarem opcao de linha de comando:
#     node _gerar-mp4.js --w=720 --fps=30 <arquivo.html>
#
# Por que: medido, o gargalo e o codificador H.264 do MediaRecorder rodando em
# software — ~69 ms por quadro em 1080x1920, o que limita a ~14 quadros/s.
# O custo do codificador acompanha a AREA do quadro, entao baixar a resolucao
# compra taxa de quadros. Com a opcao da para medir o cambio em vez de supor.
#
# Cada ancora tem que casar EXATAMENTE uma vez, senao aborta sem gravar.
import io, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVER = os.path.join(RAIZ, '_gerar-mp4.js')
RENDER = os.path.join(RAIZ, '_mp4', 'render.js')

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
    return d, crlf

# ---------- 1. render.js: le a largura e a taxa da URL ----------
t_render = [
    (
        '  var W = 1080, H = 1920, FPS = 15, LOOK = 3;',
        '''  /* Tamanho e taxa vem da URL (o _gerar-mp4.js injeta ?mp4w=&mp4fps=).
     Padrao 1080x1920 a 30. O gargalo de verdade e o codificador H.264 do
     MediaRecorder, que roda em software: ~69 ms por quadro em 1080x1920, o que
     segura tudo em ~14 quadros/s. O custo acompanha a AREA do quadro, entao
     baixar a resolucao compra taxa. */
  var W = (function () { var m = /[?&]mp4w=(\\d+)/.exec(location.search); return m ? parseInt(m[1], 10) : 1080; })();
  var H = Math.round(W * 16 / 9);
  var FPS = (function () { var m = /[?&]mp4fps=(\\d+)/.exec(location.search); return m ? parseInt(m[1], 10) : 30; })();
  var LOOK = 3;'''
    ),
    (
        '  var S = W / 405;                 // o cartao e 405x720; o canvas e 1080x1920',
        '  var S = W / 405;                 // o cartao e 405x720; o canvas e WxH'
    ),
]
r = aplicar(RENDER, t_render, 'render.js')

# ---------- 2. _gerar-mp4.js: aceita --w= e --fps= ----------
t_driver = [
    (
        "const CDP_PORT = 9333;",
        '''const CDP_PORT = 9333;
/* --w=NNN e --fps=NN sobrescrevem o tamanho/taxa do mp4 (padrao 1080x1920 a 30).
   O custo de codificar acompanha a area, entao isso e o botao de troca entre
   resolucao e fluidez. */
const LARGURA = (function () {
  const a = process.argv.find(x => /^--w=\\d+$/.test(x));
  return a ? parseInt(a.slice(4), 10) : 1080;
})();
const TAXA = (function () {
  const a = process.argv.find(x => /^--fps=\\d+$/.test(x));
  return a ? parseInt(a.slice(6), 10) : 30;
})();'''
    ),
    (
        "    '--window-size=1080,1920', '--force-device-scale-factor=1',",
        "    '--window-size=' + LARGURA + ',' + Math.round(LARGURA * 16 / 9),\n"
        "    '--force-device-scale-factor=1',"
    ),
    (
        "    'http://127.0.0.1:' + porta + '/short.html',",
        "    'http://127.0.0.1:' + porta + '/short.html?mp4w=' + LARGURA + '&mp4fps=' + TAXA,"
    ),
]
d2 = aplicar(DRIVER, t_driver, '_gerar-mp4.js')

if problemas:
    print('ABORTADO, nada foi gravado:')
    for p in problemas:
        print('  ' + p)
    sys.exit(1)

with io.open(RENDER, 'w', encoding='utf-8', newline='') as f:
    f.write(r[0])
with io.open(DRIVER, 'w', encoding='utf-8', newline='') as f:
    f.write(d2[0])

print('ok: render.js e _gerar-mp4.js atualizados')
for caminho, termos in [(RENDER, ['mp4w=', 'mp4fps=', 'var LOOK = 3']),
                        (DRIVER, ['const LARGURA', 'const TAXA', '?mp4w='])]:
    with io.open(caminho, encoding='utf-8') as f:
        d = f.read()
    print('  ' + os.path.basename(caminho) + ': ' +
          ', '.join('%s=%d' % (t, d.count(t)) for t in termos))
