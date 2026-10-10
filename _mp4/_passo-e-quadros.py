"""_mp4/_passo-e-quadros.py — poe o PASSO (intervalo minimo entre quadros) no
render.js e no _gerar-mp4.js.

Por que: o MediaRecorder DESCARTA quadro quando a fila do codificador enche.
Medido: 76% dos quadros sobreviveram em CFR a 19 q/s, e 74% em tempo real. Quadro
descartado e' pior que quadro repetido — o anterior fica 2x mais tempo na tela e
o olho le isso como travamento. Em CFR o relogio nao importa, entao da' para
alimentar devagar de proposito e nao perder nenhum.

Ancoras com contagem exata; aborta sem gravar se alguma nao for unica.
"""
import sys

trocas_render = [
    (
        "  var CFR = /[?&]mp4cfr=1/.test(location.search);\n",
        """  var CFR = /[?&]mp4cfr=1/.test(location.search);
  /* PASSO = intervalo MINIMO entre quadros, em ms. Em CFR o relogio nao importa
     (o arquivo e' retimado no fim), mas o MediaRecorder DESCARTA quadro quando a
     fila do codificador enche: medido, sobreviveu so 76% dos quadros a 19 q/s.
     Quadro descartado e' pior que quadro repetido — o anterior fica o DOBRO do
     tempo na tela e o olho le isso como travamento. Entao alimenta devagar. */
  var PASSO = (function () {
    var m = /[?&]mp4passo=(\\d+)/.exec(location.search);
    return m ? parseInt(m[1], 10) : 0;
  })();
""",
    ),
    (
        "    setTimeout(tickCFR, 0);",
        "    setTimeout(tickCFR, PASSO);",
    ),
    (
        """      L('CFR: ' + totalFrames + ' quadros em ' + gasto.toFixed(1) + ' s (' +
        (totalFrames / gasto).toFixed(1) + ' quadros/s de render) — sem repetidos por construcao');""",
        """      L('CFR: ' + totalFrames + ' quadros em ' + gasto.toFixed(1) + ' s (' +
        (totalFrames / gasto).toFixed(1) + ' quadros/s de render, passo ' + PASSO +
        ' ms) — sem repetidos por construcao');""",
    ),
]

trocas_driver = [
    (
        "const CFR = process.argv.includes('--cfr=1');\n",
        """const CFR = process.argv.includes('--cfr=1');
/* --passo=NN = intervalo minimo entre quadros em CFR, em ms. Existe para NAO
   perder quadro: o MediaRecorder descarta quando a fila do codificador enche. */
const PASSO = (function () {
  const a = process.argv.find(x => /^--passo=\\d+$/.test(x));
  return a ? parseInt(a.slice(8), 10) : 0;
})();
""",
    ),
    (
        "      '&mp4kbps=' + KBPS + (CFR ? '&mp4cfr=1' : ''),",
        "      '&mp4kbps=' + KBPS + (CFR ? '&mp4cfr=1' : '') + (PASSO ? '&mp4passo=' + PASSO : ''),",
    ),
    (
        """      console.log('  duracao : crua ' + real.toFixed(1) + 's (ritmo do render) — falta rodar');""",
        """      console.log('  duracao : crua ' + real.toFixed(1) + 's (ritmo do render) — falta rodar');
      console.log('            (passo ' + PASSO + ' ms)');""",
    ),
]

for arq, trocas in (('_mp4/render.js', trocas_render), ('_gerar-mp4.js', trocas_driver)):
    d = open(arq, encoding='utf-8').read()
    orig = d
    for i, (velho, novo) in enumerate(trocas, 1):
        n = d.count(velho)
        print('%s troca %d: casou %d vez(es)' % (arq, i, n))
        if n != 1:
            print('ABORTADO: ancora nao unica. Nada foi gravado.')
            sys.exit(1)
        d = d.replace(velho, novo, 1)
    assert d != orig
    open(arq, 'w', encoding='utf-8', newline='').write(d)
    print('gravado: %s (%d -> %d bytes)' % (arq, len(orig), len(d)))
