# -*- coding: utf-8 -*-
"""_consertar-pao-contraste.py — conserta os 3 defeitos de contraste do short de pao.

    python _consertar-pao-contraste.py

Medido com `_medir-contraste-pao.py` ANTES (limite ~130 = "dá pra ver"):

  cena 0  pote de vidro sobre o halo ......... 52  FRACO
  cena 0  levain dentro do pote .............. 66  FRACO   -> o pote lia como BLOCO VAZIO
  cena 2  circulo levain x circulo farinha ... 14  INVISIVEL -> os dois eram o MESMO circulo
  cena 4  massa sobre o halo .................  2  INVISIVEL -> a massa era o proprio halo

DEPOIS:
  cena 0  levain #d9b872 dentro do pote ...... 154
  cena 2  levain x farinha ................... 141
  cena 4  massa #d4ad64 sobre o halo ......... 131   (e 150 sobre o fundo)

Consertos:
  - cena 0: o levain vira TRIGO ESCURO (#d9b872) em vez de creme, e sobe no pote;
  - cena 2: os tres circulos ganham cores DISTINTAS (trigo / creme claro / azul);
  - cena 4: a massa vira trigo e a rede de gluten vira marrom escuro;
  - a colher vira COLHER (era um pirulito: cabo fino + bolinha) e vai pro centro;
  - saem os tres rotulos "1" debaixo dos circulos: o "1 : 1 : 1" ja' diz isso.

Ancoras contadas, aborta SEM GRAVAR.
"""
import io
import sys

ALVOS = ['pao/shorts-sourdough-en.html', 'pao/shorts-sourdough.html']

TROCAS = [
    # ---------------------------------------------------------- cena 0: o pote
    ('levain sobe no pote e vira trigo',
     '<path d="M-44,66 L-44,-6 Q-44,-22 -28,-22 L28,-22 Q44,-22 44,-6 L44,66 Z" fill="#efe0bd"/>',
     '<path d="M-44,74 L-44,-6 Q-44,-22 -28,-22 L28,-22 Q44,-22 44,-6 L44,74 Z" fill="#d9b872"/>', 1),
    ('contorno do mound de farinha mais forte',
     '<path d="M-46,54 Q-42,2 -15,-8 Q10,-18 27,1 Q44,19 42,54 Z" fill="#f2e6c9" stroke="#c9ab6d" stroke-width="3"/>',
     '<path d="M-46,54 Q-42,2 -15,-8 Q10,-18 27,1 Q44,19 42,54 Z" fill="#f2e6c9" stroke="#b08f4e" stroke-width="3.5"/>', 1),
    ('gota de agua maior',
     '<path d="M-10,-18 Q0,-30 10,-18 Q10,-4 0,12 Q-10,-4 -10,-18Z" fill="#7fb2e0" stroke="#3d7ab5" stroke-width="2.5"/>',
     '<path d="M-14,-24 Q0,-40 14,-24 Q14,-4 0,16 Q-14,-4 -14,-24Z" fill="#7fb2e0" stroke="#3d7ab5" stroke-width="2.5"/>', 1),

    # ---------------------------------------------------------- cena 2: os 3 circulos
    ('circulo do levain vira trigo',
     '<circle cx="0" cy="0" r="40" fill="#efe0bd" stroke="#8a6a3b" stroke-width="3"/>',
     '<circle cx="0" cy="0" r="40" fill="#d9b872" stroke="#8a6a3b" stroke-width="3"/>', 1),
    ('circulo da farinha clareia',
     '<circle cx="0" cy="0" r="40" fill="#f2e6c9" stroke="#c9ab6d" stroke-width="3"/>',
     '<circle cx="0" cy="0" r="40" fill="#fbf7ec" stroke="#c9ab6d" stroke-width="3"/>', 1),
    ('circulo da agua fica azul de verdade',
     '<circle cx="0" cy="0" r="40" fill="#e6f1fb" stroke="#3d7ab5" stroke-width="3"/>',
     '<circle cx="0" cy="0" r="40" fill="#6fb0dd" stroke="#1f5c8a" stroke-width="3"/>', 1),
    ('sai o rotulo "1" do levain e da farinha',
     '      <text x="0" y="64" text-anchor="middle" font-size="13" font-weight="700" fill="#8a6a3b" font-family="system-ui">1</text>\n',
     '', 2),
    ('sai o rotulo "1" da agua',
     '      <text x="0" y="64" text-anchor="middle" font-size="13" font-weight="700" fill="#3d7ab5" font-family="system-ui">1</text>\n',
     '', 1),
    ('a colher vira COLHER (era um pirulito)',
     '''    <g transform="translate(202,556)">
      <g style="animation:chop2x .7s ease-in-out infinite">
        <rect x="-4" y="-52" width="8" height="46" rx="3" fill="#8a6a3b"/>
        <ellipse cx="0" cy="6" rx="16" ry="11" fill="#d9c9a3" stroke="#8a6a3b" stroke-width="2.5"/>
      </g>
    </g>''',
     '''    <g transform="translate(202,552)">
      <g style="animation:chop2x .7s ease-in-out infinite">
        <g transform="rotate(-22)">
          <path d="M-3.5,-66 L3.5,-66 L5,-10 L-5,-10 Z" fill="#c0ab7d" stroke="#8a6a3b" stroke-width="2"/>
          <ellipse cx="0" cy="10" rx="20" ry="15" fill="#efe0bd" stroke="#8a6a3b" stroke-width="2.5"/>
          <ellipse cx="0" cy="10" rx="11" ry="7" fill="#d9c9a3"/>
        </g>
      </g>
    </g>''', 1),

    # ---------------------------------------------------------- cena 4: a massa
    ('halo da massa mais leve',
     '<circle cx="202" cy="282" r="140" fill="#e8d9b5" opacity=".5"/>',
     '<circle cx="202" cy="282" r="140" fill="#e8d9b5" opacity=".35"/>', 1),
    ('a massa vira trigo',
     '<circle cx="0" cy="0" r="104" fill="#f2e6c9" stroke="#c9ab6d" stroke-width="4"/>',
     '<circle cx="0" cy="0" r="104" fill="#d4ad64" stroke="#a9713a" stroke-width="4"/>', 1),
    ('a rede de gluten fica escura',
     '<g stroke="#c9ab6d" stroke-width="2.5" fill="none" opacity=".85">',
     '<g stroke="#7a4d1c" stroke-width="2.5" fill="none" opacity=".85">', 1),
]


def main():
    falhou = False
    for arq in ALVOS:
        with io.open(arq, 'r', encoding='utf-8', newline='') as fh:
            d = fh.read()
        eol = '\r\n' if d.count('\r\n') else '\n'
        print('\n%s' % arq)
        for i, (rotulo, velho, novo, esperado) in enumerate(TROCAS, 1):
            v = velho.replace('\n', eol)
            n = novo.replace('\n', eol)
            c = d.count(v)
            if c != esperado:
                print('  %2d. %-40s casou %d (esperado %d) ERRO'
                      % (i, rotulo, c, esperado))
                falhou = True
                continue
            d = d.replace(v, n)
            print('  %2d. %-40s ok (%d)' % (i, rotulo, c))
        if falhou:
            continue
        with io.open(arq, 'w', encoding='utf-8', newline='') as fh:
            fh.write(d)
        print('  gravado: %d bytes' % len(d))

    if falhou:
        print('\nABORTADO — nada foi gravado.')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
