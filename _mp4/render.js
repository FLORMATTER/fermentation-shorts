/* _mp4/render.js — motor de gravacao.
   Injetado automaticamente pelo _gerar-mp4.js antes de </body>. Nao fica gravado
   no short: o arquivo original continua limpo.

   O que ele faz:
   1. Mede a barra de legenda ANTES de mexer no layout (a medida tem que sair no
      espaco do cartao 405x720, senao o canvas desenha a barra no lugar errado).
   2. Esconde todo o overlay HTML — barra, rotulo, marca d'agua e legenda sao
      redesenhados no canvas, porque o MediaRecorder grava SO o canvas.
   3. Para cada quadro: congela as animacoes CSS em currentTime = tempo local da
      cena, clona o <svg> da cena e ASSA os valores computados de transform e
      opacity no clone. Sem assar, o SVG serializado sai sem animacao nenhuma
      (animacao CSS nao vive no DOM, e <img> com SVG nao anima).
   4. Desenha em tempo real e grava com MediaRecorder em H.264/MP4.

   Por que assar em vez de tirar screenshot: um screenshot por quadro exigiria
   1700 capturas via CDP. Aqui o navegador desenha, e o proprio navegador
   codifica — sem ffmpeg, sem arquivo intermediario.
*/
(function () {
  'use strict';

  /* FPS = taxa REAL do arquivo. Nao da para pedir 30: medido, cada quadro custa
     ~32 ms de thread principal entre assar, rasterizar e o proprio codificador
     H.264 do MediaRecorder em 1080x1920 — e 30 quadros/s precisariam de 33 ms
     no total. Pedindo 30 o relogio nao acompanha e o video sai com 10 quadros/s
     de verdade. Pedindo 15 o render entrega os 15 e a duracao bate. */
  /* Tamanho e taxa vem da URL (o _gerar-mp4.js injeta ?mp4w=&mp4fps=).
     Padrao 1080x1920 a 30. O gargalo de verdade e o codificador H.264 do
     MediaRecorder, que roda em software: ~69 ms por quadro em 1080x1920, o que
     segura tudo em ~14 quadros/s. O custo acompanha a AREA do quadro, entao
     baixar a resolucao compra taxa. */
  var W = (function () { var m = /[?&]mp4w=(\d+)/.exec(location.search); return m ? parseInt(m[1], 10) : 1080; })();
  var H = Math.round(W * 16 / 9);
  var FPS = (function () { var m = /[?&]mp4fps=(\d+)/.exec(location.search); return m ? parseInt(m[1], 10) : 30; })();
  var LOOK = 3;
  /* LOOK = quantos quadros adiante assar. NAO precisa ser grande: o que manda
     e a latencia de UMA rasterizacao. Com LOOK=8 o tique pedia quadros mais
     rapido do que conseguia desenhar (203 rasterizados para 84 desenhados).
     ORCAMENTO = teto de ms por tique gastos assando, para o tique nunca
     engasgar e o desenho sair no relogio. */
  var ORCAMENTO = 6;
  /* LOOK era 48. Cada bake() mexe em classList e em animation.currentTime, e
     isso forca um recalculo de estilo na pagina TODA (8 cenas, ~800 nos).
     Com 48 quadros assados por tique o navegador gastava ~100 ms por quadro
     desenhado: o short saia a 10 quadros/s. Com fila curta sobra tempo. */
  var S = W / 405;                 // o cartao e 405x720; o canvas e WxH
  /* BITRATE vinha FIXO em 8 Mbps e o --kbps do _gerar-mp4.js era ignorado: o
     driver mandava ?mp4kbps= na URL e ninguem lia. O codificador e' o gargalo,
     entao o bitrate e' um botao de verdade — 8 Mbps derrubava o render. */
  var BITRATE = (function () {
    var m = /[?&]mp4kbps=(\d+)/.exec(location.search);
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
  /* PASSO = intervalo MINIMO entre quadros, em ms. Em CFR o relogio nao importa
     (o arquivo e' retimado no fim), mas o MediaRecorder DESCARTA quadro quando a
     fila do codificador enche: medido, sobreviveu so 76% dos quadros a 19 q/s.
     Quadro descartado e' pior que quadro repetido — o anterior fica o DOBRO do
     tempo na tela e o olho le isso como travamento. Entao alimenta devagar. */
  var PASSO = (function () {
    var m = /[?&]mp4passo=(\d+)/.exec(location.search);
    return m ? parseInt(m[1], 10) : 0;
  })();
  var MIMES = ['video/mp4;codecs=avc1.42E01E', 'video/mp4', 'video/webm;codecs=vp9'];

  window.__log = window.__log || [];
  function L(s) { window.__log.push(s); }

  if (typeof scenes === 'undefined' || !scenes || !scenes.length) {
    window.__done = 'FAIL';
    L('nao achei o array scenes');
    return;
  }

  var TOTAL = 0;
  for (var q = 0; q < scenes.length; q++) TOTAL += scenes[q].ms;
  var totalFrames = Math.ceil(TOTAL / 1000 * FPS);

  /* ---------- 1. mede a legenda no espaco do cartao (405) ---------- */
  var capEl = document.getElementById('cap');
  var capH = capEl ? capEl.offsetHeight : 73;
  if (!capH || capH < 40 || capH > 130) { L('altura de legenda estranha: ' + capH + ' (uso 73)'); capH = 73; }
  var capTop = 720 - capH;
  var capY = capTop + 27;
  var subY = capTop + 51;
  L('legenda: ' + capH + 'px do cartao (topo y=' + capTop + ')');

  /* ---------- 2. esconde o overlay HTML ---------- */
  var st = document.createElement('style');
  st.textContent =
    '#cover,.ui,.bar,.tag,.wm,.cap{display:none!important}' +
    '#stage{width:' + W + 'px!important;height:' + H + 'px!important;' +
    'border-radius:0!important;box-shadow:none!important;transform:none!important;' +
    'background:transparent!important;overflow:hidden!important}' +
    'svg.scene{transition:none!important}';
  document.head.appendChild(st);

  var stage = document.getElementById('stage');
  var cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  cv.style.cssText = 'position:absolute;left:0;top:0;z-index:9999';
  stage.appendChild(cv);
  var cx = cv.getContext('2d');

  /* ---------- overlay estatico de cada cena (uma imagem por cena) ---------- */
  function esc(t) {
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  var marca = (document.querySelector('.wm') || {}).textContent || '';
  var marcaPlaceholder = /@yourchannel|@seucanal|@yourhandle/i.test(marca);
  if (marcaPlaceholder) L('marca d\'agua OMITIDA no mp4 (e placeholder: ' + marca + ')');

  function overlayURL(s) {
    var F = 'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,system-ui,sans-serif"';
    var t = '<svg xmlns="http://www.w3.org/2000/svg" width="' + W + '" height="' + H +
            '" viewBox="0 0 405 720">' +
            '<rect x="0" y="0" width="405" height="4" fill="rgba(0,0,0,.12)"/>' +
            /* Sem o campo `tag` o rotulo sairia escrito "undefined" no video. Nao
               desenhar nada e' feio; "undefined" e' defeito. */
            (s.tag ?
              '<text x="202" y="31" text-anchor="middle" font-size="10" font-weight="800" ' +
              'fill="#2c2c2a" opacity=".5" letter-spacing="2" ' + F + '>' + esc(s.tag) + '</text>'
              : '');
    if (!marcaPlaceholder && marca) {
      t += '<text x="389" y="26" text-anchor="end" font-size="9" font-weight="800" ' +
           'fill="#2c2c2a" opacity=".35" letter-spacing="1" ' + F + '>' + esc(marca) + '</text>';
    }
    t += '<rect x="0" y="' + capTop + '" width="405" height="' + capH + '" fill="rgba(15,14,12,.86)"/>' +
         '<text x="202" y="' + capY + '" text-anchor="middle" font-size="16" font-weight="800" ' +
         'fill="#ffffff" ' + F + '>' + esc(s.cap) + '</text>' +
         '<text x="202" y="' + subY + '" text-anchor="middle" font-size="12" font-weight="500" ' +
         'fill="#ffffff" opacity=".72" ' + F + '>' + esc(s.sub) + '</text>' +
         '</svg>';
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(t);
  }

  /* ---------- 3. indice dos elementos animados (para nao medir o SVG inteiro) ---------- */
  var animsPorCena = {};
  function indexarAnimados() {
    var mapa = {};
    document.getAnimations().forEach(function (a) {
      var alvo = a.effect && a.effect.target;
      var sv = alvo && alvo.closest ? alvo.closest('svg.scene') : null;
      if (!sv) return;
      (animsPorCena[sv.id] = animsPorCena[sv.id] || []).push(a);
      var todos = sv.querySelectorAll('*');
      for (var k = 0; k < todos.length; k++) {
        if (todos[k] === alvo) {
          (mapa[sv.id] = mapa[sv.id] || []).push(k);
          break;
        }
      }
    });
    var n = 0;
    for (var id in mapa) n += mapa[id].length;
    /* PAUSA TUDO. O CSS do short esconde cena com visibility:hidden, e nao com
       display:none — entao as animacoes das cenas escondidas NAO morrem sozinhas:
       elas continuam rodando e consumindo o tique que devia estar desenhando.
       Pausadas, o custo por quadro delas e zero; o bake posiciona a cena da vez. */
    var pausadas = 0;
    for (var id2 in animsPorCena) {
      animsPorCena[id2].forEach(function (a) { a.pause(); pausadas++; });
    }
    L('elementos animados: ' + n + ' em ' + Object.keys(animsPorCena).length +
      ' cenas (' + pausadas + ' animacoes pausadas)');
    return mapa;
  }
  var animados = indexarAnimados();
  var cenaLigada = -1;

  /* ---------- 4. assa um quadro ---------- */
  function bake(idx, local) {
    var id = scenes[idx].id;
    /* so troca as classes quando a cena MUDA — trocar a cada quadro invalidava o
       estilo das 8 cenas e era metade do custo de assar */
    if (cenaLigada !== idx) {
      for (var n = 0; n < scenes.length; n++) {
        var el = document.getElementById(scenes[n].id);
        if (n === idx) el.classList.add('on'); else el.classList.remove('on');
      }
      cenaLigada = idx;
    }
    /* so a cena da vez: as outras ja estao pausadas desde o inicio */
    var anims = animsPorCena[id] || [];
    for (var q = 0; q < anims.length; q++) anims[q].currentTime = local;

    var live = document.getElementById(id);
    var clone = live.cloneNode(true);
    var a = live.querySelectorAll('*'), b = clone.querySelectorAll('*');
    var lista = animados[id] || [];
    for (var j = 0; j < lista.length; j++) {
      var i = lista[j];
      var cs = getComputedStyle(a[i]);
      var sty = (b[i].getAttribute('style') || '')
        .replace(/animation[^;]*;?/g, '')
        .replace(/transform:[^;]*;?/g, '')
        .replace(/opacity:[^;]*;?/g, '');
      if (cs.transform && cs.transform !== 'none') sty += 'transform:' + cs.transform + ';';
      if (cs.opacity !== '' && cs.opacity !== '1') sty += 'opacity:' + cs.opacity + ';';
      b[i].setAttribute('style', sty);
    }
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    clone.setAttribute('width', W);
    clone.setAttribute('height', H);
    return 'data:image/svg+xml;charset=utf-8,' +
           encodeURIComponent(new XMLSerializer().serializeToString(clone));
  }

  function frameInfo(f) {
    var t = f / FPS * 1000, acc = 0;
    for (var n = 0; n < scenes.length; n++) {
      if (t < acc + scenes[n].ms) return { idx: n, local: t - acc };
      acc += scenes[n].ms;
    }
    return { idx: scenes.length - 1, local: scenes[scenes.length - 1].ms };
  }

  /* ---------- 5. fila com leitura antecipada ---------- */
  var ready = {}, busy = {}, lastImg = null, faltas = 0;
  function pedir(f) {
    if (f < 0 || f >= totalFrames || ready[f] || busy[f]) return;
    busy[f] = true;
    var info = frameInfo(f);
    var url;
    var _tb = performance.now();
    try { url = bake(info.idx, info.local); }
    catch (e) { delete busy[f]; L('bake falhou no quadro ' + f + ': ' + e.message); return; }
    perfBake += performance.now() - _tb; perfBakeN++;
    var img = new Image();
    var _tr = performance.now();
    img.onload = function () { perfRast += performance.now() - _tr; perfRastN++; ready[f] = img; delete busy[f]; };
    img.onerror = function () { delete busy[f]; L('quadro ' + f + ' nao decodificou'); };
    img.src = url;
  }

  var ovImg = [];
  var ovProntos = 0;
  function carregarOverlays(depois) {
    scenes.forEach(function (s, i) {
      var im = new Image();
      im.onload = function () { ovImg[i] = im; if (++ovProntos === scenes.length) depois(); };
      im.onerror = function () { if (++ovProntos === scenes.length) depois(); };
      im.src = overlayURL(s);
    });
  }

  /* ---------- 6. grava ---------- */
  /* captureStream(0) = trilha SEM taxa automatica: cada track.requestFrame()
     empurra exatamente um quadro, carimbado com a hora real da chamada.
     Com captureStream(30) quem amostra o canvas e o tique do compositor — e no
     headless esse tique roda a ~11 Hz, o que ENCOLHIA a duracao do video. */
  var cvStream = cv.captureStream(0);
  var track = cvStream.getVideoTracks()[0];
  var mime = '';
  for (var m = 0; m < MIMES.length; m++) {
    if (window.MediaRecorder && MediaRecorder.isTypeSupported(MIMES[m])) { mime = MIMES[m]; break; }
  }
  if (!mime) { window.__done = 'FAIL'; L('nenhum codec de gravacao disponivel'); return; }
  L('codec: ' + mime + ' a ' + (BITRATE / 1e6) + ' Mbps');

  var rec = new MediaRecorder(cvStream, { mimeType: mime, videoBitsPerSecond: BITRATE });
  var chunks = [];
  rec.ondataavailable = function (e) { if (e.data && e.data.size) chunks.push(e.data); };
  rec.onstop = function () {
    var blob = new Blob(chunks, { type: 'video/mp4' });
    window.__blob = blob;
    window.__size = blob.size;
    L('PRONTO ' + blob.size + ' bytes | duracao alvo ' + (TOTAL / 1000).toFixed(1) +
      's | quadros desenhados ' + desenhados + ' | repetidos por atraso: ' + faltas);
    if (window.__MP4POST) {
      fetch(window.__MP4POST, { method: 'POST', body: blob })
        .then(function () { window.__enviado = 'OK'; L('mp4 gravado no disco pelo proprio navegador'); })
        .catch(function (e) { window.__enviado = 'ERRO: ' + e.message; L('falha ao enviar: ' + e.message); });
    }
    window.__done = 'OK';
  };

  function desenha(f, t) {
    var _td = performance.now();
    var info = frameInfo(f);
    var img = ready[f];
    if (img) lastImg = img; else faltas++;
    if (lastImg) cx.drawImage(lastImg, 0, 0, W, H);
    /* O overlay TEM que ser redesenhado a cada quadro. A imagem da cena cobre o
       canvas inteiro (405x720 com fundo solido), entao "desenhar so quando a cena
       muda" apagava a barra de legenda: o video saiu sem legenda nenhuma. */
    if (ovImg[info.idx]) cx.drawImage(ovImg[info.idx], 0, 0, W, H);
    cx.fillStyle = scenes[info.idx].color;
    cx.fillRect(0, 0, Math.min(1, info.local / scenes[info.idx].ms) * W, 4 * S);
    desenhados++;
    perfDraw += performance.now() - _td; perfDrawN++;
    window.__p = f / totalFrames;
  }

  var ultimoIdx = -1, desenhados = 0, ultimoDesenho = -1;
  var INTERVALO = 1000 / FPS;
  var t0 = null;
  /* medidores: sem eles a gente chuta de onde vem o tempo perdido */
  var perfTick = 0, perfTickN = 0, perfBake = 0, perfBakeN = 0;
  var perfDraw = 0, perfDrawN = 0, perfRast = 0, perfRastN = 0;
  var perfLag = 0, perfLagN = 0, proximo = 0;
  function tick() {
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
      /* segura o ultimo quadro antes de parar. Se parar na mesma hora, o
         codificador nao carimba o quadro final e o arquivo sai ~1% mais curto
         que a conta do HTML — em 57 s isso da 0,6 s. */
      setTimeout(function () { rec.stop(); }, 150);
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
  }

  /* ---------- 7. tique de TAXA CONSTANTE ---------- */
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
        (totalFrames / gasto).toFixed(1) + ' quadros/s de render, passo ' + PASSO +
        ' ms) — sem repetidos por construcao');
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
    setTimeout(tickCFR, PASSO);
  }

  /* aquece: sem o primeiro quadro decodificado a gravacao comeca com tela vazia */
  carregarOverlays(function () {
    L('overlays prontos');
    for (var k = 0; k < LOOK; k++) pedir(k);
    var tent = 0;
    (function espera() {
      if (ready[0] || ++tent > 300) {
        L('quadro 0 ' + (ready[0] ? 'pronto' : 'NAO decodificou') + ' apos ' + tent + ' tentativas');
        rec.start();
        requestAnimationFrame(CFR ? tickCFR : tick);
      } else setTimeout(espera, 20);
    })();
  });
})();
