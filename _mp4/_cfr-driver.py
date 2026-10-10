"""_mp4/_cfr-driver.py — poe a opcao --cfr=1 no _gerar-mp4.js.

Em CFR o arquivo cru sai com a duracao do RENDER (mais longa que o video), entao
o portao de duracao do driver nao vale: quem poe a taxa certa e' o retimar.py.
Todas as ancoras com contagem exata; aborta sem gravar se alguma nao for unica.
"""
import sys

ARQ = '_gerar-mp4.js'
d = open(ARQ, encoding='utf-8').read()
orig = d

trocas = []

trocas.append((
    """   Uso:  node _gerar-mp4.js mosquito/shorts-mosquito-trap-en.html
         node _gerar-mp4.js --todos          (todo short que ainda nao tem mp4)
""",
    """   Uso:  node _gerar-mp4.js mosquito/shorts-mosquito-trap-en.html
         node _gerar-mp4.js --todos          (todo short que ainda nao tem mp4)

   Opcoes: --w=NNN (largura, padrao 1080)   --fps=NN (taxa, padrao 30)
           --kbps=NNN (bitrate, padrao 1000)  --cfr=1 (taxa constante)

   --cfr=1 e' o modo BOM: grava um quadro por indice, sem olhar o relogio, e
   depois e' so rodar  python _mp4/retimar.py <saida>.mp4  para o arquivo tocar
   em taxa constante com TODOS os quadros distintos. O modo padrao (tempo real)
   repete quadro quando o codificador nao acompanha, e quadro repetido = a
   animacao travando entre quadros.
""",
))

trocas.append((
    """const KBPS = (function () {
  const a = process.argv.find(x => /^--kbps=\\d+$/.test(x));
  return a ? parseInt(a.slice(7), 10) : 1000;
})();
""",
    """const KBPS = (function () {
  const a = process.argv.find(x => /^--kbps=\\d+$/.test(x));
  return a ? parseInt(a.slice(7), 10) : 1000;
})();
/* --cfr=1 = TAXA CONSTANTE. O render desenha todos os quadros o mais rapido que
   a maquina der (sem olhar o relogio) e o _mp4/retimar.py reescreve a duracao
   de cada amostra. Assim nenhum quadro repete. */
const CFR = process.argv.includes('--cfr=1');
""",
))

trocas.append((
    "const alvos = process.argv.slice(2).filter(a => !/^--(w|fps|kbps)=\\d+$/.test(a));",
    "const alvos = process.argv.slice(2).filter(a => !/^--[a-z]+=\\d+$/.test(a));",
))

trocas.append((
    """    'http://127.0.0.1:' + porta + '/short.html?mp4w=' + LARGURA + '&mp4fps=' + TAXA +
      '&mp4kbps=' + KBPS,""",
    """    'http://127.0.0.1:' + porta + '/short.html?mp4w=' + LARGURA + '&mp4fps=' + TAXA +
      '&mp4kbps=' + KBPS + (CFR ? '&mp4cfr=1' : ''),""",
))

trocas.append((
    """    const t0 = Date.now();
    let ultimoPct = -1, estado = null;
    while (Date.now() - t0 < (dur + 180) * 1000) {""",
    """    const t0 = Date.now();
    /* Em CFR o render NAO acompanha o relogio: ele desenha todos os quadros o
       mais rapido que der, entao uma gravacao de 57 s pode levar 3 min. */
    const teto = CFR ? dur * 8 + 300 : dur + 180;
    let ultimoPct = -1, estado = null;
    while (Date.now() - t0 < teto * 1000) {""",
))

trocas.append((
    """    const tol = Math.max(0.6, dur * 0.02);
    if (Math.abs(real - dur) > tol) {
      fs.unlinkSync(saida);
      throw new Error('saiu ' + (dur / real).toFixed(2) + 'x ' + (real < dur ? 'ACELERADO' : 'lento') +
                      ' — o canvas nao desenhou no ritmo pedido. Arquivo apagado.');
    }
    console.log('  duracao confere.');""",
    """    if (CFR) {
      /* O arquivo cru tem a duracao do RENDER, que e' maior que a do video.
         Quem poe na taxa certa e' o _mp4/retimar.py — aqui nao ha o que
         conferir, so avisar para nao esquecer o passo. */
      console.log('  duracao : crua ' + real.toFixed(1) + 's (ritmo do render) — falta rodar');
      console.log('            python _mp4/retimar.py ' + saida.replace(/\\\\/g, '/') +
                  ' --fps=' + TAXA);
    } else {
      const tol = Math.max(0.6, dur * 0.02);
      if (Math.abs(real - dur) > tol) {
        fs.unlinkSync(saida);
        throw new Error('saiu ' + (dur / real).toFixed(2) + 'x ' + (real < dur ? 'ACELERADO' : 'lento') +
                        ' — o canvas nao desenhou no ritmo pedido. Arquivo apagado.');
      }
      console.log('  duracao confere.');
    }""",
))

for i, (velho, novo) in enumerate(trocas, 1):
    n = d.count(velho)
    print('troca %d: casou %d vez(es)' % (i, n))
    if n != 1:
        print('ABORTADO: ancora %d nao e unica. Nada foi gravado.' % i)
        sys.exit(1)
    d = d.replace(velho, novo, 1)

assert d != orig
open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('gravado: %s (%d -> %d bytes)' % (ARQ, len(orig), len(d)))
