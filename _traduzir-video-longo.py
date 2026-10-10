# -*- coding: utf-8 -*-
"""
Traduz o player do video longo (7 legumes) para ingles.

Regras (ver MEMORY.md do projeto):
  - cada troca tem uma ancora EXATA e um numero esperado de ocorrencias;
  - se qualquer ancora casar um numero diferente, o script ABORTA e nao grava
    nada (nada de "Successfully edited" mentiroso);
  - escreve um arquivo NOVO (-en), preservando o original em portugues;
  - no fim varre o resultado atras de sobras de portugues.

Uso:
    python _traduzir-video-longo.py            # roda e grava
    python _traduzir-video-longo.py --check    # so verifica as ancoras
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(RAIZ, 'video-longo', 'player-video-longo-7-legumes.html')
DEST = os.path.join(RAIZ, 'video-longo', 'player-video-longo-7-legumes-en.html')

# (rotulo, antigo, novo, ocorrencias esperadas)
TROCAS = [
    # ═══════════════════════════ cabecalho / HTML estatico ═══════════════════
    ('lang', '<html lang="pt-BR">', '<html lang="en">', 1),
    ('title',
     '<title>Vídeo longo — 7 legumes fermentados (player de gravação)</title>',
     '<title>Long video — 7 fermented vegetables (recording player)</title>', 1),

    ('painel esquerdo: nome', '<div id="cname">Repolho<small id="ctag">capítulo 1 de 7</small></div>',
     '<div id="cname">Cabbage<small id="ctag">chapter 1 of 7</small></div>', 1),
    ('painel esquerdo: nivel',
     '<div id="ctext">Nível: iniciante<small id="chint">O mais fácil de todos. Se você nunca fermentou nada, comece por aqui.</small></div>',
     '<div id="ctext">Level: beginner<small id="chint">The easiest of all. If you have never fermented anything, start here.</small></div>', 1),
    ('painel esquerdo: sal', '<b id="fsal">Sal 2%</b>', '<b id="fsal">Salt 2%</b>', 1),
    ('painel esquerdo: tempo', '<b id="ftempo">7 dias</b>', '<b id="ftempo">7 days</b>', 1),
    ('painel esquerdo: nivel b', '<b id="fnivel">Iniciante</b>', '<b id="fnivel">Beginner</b>', 1),

    ('abertura: h2', '<h2>7 legumes.<br><span>30 dias.</span></h2>',
     '<h2>7 vegetables.<br><span>30 days.</span></h2>', 1),
    ('abertura: p', '<p>Do mais fácil ao mais difícil</p>', '<p>From easiest to hardest</p>', 1),

    ('marca dagua', '<div class="nwm">@seucanal</div>', '<div class="nwm">@yourchannel</div>', 1),
    ('tag do celular', '<div id="phoneTag">gravação vertical · 9:16</div>',
     '<div id="phoneTag">vertical recording · 9:16</div>', 1),
    ('rodape: rotulo', '<div id="flabel">Rodando</div>', '<div id="flabel">Running</div>', 1),

    ('botao anterior', '>◀ capítulo</button>', '>◀ chapter</button>', 1),
    ('botao pausar', '>⏸ Pausar</button>', '>⏸ Pause</button>', 1),
    ('botao proximo', '>capítulo ▶</button>', '>chapter ▶</button>', 1),
    ('botao reiniciar', '>↺ Reiniciar</button>', '>↺ Restart</button>', 1),

    ('capa: h1', '<h1>7 legumes fermentados<br>do mais fácil ao mais difícil</h1>',
     '<h1>7 fermented vegetables<br>from easiest to hardest</h1>', 1),
    ('capa: linha 1', 'Aperte play e grave a tela com o OBS em <b>1920×1080</b>.<br>',
     'Hit play and record the screen with OBS at <b>1920×1080</b>.<br>', 1),
    ('capa: linha 2', 'Deixe rolar até o fim — são cerca de 6 minutos de animação.<br>',
     'Let it run to the end — about 6 minutes of animation.<br>', 1),
    ('capa: linha 3', 'Depois corte no CapCut e cole os vídeos reais nos intervalos.',
     'Then cut it in CapCut and paste the real clips in the gaps.', 1),
    ('capa: aviso', 'Antes de gravar: esconda o mouse no canto e não mexa em nada.',
     'Before recording: hide the mouse in a corner and do not touch anything.', 1),

    # ═══════════════════════════ CAPS: nome / nivel ═══════════════════════════
    ('cap 1 nome', "nome:'Repolho', num:'01', nivel:'Iniciante',",
     "nome:'Cabbage', num:'01', nivel:'Beginner',", 1),
    ('cap 1 hint',
     "hint:'O mais fácil de todos. Se você nunca fermentou nada, comece por aqui.',",
     "hint:'The easiest of all. If you have never fermented anything, start here.',", 1),
    ('cap 2 nome', "nome:'Cenoura', num:'02', nivel:'Iniciante',",
     "nome:'Carrot', num:'02', nivel:'Beginner',", 1),
    ('cap 2 hint',
     "hint:'Também é para iniciante, mas solta pouca água — vai precisar de salmoura.',",
     "hint:'Beginner-friendly too, but it releases little water — you will need brine.',", 1),
    ('cap 3 nome', "nome:'Rabanete', num:'03', nivel:'Iniciante',",
     "nome:'Radish', num:'03', nivel:'Beginner',", 1),
    ('cap 3 hint',
     "hint:'O mais rápido da lista. Cuidado com um detalhe: só 3 minutos de massagem.',",
     "hint:'The fastest on the list. Watch one detail: only 3 minutes of massage.',", 1),
    ('cap 4 nome', "nome:'Couve-flor', num:'04', nivel:'Intermediário',",
     "nome:'Cauliflower', num:'04', nivel:'Intermediate',", 1),
    ('cap 4 hint',
     "hint:'Aqui o sal sobe para 2,5%, porque a couve-flor solta menos água. E quebre com a mão.',",
     "hint:'Here the salt goes up to 2.5%, because cauliflower releases less water. And break it with your hands.',", 1),
    ('cap 5 nome', "nome:'Beterraba', num:'05', nivel:'Intermediário',",
     "nome:'Beet', num:'05', nivel:'Intermediate',", 1),
    ('cap 5 hint',
     "hint:'A mais bonita do vídeo — e a que deixa sua mão rosa por dois dias.',",
     "hint:'The prettiest in the video — and the one that turns your hand pink for two days.',", 1),
    ('cap 6 nome', "nome:'Beterraba + couve', num:'06', nivel:'Paciente',",
     "nome:'Beet + cabbage', num:'06', nivel:'Patient',", 1),
    ('cap 6 hint',
     "hint:'Em camadas alternadas, nunca misturado. A couve absorve a cor da beterraba.',",
     "hint:'In alternating layers, never mixed. The cabbage absorbs the colour of the beet.',", 1),
    ('cap 7 nome', "nome:'Alho no mel', num:'07', nivel:'Avançado',",
     "nome:'Garlic in honey', num:'07', nivel:'Advanced',", 1),
    ('cap 7 hint',
     "hint:'O clímax. Sem sal, sem vinagre, só mel cru. E o único onde uma gota de água estraga tudo.',",
     "hint:'The climax. No salt, no vinegar, only raw honey. And the only one where a single drop of water ruins everything.',", 1),

    # ═══════════════════════════ CAPS: sal / tempo ════════════════════════════
    ('sal/tempo 1', "sal:'Sal 2%', tempo:'7 dias', cor:'#3b6d11',",
     "sal:'Salt 2%', tempo:'7 days', cor:'#3b6d11',", 1),
    ('sal/tempo 2', "sal:'Sal 2%', tempo:'6 dias', cor:'#ba7517',",
     "sal:'Salt 2%', tempo:'6 days', cor:'#ba7517',", 1),
    ('sal/tempo 3', "sal:'Sal 2%', tempo:'5-7 dias', cor:'#c1272d',",
     "sal:'Salt 2%', tempo:'5-7 days', cor:'#c1272d',", 1),
    ('sal/tempo 4', "sal:'Sal 2,5%', tempo:'7-10 dias', cor:'#7a8f2a',",
     "sal:'Salt 2.5%', tempo:'7-10 days', cor:'#7a8f2a',", 1),
    ('sal/tempo 5', "sal:'Sal 2%', tempo:'9 dias', cor:'#8e3a68',",
     "sal:'Salt 2%', tempo:'9 days', cor:'#8e3a68',", 1),
    ('sal/tempo 6', "sal:'Sal 2%', tempo:'10-14 dias', cor:'#a01e52',",
     "sal:'Salt 2%', tempo:'10-14 days', cor:'#a01e52',", 1),
    ('sal/tempo 7', "sal:'Nem um pouco', tempo:'3-4 semanas', cor:'#b8862b',",
     "sal:'Not a bit', tempo:'3-4 weeks', cor:'#b8862b',", 1),

    # ═══════════════════════════ REPOLHO ══════════════════════════════════════
    ('r0', "cap:'Vou fermentar esse repolho', sub:'e só volto aqui no dia 7',",
     "cap:'I am going to ferment this cabbage', sub:'and I only come back here on day 7',", 1),
    ('r1', "cap:'Sal, repolho e paciência', sub:'não precisa de mais nada',",
     "cap:'Salt, cabbage and patience', sub:'nothing else is needed',", 1),
    ('r2', "cap:'Sal é 2% do peso', sub:'1,5 kg de repolho = 30 g de sal',",
     "cap:'Salt is 2% of the weight', sub:'1.5 kg of cabbage = 30 g of salt',", 1),
    ('r3', "cap:'Massageia 10 minutos', sub:'a água sai sozinha do repolho',",
     "cap:'Massage for 10 minutes', sub:'the water comes out of the cabbage on its own',", 1),
    ('r4', "cap:'Prensa tudo pra baixo', sub:'o líquido precisa cobrir tudo',",
     "cap:'Press everything down', sub:'the liquid has to cover everything',", 1),
    ('r5', "cap:'Agora é só esperar', sub:'volta no dia 7 pra ver',",
     "cap:'Now we just wait', sub:'come back on day 7 to check',", 1),

    # ═══════════════════════════ CENOURA ══════════════════════════════════════
    ('c0', "cap:'Vou fermentar cenoura', sub:'e volto aqui em 5 dias',",
     "cap:'I am going to ferment carrot', sub:'and I come back here in 5 days',", 1),
    ('c1', "cap:'Primeiro: descascar e cortar', sub:'em palitos, do mesmo tamanho',",
     "cap:'First: peel and cut', sub:'into sticks, all the same size',", 1),
    ('c2', "cap:'Sal é 2% do peso', sub:'200 g de cenoura = 4 g de sal',",
     "cap:'Salt is 2% of the weight', sub:'200 g of carrot = 4 g of salt',", 1),
    ('c3', "cap:'Cenoura fermenta rápido', sub:'de 5 a 7 dias já tá pronta',",
     "cap:'Carrot ferments fast', sub:'in 5 to 7 days it is ready',", 1),
    ('c4', "cap:'Prensa tudo no pote', sub:'o líquido precisa cobrir tudo',",
     "cap:'Press everything into the jar', sub:'the liquid has to cover everything',", 1),
    ('c5', "cap:'Agora é só esperar', sub:'5 dias, mexendo todo dia',",
     "cap:'Now we just wait', sub:'5 days, stirring every day',", 1),
    ('c6', "cap:'Ficou pronta', sub:'crocante, azedinha e conservada',",
     "cap:'It is ready', sub:'crunchy, a little sour and preserved',", 1),

    # ═══════════════════════════ RABANETE ═════════════════════════════════════
    ('b0', "cap:'Rabanete: o mais rápido', sub:'5 dias e já está pronto',",
     "cap:'Radish: the fastest one', sub:'5 days and it is ready',", 1),
    ('b1', "cap:'Rodelas finas de 3 mm', sub:'a espessura muda tudo',",
     "cap:'Thin 3 mm slices', sub:'the thickness changes everything',", 1),
    ('b2', "cap:'Aqui o sal também é 2%', sub:'300 g de rabanete = 6 g de sal',",
     "cap:'Here the salt is 2% too', sub:'300 g of radish = 6 g of salt',", 1),
    ('b3', "cap:'SÓ 3 MINUTOS de massagem', sub:'mais que isso vira papa',",
     "cap:'ONLY 3 MINUTES of massage', sub:'any more than that turns to mush',", 1),
    ('b4', "cap:'Prensa no pote pequeno', sub:'rabanete solta pouca água',",
     "cap:'Press into a small jar', sub:'radish releases very little water',", 1),
    ('b5', "cap:'5 dias na bancada', sub:'prova no dia 5, não antes',",
     "cap:'5 days on the counter', sub:'taste it on day 5, not before',", 1),
    ('b6', "cap:'Crocante e cor de rosa vivo', sub:'o mais bonito da lista',",
     "cap:'Crunchy and bright pink', sub:'the prettiest on the list',", 1),

    # ═══════════════════════════ COUVE-FLOR ═══════════════════════════════════
    ('f0', "cap:'Couve-flor fermentada', sub:'quebrada com a mão, não com faca',",
     "cap:'Fermented cauliflower', sub:'broken by hand, not with a knife',", 1),
    # aqui tambem conserta o erro de digitacao "QUebre"
    ('f1', "cap:'QUebre com a mão', sub:'a faca machuca e amarga',",
     "cap:'Break it with your hands', sub:'a knife bruises it and makes it bitter',", 1),
    ('f2', "cap:'O sal aqui é 2,5%', sub:'mais que os outros, e tem motivo',",
     "cap:'Here the salt is 2.5%', sub:'more than the others, and there is a reason',", 1),
    ('f3', "cap:'7 a 10 dias', sub:'é a mais lenta das hortaliças',",
     "cap:'7 to 10 days', sub:'it is the slowest of the vegetables',", 1),
    ('f4', "cap:'Prensa com peso em cima', sub:'a couve-flor flutua muito',",
     "cap:'Press it with a weight on top', sub:'cauliflower floats a lot',", 1),
    ('f5', "cap:'Agora é só esperar', sub:'10 dias é o ponto ideal',",
     "cap:'Now we just wait', sub:'10 days is the sweet spot',", 1),
    ('f6', "cap:'Textura surpreendente', sub:'fica firme, quase crocante',",
     "cap:'Surprising texture', sub:'it stays firm, almost crunchy',", 1),

    # ═══════════════════════════ BETERRABA ════════════════════════════════════
    ('t0', "cap:'Beterraba fermentada', sub:'a mais bonita da lista',",
     "cap:'Fermented beet', sub:'the prettiest on the list',", 1),
    ('t1', "cap:'Descasca e corta em cubos', sub:'cubo de 2 cm, não fatia',",
     "cap:'Peel and cut into cubes', sub:'2 cm cubes, not slices',", 1),
    ('t2', "cap:'Sal 2% também', sub:'400 g de beterraba = 8 g de sal',",
     "cap:'Salt 2% here too', sub:'400 g of beet = 8 g of salt',", 1),
    ('t3', "cap:'Ela solta muito líquido', sub:'a cor sangra e colore a salmoura',",
     "cap:'It releases a lot of liquid', sub:'the colour bleeds and dyes the brine',", 1),
    ('t4', "cap:'Prensa pra baixo', sub:'o líquido cobrir tudo é essencial',",
     "cap:'Press it down', sub:'the liquid covering everything is essential',", 1),
    ('t5', "cap:'9 dias de espera', sub:'beterraba é mais lenta',",
     "cap:'9 days of waiting', sub:'beet is slower',", 1),
    ('t6', "cap:'CUIDADO: sua mão fica rosa', sub:'e leva uns 2 dias pra sair',",
     "cap:'CAREFUL: your hand turns pink', sub:'and it takes about 2 days to fade',", 1),

    # ═══════════════════════════ ALHO NO MEL ══════════════════════════════════
    ('a0', "cap:'Alho fermentado no mel', sub:'sem sal. sem vinagre. só duas coisas.',",
     "cap:'Garlic fermented in honey', sub:'no salt. no vinegar. only two things.',", 1),
    ('a1', "cap:'Descasca todos os dentes', sub:'amassa com o lado da faca primeiro',",
     "cap:'Peel every clove', sub:'crush it with the side of the knife first',", 1),
    ('a2', "cap:'O passo que quase todo mundo erra', sub:'água é o inimigo número 1',",
     "cap:'The step almost everyone gets wrong', sub:'water is enemy number 1',", 1),
    ('a3', "cap:'Cobre com mel cru', sub:'pelo menos 2 cm acima dos dentes',",
     "cap:'Cover it with raw honey', sub:'at least 2 cm above the cloves',", 1),
    ('a4', "cap:'Vira o pote todo dia', sub:'duas vezes por dia na primeira semana',",
     "cap:'Flip the jar every day', sub:'twice a day in the first week',", 1),
    ('a5', "cap:'O alho vira âmbar', sub:'bolhas = está funcionando',",
     "cap:'The garlic turns amber', sub:'bubbles = it is working',", 1),
    ('a6', "cap:'De 3 a 4 semanas', sub:'o fermento mais lento de todos',",
     "cap:'From 3 to 4 weeks', sub:'the slowest ferment of them all',", 1),
    ('a7', "cap:'Pronto pra comer', sub:'e ainda rende um mel de alho',",
     "cap:'Ready to eat', sub:'and you also get garlic honey',", 1),

    # ═══════════════════════════ cena-cartao ══════════════════════════════════
    ('cartao cap', "cap:'▶ AGORA ENTRA O VÍDEO REAL',",
     "cap:'▶ NOW THE REAL VIDEO GOES IN',", 1),
    ('cartao sub', "sub:'grave: ' + filmTimes[i],", "sub:'record: ' + filmTimes[i],", 1),
    ('cartao 1', "'repolho fatiado sendo massageado com sal',",
     "'shredded cabbage being massaged with salt',", 1),
    ('cartao 2', "'cenoura em palitos entrando no pote',",
     "'carrot sticks going into the jar',", 1),
    ('cartao 3', "'rabanete fatiado em rodelas de 3 mm',",
     "'radish sliced into 3 mm rounds',", 1),
    ('cartao 4', "'couve-flor sendo quebrada com a MÃO',",
     "'cauliflower being broken BY HAND',", 1),
    ('cartao 5', "'beterraba cortada + a mão ficando rosa',",
     "'beet being cut + the hand turning pink',", 1),
    ('cartao 6', "'camadas de beterraba e couve no pote',",
     "'layers of beet and cabbage in the jar',", 1),
    ('cartao 7', "'alho secando na toalha antes do mel'",
     "'garlic drying on the cloth before the honey'", 1),

    # ═══════════════════════════ textos dentro dos SVGs ═══════════════════════
    ('txt 1,5', '>1,5</text>', '>1.5</text>', 1),
    ('txt gramas', '>gramas</text>', '>grams</text>', 1),
    ('txt 7 dias', '>7 dias</text>', '>7 days</text>', 1),
    ('txt de sal', '>de sal</text>', '>of salt</text>', 4),
    ('txt 5 A 7 DIAS', '>5 A 7 DIAS</text>', '>5 TO 7 DAYS</text>', 1),
    ('txt 5 DIAS DEPOIS', '>5 DIAS DEPOIS</text>', '>5 DAYS LATER</text>', 1),
    ('txt Pronta pra comer', '>Pronta pra comer</text>', '>Ready to eat</text>', 1),
    ('txt crocante e azedinha', '>crocante e azedinha</text>',
     '>crunchy and a little sour</text>', 1),
    ('txt 3 MIN', '>3 MIN · NEM UM MINUTO A MAIS</text>',
     '>3 MIN · NOT ONE MINUTE MORE</text>', 1),
    ('txt 5 DIAS', '>5 DIAS</text>', '>5 DAYS</text>', 1),
    ('txt Pronto em 5 dias', '>Pronto em 5 dias</text>', '>Ready in 5 days</text>', 1),
    ('txt crocante rosa vivo', '>crocante, rosa vivo e azedinho</text>',
     '>crunchy, bright pink and a little sour</text>', 1),
    ('txt 12,5 g', '>12,5 g</text>', '>12.5 g</text>', 1),
    ('txt 2,5% E NAO 2%', '>2,5% E NÃO 2%</text>', '>2.5% AND NOT 2%</text>', 1),
    ('txt pouca agua', '>ela solta muito pouca água</text>',
     '>it releases very little water</text>', 1),
    ('txt 7 A 10 DIAS', '>7 A 10 DIAS</text>', '>7 TO 10 DAYS</text>', 1),
    ('txt 7 a 10 dias', '>7 a 10 dias</text>', '>7 to 10 days</text>', 1),
    ('txt Firme e saborosa', '>Firme e saborosa</text>', '>Firm and tasty</text>', 1),
    ('txt nao fica mole', '>não fica mole como você imagina</text>',
     '>it does not go soft like you would expect</text>', 1),
    ('txt 9 DIAS', '>9 DIAS</text>', '>9 DAYS</text>', 1),
    ('txt mao rosa', '>SIM, SUA MÃO FICA ROSA</text>', '>YES, YOUR HAND TURNS PINK</text>', 1),
    ('txt 1 a 2 dias', '>de 1 a 2 dias. não tem jeito.</text>',
     '>1 to 2 days. no way around it.</text>', 1),
    ('txt SEM SAL', '>SEM SAL NENHUM</text>', '>NO SALT AT ALL</text>', 1),
    ('txt SO ALHO E MEL', '>SÓ ALHO E MEL CRU</text>', '>ONLY GARLIC AND RAW HONEY</text>', 1),
    ('txt AGUA = MOFO', '>ÁGUA = MOFO</text>', '>WATER = MOLD</text>', 1),
    ('txt seque', '>Seque cada dente com um pano limpo.</text>',
     '>Dry every clove with a clean cloth.</text>', 1),
    ('txt uma gota', '>Uma gota só pode estragar o pote todo.</text>',
     '>A single drop can ruin the whole jar.</text>', 1),
    ('txt MEL ATE O TOPO', '>MEL ATÉ O TOPO</text>', '>HONEY TO THE TOP</text>', 1),
    ('txt cubra 2cm', '>Cubra cada dente com 2 cm de mel</text>',
     '>Cover every clove with 2 cm of honey</text>', 1),
    ('txt POR QUE VIRAR', '>POR QUE VIRAR?</text>', '>WHY FLIP IT?</text>', 1),
    ('txt mel pesado', '>O mel é pesado e desce. Virando,</text>',
     '>Honey is heavy and sinks. By flipping,</text>', 1),
    ('txt todo dente', '>todo dente fica coberto.</text>', '>every clove stays covered.</text>', 1),
    ('txt DIA 1', '>DIA 1</text>', '>DAY 1</text>', 2),
    ('txt Claro cru', '>Claro · cru</text>', '>Pale · raw</text>', 1),
    ('txt DIA 21', '>DIA 21</text>', '>DAY 21</text>', 2),
    ('txt Ambar doce', '>Âmbar · doce</text>', '>Amber · sweet</text>', 1),
    ('txt alho ambar', '>O ALHO FICA ÂMBAR E MACIO</text>',
     '>THE GARLIC TURNS AMBER AND SOFT</text>', 1),
    ('txt azul ou verde', '>Se ficar AZUL ou VERDE: ainda é seguro.</text>',
     '>If it turns BLUE or GREEN: it is still safe.</text>', 1),
    ('txt reacao natural', '>É reação natural, não é mofo.</text>',
     '>It is a natural reaction, not mold.</text>', 1),
    ('txt DIAS', '>DIAS</text>', '>DAYS</text>', 1),
    ('txt pote fecha', '>pote fecha</text>', '>jar sealed</text>', 1),
    ('txt prova', '>prova</text>', '>taste it</text>', 1),
    ('txt DIA 30+', '>DIA 30+</text>', '>DAY 30+</text>', 1),
    ('txt geladeira', '>geladeira</text>', '>fridge</text>', 1),
    ('txt 3 a 4 semanas', '>3 A 4 SEMANAS NO MÍNIMO</text>',
     '>AT LEAST 3 TO 4 WEEKS</text>', 1),
    ('txt mais lento', '>Este é o mais lento da série — não tenha pressa</text>',
     '>This is the slowest of the series — take your time</text>', 1),
    ('txt abra o pote', '>Abra o pote todo dia pra soltar o gás</text>',
     '>Open the jar every day to release the gas</text>', 1),
    ('txt USE EM', '>USE EM</text>', '>USE IT ON</text>', 1),
    ('txt Pao', '>Pão</text>', '>Bread</text>', 1),
    ('txt Salada', '>Salada</text>', '>Salad</text>', 1),
    ('txt Arroz', '>Arroz</text>', '>Rice</text>', 1),
    ('txt Carne', '>Carne</text>', '>Meat</text>', 1),
    ('txt Molhos', '>Molhos</text>', '>Sauces</text>', 1),
    ('txt ganha mel', '>E VOCÊ AINDA GANHA MEL DE ALHO</text>',
     '>AND YOU ALSO GET GARLIC HONEY</text>', 1),
    ('txt qual fermento', '>Qual eu fermento depois desse?</text>',
     '>Which one should I ferment next?</text>', 1),
    ('txt comentarios', '>Escreve nos comentários</text>', '>Write it in the comments</text>', 1),
    ('txt VIDEO REAL', '>VÍDEO REAL</text>', '>REAL VIDEO</text>', 1),
    ('txt corte aqui', '>corte aqui e cole o vídeo do celular</text>',
     '>cut here and paste the phone clip</text>', 1),
    ('txt 15 SEGUNDOS', '>15 SEGUNDOS</text>', '>15 SECONDS</text>', 1),

    # ═══════════════════════════ strings do motor JS ══════════════════════════
    ('js capitulo', "'<small id=\"ctag\">capítulo ' + (ci + 1) + ' de 7</small>'",
     "'<small id=\"ctag\">chapter ' + (ci + 1) + ' of 7</small>'", 1),
    ('js nivel', "'Nível: ' + c.nivel.toLowerCase()", "'Level: ' + c.nivel.toLowerCase()", 1),
    ('js assistir', "textContent = '▶ Assistir';", "textContent = '▶ Watch';", 1),
    ('js pausar', "textContent = '⏸ Pausar';", "textContent = '⏸ Pause';", 2),
    ('js continuar', "textContent = '▶ Continuar';", "textContent = '▶ Resume';", 1),
]

# palavras que nao podem sobrar no arquivo final
SOBRAS = ['legumes', 'legume', 'fermentad', 'Repolho', 'repolho', 'Cenoura', 'cenoura',
          'Rabanete', 'rabanete', 'Couve', 'couve', 'Beterraba', 'beterraba', 'Alho',
          'alho', 'mel', 'dias', 'dia ', 'semanas', 'salmoura', 'pote', 'dente',
          'Iniciante', 'Intermediário', 'Paciente', 'Avançado', 'capítulo', 'Nível',
          'Pausar', 'Reiniciar', 'Assistir', 'Continuar', 'Rodando', 'gravação',
          'seucanal', 'vídeo real', 'VÍDEO', 'MOFO', 'água', 'ÁGUA', 'mão', 'MÃO',
          'sal ', 'Sal ', 'de sal', 'o líquido', 'quebrada', 'machuca', 'vira papa',
          'ninguém', 'você', 'não ', 'pra ', 'pro ', 'tá ']


def main():
    check_only = '--check' in sys.argv
    txt = io.open(ORIG, encoding='utf-8').read()
    antes = len(txt)

    falhas = []
    for rotulo, velho, novo, n in TROCAS:
        c = txt.count(velho)
        if c != n:
            falhas.append('%-22s ancora casou %d vez(es), esperado %d\n'
                          '      -> %s' % (rotulo, c, n, velho[:110]))
        else:
            txt = txt.replace(velho, novo, n)

    if falhas:
        print('=' * 72)
        print('ABORTADO — %d ancora(s) fora do esperado. NADA foi gravado.' % len(falhas))
        print('=' * 72)
        for f in falhas:
            print('  [X] ' + f)
        return 1

    print('ancoras: %d/%d casaram exatamente' % (len(TROCAS), len(TROCAS)))

    # ── varredura de sobras ────────────────────────────────────────────────
    # os comentarios de codigo ficam em portugues de proposito (sao anotacoes
    # para o usuario, nao texto de tela) — entao saem da varredura.
    corpo = re.sub(r'/\*.*?\*/', ' ', txt, flags=re.S)
    corpo = re.sub(r'<!--.*?-->', ' ', corpo, flags=re.S)
    corpo = re.sub(r'//[^\n]*', ' ', corpo)
    sobras = {}
    for p in SOBRAS:
        n = corpo.count(p)
        if n:
            sobras[p] = n
    if sobras:
        print('\nsobras de portugues (conferir):')
        for p, n in sorted(sobras.items(), key=lambda x: -x[1]):
            print('  %-16s %d' % (p, n))
    else:
        print('sobras de portugues: nenhuma')

    # ── numeros com virgula decimal ────────────────────────────────────────
    dec = re.findall(r'\d,\d', corpo)
    if dec:
        print('numeros com virgula decimal (devem virar ponto):', sorted(set(dec)))

    if check_only:
        print('\n--check: nada foi gravado.')
        return 0

    io.open(DEST, 'w', encoding='utf-8', newline='').write(txt)
    print('\ngravado: %s' % DEST)
    print('bytes  : %d -> %d' % (antes, len(txt.encode('utf-8'))))
    print('linhas : %d' % (txt.count('\n') + 1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
