/* _mp4/quadros-mp4.js — extrai quadros REAIS de um .mp4 para conferir olhando.
 *
 * Por que nao usar seek: a versao antiga (conferir-mp4.py) buscava 8 instantes com
 * `v.currentTime = t`. Dois defeitos somados davam veredito FALSO de "8 quadros
 * identicos":
 *   1. disparar os 8 seeks de uma vez faz o navegador coalescer tudo num so;
 *   2. a "rede de seguranca" de 1200 ms desenhava de qualquer jeito, e com
 *      --virtual-time-budget esse timer dispara na hora — entao o canvas pegava
 *      o quadro que estivesse decodificado, nao o quadro buscado.
 *
 * Aqui nao tem seek: o video TOCA do comeco ao fim e a gente tira uma foto quando
 * o tempo de midia cruza cada alvo (requestVideoFrameCallback). E o caminho que o
 * proprio player usa, entao nao tem como divergir.
 *
 * Uso: node _mp4/quadros-mp4.js <arquivo.mp4> [quantos]
 * Saida: _revisao/<nome>-mp4.png
 */
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const RAIZ = path.dirname(__dirname);
const REL = process.argv[2];
const N = parseInt(process.argv[3] || '8', 10);
/* --tempos=0.5,4.4,30,56.5 : amostra estes instantes em vez de dividir por igual.
   Serve para conferir as PONTAS (0 s e o fim), onde o MediaRecorder costuma
   deixar quadro em branco. */
const TEMPOS = (function () {
  const a = process.argv.find(x => x.indexOf('--tempos=') === 0);
  return a ? a.slice(9).split(',').map(Number).filter(n => !isNaN(n)) : [];
})();
const CDP_PORT = 9351;

if (!REL) { console.error('uso: node _mp4/quadros-mp4.js <arquivo.mp4> [quantos]'); process.exit(1); }
const ARQ = path.resolve(RAIZ, REL);
if (!fs.existsSync(ARQ)) { console.error('nao existe: ' + ARQ); process.exit(1); }
const MP4 = fs.readFileSync(ARQ);

const PAGINA = `<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
body{margin:0;background:#111;font:600 12px system-ui;color:#eee}
#g{display:flex;flex-wrap:wrap;gap:8px;padding:8px}
figure{margin:0;width:270px}
canvas{width:270px;height:480px;display:block;background:#000}
figcaption{padding:3px 0}
</style></head><body>
<div id="g"></div>
<video id="v" src="/video.mp4" preload="auto" muted playsinline style="display:none"></video>
<script>
window.__log = []; window.__erro = '';
function L(s){ window.__log.push(s); }
var v = document.getElementById('v'), g = document.getElementById('g');
var N = ${N}, alvos = [], cvs = [], feitos = 0, DUR = 0;

function cria(){
  DUR = v.duration;
  L('duracao no player: ' + DUR.toFixed(2) + 's');
  L('resolucao: ' + v.videoWidth + 'x' + v.videoHeight);
  if (!(DUR > 0)) { window.__erro = 'duracao invalida'; window.__done = 'FAIL'; return; }
  var pedidos = ${JSON.stringify(TEMPOS)};
  if (pedidos.length) { alvos = pedidos.slice(); N = alvos.length; }
  else { var passo = DUR / (N + 1); for (var q = 1; q <= N; q++) alvos.push(passo * q); }
  for (var j = 0; j < alvos.length; j++){
    var cv = document.createElement('canvas');
    cv.width = 540; cv.height = 960;
    var fig = document.createElement('figure');
    var cp = document.createElement('figcaption');
    cp.textContent = 't = ' + alvos[j].toFixed(1) + 's';
    fig.appendChild(cv); fig.appendChild(cp); g.appendChild(fig);
    cvs.push({ cv: cv, ok: false });
  }
  if (typeof v.requestVideoFrameCallback !== 'function'){
    window.__erro = 'sem requestVideoFrameCallback'; window.__done = 'FAIL'; return;
  }
  v.play().catch(function(e){ window.__erro = 'play falhou: ' + e.message; window.__done = 'FAIL'; });
  v.requestVideoFrameCallback(passo_);
}

function passo_(agora, meta){
  var t = meta.mediaTime;
  for (var j = 0; j < N; j++){
    if (!cvs[j].ok && t >= alvos[j]){
      cvs[j].cv.getContext('2d').drawImage(v, 0, 0, 540, 960);
      cvs[j].ok = true; feitos++;
      L('quadro ' + (j + 1) + ' capturado em t=' + t.toFixed(2) + 's');
    }
  }
  if (feitos >= N) { window.__done = 'OK'; return; }
  v.requestVideoFrameCallback(passo_);
}

v.addEventListener('loadedmetadata', cria);
v.addEventListener('ended', function(){
  L('video terminou com ' + feitos + ' de ' + N + ' quadros');
  window.__done = 'OK';
});
v.addEventListener('error', function(){ window.__erro = 'video nao carregou'; window.__done = 'FAIL'; });
<\/script></body></html>`;

