# _mp4/_consertar-orcamento.py
# Dois consertos no _mp4/render.js, depois da medicao:
#
# 1. AS 7 CENAS ESCONDIDAS CONTINUAM ANIMANDO.
#    O CSS do short esconde cena com `visibility:hidden` (nao `display:none`),
#    entao as 64 animacoes das 8 cenas rodam durante toda a gravacao. O bake()
#    varria document.getAnimations() a cada quadro por causa disso. Agora a gente
#    guarda os objetos de animacao POR CENA e PAUSA todos no inicio; o bake so
#    mexe na cena da vez.
#
# 2. FILA LONGA DEMAIS.
#    LOOK=8 com o tique a ~13 Hz pedia quadros mais rapido do que desenhava:
#    203 quadros rasterizados para 84 desenhados. Com LOOK=3 e orcamento menor o
#    tique nao engasga e o desenho acompanha o relogio.
#
# Cada ancora tem que casar EXATAMENTE uma vez, senao aborta sem gravar.
import io, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALVO = os.path.join(RAIZ, '_mp4', 'render.js')

with io.open(ALVO, encoding='utf-8') as f:
    d = f.read()
crlf = '\r\n' in d
def N(s):
    return s.replace('\n', '\r\n') if crlf else s

trocas = []

# ---- 1. LOOK e ORCAMENTO ----
trocas.append((
    N('  var W = 1080, H = 1920, FPS = 30, LOOK = 8;\n'
      '  /* ORCAMENTO = quantos ms por tique podem ser gastos ASSANDO.\n'
      '     A fila por numero fixo de quadros (LOOK) travava o tique inteiro quando\n'
      '     assar+rasterizar ficava caro. Com orcamento, o desenho nunca espera. */\n'
      '  var ORCAMENTO = 10;'),
    N('  var W = 1080, H = 1920, FPS = 30, LOOK = 3;\n'
      '  /* LOOK = quantos quadros adiante assar. NAO precisa ser grande: o que manda\n'
      '     e a latencia de UMA rasterizacao. Com LOOK=8 o tique pedia quadros mais\n'
      '     rapido do que conseguia desenhar (203 rasterizados para 84 desenhados).\n'
      '     ORCAMENTO = teto de ms por tique gastos assando, para o tique nunca\n'
      '     engasgar e o desenho sair no relogio. */\n'
      '  var ORCAMENTO = 6;')
))

# ---- 2. indexarAnimados: guarda as animacoes por cena e PAUSA todas ----
ANTIGO_IDX = N('''  function indexarAnimados() {
    var mapa = {};
    document.getAnimations().forEach(function (a) {
      var alvo = a.effect && a.effect.target;
      var sv = alvo && alvo.closest ? alvo.closest('svg.scene') : null;
      if (!sv) return;
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
    L('elementos animados: ' + n);
    return mapa;
  }
  var animados = indexarAnimados();
  var cenaLigada = -1;''')

NOVO_IDX = N('''  var animsPorCena = {};
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
  var cenaLigada = -1;''')
trocas.append((ANTIGO_IDX, NOVO_IDX))

# ---- 3. bake: mexe SO nas animacoes da cena da vez ----
ANTIGO_BAKE = N('''    document.getAnimations().forEach(function (a) {
      var alvo = a.effect && a.effect.target;
      var sv = alvo && alvo.closest ? alvo.closest('svg.scene') : null;
      if (sv && sv.id === id) { a.pause(); a.currentTime = local; }
    });''')
NOVO_BAKE = N('''    /* so a cena da vez: as outras ja estao pausadas desde o inicio */
    var anims = animsPorCena[id] || [];
    for (var q = 0; q < anims.length; q++) anims[q].currentTime = local;''')
trocas.append((ANTIGO_BAKE, NOVO_BAKE))

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
for termo in ['LOOK = 3', 'ORCAMENTO = 6', 'animsPorCena', 'animacoes pausadas',
              'document.getAnimations().forEach(function (a) {\n      var alvo']:
    print('  %-46s %d' % (termo.replace('\n', ' / ')[:46], d.count(termo)))
