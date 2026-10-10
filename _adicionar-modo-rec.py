# -*- coding: utf-8 -*-
"""Adiciona o modo ?rec (gravacao) nos arquivos EN.

Sem ?rec na URL, NADA muda. Com ?rec, o palco preenche 1080x1920
(ou 1920x1080 no video longo), a capa some, os botoes somem e a
animacao comeca sozinha. Verificado por render: o texto sai nitido.
"""
import re, glob, os, shutil, sys

APLICAR = '--apply' in sys.argv

BLOCO = """<script>
/* ?rec = modo gravacao.
   Sem ?rec na URL, nada muda: e o short normal.
   Com ?rec, o quadro preenche 1080x1920 (1920x1080 no video longo),
   a capa e os botoes somem e a animacao comeca sozinha. */
(function () {
  if (location.search.indexOf('rec') < 0) return;
  var css = '#cover{display:none!important}.ui{display:none!important}'
          + '#stage{border-radius:0!important;box-shadow:none!important}';
  var st = document.getElementById('stage');
  if (st) {
    var w = st.offsetWidth, h = st.offsetHeight;
    if (w && h) {
      css += '#stage{transform:scale(' + ((h > w ? 1920 : 1080) / h)
           + ')!important;transform-origin:center center!important}';
    }
  }
  if (document.getElementById('frame')) {
    css += '#frame{transform:scale(1)!important;left:0!important;top:0!important}';
  }
  var tag = document.createElement('style');
  tag.textContent = css;
  document.head.appendChild(tag);
  if (typeof showChapters === 'function') showChapters(false);
  setTimeout(function () { if (typeof play === 'function') play(); }, 500);
})();
</script>
"""

vistos, alvos = set(), []
for padrao in ('*/shorts*.html', '*/*.html'):
    for f in sorted(glob.glob(padrao)):
        f = f.replace('\\', '/')
        if f in vistos:
            continue
        vistos.add(f)
        b = os.path.basename(f)
        if '-en' not in b:
            continue
        if any(x in f for x in ('_teste-rec', '_arquivo', 'galeria',
                                'guia-capcut', 'aula')):
            continue
        if b.startswith('cartao-'):
            continue
        alvos.append(f)

print('arquivos EN a considerar:', len(alvos))
print()

mudou = 0
for f in alvos:
    d = open(f, encoding='utf-8').read()
    if '?rec = modo gravacao' in d:
        print('%-50s ja tem ?rec' % f)
        continue

    i = d.find('#stage')
    if i < 0:
        i = d.find('#frame')
    bloco = d[i:i + 400] if i >= 0 else ''
    w = re.search(r'width:\s*(\d+)px', bloco)
    h = re.search(r'height:\s*(\d+)px', bloco)
    tam = '%sx%s' % (w.group(1) if w else '?', h.group(1) if h else '?')

    if i < 0 or not h:
        print('%-50s %-10s container nao legivel -> PULADO' % (f, tam))
        continue
    if '</body>' not in d:
        print('%-50s %-10s sem </body> -> PULADO' % (f, tam))
        continue

    novo = d.replace('</body>', BLOCO + '</body>', 1)
    assert novo != d
    print('%-50s %-10s %s' % (f, tam, 'GRAVANDO' if APLICAR else 'aplicaria'))
    if APLICAR:
        shutil.copy2(f, f + '.antes-do-rec')
        open(f, 'w', encoding='utf-8').write(novo)
        mudou += 1

print()
print('%d arquivo(s) gravado(s).' % mudou if APLICAR
      else 'dry-run — rode com --apply para gravar')
