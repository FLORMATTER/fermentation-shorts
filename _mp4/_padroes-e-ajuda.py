"""_mp4/_padroes-e-ajuda.py — o cabecalho do _gerar-mp4.js estava mentindo.

Dizia que o retimar era um passo manual a rodar depois (nao e' mais: o driver faz
sozinho) e que o --passo nao existia. Tambem: o --passo tinha padrao 0, que e' o
pior valor possivel — em 1080p sobrevivem 69% dos quadros. Agora o padrao e' 60
(~97% a ~2x a duracao do video).

Tres ancoras contadas. Aborta sem gravar se alguma nao casar uma vez.
"""
import sys

ARQ = '_gerar-mp4.js'
d = open(ARQ, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in d else '\n'
print('%s: fim de linha %s' % (ARQ, 'CRLF' if nl == '\r\n' else 'LF'))
orig = d

TROCAS = [
    # 1) cabecalho
    ("""   Uso:  node _gerar-mp4.js mosquito/shorts-mosquito-trap-en.html
         node _gerar-mp4.js --todos          (todo short que ainda nao tem mp4)

   Opcoes: --w=NNN (largura, padrao 1080)   --fps=NN (taxa, padrao 30)
           --kbps=NNN (bitrate, padrao 1000)  --cfr=1 (taxa constante)

   --cfr=1 e' o modo BOM: grava um quadro por indice, sem olhar o relogio, e
   depois e' so rodar  python _mp4/retimar.py <saida>.mp4  para o arquivo tocar
   em taxa constante com TODOS os quadros distintos. O modo padrao (tempo real)
   repete quadro quando o codificador nao acompanha, e quadro repetido = a
   animacao travando entre quadros.
""",
     """   Uso:  node _gerar-mp4.js mosquito/shorts-mosquito-trap-en.html
         node _gerar-mp4.js --todos           (o lote: short publicavel, sem mp4)
         node _gerar-mp4.js --todos --lista   (so' mostra o lote e sai)

   Opcoes: --w=NNN (largura, padrao 1080)    --fps=NN (taxa, padrao 30)
           --kbps=NNN (bitrate, padrao 3000) --cfr=1 (taxa constante)
           --passo=NN (ms entre quadros, padrao 60)   --sem-retimar
           --todos-tudo (desliga o filtro do --todos)

   --cfr=1 e' o modo BOM: grava um quadro por indice, sem olhar o relogio. No fim
   o proprio driver roda o _mp4/retimar.py e CONFERE a duracao (--sem-retimar
   desliga). O modo padrao (tempo real) deixa quadro CAIR quando o codificador nao
   acompanha, e quadro que cai = a animacao travando entre quadros.

   --passo e' o que evita a queda (medido em 1080p, 624 quadros de 20,8 s):
        0 ms -> 69% sobrevivem   (0,9x a duracao do video)
       40 ms -> 95%              (1,5x)
       80 ms -> 97%              (2,6x)
      120 ms -> 99%              (4,0x)
   Em 60 ms sai ~97% a ~2x a duracao — 29 q/s na pratica, indistinguivel de 30.
"""),

    # 2) bitrate padrao
    ("""/* teto de bitrate em kbps (padrao 1000). O codificador e' o gargalo e o
   bitrate mexe nele. */
const KBPS = (function () {
  const a = process.argv.find(x => /^--kbps=\\d+$/.test(x));
  return a ? parseInt(a.slice(7), 10) : 1000;
})();""",
     """/* teto de bitrate em kbps (padrao 3000). 3000 e' o que os mp4 ja entregues
   usam; 1080x1920 de desenho chapado nao precisa de mais. */
const KBPS = (function () {
  const a = process.argv.find(x => /^--kbps=\\d+$/.test(x));
  return a ? parseInt(a.slice(7), 10) : 3000;
})();"""),

    # 3) passo padrao
    ("""/* --passo=NN = intervalo minimo entre quadros em CFR, em ms. Existe para NAO
   perder quadro: o MediaRecorder descarta quando a fila do codificador enche. */
const PASSO = (function () {
  const a = process.argv.find(x => /^--passo=\\d+$/.test(x));
  return a ? parseInt(a.slice(8), 10) : 0;
})();""",
     """/* --passo=NN = intervalo minimo entre quadros em CFR, em ms. Existe para NAO
   perder quadro: o requestFrame() do captureStream(0) SOBRESCREVE o quadro que
   ainda nao foi consumido, e o MediaRecorder descarta o resto quando a fila do
   codificador enche. Sem espera, em 1080p, 31% dos quadros somem.
   Padrao 60: medido em ~97% de sobrevivencia a ~2x a duracao do video. */
const PASSO = (function () {
  const a = process.argv.find(x => /^--passo=\\d+$/.test(x));
  return a ? parseInt(a.slice(8), 10) : 60;
})();"""),
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
