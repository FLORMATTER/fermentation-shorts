"""_mp4/_filtrar-lote.py — o --todos passa a escolher direito, e ganha --lista.

Por que: o --todos varre a arvore inteira atras de `<svg class="scene"`. Isso pega
coisa que NAO e' short da serie:

  _revisao/_tmp/sheet0.html   folha de contato do _revisar-cenas.py (TEMP)
  _arquivo/*.html             prototipos antigos
  video-longo/player-*.html   16:9, tem fluxo proprio
  *-1080x1920.html            variante de estilo do MESMO video (regra: um por legume)
  shorts-*.html  (sem -en)    o original PT — o canal publica em ingles

Sem isso um lote de 13 vira um lote de 38, com prototipo e folha de contato no meio.

--lista  imprime o lote e sai, sem gravar. Serve para aprovar antes de gastar 3 h.
--todos-tudo  desliga o filtro (comportamento antigo).

Tres ancoras contadas. Aborta sem gravar se alguma nao casar uma vez.
"""
import sys

ARQ = '_gerar-mp4.js'
d = open(ARQ, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in d else '\n'
print('%s: fim de linha %s' % (ARQ, 'CRLF' if nl == '\r\n' else 'LF'))
orig = d

TROCAS = [
    # 1) a funcao de filtro, logo antes do bloco de escolha
    ("""/* tira as opcoes (--w=, --fps=) da lista de arquivos a gravar */
const alvos = process.argv.slice(2).filter(a => !/^--[a-z]+=\\d+$/.test(a));
let lista;
""",
     """/* tira as opcoes (--w=, --fps=) da lista de arquivos a gravar */
const alvos = process.argv.slice(2).filter(a => !/^--[a-z]+=\\d+$/.test(a));
/* --todos varre a arvore atras de `<svg class="scene"`, e isso pega coisa que nao
   e' short da serie. O filtro abaixo deixa passar so' o que se publica. */
const SO_EN = !process.argv.includes('--todos-tudo');
const LISTA = process.argv.includes('--lista');
function eShortPublicavel(f) {
  if (f.startsWith('_arquivo/')) return false;        /* prototipo */
  if (f.startsWith('_revisao/')) return false;        /* folha de contato (TEMP) */
  if (/player-video-longo/.test(f)) return false;     /* 16:9, fluxo proprio */
  if (/-1080x1920\\.html$/i.test(f)) return false;     /* variante do mesmo video */
  if (!/-en\\.html$/i.test(f)) return false;           /* original PT */
  return true;
}
let lista;
"""),

    # 2) aplicar o filtro
    ("""  lista = lista.filter(f => !fs.existsSync(path.join(RAIZ, f.replace(/\\.html$/i, '.mp4'))));
} else {""",
     """  lista = lista.filter(f => !fs.existsSync(path.join(RAIZ, f.replace(/\\.html$/i, '.mp4'))));
  if (SO_EN) lista = lista.filter(eShortPublicavel);
} else {"""),

    # 3) --lista: mostrar e sair
    ("""if (!lista.length) { console.log('nada para gravar.'); process.exit(0); }
console.log('a gravar: ' + lista.length + ' short(s)\\n');
""",
     """if (!lista.length) { console.log('nada para gravar.'); process.exit(0); }

if (LISTA) {
  let total = 0;
  console.log('lote (' + lista.length + ' short(s), filtro ' + (SO_EN ? 'ligado' : 'DESLIGADO') + '):\\n');
  for (const f of lista) {
    const s = duracaoDoHtml(fs.readFileSync(path.join(RAIZ, f), 'utf8'));
    total += s;
    console.log('  ' + s.toFixed(1).padStart(6) + 's  ' + f);
  }
  console.log('\\n  total ' + total.toFixed(0) + 's de video');
  console.log('  ~' + (total * 8 / 60).toFixed(0) + ' min de render em 1080p (passo 150)');
  console.log('\\n  nada foi gravado (--lista).');
  process.exit(0);
}

console.log('a gravar: ' + lista.length + ' short(s)\\n');
"""),
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
