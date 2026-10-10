# -*- coding: utf-8 -*-
"""
Conserta, em alho/shorts-garlic-honey-en.html e cebola/shorts-cebola-beterraba.html:

  (1) <text> dentro de <rect>  ->  NUNCA e renderizado (conteudo vazio no SVG)
      vira <g><rect/><text/></g>
  (2) texto com y > 638  ->  fica atras da faixa .cap (que comeca em y ~= 647)

Uso:
    python _consertar-cards.py            # dry-run, so mostra o que faria
    python _consertar-cards.py --apply    # grava

Cada substituicao declara quantas ocorrencias espera. Se o numero nao bater,
o arquivo inteiro e ABORTADO sem ser gravado.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SCENE_RE = re.compile(r'<svg class="scene[^>]*id="(s\d)"[\s\S]*?</svg>')


# ────────────────────────────── ALHO ──────────────────────────────
ALHO = {
    's0': [
        ('<text x="202" y="596" text-anchor="middle" font-size="27"',
         '<text x="202" y="584" text-anchor="middle" font-size="27"', 1),
        ('<text x="202" y="624" text-anchor="middle" font-size="14"',
         '<text x="202" y="612" text-anchor="middle" font-size="14"', 1),
        ('<text x="202" y="660" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="638" text-anchor="middle" font-size="11.5"', 1),
    ],
    's1': [
        ('<text x="202" y="596" text-anchor="middle" font-size="21"',
         '<text x="202" y="584" text-anchor="middle" font-size="21"', 1),
        ('<text x="202" y="628" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="610" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="650" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="634" text-anchor="middle" font-size="11.5"', 1),
    ],
    's2': [
        ('<rect x="40" y="524" width="325" height="132" rx="14"',
         '<rect x="40" y="500" width="325" height="114" rx="14"', 1),
        ('<text x="202" y="560" text-anchor="middle" font-size="13"',
         '<text x="202" y="526" text-anchor="middle" font-size="13"', 1),
        ('<text x="202" y="590" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="550" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="612" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="570" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="634" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="590" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="686" text-anchor="middle" font-size="13"',
         '<text x="202" y="636" text-anchor="middle" font-size="13"', 1),
    ],
    's3': [
        # sobe jarro + mel escorrendo em 30
        ('    <!-- jar body -->\n',
         '    <g transform="translate(0,-30)">\n    <!-- jar body -->\n', 1),
        ('      <ellipse cx="258" cy="332" rx="11" ry="4" fill="#fbe7ab"/>\n    </g>\n',
         '      <ellipse cx="258" cy="332" rx="11" ry="4" fill="#fbe7ab"/>\n    </g>\n    </g>\n', 1),
        ('<text x="202" y="626" text-anchor="middle" font-size="21"',
         '<text x="202" y="590" text-anchor="middle" font-size="21"', 1),
        ('<text x="202" y="656" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="614" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="678" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="636" text-anchor="middle" font-size="11.5"', 1),
    ],
    's4': [
        ('translate(202,436)', 'translate(202,406)', 2),
        ('<rect x="40" y="576" width="325" height="86" rx="14"',
         '<rect x="40" y="544" width="325" height="96" rx="14"', 1),
        ('<text x="202" y="606" text-anchor="middle" font-size="13"',
         '<text x="202" y="570" text-anchor="middle" font-size="13"', 1),
        ('<text x="202" y="630" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="594" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="650" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="614" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="692" text-anchor="middle" font-size="13"',
         '<text x="202" y="634" text-anchor="middle" font-size="13"', 1),
    ],
    's5': [
        ('translate(0,436)', 'translate(0,416)', 1),
        ('    <rect x="40" y="648" width="325" height="52" rx="12" fill="#fdf0e2" stroke="#f0c9a0" stroke-width="2">\n'
         '      <text x="202" y="670" text-anchor="middle" font-size="12" font-weight="900" fill="#c2551f" font-family="system-ui">\u26a0 If garlic turns BLUE or GREEN: still safe.</text>\n'
         '      <text x="202" y="688" text-anchor="middle" font-size="11" font-weight="600" fill="#7a4a26" font-family="system-ui">That is a natural reaction. It is not mold.</text>\n'
         '    </rect>\n',
         '    <g>\n'
         '      <rect x="40" y="592" width="325" height="48" rx="12" fill="#fdf0e2" stroke="#f0c9a0" stroke-width="2"/>\n'
         '      <text x="202" y="612" text-anchor="middle" font-size="12" font-weight="900" fill="#c2551f" font-family="system-ui">\u26a0 If garlic turns BLUE or GREEN: still safe.</text>\n'
         '      <text x="202" y="631" text-anchor="middle" font-size="11" font-weight="600" fill="#7a4a26" font-family="system-ui">That is a natural reaction. It is not mold.</text>\n'
         '    </g>\n', 1),
        ('<text x="202" y="578" text-anchor="middle" font-size="17"',
         '<text x="202" y="540" text-anchor="middle" font-size="17"', 1),
        ('<text x="202" y="606" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="562" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="628" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="580" text-anchor="middle" font-size="11.5"', 1),
    ],
    's6': [
        ('    <rect x="40" y="576" width="325" height="84" rx="13" fill="#ffffff" stroke="#e6dcc6" stroke-width="2">\n'
         '      <text x="202" y="602" text-anchor="middle" font-size="12" font-weight="900" fill="#3d3222" font-family="system-ui">Keep it at room temperature</text>\n'
         '      <text x="202" y="624" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">Dark place. Loose lid for the first days</text>\n'
         '      <text x="202" y="646" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">it will foam up and can overflow</text>\n'
         '    </rect>\n',
         '    <g>\n'
         '      <rect x="40" y="538" width="325" height="76" rx="13" fill="#ffffff" stroke="#e6dcc6" stroke-width="2"/>\n'
         '      <text x="202" y="564" text-anchor="middle" font-size="12" font-weight="900" fill="#3d3222" font-family="system-ui">Keep it at room temperature</text>\n'
         '      <text x="202" y="586" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">Dark place. Loose lid for the first days</text>\n'
         '      <text x="202" y="606" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">it will foam up and can overflow</text>\n'
         '    </g>\n', 1),
        ('<text x="202" y="524" text-anchor="middle" font-size="15"',
         '<text x="202" y="502" text-anchor="middle" font-size="15"', 1),
        ('<text x="202" y="550" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="522" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="692" text-anchor="middle" font-size="12.5"',
         '<text x="202" y="636" text-anchor="middle" font-size="12.5"', 1),
    ],
    's7': [
        ('    <rect x="40" y="622" width="325" height="56" rx="13" fill="#f3ece0" stroke="#ddd0b8" stroke-width="2" style="animation:slideUp .7s ease both; animation-delay:1.7s">\n'
         '      <text x="202" y="646" text-anchor="middle" font-size="12.5" font-weight="900" fill="#3d3222" font-family="system-ui">Which one should I ferment next?</text>\n'
         '      <text x="202" y="666" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">Tell me in the comments \U0001f447</text>\n'
         '    </rect>\n',
         '    <g style="animation:slideUp .7s ease both; animation-delay:1.7s">\n'
         '      <rect x="40" y="590" width="325" height="52" rx="13" fill="#f3ece0" stroke="#ddd0b8" stroke-width="2"/>\n'
         '      <text x="202" y="612" text-anchor="middle" font-size="12.5" font-weight="900" fill="#3d3222" font-family="system-ui">Which one should I ferment next?</text>\n'
         '      <text x="202" y="630" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7a5e" font-family="system-ui">Tell me in the comments \U0001f447</text>\n'
         '    </g>\n', 1),
        ('<text x="202" y="576" text-anchor="middle" font-size="16"',
         '<text x="202" y="556" text-anchor="middle" font-size="16"', 1),
        ('<text x="202" y="602" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="578" text-anchor="middle" font-size="11.5"', 1),
    ],
}


# ───────────────────────────── CEBOLA ─────────────────────────────
CEBOLA = {
    's0': [
        ('<text x="202" y="596" text-anchor="middle" font-size="25"',
         '<text x="202" y="584" text-anchor="middle" font-size="25"', 1),
        ('<text x="202" y="624" text-anchor="middle" font-size="13"',
         '<text x="202" y="612" text-anchor="middle" font-size="13"', 1),
        ('<text x="202" y="660" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="638" text-anchor="middle" font-size="11.5"', 1),
    ],
    's1': [
        ('<text x="202" y="470" text-anchor="middle" font-size="21"',
         '<text x="202" y="452" text-anchor="middle" font-size="21"', 1),
        ('<text x="202" y="500" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="474" text-anchor="middle" font-size="11.5"', 1),
        ('<rect x="40" y="524" width="325" height="102" rx="14" fill="#fff" stroke="#e6d4de" stroke-width="2"/>',
         '<rect x="40" y="494" width="325" height="110" rx="14" fill="#fff" stroke="#e6d4de" stroke-width="2"/>', 1),
        ('<text x="202" y="552" text-anchor="middle" font-size="12.5"',
         '<text x="202" y="520" text-anchor="middle" font-size="12.5"', 1),
        ('<text x="202" y="576" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="544" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="596" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="564" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="616" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="584" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="664" text-anchor="middle" font-size="12"',
         '<text x="202" y="632" text-anchor="middle" font-size="12"', 1),
    ],
    's2': [
        ('<rect x="40" y="572" width="325" height="96" rx="14" fill="#fff" stroke="#e6d4de" stroke-width="2"/>',
         '<rect x="40" y="542" width="325" height="76" rx="14" fill="#fff" stroke="#e6d4de" stroke-width="2"/>', 1),
        ('<text x="202" y="604" text-anchor="middle" font-size="17"',
         '<text x="202" y="566" text-anchor="middle" font-size="17"', 1),
        ('<text x="202" y="628" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="587" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="650" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="607" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="692" text-anchor="middle" font-size="12"',
         '<text x="202" y="636" text-anchor="middle" font-size="12"', 1),
    ],
    's3': [
        ('    <rect x="40" y="666" width="325" height="44" rx="12" fill="#fdf0e2" stroke="#f0c9a0" stroke-width="2">\n'
         '      <text x="202" y="694" text-anchor="middle" font-size="11.5" font-weight="700" fill="#c2551f" font-family="system-ui">\U0001f6ab Sem adicionar \u00e1gua. Elas soltam a delas.</text>\n'
         '    </rect>\n',
         '    <g>\n'
         '      <rect x="40" y="612" width="325" height="34" rx="12" fill="#fdf0e2" stroke="#f0c9a0" stroke-width="2"/>\n'
         '      <text x="202" y="633" text-anchor="middle" font-size="11.5" font-weight="700" fill="#c2551f" font-family="system-ui">\U0001f6ab Sem adicionar \u00e1gua. Elas soltam a delas.</text>\n'
         '    </g>\n', 1),
        ('<text x="202" y="592" text-anchor="middle" font-size="21"',
         '<text x="202" y="560" text-anchor="middle" font-size="21"', 1),
        ('<text x="202" y="622" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="584" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="644" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="604" text-anchor="middle" font-size="11.5"', 1),
    ],
    's4': [
        ('    <!-- jar -->\n',
         '    <g transform="translate(0,-24)">\n    <!-- jar -->\n', 1),
        ('      <line x1="272" y1="498" x2="288" y2="498" stroke="#c9a8bc" stroke-width="1.4"/>\n    </g>\n',
         '      <line x1="272" y1="498" x2="288" y2="498" stroke="#c9a8bc" stroke-width="1.4"/>\n    </g>\n    </g>\n', 1),
        ('<text x="202" y="600" text-anchor="middle" font-size="20"',
         '<text x="202" y="578" text-anchor="middle" font-size="20"', 1),
        ('<text x="202" y="628" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="602" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="650" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="622" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="684" text-anchor="middle" font-size="12"',
         '<text x="202" y="642" text-anchor="middle" font-size="12"', 1),
    ],
    's5': [
        ('translate(0,418)', 'translate(0,396)', 1),
        ('translate(0,538)', 'translate(0,512)', 1),
        ('<text x="202" y="626" text-anchor="middle" font-size="16"',
         '<text x="202" y="584" text-anchor="middle" font-size="16"', 1),
        ('<text x="202" y="652" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="608" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="674" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="628" text-anchor="middle" font-size="11.5"', 1),
    ],
    's6': [
        ('    <rect x="40" y="576" width="325" height="84" rx="13" fill="#fff" stroke="#e6d4de" stroke-width="2">\n'
         '      <text x="202" y="602" text-anchor="middle" font-size="12" font-weight="900" fill="#3d1f33" font-family="system-ui">2 dias no balc\u00e3o, depois geladeira</text>\n'
         '      <text x="202" y="624" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7284" font-family="system-ui">Mantenha tudo prensado abaixo da \u00e1gua</text>\n'
         '      <text x="202" y="646" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7284" font-family="system-ui">Solte o g\u00e1s do pote uma vez por dia</text>\n'
         '    </rect>\n',
         '    <g>\n'
         '      <rect x="40" y="538" width="325" height="76" rx="13" fill="#fff" stroke="#e6d4de" stroke-width="2"/>\n'
         '      <text x="202" y="564" text-anchor="middle" font-size="12" font-weight="900" fill="#3d1f33" font-family="system-ui">2 dias no balc\u00e3o, depois geladeira</text>\n'
         '      <text x="202" y="586" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7284" font-family="system-ui">Mantenha tudo prensado abaixo da \u00e1gua</text>\n'
         '      <text x="202" y="606" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7284" font-family="system-ui">Solte o g\u00e1s do pote uma vez por dia</text>\n'
         '    </g>\n', 1),
        ('<text x="202" y="524" text-anchor="middle" font-size="16"',
         '<text x="202" y="502" text-anchor="middle" font-size="16"', 1),
        ('<text x="202" y="550" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="522" text-anchor="middle" font-size="11.5"', 1),
        ('<text x="202" y="692" text-anchor="middle" font-size="12.5"',
         '<text x="202" y="636" text-anchor="middle" font-size="12.5"', 1),
    ],
    's7': [
        ('    <rect x="40" y="618" width="325" height="56" rx="13" fill="#f8ecf2" stroke="#e4d2de" stroke-width="2" style="animation:slideUp .7s ease both; animation-delay:1.7s">\n'
         '      <text x="202" y="642" text-anchor="middle" font-size="12.5" font-weight="900" fill="#3d1f33" font-family="system-ui">Qual dupla voc\u00ea quer que eu fa\u00e7a?</text>\n'
         '      <text x="202" y="662" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7284" font-family="system-ui">Comenta a\u00ed \U0001f447</text>\n'
         '    </rect>\n',
         '    <g style="animation:slideUp .7s ease both; animation-delay:1.7s">\n'
         '      <rect x="40" y="590" width="325" height="52" rx="13" fill="#f8ecf2" stroke="#e4d2de" stroke-width="2"/>\n'
         '      <text x="202" y="612" text-anchor="middle" font-size="12.5" font-weight="900" fill="#3d1f33" font-family="system-ui">Qual dupla voc\u00ea quer que eu fa\u00e7a?</text>\n'
         '      <text x="202" y="630" text-anchor="middle" font-size="11" font-weight="600" fill="#8a7284" font-family="system-ui">Comenta a\u00ed \U0001f447</text>\n'
         '    </g>\n', 1),
        ('<text x="202" y="572" text-anchor="middle" font-size="16"',
         '<text x="202" y="552" text-anchor="middle" font-size="16"', 1),
        ('<text x="202" y="598" text-anchor="middle" font-size="11.5"',
         '<text x="202" y="574" text-anchor="middle" font-size="11.5"', 1),
    ],
}


def aplicar(bloco, subs, cena):
    d = bloco
    for old, new, esperado in subs:
        achou = d.count(old)
        if achou != esperado:
            print('   !! %s: esperava %d ocorrencia(s), achei %d' % (cena, esperado, achou))
            print('      padrao: %r' % old[:90])
            return None
        d = d.replace(old, new)
    return d


def processar(caminho, plano, aplicar_de_verdade):
    bruto = io.open(caminho, encoding='utf-8', newline='').read()
    atual = bruto
    ok = True
    for m in list(SCENE_RE.finditer(bruto)):
        cena = m.group(1)
        if cena not in plano:
            continue
        novo = aplicar(m.group(0), plano[cena], cena)
        if novo is None:
            ok = False
            continue
        if novo != m.group(0):
            print('   [ok] %s' % cena)
            atual = atual.replace(m.group(0), novo)
    if not ok:
        print('   ABORTADO (nada foi gravado)')
        return False
    if atual == bruto:
        print('   (sem mudancas)')
        return True
    if aplicar_de_verdade:
        io.open(caminho, 'w', encoding='utf-8', newline='').write(atual)
        print('   GRAVADO')
    else:
        print('   (dry-run)')
    return True


def main():
    aplicar_de_verdade = '--apply' in sys.argv
    alvos = [
        (os.path.join(ROOT, 'alho', 'shorts-garlic-honey-en.html'), ALHO),
        (os.path.join(ROOT, 'cebola', 'shorts-cebola-beterraba.html'), CEBOLA),
    ]
    for caminho, plano in alvos:
        print('\n== %s' % os.path.relpath(caminho, ROOT))
        processar(caminho, plano, aplicar_de_verdade)


if __name__ == '__main__':
    main()
