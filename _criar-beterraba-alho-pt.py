# -*- coding: utf-8 -*-
"""_criar-beterraba-alho-pt.py — o ORIGINAL PT do short BETERRABA + ALHO (#19).

    python _criar-beterraba-alho-pt.py

Por que: o #19 nasceu em INGLES, ja' no formato de upload (1080x1920), e a serie
e' **original PT + irmao `-en`**.

Nome do destino: `shorts-beet-garlic-1080x1920.html` — o PT e' o `-en` **sem o
`-en`**, preservando o sufixo. E' assim que o `_sobras-vs-original.py` pareia
(ele tira o `-en` e mantem o resto); com outro nome o par nao seria conferido.

Este e' o arquivo mais "falado" da serie: e' um player de producao ("maos, sem
rosto, sem voz"), entao alem das 8 cenas ele tem a legenda do rodape, a linha de
especificacao e a dica de uso. Tudo isso e' texto que o espectador le' — entra.

Metodo: ancoras CONTADAS (aborta sem gravar se alguma casar diferente). Ha duas
armadilhas medidas neste arquivo, e as duas estao tratadas:
  - `BEET` e `GARLIC` aparecem **2 vezes** cada (as camadas do pote) -> contagem 2;
  - `WEEK 2` aparece **2 vezes** (a linha do tempo e o cartao do resultado) -> 2.
O bloco `const scenes` sai por REGEX, porque ele guarda `\\u00b7` e `\\u2014`
como escape literal e o alinhamento a espaco muda de arquivo para arquivo.
"""
import io
import re
import sys

ORIGEM = 'beterraba/shorts-beet-garlic-en-1080x1920.html'
DESTINO = 'beterraba/shorts-beet-garlic-1080x1920.html'

