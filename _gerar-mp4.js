/* _gerar-mp4.js — grava um short HTML+SVG direto em .mp4, sem ffmpeg.

   Uso:  node _gerar-mp4.js mosquito/shorts-mosquito-trap-en.html
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

   Como funciona:
   1. injeta o _mp4/render.js no HTML;
   2. serve essa pagina por HTTP num servidor proprio (mesma origem -> o navegador
      DEVOLVE o mp4 por POST, sem passar pelo CDP e sem limite de tamanho);
   3. abre no Chrome headless; o proprio navegador desenha quadro a quadro e
      codifica em H.264/MP4;
   4. confere a duracao real do arquivo e RECUSA se nao bater com o esperado.

   O short original NUNCA e alterado.
*/
const { spawn, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const http = require('http');

const RAIZ = __dirname;
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const CDP_PORT = 9333;
/* --w=NNN e --fps=NN sobrescrevem o tamanho/taxa do mp4 (padrao 1080x1920 a 30).
   O custo de codificar acompanha a area, entao isso e o botao de troca entre
   resolucao e fluidez. */
const LARGURA = (function () {
  const a = process.argv.find(x => /^--w=\d+$/.test(x));
  return a ? parseInt(a.slice(4), 10) : 1080;
})();
const TAXA = (function () {
  const a = process.argv.find(x => /^--fps=\d+$/.test(x));
  return a ? parseInt(a.slice(6), 10) : 30;
})();
/* teto de bitrate em kbps (padrao 3000). 3000 e' o que os mp4 ja entregues
   usam; 1080x1920 de desenho chapado nao precisa de mais. */
const KBPS = (function () {
  const a = process.argv.find(x => /^--kbps=\d+$/.test(x));
  return a ? parseInt(a.slice(7), 10) : 3000;
})();
/* --cfr=1 = TAXA CONSTANTE. O render desenha todos os quadros o mais rapido que
   a maquina der (sem olhar o relogio) e o _mp4/retimar.py reescreve a duracao
   de cada amostra. Assim nenhum quadro repete. */
const CFR = process.argv.includes('--cfr=1');
/* --passo=NN = intervalo minimo entre quadros em CFR, em ms. Existe para NAO
   perder quadro: o requestFrame() do captureStream(0) SOBRESCREVE o quadro que
   ainda nao foi consumido, e o MediaRecorder descarta o resto quando a fila do
   codificador enche. Sem espera, em 1080p, 31% dos quadros somem.
   Padrao 60: medido em ~97% de sobrevivencia a ~2x a duracao do video. */
const PASSO = (function () {
  const a = process.argv.find(x => /^--passo=\d+$/.test(x));
  return a ? parseInt(a.slice(8), 10) : 60;
})();
/* Em CFR o arquivo cru tem a duracao do RENDER, nao a do video — entao retimar
   faz parte da gravacao, nao e' um passo separado. --sem-retimar desliga. */
const SEM_RETIMAR = process.argv.includes('--sem-retimar');

/* tira as opcoes (--w=, --fps=) da lista de arquivos a gravar */
const alvos = process.argv.slice(2).filter(a => !/^--[a-z]+=\d+$/.test(a));
/* --todos varre a arvore atras de `<svg class="scene"`, e isso pega coisa que nao
   e' short da serie. O filtro abaixo deixa passar so' o que se publica. */
const SO_EN = !process.argv.includes('--todos-tudo');
const LISTA = process.argv.includes('--lista');
/* Duplicata sob OUTRO NOME. A regra do gemeo (mais abaixo) tira o sufixo e
   procura o MESMO nome — o que nao resolve este caso, porque o mesmo video
   existe com outro nome. Comparado cena a cena em 19/09:
   `repolho/shorts-sauerkraut-en-1080x1920.html` e' o MESMO video que
   `repolho/shorts-repolho-maos-canva-en.html` — 8 cenas, 52,0 s, mesmas
   tags (`SAUERKRAUT n / 8`), mesmos titulos internos, mesmo CTA. E o
   `shorts-repolho-maos-canva-en.mp4` ja' existe (52,00 s, 1080x1920).
   Isto NAO e' filtro que esconde trabalho: e' lista NOMEADA, com o motivo,
   de duplicata ja' conferida. Para gravar de proposito, passar o arquivo
   pelo nome — argumento explicito nao passa por este filtro. */
const DUPLICATAS = {
  'repolho/shorts-sauerkraut-en-1080x1920.html':
    'mesmo video que repolho/shorts-repolho-maos-canva-en.html (8 cenas / 52,0 s / mp4 pronto)'
};
function eShortPublicavel(f) {
  if (DUPLICATAS[f]) return false;                    /* duplicata sob outro nome */
  if (f.startsWith('_arquivo/')) return false;        /* prototipo */
  if (f.startsWith('_revisao/')) return false;        /* folha de contato (TEMP) */
  if (/player-video-longo/.test(f)) return false;     /* 16:9, fluxo proprio */
  /* O sufixo do formato de upload (`-1080x1920`) vem DEPOIS do `-en`, entao a
     regra do `-en` (logo abaixo) nao o reconhecia e o arquivo sumia do lote.
     Tirar o sufixo ANTES deixa as outras regras verem o nome de verdade.
     E o sufixo so' marca VARIANTE se o gemeo sem ele existir: sem gemeo, e' um
     video proprio que nasceu no formato de upload. A regra antiga (negar pelo
     sufixo, ponto) escondia dois videos de verdade:
     `beterraba/shorts-beet-garlic-en` e `repolho/shorts-sauerkraut-en`.
     Filtro que esconde trabalho e' pior que filtro nenhum. */
  let nome = f.replace(/\.html$/i, '');
  const SUF = '-1080x1920';
  if (nome.toLowerCase().endsWith(SUF)) {
    const base = nome.slice(0, -SUF.length) + '.html';
    if (fs.existsSync(path.join(RAIZ, base))) return false;
    nome = nome.slice(0, -SUF.length);
  }
  if (!/-en$/i.test(nome)) return false;              /* original PT */
  return true;
}
let lista;
if (!alvos.length || alvos[0] === '--todos' || LISTA) {
  lista = [];
  (function anda(dir) {
    for (const f of fs.readdirSync(dir)) {
      const p = path.join(dir, f);
      const st = fs.statSync(p);
      if (st.isDirectory()) {
        if (f.startsWith('.') || f === 'node_modules') continue;
        anda(p);
      } else if (/\.html$/i.test(f) && /<svg class="scene/.test(fs.readFileSync(p, 'utf8'))) {
        lista.push(path.relative(RAIZ, p).replace(/\\/g, '/'));
      }
    }
  })(RAIZ);
  lista = lista.filter(f => !fs.existsSync(path.join(RAIZ, f.replace(/\.html$/i, '.mp4'))));
  if (SO_EN) lista = lista.filter(eShortPublicavel);
} else {
  lista = alvos.map(a => a.replace(/\\/g, '/'));
}

if (!lista.length) { console.log('nada para gravar.'); process.exit(0); }

if (LISTA) {
  let total = 0;
  const pastas = new Map();
  for (const f of lista) {
    const s = duracaoDoHtml(fs.readFileSync(path.join(RAIZ, f), 'utf8'));
    total += s;
    const p = f.split('/')[0];
    if (!pastas.has(p)) pastas.set(p, []);
    pastas.get(p).push([s, f]);
  }
  console.log('lote (' + lista.length + ' short(s), filtro ' + (SO_EN ? 'ligado' : 'DESLIGADO') +
              '):\n');
  for (const [p, itens] of pastas) {
    const soma = itens.reduce((a, b) => a + b[0], 0);
    /* Pasta com mais de um candidato = o MESMO video em estilo diferente. A regra
       do canal e' postar um por legume (risco de "conteudo inautentico"). */
    const marca = itens.length > 1 ? '  <-- ' + itens.length + ' variantes do MESMO video' : '';
    console.log('  ' + p + '/' + marca);
    for (const [s, f] of itens) console.log('      ' + s.toFixed(1).padStart(6) + 's  ' + f.split('/').pop());
    if (itens.length > 1) console.log('      ' + soma.toFixed(1).padStart(6) + 's  (a pasta toda)');
  }
  console.log('\n  total ' + total.toFixed(0) + 's de video');
  /* render/video ~= 0,3 + 0,031 * passo, ajustado nos pontos medidos em 1080p
     (40 ms -> 1,5x | 80 ms -> 2,6x | 120 ms -> 4,0x). E' estimativa, nao promessa. */
  console.log('  ~' + (total * (0.3 + 0.031 * PASSO) / 60).toFixed(0) +
              ' min de render em 1080p (passo ' + PASSO + ' ms)');
  console.log('\n  nada foi gravado (--lista).');
  process.exit(0);
}

console.log('a gravar: ' + lista.length + ' short(s)\n');

const sleep = ms => new Promise(r => setTimeout(r, ms));

function duracaoDoHtml(html) {
  const ms = [...html.matchAll(/\bms\s*:\s*(\d+)/g)].map(m => +m[1]);
  return ms.reduce((a, b) => a + b, 0) / 1000;
}

/* Le a duracao real do .mp4 pelo box mvhd. Sem ffmpeg. */
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

async function gravar(rel) {
  const origem = path.join(RAIZ, rel);
  const html = fs.readFileSync(origem, 'utf8');
  const dur = duracaoDoHtml(html);
  if (!dur) { console.log('  PULADO (nao achei duracao): ' + rel); return false; }
  const saida = origem.replace(/\.html?$/i, '.mp4');

  const render = fs.readFileSync(path.join(RAIZ, '_mp4', 'render.js'), 'utf8');
  const pagina = html.replace(/<\/body>/i,
    '<script>window.__MP4POST="/save";</script>\n<script>\n' + render + '\n</script>\n</body>');

  let terminou = null;
  const srv = http.createServer((req, res) => {
    if (req.method === 'POST' && req.url.indexOf('/save') === 0) {
      const partes = [];
      req.on('data', c => partes.push(c));
      req.on('end', () => {
        const buf = Buffer.concat(partes);
        fs.writeFileSync(saida, buf);
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('ok');
        terminou = buf.length;
      });
      return;
    }
    if (req.url.indexOf('/short.html') === 0) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(pagina);
      return;
    }
    res.writeHead(404); res.end();
  });
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const porta = srv.address().port;

  const perfil = path.join(os.tmpdir(), 'mp4-chrome-profile');
  /* Perfil NOVO a cada gravacao. Reusar o mesmo perfil degrada o render: a mesma
     configuracao caiu de 16,1 para 11,5 quadros/s ao longo de uma sessao, e
     apagar o perfil devolveu o desempenho. */
  try { fs.rmSync(perfil, { recursive: true, force: true }); } catch (e) {}
  fs.mkdirSync(perfil, { recursive: true });
  const chrome = spawn(CHROME, [
    '--headless=new', '--remote-debugging-port=' + CDP_PORT, '--user-data-dir=' + perfil,
    '--no-first-run', '--no-default-browser-check', '--disable-extensions',
    '--no-sandbox', '--mute-audio', '--hide-scrollbars',
    '--window-size=' + LARGURA + ',' + Math.round(LARGURA * 16 / 9),
    '--force-device-scale-factor=1',
    '--disable-background-timer-throttling', '--disable-renderer-backgrounding',
    '--disable-backgrounding-occluded-windows',

    'http://127.0.0.1:' + porta + '/short.html?mp4w=' + LARGURA + '&mp4fps=' + TAXA +
      '&mp4kbps=' + KBPS + (CFR ? '&mp4cfr=1' : '') + (PASSO ? '&mp4passo=' + PASSO : ''),
  ], { stdio: 'ignore' });

  let ok = false;
  try {
    let tl = null;
    for (let i = 0; i < 80; i++) {
      try {
        const r = await fetch('http://127.0.0.1:' + CDP_PORT + '/json/list');
        const j = await r.json();
        tl = j.find(t => t.type === 'page' && t.url.indexOf('/short.html') > 0) || j.find(t => t.type === 'page');
        if (tl) break;
      } catch (e) {}
      await sleep(250);
    }
    if (!tl) throw new Error('o Chrome nao abriu a pagina');

    const ws = new WebSocket(tl.webSocketDebuggerUrl);
    let id = 0;
    const esperando = new Map();
    ws.addEventListener('message', ev => {
      const m = JSON.parse(ev.data);
      if (m.id && esperando.has(m.id)) { esperando.get(m.id)(m); esperando.delete(m.id); }
    });
    await new Promise((res, rej) => {
      ws.addEventListener('open', res);
      ws.addEventListener('error', () => rej(new Error('websocket falhou')));
    });
    const send = (method, params) => new Promise(res => {
      const i = ++id; esperando.set(i, res);
      ws.send(JSON.stringify({ id: i, method, params: params || {} }));
    });
    await send('Page.enable');
    await send('Runtime.enable');

    const t0 = Date.now();
    /* Em CFR o render NAO acompanha o relogio: ele desenha todos os quadros o
       mais rapido que der, entao uma gravacao de 57 s pode levar 3 min. */
    const teto = CFR ? dur * 8 + 300 : dur + 180;
    let ultimoPct = -1, estado = null;
    while (Date.now() - t0 < teto * 1000) {
      const r = await send('Runtime.evaluate', {
        expression: 'JSON.stringify({d:window.__done||"",e:window.__enviado||"",p:window.__p||0})',
        returnByValue: true,
      });
      const v = r.result && r.result.result && r.result.result.value;
      if (v) {
        const o = JSON.parse(v);
        const pct = Math.floor(o.p * 100);
        if (pct !== ultimoPct) { ultimoPct = pct; process.stdout.write('\r  gravando ' + String(pct).padStart(3) + '%   '); }
        if (o.d && o.e) { estado = o; break; }
        if (o.d === 'FAIL') { estado = o; break; }
      }
      await sleep(350);
    }
    const lg = await send('Runtime.evaluate', { expression: 'JSON.stringify(window.__log||[])', returnByValue: true });
    const linhas = JSON.parse((lg.result && lg.result.result && lg.result.result.value) || '[]');
    console.log('');
    linhas.forEach(l => console.log('    ' + l));

    if (!estado || estado.d !== 'OK') throw new Error('gravacao nao terminou: ' + (estado ? estado.d : 'TIMEOUT'));
    if (estado.e !== 'OK') throw new Error('o navegador nao conseguiu gravar o arquivo: ' + estado.e);
    if (!terminou) throw new Error('o arquivo nao chegou pelo POST');

    const mb = fs.statSync(saida).size / 1048576;
    const real = duracaoMp4(fs.readFileSync(saida));
    console.log('  arquivo : ' + saida.replace(RAIZ + path.sep, '').replace(/\\/g, '/') + '  (' + mb.toFixed(1) + ' MB)');
    console.log('  duracao : alvo ' + dur.toFixed(1) + 's | no arquivo ' + real.toFixed(1) + 's');
    if (!real) throw new Error('nao consegui ler a duracao do mp4');
    /* tolerancia PROPORCIONAL: o codificador sempre perde ~1% no fim (o ultimo
       quadro nao e carimbado). 0,6 s fixos reprovavam um video de 57 s que estava
       certo e aprovavam 0,6 s de erro num video de 5 s. */
    if (CFR && !SEM_RETIMAR) {
      /* Retima AQUI. Deixar para depois e' pe' de cabra: o arquivo cru dura o
         render inteiro (4 a 5x o video) e nada no arquivo avisa disso. */
      const quadros = Math.ceil(dur * TAXA);
      const r = spawnSync('python',
        [path.join(RAIZ, '_mp4', 'retimar.py'), saida, '--fps=' + TAXA, '--quadros=' + quadros],
        { encoding: 'utf8' });
      if (r.error) throw new Error('nao consegui rodar o retimar.py: ' + r.error.message);
      (r.stdout || '').trim().split('\n').forEach(l => console.log('    ' + l));
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
    } else {
      const tol = Math.max(0.6, dur * 0.02);
      if (Math.abs(real - dur) > tol) {
        fs.unlinkSync(saida);
        throw new Error('saiu ' + (dur / real).toFixed(2) + 'x ' + (real < dur ? 'ACELERADO' : 'lento') +
                        ' — o canvas nao desenhou no ritmo pedido. Arquivo apagado.');
      }
      console.log('  duracao confere.');
    }
    ws.close();
    ok = true;
  } catch (e) {
    console.log('  ERRO: ' + e.message);
  } finally {
    try { chrome.kill(); } catch (_) {}
    try { srv.close(); } catch (_) {}
  }
  return ok;
}

(async () => {
  let bons = 0;
  for (const rel of lista) {
    console.log('== ' + rel);
    if (await gravar(rel)) bons++;
    await sleep(600);
  }
  console.log('\n' + bons + '/' + lista.length + ' gravado(s).');
  process.exit(bons === lista.length ? 0 : 1);
})();
