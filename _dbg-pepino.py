# -*- coding: utf-8 -*-
"""Debug: por que o regex do bloco `dente` nao casa."""
import io
import re

d = io.open('_criar-pepino-alho.py', encoding='utf-8', newline='').read()

for nome, fim in (('dente', r'\n\n\ndef colher_sal\('),
                  ('bulbo_alho', r'\n\n\n# ---'),
                  ('s0', r'\n\n\n# ---'),
                  ('s3', r'\n\n\n# ---')):
    pat = re.compile(r'def %s\(.*?\n(?=%s)' % (nome, fim), re.S)
    print('%-11s padrao=%r' % (nome, pat.pattern))
    print('%-11s inicio em %d | findall %d'
          % (nome, d.find('def %s(' % nome), len(pat.findall(d))))

print()
print('--- o que vem depois de `def dente` ---')
i = d.find('def dente(')
print(repr(d[i:i + 40]))
j = d.find('colher_sal')
print(repr(d[j - 30:j + 20]))
print('--- o que vem depois de `def bulbo_alho` ---')
k = d.find('def bulbo_alho(')
print(repr(d[k:k + 30]))
m = d.find('# ---')
print(repr(d[m - 30:m + 40]))
print('--- quantos `\\n\\n\\n` existem ---', d.count('\n\n\n'))
