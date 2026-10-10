# _mp4/_instrumentar-render.py
# Poe medidores no _mp4/render.js e troca a fila de assar por ORCAMENTO DE TEMPO.
#
# Por que: o render saiu a 9 quadros/s. Medido no bench3, o bake() custa 3,7 ms
# (nao 17,5 ms como eu supus). Entao o tempo esta em outro lugar — provavelmente
# na rasterizacao do SVG 1080x1920, que acontece entre um tique e outro e nao
# aparece em nenhuma conta. Os medidores abaixo mostram isso no log.
#
# Cada ancora tem que casar EXATAMENTE uma vez, senao o script aborta sem gravar.
import io, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALVO = os.path.join(RAIZ, '_mp4', 'render.js')

with io.open(ALVO, encoding='utf-8') as f:
    d = f.read()

crlf = '\r\n' in d
fim = '\r\n' if crlf else '\n'

def N(s):
    return s.replace('\n', fim) if crlf else s

trocas = []

# ---- 1. variaveis do perfil + ORCAMENTO ----
trocas.append((
    N('  var W = 1080, H = 1920, FPS = 30, LOOK = 6;'),
    N('  var W = 1080, H = 1920, FPS = 30, LOOK = 8;\n'
      '  /* ORCAMENTO = quantos ms por tique podem ser gastos ASSANDO.\n'
      '     A fila por numero fixo de quadros (LOOK) travava o tique inteiro quando\n'
      '     assar+rasterizar ficava caro. Com orcamento, o desenho nunca espera. */\n'
      '  var ORCAMENTO = 10;')
))

# ---- 2. medidores ----
trocas.append((
    N('  var ultimoIdx = -1, desenhados = 0, ultimoDesenho = -1;\n'
      '  var INTERVALO = 1000 / FPS;\n'
      '  var t0 = null;'),
    N('  var ultimoIdx = -1, desenhados = 0, ultimoDesenho = -1;\n'
      '  var INTERVALO = 1000 / FPS;\n'
      '  var t0 = null;\n'
      '  /* medidores: sem eles a gente chuta de onde vem o tempo perdido */\n'
      '  var perfTick = 0, perfTickN = 0, perfBake = 0, perfBakeN = 0;\n'
      '  var perfDraw = 0, perfDrawN = 0, perfRast = 0, perfRastN = 0;\n'
      '  var perfLag = 0, perfLagN = 0, proximo = 0;')
))

# ---- 3. pedir: mede o assar e a rasterizacao ----
trocas.append((
    N('    var info = frameInfo(f);\n'
      '    var url;\n'
      '    try { url = bake(info.idx, info.local); }\n'
      '    catch (e) { delete busy[f]; L(\'bake falhou no quadro \' + f + \': \' + e.message); return; }\n'
      '    var img = new Image();\n'
      '    img.onload = function () { ready[f] = img; delete busy[f]; };'),
    N('    var info = frameInfo(f);\n'
      '    var url;\n'
      '    var _tb = performance.now();\n'
      '    try { url = bake(info.idx, info.local); }\n'
      '    catch (e) { delete busy[f]; L(\'bake falhou no quadro \' + f + \': \' + e.message); return; }\n'
      '    perfBake += performance.now() - _tb; perfBakeN++;\n'
      '    var img = new Image();\n'
      '    var _tr = performance.now();\n'
      '    img.onload = function () { perfRast += performance.now() - _tr; perfRastN++; ready[f] = img; delete busy[f]; };')
))

# ---- 4. desenha: mede o desenho ----
trocas.append((
    N('  function desenha(f, t) {\n'
      '    var info = frameInfo(f);\n'
      '    var img = ready[f];'),
    N('  function desenha(f, t) {\n'
      '    var _td = performance.now();\n'
      '    var info = frameInfo(f);\n'
      '    var img = ready[f];')
))
trocas.append((
    N('    desenhados++;\n'
      '    window.__p = f / totalFrames;\n'
      '  }'),
    N('    desenhados++;\n'
      '    perfDraw += performance.now() - _td; perfDrawN++;\n'
      '    window.__p = f / totalFrames;\n'
      '  }')
))