T = [
    # --------------------------------------------------------------- cabecalho
    ('idioma do html', '<html lang="en">', '<html lang="pt-BR">', 1),
    ('titulo da aba',
     'Animation — Fermented Beets with Garlic (EN · white hands · 1080x1920 upload format)',
     'Animação — Beterraba fermentada com alho (PT · mãos brancas · formato de upload 1080x1920)', 1),
    ('tag estatica', '>BEETS+GARLIC 1 / 8</div>', '>BETERRABA+ALHO 1 / 8</div>', 1),
    ('barra estatica',
     'Fermented beets with garlic<small>2% salt · ready in 1 to 2 weeks</small>',
     'Beterraba fermentada com alho<small>2% de sal · pronta em 1 a 2 semanas</small>', 1),

    # --------------------------------------------------------------- cena 1
    ('cena1 topo', '>HANDS ONLY · NO FACE · NO VOICE</text>',
     '>SÓ MÃOS · SEM ROSTO · SEM VOZ</text>', 1),
    ('cena1 titulo', '>BEETS + GARLIC</text>', '>BETERRABA + ALHO</text>', 1),
    ('cena1 subtitulo', '>FERMENTED TOGETHER</text>', '>FERMENTADAS JUNTAS</text>', 1),
    ('cena1 resumo', '>2% salt. Ready in 1 to 2 weeks.</text>',
     '>2% de sal. Pronta em 1 a 2 semanas.</text>', 1),

    # --------------------------------------------------------------- cena 2
    ('cena2 etapa', '>STEP 1 · PEEL AND CUT</text>', '>PASSO 1 · DESCASQUE E CORTE</text>', 1),
    ('cena2 titulo', '>CUT INTO WEDGES</text>', '>CORTE EM CUNHAS</text>', 1),
    ('cena2 detalhe', '>About 2 cm thick, skin off</text>',
     '>Mais ou menos 2 cm, sem casca</text>', 1),
    ('cena2 caixa', '>NOT GRATED</text>', '>NÃO RALADA</text>', 1),
    ('cena2 caixa detalhe',
     '>Grated beets turn to mush — wedges stay crunchy</text>',
     '>Beterraba ralada vira papa — em cunhas fica crocante</text>', 1),

    # --------------------------------------------------------------- cena 3
    ('cena3 etapa', '>STEP 2 · THE GARLIC</text>', '>PASSO 2 · O ALHO</text>', 1),
    ('cena3 titulo', '>PEEL, THEN CRUSH</text>', '>DESCASQUE, DEPOIS AMASSE</text>', 1),
    ('cena3 detalhe', '>Smash each clove once with the flat blade</text>',
     '>Amasse cada dente uma vez com o lado chato</text>', 1),
    ('cena3 caixa', '>WHY CRUSH IT?</text>', '>POR QUE AMASSAR?</text>', 1),
    ('cena3 caixa detalhe',
     '>A crushed clove gives up its oil — that is the flavour</text>',
     '>O dente amassado solta o óleo — é ele que dá o sabor</text>', 1),

    # --------------------------------------------------------------- cena 4
    ('cena4 etapa', '>STEP 3 · LAYER IT, DO NOT MIX</text>',
     '>PASSO 3 · CAMADAS, NÃO MISTURE</text>', 1),
    ('cena4 rotulo beterraba', '>BEET</text>', '>BETERRABA</text>', 2),
    ('cena4 rotulo alho', '>GARLIC</text>', '>ALHO</text>', 2),
    ('cena4 titulo', '>ONE LAYER AT A TIME</text>', '>UMA CAMADA POR VEZ</text>', 1),
    ('cena4 detalhe', '>Beet, then garlic, then beet again</text>',
     '>Beterraba, depois alho, depois beterraba</text>', 1),
    ('cena4 detalhe2', '>Mix it all and you lose the layers</text>',
     '>Misturando, você perde as camadas</text>', 1),
    ('cena4 detalhe3', '>Press it down as you go</text>',
     '>Prense conforme for montando</text>', 1),

    # --------------------------------------------------------------- cena 5
    ('cena5 etapa', '>STEP 4 · THE SALT</text>', '>PASSO 4 · O SAL</text>', 1),
    ('cena5 titulo', '>2% SALT, NOT MORE</text>', '>2% DE SAL, NÃO MAIS</text>', 1),
    ('cena5 detalhe', '>20 g of salt for every 1 kg of beet and garlic</text>',
     '>20 g de sal para cada 1 kg de beterraba e alho</text>', 1),
    ('cena5 caixa', '>NO IODINE</text>', '>SEM IODO</text>', 1),
    ('cena5 caixa detalhe',
     '>Iodized salt stops the ferment. Use coarse salt.</text>',
     '>Sal iodado trava a fermentação. Use sal grosso.</text>', 1),

    # --------------------------------------------------------------- cena 6
    ('cena6 topo', '>WHAT HAPPENS INSIDE</text>', '>O QUE ACONTECE POR DENTRO</text>', 1),
    ('cena6 dia1', '>DAY 1</text>', '>DIA 1</text>', 1),
    ('cena6 dia1 detalhe', '>pale · sharp garlic</text>', '>claro · alho ardido</text>', 1),
    ('cena6 semana2', '>WEEK 2</text>', '>SEMANA 2</text>', 2),
    ('cena6 semana2 detalhe', '>deep purple · mellow</text>', '>roxo forte · suave</text>', 1),
    ('cena6 caixa', '>THE GARLIC MELLOWS OUT</text>', '>O ALHO SUAVIZA</text>', 1),
    ('cena6 caixa detalhe',
     '>Raw garlic burns. Fermented garlic turns sweet.</text>',
     '>Alho cru arde. Alho fermentado fica doce.</text>', 1),
    ('cena6 cor', '>The colour comes from betalain</text>',
     '>A cor vem da betalaína</text>', 1),
    ('cena6 cor detalhe', '>It leaks out of the beet and paints everything</text>',
     '>Ela sai da beterraba e pinta tudo</text>', 1),
    ('cena6 cor detalhe2', '>purple — the onion trick, beetroot style</text>',
     '>de roxo — o truque da cebola, versão beterraba</text>', 1),

    # --------------------------------------------------------------- cena 7
    ('cena7 topo', '>HOW LONG · IN WEEKS</text>', '>QUANTO TEMPO · EM SEMANAS</text>', 1),
    ('cena7 unidade', '>WEEKS</text>', '>SEMANAS</text>', 1),
    ('cena7 semana1', '>WEEK 1</text>', '>SEMANA 1</text>', 1),
    ('cena7 bancada', '>counter</text>', '>bancada</text>', 1),
    ('cena7 semana3', '>WEEK 3+</text>', '>SEMANA 3+</text>', 1),
    ('cena7 geladeira', '>fridge</text>', '>geladeira</text>', 1),
    ('cena7 meses', '>months</text>', '>meses</text>', 1),
    ('cena7 pilula', '>READY IN 1 TO 2 WEEKS</text>', '>PRONTA EM 1 A 2 SEMANAS</text>', 1),
    ('cena7 detalhe', '>One week on the counter, one week in the fridge</text>',
     '>Uma semana na bancada, uma na geladeira</text>', 1),
    ('cena7 linha1', '>Week 1: room temperature, 18-22 °C</text>',
     '>Semana 1: temperatura ambiente, 18-22 °C</text>', 1),
    ('cena7 linha2', '>Keep everything under the liquid. Burp the jar daily.</text>',
     '>Tudo embaixo do líquido. Solte o gás todo dia.</text>', 1),
    ('cena7 linha3', '>Week 2: taste it — then move it to the fridge.</text>',
     '>Semana 2: prove — depois vai pra geladeira.</text>', 1),
    ('cena7 rodape', '>Longer wait = deeper colour, softer garlic</text>',
     '>Mais tempo = cor mais forte, alho mais macio</text>', 1),

    # --------------------------------------------------------------- cena 8
    ('cena8 topo', '>READY · WHERE TO USE IT</text>', '>PRONTA · ONDE USAR</text>', 1),
    ('cena8 titulo', '>USE IT ON</text>', '>USE EM</text>', 1),
    ('cena8 saladas', '>Salads</text>', '>Saladas</text>', 1),
    ('cena8 burgers', '>Burgers</text>', '>Hambúrgueres</text>', 1),
    ('cena8 ovos', '>Eggs</text>', '>Ovos</text>', 1),
    ('cena8 sopas', '>Soups</text>', '>Sopas</text>', 1),
    ('cena8 queijos', '>Cheese</text>', '>Queijos</text>', 1),
    ('cena8 puro', '>Straight</text>', '>Puro</text>', 1),
    ('cena8 caixa', '>PURPLE, SOUR, GARLICKY</text>', '>ROXA, ÁCIDA, COM ALHO</text>', 1),
    ('cena8 caixa detalhe',
     '>The colour alone makes any plate look expensive</text>',
     '>Só a cor já deixa qualquer prato com cara de caro</text>', 1),
    ('cta', '>Which one should I ferment next?</text>',
     '>Qual eu fermento depois desse?</text>', 1),
    ('cta comentarios', '>Tell me in the comments 👇</text>',
     '>Comenta aí 👇</text>', 1),

    # --------------------------------------------------------------- rodape e botoes
    ('linha de especificacao', '>Beets + garlic · 8 scenes · 54s<br>',
     '>Beterraba + alho · 8 cenas · 54s<br>', 1),
    ('linha de especificacao 2', '· white hands · ready to record</p>',
     '· mãos brancas · pronto pra gravar</p>', 1),
    ('dica de uso', '>Click ▶ to start. Space = play / pause.<br>',
     '>Clique no ▶ pra começar. Espaço = play / pause.<br>', 1),
    ('dica de uso 2', '>Add <b>?play</b> to the URL to auto-start.</p>',
     '>Adicione <b>?play</b> na URL pra iniciar sozinho.</p>', 1),
    ('botao pause (botao + JS)', '⏸ Pause', '⏸ Pausar', 2),
    ('botao play', "'▶ Play'", "'▶ Assistir'", 1),
]