const srv = http.createServer((req, res) => {
  if (req.url.indexOf('/video.mp4') === 0) {
    const r = req.headers.range;
    if (r) {
      const m = /bytes=(\d*)-(\d*)/.exec(r);
      const ini = m[1] ? parseInt(m[1], 10) : 0;
      const fim = m[2] ? parseInt(m[2], 10) : MP4.length - 1;
      res.writeHead(206, {
        'Content-Type': 'video/mp4',
        'Accept-Ranges': 'bytes',
        'Content-Range': 'bytes ' + ini + '-' + fim + '/' + MP4.length,
        'Content-Length': fim - ini + 1,
      });
      res.end(MP4.slice(ini, fim + 1));
      return;
    }
    res.writeHead(200, { 'Content-Type': 'video/mp4', 'Accept-Ranges': 'bytes', 'Content-Length': MP4.length });
    res.end(MP4);
    return;
  }
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(PAGINA);
});

const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const porta = srv.address().port;
  const perfil = path.join(os.tmpdir(), 'quadros-chrome-profile');
  fs.mkdirSync(perfil, { recursive: true });

  const chrome = spawn(CHROME, [
    '--headless=new', '--remote-debugging-port=' + CDP_PORT, '--user-data-dir=' + perfil,
    '--no-first-run', '--no-default-browser-check', '--disable-extensions',
    '--no-sandbox', '--mute-audio', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required',
    '--window-size=1140,1060', '--force-device-scale-factor=1',
    'http://127.0.0.1:' + porta + '/',
  ], { stdio: 'ignore' });

  let ws = null;
  try {
    let tl = null;
    for (let i = 0; i < 80; i++) {
      try {
        const r = await fetch('http://127.0.0.1:' + CDP_PORT + '/json/list');
        const j = await r.json();
        tl = j.find(t => t.type === 'page' && t.url.indexOf('127.0.0.1:' + porta) > 0);
        if (tl) break;
      } catch (e) {}
      await sleep(250);
    }
    if (!tl) throw new Error('Chrome nao abriu');

    ws = new WebSocket(tl.webSocketDebuggerUrl);
    let id = 0; const pend = new Map();
    ws.addEventListener('message', ev => {
      const m = JSON.parse(ev.data);
      if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); }
    });
    await new Promise((res, rej) => {
      ws.addEventListener('open', res); ws.addEventListener('error', rej);
    });
    const send = (method, params) => new Promise(res => {
      const i = ++id; pend.set(i, res);
      ws.send(JSON.stringify({ id: i, method, params: params || {} }));
    });

    await send('Runtime.enable');
    await send('Page.enable');

    let estado = null;
    const t0 = Date.now();
    while (Date.now() - t0 < 240000) {
      const r = await send('Runtime.evaluate', {
        expression: 'JSON.stringify({d:window.__done||"",e:window.__erro||"",l:window.__log||[]})',
        returnByValue: true,
      });
      const val = r.result && r.result.result && r.result.result.value;
      if (val) {
        const o = JSON.parse(val);
        if (o.d) { estado = o; break; }
      }
      await sleep(500);
    }

    if (!estado) {
      console.log('(timeout esperando o video tocar ate o fim)');
    } else {
      estado.l.forEach(l => console.log('  ' + l));
      if (estado.e) console.log('  ERRO: ' + estado.e);
    }

    const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
    const data = shot.result && shot.result.data;
    if (!data) throw new Error('nao consegui tirar o screenshot');
    const png = path.join(RAIZ, '_revisao', path.basename(ARQ).replace(/\.mp4$/i, '-mp4.png'));
    fs.mkdirSync(path.dirname(png), { recursive: true });
    fs.writeFileSync(png, Buffer.from(data, 'base64'));
    console.log('  quadros extraidos: ' + png);
    process.exitCode = (estado && estado.d === 'OK') ? 0 : 1;
  } catch (e) {
    console.error('ERRO: ' + e.message);
    process.exitCode = 1;
  } finally {
    try { if (ws) ws.close(); } catch (_) {}
    chrome.kill();
    srv.close();
  }
})();
