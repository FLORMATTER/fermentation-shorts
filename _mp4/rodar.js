/* _mp4/rodar.js — abre uma pagina no Chrome headless e imprime window.__log.
   Uso: node _mp4/rodar.js <url> [segundos] [--file-access] */
const { spawn } = require('child_process');
const path = require('path');
const os = require('os');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const URL_ = process.argv[2];
const MAXS = parseInt(process.argv[3] || '60', 10);
const FILE_ACCESS = process.argv.includes('--file-access');
const PORT = 9345;

const perfil = path.join(os.tmpdir(), 'rodar-chrome-profile');
const args = [
  '--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + perfil,
  '--no-first-run', '--no-default-browser-check', '--disable-extensions',
  '--no-sandbox', '--mute-audio', '--hide-scrollbars', '--window-size=1200,1400',
];
if (FILE_ACCESS) args.push('--allow-file-access-from-files');
args.push(URL_);
const chrome = spawn(CHROME, args, { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  let tl = null;
  for (let i = 0; i < 80; i++) {
    try {
      const r = await fetch('http://127.0.0.1:' + PORT + '/json/list');
      const j = await r.json();
      tl = j.find(t => t.type === 'page');
      if (tl) break;
    } catch (e) {}
    await sleep(250);
  }
  if (!tl) { console.log('Chrome nao abriu'); process.exit(1); }
  const ws = new WebSocket(tl.webSocketDebuggerUrl);
  let id = 0; const esperando = new Map();
  ws.addEventListener('message', ev => {
    const m = JSON.parse(ev.data);
    if (m.id && esperando.has(m.id)) { esperando.get(m.id)(m); esperando.delete(m.id); }
  });
  await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
  const send = (method, params) => new Promise(res => {
    const i = ++id; esperando.set(i, res);
    ws.send(JSON.stringify({ id: i, method, params: params || {} }));
  });
  await send('Runtime.enable');
  const t0 = Date.now();
  let visto = null;
  while (Date.now() - t0 < MAXS * 1000) {
    const r = await send('Runtime.evaluate', {
      expression: 'JSON.stringify({d:window.__done||"",l:window.__log||[]})', returnByValue: true,
    });
    const v = r.result && r.result.result && r.result.result.value;
    if (v) {
      const o = JSON.parse(v);
      if (o.d) { visto = o; break; }
    }
    await sleep(400);
  }
  console.log(visto ? visto.l.join('\n') : '(timeout, nada em __log)');
  ws.close(); chrome.kill();
  process.exit(visto && visto.d === 'OK' ? 0 : 1);
})().catch(e => { console.error('ERRO:', e.message); try { chrome.kill(); } catch (_) {} process.exit(1); });