SCENES_NOVO = """const scenes = [
  { id:'s0', ms:6000, tag:'BETERRABA+ALHO 1 / 8', cap:'Uma beterraba, uma cabeça de alho', sub:'2% de sal \\u00b7 pronta em 1 a 2 semanas', color:'#a01e52' },
  { id:'s1', ms:6500, tag:'BETERRABA+ALHO 2 / 8', cap:'Sem casca, em cunhas de 2 cm', sub:'beterraba ralada vira papa \\u2014 em cunhas fica crocante', color:'#8f2450' },
  { id:'s2', ms:6500, tag:'BETERRABA+ALHO 3 / 8', cap:'Uma amassada por dente', sub:'é isso que solta o óleo', color:'#c2551f' },
  { id:'s3', ms:7500, tag:'BETERRABA+ALHO 4 / 8', cap:'Beterraba, alho, beterraba, alho', sub:'em camadas, você tira o que quiser', color:'#a01e52' },
  { id:'s4', ms:7000, tag:'BETERRABA+ALHO 5 / 8', cap:'20 g de sal por 1 kg', sub:'sal grosso \\u2014 iodo trava a fermentação', color:'#ba7517' },
  { id:'s5', ms:7000, tag:'BETERRABA+ALHO 6 / 8', cap:'Dia 1 ardido, semana 2 doce', sub:'a betalaína da beterraba pinta o alho', color:'#0f6e56' },
  { id:'s6', ms:7000, tag:'BETERRABA+ALHO 7 / 8', cap:'Uma semana fora, uma no frio', sub:'18-22 \\u00b0C \\u00b7 solte o gás todo dia', color:'#0f6e56' },
  { id:'s7', ms:6500, tag:'BETERRABA+ALHO 8 / 8', cap:'Saladas, hambúrguer, ovos', sub:'dura meses na geladeira', color:'#3d1f33' }
];"""


