"""_mp4/_retimar-automatico.py — o _gerar-mp4.js passa a retimar sozinho em CFR.

Por que: em CFR o arquivo cru tem a duracao do RENDER (4 a 5x a do video). O
passo de retimar era manual e o driver so' imprimia um lembrete — um lembrete que
e' facil de ignorar. Numa lote de 13 videos isso vira um video de 280 s entregue
como se fosse de 57 s. Agora o proprio driver roda o retimar.py e CONFERE a
duracao depois.

    --sem-retimar   desliga (para depurar o arquivo cru)
"""
import sys

ARQ = '_gerar-mp4.js'
d = open(ARQ, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in d else '\n'
print('%s: fim de linha %s' % (ARQ, 'CRLF' if nl == '\r\n' else 'LF'))
orig = d

TROCAS = [
    # spawnSync ao lado de spawn
    ("const { spawn } = require('child_process');",
     "const { spawn, spawnSync } = require('child_process');"),

    # opcao nova
    ("""const PASSO = (function () {
  const a = process.argv.find(x => /^--passo=\\d+$/.test(x));
  return a ? parseInt(a.slice(8), 10) : 0;
})();
""",
     """const PASSO = (function () {
  const a = process.argv.find(x => /^--passo=\\d+$/.test(x));
  return a ? parseInt(a.slice(8), 10) : 0;
})();
/* Em CFR o arquivo cru tem a duracao do RENDER, nao a do video — entao retimar
   faz parte da gravacao, nao e' um passo separado. --sem-retimar desliga. */
const SEM_RETIMAR = process.argv.includes('--sem-retimar');
"""),

    # retima + confere
    ("""    if (CFR) {
      /* O arquivo cru tem a duracao do RENDER, que e' maior que a do video.
         Quem poe na taxa certa e' o _mp4/retimar.py — aqui nao ha o que
         conferir, so avisar para nao esquecer o passo. */
      console.log('  duracao : crua ' + real.toFixed(1) + 's (ritmo do render) — falta rodar');
      console.log('            (passo ' + PASSO + ' ms)');
      console.log('            python _mp4/retimar.py ' + saida.replace(/\\\\/g, '/') +
                  ' --fps=' + TAXA);
    } else {""",
     """    if (CFR && !SEM_RETIMAR) {
      /* Retima AQUI. Deixar para depois e' pe' de cabra: o arquivo cru dura o
         render inteiro (4 a 5x o video) e nada no arquivo avisa disso. */
      const quadros = Math.ceil(dur * TAXA);
      const r = spawnSync('python',
        [path.join(RAIZ, '_mp4', 'retimar.py'), saida, '--fps=' + TAXA, '--quadros=' + quadros],
        { encoding: 'utf8' });
      if (r.error) throw new Error('nao consegui rodar o retimar.py: ' + r.error.message);
      (r.stdout || '').trim().split('\\n').forEach(l => console.log('    ' + l));
      if (r.status !== 0) throw new Error('o retimar.py saiu com codigo ' + r.status);
      const fim = duracaoMp4(fs.readFileSync(saida));
      if (!fim) throw new Error('nao consegui ler a duracao depois de retimar');
      if (Math.abs(fim - dur) > 0.05) {
        throw new Error('retimado deu ' + fim.toFixed(2) + 's e o video tem ' + dur.toFixed(2) + 's');
      }
      console.log('  duracao : ' + fim.toFixed(1) + 's a ' + TAXA + ' q/s constante' +
                  '  (cru ' + real.toFixed(1) + 's, passo ' + PASSO + ' ms)');
    } else if (CFR) {
      console.log('  duracao : crua ' + real.toFixed(1) + 's — sem retimar (--sem-retimar)');
    } else {"""),
]

for i, (velho, novo) in enumerate(TROCAS, 1):
    v = velho.replace('\n', nl)
    nv = novo.replace('\n', nl)
    n = d.count(v)
    print('troca %d: casou %d vez(es)' % (i, n))
    if n != 1:
        print('ABORTADO: ancora %d nao e unica. Nada foi gravado.' % i)
        sys.exit(1)
    d = d.replace(v, nv, 1)

assert d != orig
open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('gravado: %s (%d -> %d bytes)' % (ARQ, len(orig), len(d)))
