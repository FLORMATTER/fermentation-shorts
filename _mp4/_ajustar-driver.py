# -*- coding: utf-8 -*-
"""Ajusta o _gerar-mp4.js: (1) usa GPU no Chrome, (2) recusa mp4 com duracao errada.
   Aborta SEM GRAVAR se qualquer ancora nao casar exatamente 1 vez."""
import io, sys

ARQ = '_gerar-mp4.js'

A1_OLD = "    '--disable-gpu', '--no-sandbox', '--mute-audio', '--hide-scrollbars',"
A1_NEW = ("    // SEM --disable-gpu: em software o canvas so desenhava ~18 quadros/s,\n"
          "    // e o MediaRecorder entao carimbava 1/30 s por quadro entregue -> video acelerado.\n"
          "    '--no-sandbox', '--mute-audio', '--hide-scrollbars',")

A2_OLD = """function duracaoDoHtml(html) {"""

A2_NEW = """/* Le a duracao real do .mp4 pelo box mvhd. Sem ffmpeg. */
function duracaoMp4(buf) {
  let i = -1;
  while ((i = buf.indexOf('mvhd', i + 1)) >= 0) {
    try {
      if (buf[i + 4] === 1) {
        const ts = buf.readUInt32BE(i + 24);
        const du = Number(buf.readBigUInt64BE(i + 28));
        if (ts > 0 && du > 0) return du / ts;
      } else {
        const ts = buf.readUInt32BE(i + 16);
        const du = buf.readUInt32BE(i + 20);
        if (ts > 0 && du > 0) return du / ts;
      }
    } catch (e) {}
  }
  return 0;
}

function duracaoDoHtml(html) {"""

A3_OLD = """    fs.closeSync(fd);
    const mb = fs.statSync(saida).size / 1048576;
    console.log('\\r  OK -> ' + saida.replace(RAIZ + path.sep, '').replace(/\\\\/g, '/') +
                '  (' + mb.toFixed(1) + ' MB, ' + dur.toFixed(1) + 's)');
    ws.close();
    ok = true;"""

A3_NEW = """    fs.closeSync(fd);
    const mb = fs.statSync(saida).size / 1048576;
    const real = duracaoMp4(fs.readFileSync(saida));
    console.log('\\r  OK -> ' + saida.replace(RAIZ + path.sep, '').replace(/\\\\/g, '/') +
                '  (' + mb.toFixed(1) + ' MB)');
    console.log('  duracao: pedida ' + dur.toFixed(1) + 's | no arquivo ' + real.toFixed(1) + 's');
    if (!real) throw new Error('nao consegui ler a duracao do mp4');
    if (Math.abs(real - dur) > 0.6) {
      console.log('  *** RECUSADO: saiu ' + (dur / real).toFixed(2) + 'x ' +
                  (real < dur ? 'ACELERADO' : 'lento') +
                  ' — o canvas nao desenhou no ritmo pedido. Arquivo apagado.');
      fs.unlinkSync(saida);
      throw new Error('duracao errada');
    }
    console.log('  duracao confere.');
    ws.close();
    ok = true;"""

SUBS = [('GPU ligada', A1_OLD, A1_NEW),
        ('leitor de mvhd', A2_OLD, A2_NEW),
        ('checagem de duracao', A3_OLD, A3_NEW)]

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