def main():
    with io.open(ORIGEM, 'r', encoding='utf-8', newline='') as fh:
        d = fh.read()
    crlf = d.count('\r\n')
    eol = '\r\n' if crlf else '\n'
    print('origem     : %s (%d bytes)' % (ORIGEM, len(d)))
    print('fim de linha: %s' % ('CRLF' if crlf else 'LF'))

    falhou = []
    for i, (rotulo, velho, novo, esperado) in enumerate(T, 1):
        c = d.count(velho)
        if c != esperado:
            falhou.append((i, rotulo, c, esperado))
            print('  %2d. %-28s casou %d (esperado %d) ERRO' % (i, rotulo, c, esperado))
            continue
        d = d.replace(velho, novo)
    print('  ancoras ok: %d de %d' % (len(T) - len(falhou), len(T)))

    # --- barra de legenda por regex (guarda \\u00b7 e \\u2014 como escape literal)
    m = re.search(r'const scenes = \[.*?\n\];', d, re.S)
    if not m:
        print('  ERRO: nao achei `const scenes`')
        falhou.append((0, 'const scenes', 0, 1))
    else:
        velho_bloco = m.group(0)
        ms_a = re.findall(r'ms:(\d+)', velho_bloco)
        cor_a = re.findall(r"color:'([^']+)'", velho_bloco)
        novo_bloco = SCENES_NOVO.replace('\n', eol)
        if ms_a != re.findall(r'ms:(\d+)', novo_bloco):
            print('      ERRO: duracoes mudaram')
            falhou.append((0, 'duracoes', 0, 1))
        elif cor_a != re.findall(r"color:'([^']+)'", novo_bloco):
            print('      ERRO: cores da barra mudaram')
            falhou.append((0, 'cores', 0, 1))
        else:
            print('  %2d. %-28s %d cenas, duracoes e cores iguais'
                  % (len(T) + 1, 'barra de legenda', len(ms_a)))
            d = d.replace(velho_bloco, novo_bloco, 1)

    if falhou:
        print('\nABORTADO — nada foi gravado. Falhas: %s' % [f[1] for f in falhou])
        return 1

    a = io.open(ORIGEM, 'r', encoding='utf-8', newline='').read()
    esq = lambda s: re.findall(r'(?:ms|color|id|fill|stroke|font-size|viewBox)[:=]"?(#?\w[\w%., -]*)', s)
    if esq(a) != esq(d):
        print('\nAVISO: o esqueleto (ms/color/id/fill/...) mudou — conferir!')
        return 1
    print('esqueleto identico (ms, color, id, fill, stroke, font-size)')

    with io.open(DESTINO, 'w', encoding='utf-8', newline='') as fh:
        fh.write(d)
    print('gravado: %s (%d bytes)' % (DESTINO, len(d)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
