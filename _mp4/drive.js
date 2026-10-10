/* Driver minimo de CDP (sem dependencia nenhuma: Node 22 tem fetch e WebSocket).
   Uso: node _mp4/drive.js <url> <pasta-download> <segundos-max> */
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const URL_ = process.argv[2];
const DL = process.argv[3];
const MAXS = parseInt(process.argv[4] || '90', 10);
const PORT = 9333;

const profile = path.join(os.tmpdir(), 'mp4-chrome-profile');
fs.mkdirSync(profile, { recursive: true });
fs.mkdirSync(DL, { recursive: true });

const args = [
  '--headless=new',
  '--remote-debugging-port=' + PORT,
  '--user-data-dir=' + profile,
  '--no-first-run', '--no-default-browser-check', '--disable-extensions',
  '--disable-gpu', '--no-sandbox', '--mute-audio', '--hide-scrollbars',
  '--window-size=1080,1920',
  '--disable-background-timer-throttling',
  '--disable-renderer-backgrounding',
  '--disable-backgrounding-occluded-windows',
  '--autoplay-policy=no-user-gesture-required',
  URL_,
];
const chrome = spawn(CHROME, args, { stdio: 'ignore' });

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function targets() {
  const r = await fetch('http://127.0.0.1:' + PORT + '/json/list');
  return r.json();
}

async function main() {
  let list = null;
  for (let i = 0; i < 60; i++) {
    try { list = await targets(); if (list && list.length) break; } catch (e) {}
    await sleep(250);
  }
  if (!list) throw new Error('nao consegui falar com o Chrome');
  const page = list.find(t => t.type === 'page' && t.url.indexOf('http') !== 0 || t.type === 'page');
  if (!page) throw new Error('sem target de pagina');
  console.log('target:', page.url.slice(0, 90));

  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 0;
  const waiting = new Map();
  ws.addEventListener('message', ev => {
    const m = JSON.parse(ev.data);
    if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); }
  });
  await new Promise((res, rej) => {
    ws.addEventListener('open', res);
    ws.addEventListener('error', rej);
  });
  const send = (method, params) => new Promise(res => {
    const i = ++id;
    waiting.set(i, res);
    ws.send(JSON.stringify({ id: i, method, params: params || {} }));
  });

  await send('Page.enable');
  await send('Runtime.enable');
  await send('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: DL, eventsEnabled: true });

  const t0 = Date.now();
  let done = null;
  while (Date.now() - t0 < MAXS * 1000) {
    const r = await send('Runtime.evaluate', {
      expression: 'JSON.stringify({d: window.__done||"", l: window.__log||[], s: window.__size||0})',
      returnByValue: true,
    });
    const v = r.result && r.result.result && r.result.result.value;
    if (v) {
      const o = JSON.parse(v);
      if (o.d) { done = o; console.log('log da pagina:\n  ' + o.l.join('\n  ')); break; }
    }
    await sleep(400);
  }
  console.log('resultado:', done ? done.d + ' size=' + done.s : 'TIMEOUT');

  // ---- tira o blob de dentro do navegador em pedacos de 4 MB ----
  if (done && done.d === 'OK' && done.s > 0) {
    const CH = 4 * 1024 * 1024;
    const saida = path.join(DL, path.basename(URL_).replace(/\.html?$/i, '') + '.mp4');
    const fd = fs.openSync(saida, 'w');
    const expr =
      '(function(){var b=window.__blob.slice(window.__off, window.__off+' + CH + ');' +
      'return b.arrayBuffer().then(function(ab){var u=new Uint8Array(ab),s="";' +
      'for(var i=0;i<u.length;i+=0x8000){s+=String.fromCharCode.apply(null,u.subarray(i,i+0x8000));}' +
      'return btoa(s);});})()';
    let off = 0, escrito = 0;
    while (escrito < done.s) {
      await send('Runtime.evaluate', {
        expression: 'window.__off=' + off + ';1', returnByValue: true,
      });
      const r = await send('Runtime.evaluate', {
        expression: expr, awaitPromise: true, returnByValue: true,
      });
      const res = r.result && r.result.result;
      const b64 = res && res.value;
      if (!b64) {
        console.log('  falhou no pedaco ' + off + ' :: ' +
          JSON.stringify((r.result && (r.result.exceptionDetails || r.result.result)) || {}).slice(0, 300));
        break;
      }
      const buf = Buffer.from(b64, 'base64');
      fs.writeSync(fd, buf);
      escrito += buf.length;
      off += CH;
      process.stdout.write('\r  ' + Math.round(escrito / done.s * 100) + '% (' + escrito + ' bytes)   ');
    }
    fs.closeSync(fd);
    console.log('\nmp4 gravado: ' + saida + '  (' + fs.statSync(saida).size + ' bytes)');
  }
  ws.close();
  chrome.kill();
}

main().catch(e => { console.error('ERRO:', e.message); try { chrome.kill(); } catch (_) {} process.exit(1); });
