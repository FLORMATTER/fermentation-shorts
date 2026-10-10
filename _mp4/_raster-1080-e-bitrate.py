# -*- coding: utf-8 -*-
"""1. Rasterizar o SVG SEMPRE em 1080x1920, independente do tamanho do mp4.
      O custo de rasterizar um SVG nao depende do tamanho do bitmap (medido em
      bench4/bench7), mas o custo de CODAR depende — entao da para gravar em
      540x960 (rapido) recebendo a arte rasterizada em 1080 e reduzida no
      drawImage. Isso e' supersampling: o 540x960 sai bem mais nitido do que
      rasterizar direto em 540.
   2. Bitrate padrao 1 Mbps (configuravel por --kbps=). O codificador e' o
      gargalo e o bitrate mexe nele: em 720, 8 Mbps -> 10,2 q/s e 2 Mbps -> 13,7.
      O arquivo entregue tinha ~0,7 Mbps REAL, entao 1 Mbps de teto nao corta nada.

   Cada ancora tem que casar EXATAMENTE uma vez, senao aborta sem gravar."""
import io, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDER = os.path.join(RAIZ, '_mp4', 'render.js')
DRIVER = os.path.join(RAIZ, '_gerar-mp4.js')

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

t_render = [
    (
        '  var BITRATE = 8000 * 1000;',
        '''  /* 1 Mbps de teto. O arquivo de 720p entregue tinha ~0,7 Mbps REAIS (arte
     chapada comprime muito), entao o teto nao corta qualidade — e o bitrate e'
     um botao do codificador, que e' o gargalo. Em 720: 8 Mbps -> 10,2 q/s,
     2 Mbps -> 13,7 q/s. */
  var BITRATE = (function () {
    var m = /[?&]mp4kbps=(\\d+)/.exec(location.search);
    return (m ? parseInt(m[1], 10) : 1000) * 1000;
  })();'''
    ),
    (
        '  var S = W / 405;                 // o cartao e 405x720; o canvas e WxH',
        '''  /* RAS = tamanho em que o SVG e' rasterizado, SEMPRE 1080x1920, mesmo que o
     mp4 saia em 540x960. Rasterizar um SVG custa quase o mesmo em qualquer
     tamanho (medido), mas CODIFICAR custa por area — entao rasterizar grande e
     reduzir no drawImage da supersampling de graca: o 540x960 sai nitido. */
  var RAS = 1080;
  var RASH = Math.round(RAS * 720 / 405);
  var S = W / 405;                 // o cartao e 405x720; o canvas e WxH'''
    ),
    (
        """    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    clone.setAttribute('width', W);
    clone.setAttribute('height', H);""",
        """    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    clone.setAttribute('width', RAS);
    clone.setAttribute('height', RASH);"""
    ),
    (
        """    var t = '<svg xmlns="http://www.w3.org/2000/svg" width="' + W + '" height="' + H +
            '" viewBox="0 0 405 720">' +""",
        """    var t = '<svg xmlns="http://www.w3.org/2000/svg" width="' + RAS + '" height="' + RASH +
            '" viewBox="0 0 405 720">' +"""
    ),
]

t_driver = [
    (
        "const alvos = process.argv.slice(2).filter(a => !/^--(w|fps)=\\d+$/.test(a));",
        "const alvos = process.argv.slice(2).filter(a => !/^--(w|fps|kbps)=\\d+$/.test(a));"
    ),
    (
        "const TAXA = (function () {\n  const a = process.argv.find(x => /^--fps=\\d+$/.test(x));\n  return a ? parseInt(a.slice(6), 10) : 30;\n})();",
        "const TAXA = (function () {\n  const a = process.argv.find(x => /^--fps=\\d+$/.test(x));\n  return a ? parseInt(a.slice(6), 10) : 30;\n})();\n"
        "/* teto de bitrate em kbps (padrao 1000). O codificador e' o gargalo e o\n"
        "   bitrate mexe nele. */\n"
        "const KBPS = (function () {\n  const a = process.argv.find(x => /^--kbps=\\d+$/.test(x));\n  return a ? parseInt(a.slice(7), 10) : 1000;\n})();"
    ),
    (
        "    'http://127.0.0.1:' + porta + '/short.html?mp4w=' + LARGURA + '&mp4fps=' + TAXA,",
        "    'http://127.0.0.1:' + porta + '/short.html?mp4w=' + LARGURA + '&mp4fps=' + TAXA +\n"
        "      '&mp4kbps=' + KBPS,"
    ),
]

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
for caminho, termos in [(RENDER, ['var RAS = 1080', 'mp4kbps=', "clone.setAttribute('width', RAS)", 'BITRATE']),
                        (DRIVER, ['const KBPS', 'kbps=', '--(w|fps|kbps)'])]:
    with io.open(caminho, encoding='utf-8') as f:
        d = f.read()
    print('  ' + os.path.basename(caminho) + ': ' +
          ', '.join('%s=%d' % (t, d.count(t)) for t in termos))
