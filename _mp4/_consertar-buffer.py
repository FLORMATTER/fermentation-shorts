# -*- coding: utf-8 -*-
"""Conserta a leitura antecipada — a causa dos quadros repetidos.

   O defeito: o laco pedia `k = f .. f+LOOK-1`, mas o ORCAMENTO de 6 ms so deixa
   assar ~1 quadro por tique. Resultado: a cada tique assavamos o quadro que
   precisavamos desenhar NAQUELE instante — sempre tarde. O quadro nunca estava
   pronto e o motor redesenhava o anterior: 59-84 quadros repetidos por 100.

   Dois consertos:
   1. Aquecer um BUFFER de verdade antes de comecar a gravar (antes, o aquecimento
      era de 3 quadros, o mesmo tamanho da janela).
   2. Pedir a partir de `f + 1` (nunca o quadro da vez) e manter a janela cheia.
      Assim o quadro e' assado ANTES de ser preciso, e o que se desenha e' sempre
      imagem nova. Se a producao nao acompanhar, o video fica com MENOS quadros
      por segundo — nao com quadros repetidos, que e' o que le como travada.

   Tambem reverte o contexto alpha:false/desynchronized: nao acelerou nada e mudou
   o tamanho do arquivo.

   Cada ancora tem que casar EXATAMENTE uma vez, senao aborta sem gravar."""
import io, os, sys

ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render.js')

trocas = []

# ---- 1. reverte o contexto opaco ----
trocas.append((
'''  /* alpha:false -> o canvas e opaco (as cenas tem fundo solido); tirar o canal
     alfa do caminho quente acelera a rasterizacao e a copia para o codificador.
     desynchronized:true -> nao ha tela para sincronizar, a gravacao le o canvas
     direto. Nenhum dos dois muda um pixel do que sai. */
  var cx = cv.getContext('2d', { alpha: false, desynchronized: true });''',
'''  /* Testado e revertido: {alpha:false, desynchronized:true} NAO acelerou nada
     (1080: 13,7 -> 13,8 q/s) e ainda mudou o tamanho do arquivo. */
  var cx = cv.getContext('2d');'''))

# ---- 2. a janela de leitura antecipada ----
trocas.append((
'''  var ORCAMENTO = 6;''',
'''  var ORCAMENTO = 12;
  /* AQUECER = quantos quadros ficam prontos ANTES de comecar a gravar. Com um
     buffer de verdade o desenho nunca espera; sem ele o motor assa o quadro da
     vez e sempre chega tarde. */
  var AQUECER = 24;'''))

# ---- 3. pedir a partir de f+1, nao de f ----
trocas.append((
'''    var limite = performance.now() + ORCAMENTO;
    for (var k = f; k < f + LOOK && performance.now() < limite; k++) pedir(k);''',
'''    var limite = performance.now() + ORCAMENTO;
    /* k comeca em f+1: o quadro da vez ja tem que estar pronto (veio do buffer).
       Pedindo de f em diante a gente assava justamente o quadro que ia desenhar
       agora — tarde por definicao. */
    for (var k = f + 1; k < f + AQUECER && performance.now() < limite; k++) pedir(k);'''))

# ---- 4. aquecimento de verdade ----
trocas.append((
'''    for (var k = 0; k < LOOK; k++) pedir(k);
    var tent = 0;
    (function espera() {
      if (ready[0] || ++tent > 300) {
        L('quadro 0 ' + (ready[0] ? 'pronto' : 'NAO decodificou') + ' apos ' + tent + ' tentativas');
        rec.start();
        requestAnimationFrame(tick);
      } else setTimeout(espera, 20);
    })();''',
'''    for (var k = 0; k < AQUECER; k++) pedir(k);
    var tent = 0;
    (function espera() {
      var prontos = 0;
      for (var k = 0; k < AQUECER; k++) if (ready[k]) prontos++;
      /* espera o buffer encher; se travar, segue com o que tiver */
      if (prontos >= AQUECER || ++tent > 400) {
        L('buffer: ' + prontos + '/' + AQUECER + ' quadros prontos antes de gravar');
        rec.start();
        requestAnimationFrame(tick);
      } else setTimeout(espera, 20);
    })();'''))

d = io.open(ARQ, encoding='utf-8', newline='').read()
falhou = False
for i, (old, novo) in enumerate(trocas, 1):
    n = d.count(old)
    print('troca %d: %d ocorrencia(s) %s' % (i, n, 'OK' if n == 1 else '<-- FALHOU'))
    if n != 1:
        falhou = True
if falhou:
    print('\nABORTADO: nada foi gravado.')
    sys.exit(1)

for old, novo in trocas:
    d = d.replace(old, novo, 1)
io.open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('\nGRAVADO: %s' % ARQ)
for t in ['var AQUECER = 24', 'for (var k = f + 1;', 'buffer: ', "getContext('2d')"]:
    print('  %-28s %d' % (t, d.count(t)))
