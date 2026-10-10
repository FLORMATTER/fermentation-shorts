# -*- coding: utf-8 -*-
"""Testa se transform:scale no #stage mantem o texto nitido a 1080x1920,
comparado com 'gravar pequeno e esticar no editor'.
"""
import os, subprocess
from PIL import Image

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
ORIG = 'rabanete/shorts-rabanete-animado-en.html'
OUT = '_teste-rec'
os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(OUT, 'profile')


def render(html_path, w, h, png):
    png = os.path.abspath(png)
    prof = os.path.abspath(TMP + '-' + os.path.basename(png).replace('.png', ''))
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
                    '--no-first-run', '--disable-extensions',
                    '--hide-scrollbars', '--force-device-scale-factor=1',
                    '--virtual-time-budget=6000',
                    '--user-data-dir=' + prof,
                    '--screenshot=' + png,
                    '--window-size=%d,%d' % (w, h),
                    'file:///' + os.path.abspath(html_path).replace('\\', '/')],
                   capture_output=True, timeout=90)
    print('  ->', png, 'existe' if os.path.exists(png) else 'FALHOU')


d = open(ORIG, encoding='utf-8').read()
assert '</style>' in d

INJ = """
  #stage { transform: scale(2.6667); transform-origin: center center;
           border-radius: 0 !important; box-shadow: none !important; }
  .cover { display: none !important; }
"""
patched = d.replace('</style>', INJ + '</style>', 1)
assert patched != d, 'nao consegui injetar o estilo'
p = os.path.join(OUT, 'patched.html')
open(p, 'w', encoding='utf-8').write(patched)

print('1) patched a 1080x1920 (transform)')
render(p, 1080, 1920, os.path.join(OUT, 'A-escalado.png'))

# para o comparativo ser JUSTO: neutralizar a media query de preview,
# senao o cartao sai encolhido a 0.86 e a comparacao mente
NEUTRO = "\n  @media (max-height:790px){ #stage{ transform:none !important; } }\n"
plano = d.replace('</style>', NEUTRO + '</style>', 1)
assert plano != d
pp = os.path.join(OUT, 'plano.html')
open(pp, 'w', encoding='utf-8').write(plano)

print('2) original a 405x720 (tamanho real, sem preview)')
render(pp, 405, 720, os.path.join(OUT, 'B-pequeno.png'))

print('3) esticando o pequeno para 1080x1920 (simula gravar pequeno e esticar)')
sm = Image.open(os.path.join(OUT, 'B-pequeno.png')).convert('RGB')
print('   B tem', sm.size)
sm.resize((1080, 1920), Image.BILINEAR).save(os.path.join(OUT, 'C-esticado.png'))

faixa = (0, 1660, 1080, 1920)
A = Image.open(os.path.join(OUT, 'A-escalado.png')).convert('RGB')
C = Image.open(os.path.join(OUT, 'C-esticado.png')).convert('RGB')
print('   A tem', A.size)
a = A.crop(faixa)
c = C.crop(faixa)

comp = Image.new('RGB', (1080, a.height * 2 + 16), (255, 255, 255))
comp.paste(a, (0, 0))
comp.paste(c, (0, a.height + 16))
comp.save(os.path.join(OUT, 'comparacao.png'))
print('\ncomparacao.png: EM CIMA = transform, EMBAIXO = esticado')
