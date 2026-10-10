"""_mp4/_modo-cfr.py — poe o render.js em modo CFR (taxa constante) e faz o
?mp4kbps= funcionar de verdade.

Tres trocas, cada uma com contagem exata. Se qualquer ancora casar 0 ou 2+ vezes
o script ABORTA sem gravar (regra do projeto: editar o mesmo arquivo sem
contagem ja perdeu edicao duas vezes).
"""
import re
import sys

ARQ = '_mp4/render.js'
d = open(ARQ, encoding='utf-8').read()
orig = d

# ---------------------------------------------------------------- troca 1
velho1 = """  var S = W / 405;                 // o cartao e 405x720; o canvas e WxH
  var BITRATE = 8000000;
"""
novo1 = """  var S = W / 405;                 // o cartao e 405x720; o canvas e WxH
  /* BITRATE vinha FIXO em 8 Mbps e o --kbps do _gerar-mp4.js era ignorado: o
     driver mandava ?mp4kbps= na URL e ninguem lia. O codificador e' o gargalo,
     entao o bitrate e' um botao de verdade — 8 Mbps derrubava o render. */
  var BITRATE = (function () {
    var m = /[?&]mp4kbps=(\\d+)/.exec(location.search);
    return m ? parseInt(m[1], 10) * 1000 : 2000000;
  })();
  /* CFR = desenhar TODO indice de quadro uma vez, em ordem, o mais rapido que a
     maquina der, sem olhar o relogio. Duas razoes:
       1. quadro repetido fica IMPOSSIVEL por construcao — o indice nunca repete,
          e era a repeticao que fazia a animacao travar entre quadros;
       2. o codificador H.264 em software nao acompanha 30 q/s, mas em CFR isso
          deixa de importar: o arquivo sai mais longo que o video (gravado a
          ~12 q/s) e o _mp4/retimar.py reescreve a duracao de cada amostra para
          1/FPS. Todos os quadros ficam distintos E a taxa fica constante. */
  var CFR = /[?&]mp4cfr=1/.test(location.search);
"""

# ---------------------------------------------------------------- troca 2
velho2 = "  /* aquece: sem o primeiro quadro decodificado a gravacao comeca com tela vazia */"
novo2 = """  /* ---------- 7. tique de TAXA CONSTANTE ---------- */
  /* Um indice por vez, em ordem. O relogio nao decide nada: quem decide e o
     indice. Se a maquina renderiza 12 quadros/s, uma gravacao de 57 s demora
     ~150 s — e o retimar.py devolve os 30 q/s no fim. */
  var cfrF = 0, cfrT0 = null;
  function tickCFR() {
    var _tt = performance.now();
    if (cfrT0 === null) cfrT0 = _tt;
    if (cfrF >= totalFrames) {
      var gasto = (_tt - cfrT0) / 1000;
      L('CFR: ' + totalFrames + ' quadros em ' + gasto.toFixed(1) + ' s (' +
        (totalFrames / gasto).toFixed(1) + ' quadros/s de render) — sem repetidos por construcao');
      L('perfil: tique ' + (perfTick / perfTickN).toFixed(1) + ' ms | assar ' +
        (perfBakeN ? (perfBake / perfBakeN).toFixed(2) : '-') + ' ms x' + perfBakeN +
        ' | desenhar ' + (perfDrawN ? (perfDraw / perfDrawN).toFixed(2) : '-') + ' ms x' + perfDrawN +
        ' | rasterizar ' + (perfRastN ? (perfRast / perfRastN).toFixed(2) : '-') + ' ms x' + perfRastN);
      /* segura o ULTIMO quadro antes de parar — parar na hora faz o codificador
         nao carimbar a amostra final e o arquivo sai com uma a menos. */
      setTimeout(function () { rec.stop(); }, 150);
      return;
    }
    if (!ready[cfrF]) {
      pedir(cfrF);
      for (var k0 = cfrF + 1; k0 < cfrF + LOOK; k0++) pedir(k0);
      perfTick += performance.now() - _tt; perfTickN++;
      setTimeout(tickCFR, 1);
      return;
    }
    desenha(cfrF, cfrF / FPS * 1000);
    track.requestFrame();
    cfrF++;
    window.__p = cfrF / totalFrames;
    for (var k = cfrF; k < cfrF + LOOK; k++) pedir(k);
    var velhos = [];
    for (var key in ready) if (+key < cfrF - 2) velhos.push(key);
    for (var v = 0; v < velhos.length; v++) delete ready[velhos[v]];
    perfTick += performance.now() - _tt; perfTickN++;
    setTimeout(tickCFR, 0);
  }

  /* aquece: sem o primeiro quadro decodificado a gravacao comeca com tela vazia */"""

# ---------------------------------------------------------------- troca 3
velho3 = "        requestAnimationFrame(tick);"
novo3 = "        requestAnimationFrame(CFR ? tickCFR : tick);"

for nome, velho, novo in (('1', velho1, novo1), ('2', velho2, novo2), ('3', velho3, novo3)):
    n = d.count(velho)
    print('troca %s: casou %d vez(es)' % (nome, n))
    if n != 1:
        print('ABORTADO: a ancora %s nao e unica. Nada foi gravado.' % nome)
        sys.exit(1)
    d = d.replace(velho, novo, 1)

assert d != orig
open(ARQ, 'w', encoding='utf-8', newline='').write(d)
print('gravado: %s (%d -> %d bytes)' % (ARQ, len(orig), len(d)))
