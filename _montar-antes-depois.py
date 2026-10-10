# -*- coding: utf-8 -*-
"""Monta uma imagem que se explica sozinha: antes x depois do conserto do chucrute."""
from PIL import Image, ImageDraw, ImageFont

B = r'C:/Windows/Fonts/segoeuib.ttf'
R = r'C:/Windows/Fonts/segoeui.ttf'
f_tit = ImageFont.truetype(B, 30)
f_sub = ImageFont.truetype(R, 20)
f_peq = ImageFont.truetype(B, 17)

FAIXA = (0, 85, 1080, 255)          # so a parte de cima do video
H = FAIXA[3] - FAIXA[1]
PAD = 24
LARG = 1080 + PAD * 2


def faixa(arq):
    return Image.open(arq).convert('RGB').crop(FAIXA)


# altura: cabecalho ANTES + 1 faixa + gap + cabecalho DEPOIS + 3 faixas + legendas
alt = (46 + H + 34) + (46 + 3 * (24 + H) + 40) + PAD * 2
img = Image.new('RGB', (LARG, alt), (255, 255, 255))
d = ImageDraw.Draw(img)

y = PAD

# ---------- ANTES ----------
d.rectangle([0, y, 10, y + 46 + H], fill=(200, 40, 40))
d.text((PAD, y), 'ANTES  —  os dois textos ficavam na mesma linha',
       font=f_tit, fill=(160, 25, 25))
y += 46
img.paste(faixa('_teste-rec/rec-chucrute.png'), (PAD, y))
d.rectangle([PAD, y, PAD + 1080, y + H], outline=(200, 40, 40), width=3)
y += H + 34

# ---------- DEPOIS ----------
d.rectangle([0, y, 10, y + 46 + 3 * (24 + H)], fill=(30, 140, 90))
d.text((PAD, y), 'DEPOIS  —  cada um na sua linha, nada se sobrepõe',
       font=f_tit, fill=(20, 110, 70))
y += 46

for nome, arq in [('cena 2 de 5  ·  lavar e cortar',
                   '_teste-rec/fix-chucrute.png'),
                  ('cena 3 de 5  ·  massagear 10 minutos',
                   '_teste-rec/fix-cena3.png'),
                  ('cena 4 de 5  ·  2% de sal',
                   '_teste-rec/fix-cena4.png')]:
    d.text((PAD, y), nome, font=f_peq, fill=(90, 90, 88))
    y += 24
    img.paste(faixa(arq), (PAD, y))
    d.rectangle([PAD, y, PAD + 1080, y + H], outline=(30, 140, 90), width=3)
    y += H

img.save('_teste-rec/antes-e-depois-chucrute.png')
print('ok', img.size)