# ---- 5. tick: orcamento de tempo + medicao do atraso ----
ANTIGO_TICK = N('''  function tick() {
    if (t0 === null) t0 = performance.now();
    var t = performance.now() - t0;
    if (t >= TOTAL) {
      desenha(totalFrames - 1, TOTAL);
      track.requestFrame();
      L('ritmo real: ' + (desenhados / (t / 1000)).toFixed(1) + ' quadros/s (alvo ' + FPS + ')');
      rec.stop();
      return;
    }
    if (t - ultimoDesenho >= INTERVALO - 1) {
      ultimoDesenho = t;
      desenha(Math.floor(t / 1000 * FPS), t);
      track.requestFrame();
    }
    var f = Math.floor(t / 1000 * FPS);
    for (var k = f; k < f + LOOK; k++) pedir(k);
    var velhos = [];
    for (var key in ready) if (+key < f - 3) velhos.push(key);
    for (var v = 0; v < velhos.length; v++) delete ready[velhos[v]];
    /* setTimeout, nao requestAnimationFrame: no headless o rAF e servido pelo
       compositor e roda a ~11 Hz. O relogio nao tem esse limite. */
    setTimeout(tick, 6);
  }''')

NOVO_TICK = N('''  function tick() {
    var agora = performance.now();
    if (t0 === null) { t0 = agora; proximo = agora; }
    /* atraso do timer = tempo em que o thread principal ficou ocupado FORA do
       tique (rasterizacao do SVG, por exemplo). Se este numero for grande, o
       gargalo nao esta no nosso codigo. */
    perfLag += agora - proximo; perfLagN++;
    var _tt = agora;
    var t = agora - t0;
    if (t >= TOTAL) {
      desenha(totalFrames - 1, TOTAL);
      track.requestFrame();
      L('ritmo real: ' + (desenhados / (t / 1000)).toFixed(1) + ' quadros/s (alvo ' + FPS + ')');
      L('perfil: tique ' + (perfTick / perfTickN).toFixed(1) + ' ms | assar ' +
        (perfBakeN ? (perfBake / perfBakeN).toFixed(2) : '-') + ' ms x' + perfBakeN +
        ' | desenhar ' + (perfDrawN ? (perfDraw / perfDrawN).toFixed(2) : '-') + ' ms x' + perfDrawN +
        ' | rasterizar ' + (perfRastN ? (perfRast / perfRastN).toFixed(2) : '-') + ' ms x' + perfRastN +
        ' | atraso do timer ' + (perfLagN ? (perfLag / perfLagN).toFixed(1) : '-') + ' ms');
      rec.stop();
      return;
    }
    /* 1. DESENHAR PRIMEIRO. O relogio da gravacao manda: o quadro tem que sair
       na hora certa mesmo que assar esteja atrasado. */
    if (t - ultimoDesenho >= INTERVALO - 1) {
      ultimoDesenho = t;
      desenha(Math.floor(t / 1000 * FPS), t);
      track.requestFrame();
    }
    /* 2. ASSAR POR ORCAMENTO DE TEMPO. Antes era "LOOK quadros de enfiada": com
       assar+rasterizar caro o tique travava ~100 ms e a gravacao caia para
       9 quadros/s. Agora assa o que couber em ORCAMENTO ms e devolve o controle. */
    var f = Math.floor(t / 1000 * FPS);
    var limite = performance.now() + ORCAMENTO;
    for (var k = f; k < f + LOOK && performance.now() < limite; k++) pedir(k);
    var velhos = [];
    for (var key in ready) if (+key < f - 3) velhos.push(key);
    for (var v = 0; v < velhos.length; v++) delete ready[velhos[v]];
    perfTick += performance.now() - _tt; perfTickN++;
    /* setTimeout, nao requestAnimationFrame: no headless o rAF e servido pelo
       compositor e roda a ~11 Hz. O relogio nao tem esse limite. */
    proximo = performance.now() + 2;
    setTimeout(tick, 2);
  }''')

trocas.append((ANTIGO_TICK, NOVO_TICK))

# ---- aplica com contagem ----
problemas = []
for i, (velho, novo) in enumerate(trocas, 1):
    c = d.count(velho)
    if c != 1:
        problemas.append('troca %d: ancora casou %d vez(es), esperava 1' % (i, c))
if problemas:
    print('ABORTADO, nada foi gravado:')
    for p in problemas:
        print('  ' + p)
    sys.exit(1)

for velho, novo in trocas:
    d = d.replace(velho, novo)

with io.open(ALVO, 'w', encoding='utf-8', newline='') as f:
    f.write(d)

print('ok: %d trocas aplicadas em %s' % (len(trocas), ALVO))
print('fim de linha: ' + ('CRLF' if crlf else 'LF'))
for termo in ['ORCAMENTO = 10', 'perfRast', 'perfLag', 'proximo = performance.now() + 2']:
    print('  %-42s %d' % (termo, d.count(termo)))
