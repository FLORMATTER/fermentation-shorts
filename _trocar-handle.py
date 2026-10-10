# -*- coding: utf-8 -*-
"""Troca o @handle do canal em TODOS os arquivos de uma vez.

Os arquivos vem com um placeholder (`@yourchannel` nos EN, `@seucanal` nos PT).
Enquanto ele estiver la, o video publicado sai com "@yourchannel" escrito.

Uso:
    python _trocar-handle.py                      # so mostra o que existe hoje
    python _trocar-handle.py @meucanal            # dry-run com o nome novo
    python _trocar-handle.py @meucanal --apply    # grava (faz backup)
    python _trocar-handle.py --limpar --apply     # apaga o handle de vez

O nome pode vir com ou sem @ — o script normaliza.
"""
import glob, os, re, shutil, sys

args = [a for a in sys.argv[1:] if not a.startswith('--')]
APLICAR = '--apply' in sys.argv
LIMPAR = '--limpar' in sys.argv

PLACEHOLDERS = ('@yourchannel', '@seucanal', '@yourhandle')
# o .wm pode aparecer tambem em maiuscula se o texto tiver sido salvo assim
PADRAO = re.compile(r'(<div class="wm">)(@[A-Za-z0-9_.-]+)(</div>)')

if LIMPAR:
    novo_handle = ''
elif args:
    novo_handle = args[0] if args[0].startswith('@') else '@' + args[0]
    if not re.fullmatch(r'@[A-Za-z0-9_.-]+', novo_handle):
        print('handle invalido: %r  (use letras, numeros, _ . -)' % novo_handle)
        sys.exit(1)
else:
    novo_handle = None

vistos, arquivos = set(), []
for padrao in ('*/shorts*.html', '*/*.html', '*.html'):
    for f in sorted(glob.glob(padrao)):
        f = f.replace('\\', '/')
        if f in vistos:
            continue
        vistos.add(f)
        if '_teste-rec' in f or '_arquivo' in f or '_revisao' in f:
            continue
        arquivos.append(f)

print('handle atual no codigo:', PLACEHOLDERS)
print('handle novo          :', repr(novo_handle) if novo_handle is not None
      else '(nao informado — so listando)')
print()

achados = {}
for f in arquivos:
    d = open(f, encoding='utf-8', errors='replace').read()
    for m in PADRAO.finditer(d):
        achados.setdefault(m.group(2), []).append(f)

if not achados:
    print('nenhum .wm encontrado.')
    sys.exit(0)

for h, fs in sorted(achados.items()):
    print('%-16s em %d arquivo(s)' % (h, len(fs)))

if novo_handle is None:
    print('\ninforme o handle para trocar. ex: python _trocar-handle.py @meucanal')
    sys.exit(0)

mudou = 0
for f in arquivos:
    d = open(f, encoding='utf-8', errors='replace').read()
    if not PADRAO.search(d):
        continue
    novo = PADRAO.sub(lambda m: m.group(1) + novo_handle + m.group(3), d)
    if novo == d:
        continue
    mudou += 1
    if APLICAR:
        shutil.copy2(f, f + '.antes-do-handle')
        open(f, 'w', encoding='utf-8').write(novo)

print()
print('%d arquivo(s) %s' % (mudou, 'GRAVADO(S)' if APLICAR else 'a mudar (dry-run)'))
if APLICAR:
    print('backup: <arquivo>.antes-do-handle')
else:
    print('rode com --apply para gravar')
